"""
Series of classes which implement a waveform. A waveform can be created from
many input sources and must be able to output a series of samples.
"""

from .notes import NOTES
from .sample import get_sampler_from_width

import math

class Waveform(object):
    """
    Waveform is a unit of constant sound. Represents either a note, chord, or
    audio snippet.
    """

    def __init__(self, duration: float, sample_rate=22050):
        """
        Creates a new waveform.
        """
        self.duration = duration
        self.sample_rate = sample_rate

    @property
    def num_samples(self) -> int:
        """
        Interface for getting the number of samples in this waveform.

        Returns:
            The number of samples (int).
        """
        return int(self.duration * self.sample_rate)

    def get_samples(self, start_sample: int, end_sample: int) -> list:
        """
        Interface for getting a range of samples. This should return a list of
        sequential samples starting at start_sample (inclusive) and ending at
        end_sample (exclusive).

        A sample is a discrete point on the audio wave between [-1.0, 1.0]. This
        function will return an array of these.

        Args:
            start_sample: The first sample (inclusive).
            end_sample: The end sample (exclusive).

        Return:
            List of samples.
        """
        raise NotImplementedError()

    def get_frames(self,
                   start_sample: int,
                   end_sample: int,
                   bit_width: int) -> list:
        """
        Interface for getting samples as frames of the provided bit width. A
        frame is a sample converted to the given bit width.

        Args:
            start_sample: The first sample (inclusive).
            end_sample: The end sample (exclusive).
            bit_width: The bit width of each sample.

        Return:
            List of frames.
        """
        raise NotImplementedError()


class Note(Waveform):
    """
    A type of waveform that's for a single note. No transformations applied,
    just a simple sine wave.
    """

    def __init__(self, note: str, duration: float, sample_rate=22050):
        super().__init__(duration, sample_rate=sample_rate)

        if note not in NOTES:
            raise ValueError(f"{note} is not a valid note.")

        self.freq = NOTES[note]

    def get_samples(self, start_sample: int, end_sample: int) -> list:
        """
        Returns a sine wave for this sample from [start_sample, end_sample).

        Args:
            start_sample: The first sample (inclusive).
            end_sample: The end sample (exclusive).

        Return:
            List of samples.
        """
        if end_sample > self.num_samples:
            raise ValueError(
                f"Requested sample {end_sample} which is greater " +
                f"than the total number of samples {self.num_samples}"
            )

        if start_sample < 0:
            raise ValueError(
                f"start_sample must be non-negative, but was: {start_sample}"
            )

        return [
            math.sin(2 * math.pi * self.freq * t / self.sample_rate)
            for t in range(start_sample, end_sample)
        ]

    def get_frames(self,
                   start_sample: int,
                   end_sample: int,
                   bit_width: int,
                   master_volume: float) -> list:
        """
        Interface for getting samples as frames of the provided bit width. A
        frame is a sample converted to the given bit width.

        Args:
            start_sample: The first sample (inclusive).
            end_sample: The end sample (exclusive).
            bit_width: The bit width of each sample.

        Return:
            List of frames.
        """
        samples = self.get_samples(start_sample, end_sample)
        sampler = get_sampler_from_width(bit_width)

        # For each sample, convert it to the given bit_width and update the
        # frames list. Let's just modify it in-place, since it will be the same
        # size.
        for i in range(len(samples)):
            samples[i] = sampler.convert(samples[i] * master_volume)

        return samples