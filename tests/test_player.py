from engine.player import Player
from engine.tracks import Track
from engine.waves import Note

def test_play_an_a_sharp():
    # Queue an A#3 for 0.5 seconds.
    a_sharp_3 = Note("A#3", 0.5)

    # Add it the beginning of a track.
    track = Track("")
    track.add_waveform(0.0, a_sharp_3)

    player = Player([track], track.sample_rate)
    player.play()

def test_play_a_scale():
    # Play a short track with a C scale.
    track = Track("")

    track.add_waveform(0.0, Note("C5", 0.2))
    track.add_waveform(0.2, Note("D5", 0.2))
    track.add_waveform(0.4, Note("E5", 0.2))
    track.add_waveform(0.6, Note("F5", 0.2))
    track.add_waveform(0.8, Note("G5", 0.2))
    track.add_waveform(1.0, Note("A5", 0.2))
    track.add_waveform(1.2, Note("B5", 0.2))
    track.add_waveform(1.4, Note("C6", 0.2))

    player = Player([track], track.sample_rate)
    player.play()

def test_play_chords():
    # Play a few chords
    track = Track("")

    track.add_waveform(0.0, Note("C4", 0.5))
    track.add_waveform(0.0, Note("E4", 0.5))
    track.add_waveform(0.0, Note("G4", 0.5))

    track.add_waveform(0.5, Note("E4", 0.5))
    track.add_waveform(0.5, Note("G4", 0.5))
    track.add_waveform(0.5, Note("C5", 0.5))

    track.add_waveform(1.0, Note("G4", 0.5))
    track.add_waveform(1.0, Note("C5", 0.5))
    track.add_waveform(1.0, Note("E5", 0.5))

    track.add_waveform(1.5, Note("C5", 0.5))
    track.add_waveform(1.5, Note("E5", 0.5))
    track.add_waveform(1.5, Note("G5", 0.5))

    player = Player([track], track.sample_rate)
    player.play()

def test_empty_track():
    track = Track("")

    player = Player([track], track.sample_rate)
    player.play()
