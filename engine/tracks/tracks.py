"""
Represents a track, which is a unit of sounds. Tracks may either be implemented
as a series of notes or chords. Tracks may also be an imported waveform or a
concatenation of several waveforms.
"""

from engine.waves import Waveform, Note

from sortedcontainers import SortedList


def beat_to_duration(tempo, beat):
    # tempo is in bpm.
    # beat is a fraction of that.
    return (60.0 / tempo) * beat


class TimedWave(object):
    """
    Waveform with a timestamp.
    """

    def __init__(self, time: float, waveform: Waveform):
        self.time = time
        self.waveform = waveform

    def __lt__(self, other: Waveform) -> bool:
        return self.time < other.time


class Track(object):
    """
    Represents a track, which is a unit of sounds. Tracks may either be
    implemented as a series of notes or chords. Tracks may also be an imported
    waveform or a concatenation of several waveforms.
    """

    def __init__(self, name, sample_rate=22050):
        """
        Creates a new track with the specified sample rate.
        """
        self.name = name
        self.sample_rate = sample_rate

        # Initialize an empty list of Waveforms.
        self.waveforms = SortedList()

    def add_waveform(self, time: float, waveform: Waveform):
        """
        Adds a raw waveform to this track.
        """
        if time < 0.0:
            raise ValueError("Time offset must be non-negative.")

        if waveform.sample_rate != self.sample_rate:
            raise ValueError(
                "Sample rate of waveform does not match the rest of the track!")
        self.waveforms.add(TimedWave(time, waveform))

    def __add__(self, other):
        """
        Concatenates this track with another track.
        """
        if self.sample_rate != other.sample_rate:
            raise ValueError(
                f"Could not concatenate {self.name} with {other.name}. "
                f"Mistmached sample rates.")

        for wave in other.waveforms:
            self.waveforms.add(wave)
        return self

    def __radd__(self, other):
        """
        Concatenates this track with another track.
        """
        if other == 0:
            return self
        else:
            return self.__add__(other)


class CustomNotesTrack(Track):
    def __init__(self, name, tempo, sample_rate=22050):
        """
        Creates a notes track with the specified tempo.
        """
        super().__init__(name, sample_rate=sample_rate)

        self.tempo = tempo
        self.offset = 0.0

    def append_note(self, beat: float, note: str):
        """
        Append a new note to the end of this track.
        """
        duration = beat_to_duration(self.tempo, beat)
        self.add_waveform(self.offset, Note(note, duration))
        self.offset += duration

    def append_rest(self, beat: float):
        """
        Append a rest interval.
        """
        self.offset += beat_to_duration(self.tempo, beat)
