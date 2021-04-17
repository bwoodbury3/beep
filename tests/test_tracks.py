import pytest

from engine.tracks import Track
from engine.waves import Waveform

class NoopWaveform(Waveform):
    def __init__(self, index, sample_rate=22050):
        super().__init__(1.0, sample_rate=sample_rate)
        self.index = index

    def __eq__(self, other):
        return self.index == other.index


def test_track_order():
    track = Track("")
    waveform_a = NoopWaveform('a')
    waveform_b = NoopWaveform('b')

    track.add_waveform(3.0, waveform_a)
    track.add_waveform(1.0, waveform_b)
    track.add_waveform(2.0, waveform_a)
    track.add_waveform(6.0, waveform_b)
    track.add_waveform(4.0, waveform_a)

    index = 0
    expected_order = [
        (1.0, waveform_b),
        (2.0, waveform_a),
        (3.0, waveform_a),
        (4.0, waveform_a),
        (6.0, waveform_b),
    ]
    for timed_wave in track.waveforms:
        expected_item = expected_order[index]
        assert expected_item[0] == timed_wave.time
        assert expected_item[1] == timed_wave.waveform
        index += 1

def test_mismatched_sample_rate():
    track = Track("", sample_rate=20000)
    wave = Waveform(1.0, sample_rate=10000)

    with pytest.raises(ValueError):
        track.add_waveform(0.0, wave)

def test_simultaneous_waveforms():
    track = Track("")
    wave_a = NoopWaveform('a')
    wave_b = NoopWaveform('b')

    track.add_waveform(0.0, wave_a)
    track.add_waveform(0.0, wave_b)

    assert len(track.waveforms) == 2
