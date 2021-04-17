import pytest

from engine.waves import Note

def test_invalid_note():
    with pytest.raises(ValueError, match="is not a valid note."):
        # This note doesn't exist.
        note = Note("A##5", 1.0)

def test_correct_freq():
    note = Note("F0", 1.0)
    assert note.freq == 21.83

    note = Note("Ab1", 1.0)
    assert note.freq == 51.91

def test_num_samples():
    sample_rate = 100

    note = Note("F0", 1.0, sample_rate=sample_rate)
    assert note.num_samples == sample_rate

    note = Note("F0", 1.5, sample_rate=sample_rate)
    assert note.num_samples == int(1.5 * sample_rate)

    note = Note("F0", 2.0, sample_rate=sample_rate)
    assert note.num_samples == 2 * sample_rate

def test_get_samples():
    sample_rate = 1000

    note = Note("F0", 1.0, sample_rate=sample_rate)
    samples = note.get_samples(0, note.num_samples)
    assert len(samples) == sample_rate

    note = Note("F0", 2.0, sample_rate=sample_rate)
    samples = note.get_samples(0, note.num_samples)
    assert len(samples) == 2 * sample_rate

    with pytest.raises(
        ValueError,
        match="greater than the total number of samples"
    ):
        note.get_samples(0, note.num_samples + 1)
