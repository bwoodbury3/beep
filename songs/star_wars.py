from engine.tracks import ImportedAudioTrack
from engine.player import Player

def play():
    track = ImportedAudioTrack("Star Wars")
    track.add_wav_file(0.0, "songs/audio/StarWars60.wav")

    player = Player([track], sample_rate=track.sample_rate, volume=0.3, sample_width=16)
    player.play()