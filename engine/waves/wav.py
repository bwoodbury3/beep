"""
Waveform implementation which uses the .wav standard.
https://en.wikipedia.org/wiki/WAV


"""

from .audio_file import Header, InputAudioFile
from .waveform import Waveform
from engine import debug

WAV_FORMAT = Header()
"""
Wav header format, per:
http://www.topherlee.com/software/pcm-tut-wavformat.html
"""

WAV_FORMAT.add_spec("riff",          offset=0,  length=4, required_val="RIFF")
WAV_FORMAT.add_spec("file_size",     offset=4,  length=4, typespec=int)
WAV_FORMAT.add_spec("wave",          offset=8,  length=4, required_val="WAVE")
WAV_FORMAT.add_spec("fmt",           offset=12, length=4, required_val="fmt ")

WAV_FORMAT.add_spec("format_length", offset=16, length=4, typespec=int, required_val=16)
WAV_FORMAT.add_spec("format_type",   offset=20, length=2, typespec=int, required_val=1) # 1 == PCM only, we don't support Dolby Digital.
WAV_FORMAT.add_spec("num_channels",  offset=22, length=2, typespec=int)
WAV_FORMAT.add_spec("sample_rate",   offset=24, length=4, typespec=int)
WAV_FORMAT.add_spec("bytes_per_sec", offset=28, length=4, typespec=int) # (BytesPerSample * Channels * SampleRate)

WAV_FORMAT.add_spec("sample_size",   offset=32, length=2, typespec=int) # (BytesPerSample * Channels)
WAV_FORMAT.add_spec("bit_width",     offset=34, length=2, typespec=int)
WAV_FORMAT.add_spec("data",          offset=36, length=4, required_val="data")
WAV_FORMAT.add_spec("data_size",     offset=40, length=4, typespec=int)

DATA_OFFSET = 46
"""
The start of wav data.
"""

class WavFile(Waveform):
    """
    Implements the Waveform interface for a .wav file.
    """

    def __init__(self, filename: str):
        """
        Load a .wav file with the given filename.
        """
        self.filename = filename
        self.wav_file = InputAudioFile(filename, WAV_FORMAT)

        # Read in class level attributes from the wav file header.
        self._read_metadata()

        duration = float(self.data_size) / self.bytes_per_sec

        super().__init__(duration, self.sample_rate)

    def _read_metadata(self):
        """
        Helper function to read in .wav metadata.
        """
        if not self.wav_file.validate_header():
            raise ValueError(f"Could not parse wav file: {self.filename}")

        self.data_size = self.wav_file.get_header_value("data_size")
        self.bytes_per_sec = self.wav_file.get_header_value("bytes_per_sec")
        self.bit_width = self.wav_file.get_header_value("bit_width")
        self.byte_width = int(self.bit_width / 8)
        self.sample_rate = self.wav_file.get_header_value("sample_rate")
        self.num_channels = self.wav_file.get_header_value("num_channels")

        if self.data_size % self.bytes_per_sec != 0:
            raise ValueError(
                "Corrupted file - sample width does not divide evenly into" +
                "the file size.")

        if self.bit_width % 8 != 0:
            raise ValueError(
                "Corrupted file - bit width does not divide evenly into 8")

    def get_frames(self,
                   start_sample: int,
                   end_sample: int,
                   bit_width: int,
                   master_volume: float) -> list:
        """
        Get samples as frames of the provided bit width. A frame is a sample
        converted to the given bit width.

        Args:
            start_sample: The first sample (inclusive).
            end_sample: The end sample (exclusive).
            bit_width: The bit width of each sample.
            master_volume: The master volume to scale the wave by.

        Return:
            List of frames.
        """

        # TODO: Make this more flexible.
        assert bit_width == self.bit_width

        if end_sample > self.num_samples:
            raise ValueError(f"end sample {end_sample} is beyond the last sample.")

        frames = [0] * (end_sample - start_sample)
        for i in range(len(frames)):
            frames[i] = int(
                0.8 *
                self.wav_file.read_signed_int(
                    DATA_OFFSET + ((start_sample + i) * self.byte_width),
                    self.byte_width
                )
            )

        return frames