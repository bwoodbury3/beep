"""
Series of classes which implement a waveform. A waveform can be created from
many input sources and must be able to output a series of samples.
"""

from .notes import NOTES

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
        """
        return 0

    def get_samples(self, start_sample, end_sample) -> list:
        """
        Interface for getting a range of samples. This should return a list of
        sequential samples starting at start_sample (inclusive) and ending at
        end_sample (exclusive).
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
        self.duration = duration

    @property
    def num_samples(self) -> int:
        """
        Return the duration of this note times the sample rate. Always rounding
        down.
        """
        return int(self.duration * self.sample_rate)

    def get_samples(self, start_sample: int, end_sample: int) -> list:
        """
        Returns a sine wave for this sample from [start_sample, end_sample).

        Args:
            start_sample: The first sample (inclusive).
            end_sample: The end sample (exclusive).
        """
        if end_sample > self.num_samples:
            raise ValueError(
                f"Requested sample {end_sample} which is greater " +
                f"than the total number of samples {self.num_samples}"
            )

        return [
            math.sin(2 * math.pi * self.freq * t / self.sample_rate)
            for t in range(start_sample, end_sample)
        ]
