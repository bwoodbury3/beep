from engine.tracks import Track
from engine.waves import WavFile
from engine.player import Player

def play():
    track = Track("Star Wars")
    wav_file = WavFile("songs/audio/StarWars60.wav")
    track.add_waveform(0.0, wav_file)

    player = Player([track], sample_rate=track.sample_rate, volume=0.3, sample_width=16)
    player.play()