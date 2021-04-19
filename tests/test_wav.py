from engine.waves import WavFile

def test_parse_star_wars():
    star_wars_file = "songs/audio/StarWars60.wav"
    wav = WavFile(star_wars_file)

    # Let's just assert that it doesn't crash for now.
    wav.get_frames(0, 22050, 16, 0.2)