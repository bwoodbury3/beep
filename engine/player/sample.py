import types

class Sampler(object):
    """
    Initialize a Sample which is capable of converting a (1.0, 1.0) wave
    sample into a sample fitting the given bit width. Example:

        # Create an 8-bit sample which is multiplied by 2^7 then shifted by 2^7
        # to create a discrete sine wave centered around 128.
        >>> s = Sample(8, (2 ** 7) - 1, 2 ** 7)
        >>> s.convert(0.0)
        128
        >>> s.convert(1.0)
        255
        >>> s.convert(-1.0)
        1
    """
    def __init__(self,
                 sample_bits: int,
                 multiplier: float,
                 offset: int,
                 cast_func=int):
        """
        Initialize a sample format.
        """
        self.sample_bits = sample_bits
        self.multiplier = multiplier
        self.offset = offset
        self.cast_func = cast_func

        # If we're dealing with an integer, we need to truncate the value.
        # TODO: How to handle floating point?
        self.truncate = (2 ** sample_bits) - 1

    def convert(self, value: float):
        """
        Gets a sample at this bit width.

        Args:
            value: The sample to convert.

        Returns:
            The converted value, as determined by the cast function.
        """
        return min(self.cast_func(value * self.multiplier + self.offset),
                   self.truncate)

    def bytes_per_sample(self) -> int:
        """
        Returns the sample size expressed in the number of bytes or frames.
        """
        return int(self.sample_bits / 8)

# Note that 8 bit audio is signed while 16/24 bit audio is unsigned.
SAMPLE_8_BIT  = Sampler(8,  (1 << 7) - 1,  1 << 7)
SAMPLE_16_BIT = Sampler(16, (1 << 15) - 1, 1 << 7)
SAMPLE_24_BIT = Sampler(24, (1 << 23) - 1, 1 << 12)

def get_sampler_from_width(width: int) -> Sampler:
    """
    Gets a sampler from the given bit width. Supported widths include 8-bit,
    16-bit, 24-bit.

    Args:
        width: The bit width to cast to.
    """
    if width == 8:
        return SAMPLE_8_BIT
    elif width == 16:
        return SAMPLE_16_BIT
    elif width == 24:
        return SAMPLE_24_BIT
    else:
        raise ValueError(f"Unsupported bit width: {width}")