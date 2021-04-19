"""
Audio file utilities.
"""

from engine import debug, info


def typecast_int(byte_str: bytes) -> int:
    val = int.from_bytes(byte_str, byteorder='little')
    # debug(f"Converting {byte_str} to {val}")
    return val

def typecast_str(byte_str: bytes) -> str:
    return byte_str.decode("utf-8")

def typecast_bytes(byte_str: bytes) -> bytes:
    return byte_str

class Header(object):
    """
    Utility object for parsing a header in an audio file.
    """

    def __init__(self):
        self.entries = {}

    def add_spec(self,
                 entry_name: str,
                 offset: int,
                 length: int,
                 typespec=str,
                 required_val=None):
        """
        Adds a header entry per the specification.

        Args:
            entry_name: The name of the header entry.
            offset: The offset in the header.
            length: The length of the field.
            typespec: The type of this field (optional).
            required_val: The required value in every header of this file type
                          (optional). This is used for headers that have
                          hardcoded strings, such as "RIFF" at the beginning of
                          the wav format.
        """
        typecast = None
        if typespec == int:
            typecast = typecast_int
        elif typespec == str:
            typecast = typecast_str
        elif typespec == bytes:
            typecast = typecast_bytes
        else:
            raise ValueError(f"Unsupported header type: {typespec}")

        self.entries[entry_name] = {
            "offset": offset,
            "length": length,
            "typecast": typecast,
            "required_val": required_val
        }

    def get_spec(self, entry_name):
        """
        Get a header entry specification.
        """
        return self.entries[entry_name]

    def get_required_val_specs(self):
        """
        Get all header entry specifications with required values.
        """
        return {
            name: entry
            for name, entry in self.entries.items()
            if entry["required_val"] != None
        }


class InputAudioFile(object):
    """
    Loads an audio file into memory and supports seeking through.
    """

    def __init__(self, filename: str, header_format: Header):
        """
        Loads the given file into memory.
        """
        self.header = header_format
        with open(filename, "rb") as f:
            self.data = f.read()

    def __len__(self):
        return len(self.data)

    def read_bytes(self, offset, length=-1):
        """
        Seeks through the file to return the requested number of bytes. This
        operation will probably be converted to file seeking in the future.

        Args:
            offset: The offset within the data.
            length: The length of the data to read. If -1, reads the rest of the
                    file.

        Return:
            array of bytes.
        """
        if length == -1:
            length = len(self.data) - offset

        if length + offset > len(self.data):
            raise ValueError("Attempted to seek past the end of the file.")

        return self.data[offset : offset + length]

    def read_signed_int(self, offset, length):
        """
        Read an int at the given position.

        Args:
            offset: The byte offset within the file.
            length: The length of the integer in bytes.
        """
        byte_str = self.read_bytes(offset, length=length)
        return int.from_bytes(byte_str, byteorder='little', signed=True)

    def validate_header(self):
        """
        Validates all of the required fields within the header.

        Returns:
            True if header is valid, per the required header entries.
        """
        for name in self.header.get_required_val_specs():
            debug(f"Validating header entry: {name}")
            header_spec = self.header.get_spec(name)
            b = self.read_bytes(header_spec["offset"], header_spec["length"])
            if header_spec["typecast"](b) != header_spec["required_val"]:
                info(f"Unable to parse file header entry {name}")
                return False

        debug("Successfully validated header!")
        return True

    def get_header_value(self, name: str):
        """
        Gets a header value specified by the Header and the name.

        Args:
            name: The name of the entry to retrieve.

        Returns:
            object of the header type.
        """
        header_spec = self.header.get_spec(name)
        b = self.read_bytes(header_spec["offset"], header_spec["length"])
        return header_spec["typecast"](b)
