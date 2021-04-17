from sound import CustomNotesTrack, Player


def get_melody():
    track = CustomNotesTrack("Melody 01", 200)

    # Intro
    track.append_note(1/2, "E5")
    track.append_note(1/2, "E5")
    track.append_note(1/2, "REST")
    track.append_note(1/2, "E5")
    track.append_note(1/2, "REST")
    track.append_note(1/2, "C5")
    track.append_note(1/2, "E5")
    track.append_note(1/2, "REST")
    track.append_note(1/2, "G5")
    track.append_note(3/2, "REST")
    track.append_note(1/2, "G4")
    track.append_note(3/2, "REST")

    for i in range(2):
        track.append_note(1/2, "C5")
        track.append_rest(1)
        track.append_note(1/2, "G4")
        track.append_note(1, "REST")
        track.append_note(1, "E4")

        track.append_note(1/2, "REST")
        track.append_note(1, "A4")
        track.append_note(1, "B4")
        track.append_note(1/2, "Bb4")
        track.append_note(1, "A4")

        track.append_note(2/3, "G4")
        track.append_note(2/3, "E5")
        track.append_note(2/3, "G5")
        track.append_note(1, "A5")
        track.append_note(1/2, "F5")
        track.append_note(1/2, "G5")

        track.append_note(1/2, "REST")
        track.append_note(1, "E5")
        track.append_note(1/2, "C5")
        track.append_note(1/2, "D5")
        track.append_note(1, "B4")
        track.append_note(1/2, "REST")

    for i in range(2):
        track.append_rest(1)
        track.append_note(1/2, "G5")
        track.append_note(1/2, "F#5")
        track.append_note(1/2, "F5")
        track.append_note(1, "D5")
        track.append_note(1/2, "E5")

        track.append_rest(1/2)
        track.append_note(1/2, "G#4")
        track.append_note(1/2, "A4")
        track.append_note(1/2, "C5")
        track.append_rest(1/2)
        track.append_note(1/2, "A4")
        track.append_note(1/2, "C5")
        track.append_note(1/2, "D5")

        track.append_rest(1)
        track.append_note(1/2, "G5")
        track.append_note(1/2, "F#5")
        track.append_note(1/2, "F5")
        track.append_note(1, "D5")
        track.append_note(1/2, "E5")

        track.append_rest(1/2)
        track.append_note(1/2, "C6")
        track.append_rest(1/2)
        track.append_note(1/2, "C6")
        track.append_note(1, "C6")
        track.append_rest(1)

        track.append_rest(1)
        track.append_note(1/2, "G5")
        track.append_note(1/2, "F#5")
        track.append_note(1/2, "F5")
        track.append_note(1, "D5")
        track.append_note(1/2, "E5")

        track.append_rest(1/2)
        track.append_note(1/2, "G#4")
        track.append_note(1/2, "A4")
        track.append_note(1/2, "C5")
        track.append_rest(1/2)
        track.append_note(1/2, "A4")
        track.append_note(1/2, "C5")
        track.append_note(1/2, "D5")

        track.append_rest(1)
        track.append_note(1/2, "Eb5")
        track.append_note(1, "REST")
        track.append_note(1/2, "D5")
        track.append_note(1, "REST")

        track.append_note(1, "C5")
        track.append_rest(3)

    return track

def get_bass():
    bass = CustomNotesTrack("Bass 01", 200)

    bass.append_note(1/2, "D3")
    bass.append_note(1/2, "D3")
    bass.append_rest(1/2)
    bass.append_note(1/2, "D3")
    bass.append_rest(1/2)
    bass.append_note(1/2, "D3")
    bass.append_note(1/2, "D3")
    bass.append_rest(1/2)

    bass.append_note(1, "G3")
    bass.append_rest(1)
    bass.append_note(1, "G2")
    bass.append_rest(1)

    for i in range(2):
        bass.append_note(1, "G3")
        bass.append_rest(1/2)
        bass.append_note(1, "E3")
        bass.append_rest(1/2)
        bass.append_note(1, "C3")

        bass.append_rest(1/2)
        bass.append_note(1, "F3")
        bass.append_note(1, "G3")
        bass.append_note(1/2, "Gb3")
        bass.append_note(1, "F3")

        bass.append_note(2/3, "C4")
        bass.append_note(2/3, "E4")
        bass.append_note(2/3, "G4")
        bass.append_note(1, "A4")
        bass.append_note(1/2, "D4")
        bass.append_note(1/2, "E4")

        bass.append_rest(1/2)
        bass.append_note(1, "C4")
        bass.append_note(1/2, "A3")
        bass.append_note(1/2, "B3")
        bass.append_note(1, "G3")
        bass.append_rest(1/2)

    for i in range(2):
        bass.append_note(1, "C3")
        bass.append_rest(1/2)
        bass.append_note(1/2, "G3")
        bass.append_rest(1)
        bass.append_note(1, "C4")

        bass.append_note(1, "F3")
        bass.append_rest(1/2)
        bass.append_note(1/2, "C4")
        bass.append_note(1, "C4")
        bass.append_note(1, "F3")

        bass.append_note(1, "C3")
        bass.append_rest(1/2)
        bass.append_note(1/2, "G3")
        bass.append_rest(1)
        bass.append_note(1/2, "G3")
        bass.append_note(1/2, "C4")

        bass.append_rest(1/2)
        bass.append_note(1/2, "G5")
        bass.append_rest(1/2)
        bass.append_note(1/2, "G5")
        bass.append_note(1, "G5")
        bass.append_note(1, "G3")

        bass.append_note(1, "C3")
        bass.append_rest(1/2)
        bass.append_note(1/2, "G3")
        bass.append_rest(1)
        bass.append_note(1, "C4")

        bass.append_note(1, "F3")
        bass.append_rest(1/2)
        bass.append_note(1/2, "C4")
        bass.append_note(1, "C4")
        bass.append_note(1, "F3")

        bass.append_note(1, "C3")
        bass.append_note(1, "Ab3")
        bass.append_rest(1/2)
        bass.append_note(1, "Bb3")
        bass.append_rest(1/2)

        bass.append_note(1, "C4")
        bass.append_rest(1/2)
        bass.append_note(1/2, "G3")
        bass.append_note(1, "G3")
        bass.append_note(1, "C3")

    return bass

def play():
    track1 = get_melody()
    track2 = get_bass()
    player = Player([track1, track2], track1.sample_rate)
    player.play()