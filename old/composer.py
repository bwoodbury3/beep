"""
Composes a song from an input format.
"""

from sound import Sound

def beat_to_duration(tempo, beat):
    # tempo is in bpm.
    # beat is a fraction of that.
    return (60.0 / tempo) * beat

def repeat(seq, times):
    return seq * times

class Track(object):
    def __init__(self):
        self.chords = []
        self.offset = 0.0

    def add_note(self, note, beat, tempo):
        self.offset += beat_to_duration(beat)
        self.chords += [
            ((note,), self.offset)
        ]

    def add_chord(self, chord, beat, tempo):
        self.offset += beat_to_duration(beat)
        self.chords += [
            (chord, self.offset)
        ]

class Composer(object):
    def __init__(self, song):
        """
        Compile the song input.
        """
        tempo = song["tempo"]
        tracks = song["tracks"]

        self.all_tracks = []

        # The magic happens here.
        for track_name, track in tracks.items():
            single_track = self._build_single_track(tempo, track_name, track)
            self.all_tracks += [single_track]

        # TODO
        self.built_track = self.all_tracks[0]

    def _build_single_track(self, tempo, track_name, track):
        """
        Build a single track from a dictionary.
        """

        single_track = Track()

        chords = track["chords"]
        for chord in chords:
            if isinstance(chord[1], tuple):
                single_track.add_chord(chord[1], chord[0], tempo)
            else:
                single_track.add_note(chord[1], chord[0], tempo)

        return single_track

    def play_all(self):
        sound = Sound()
        sound.open()

        for track in self.built_track:
            sound.play_note(track[0], track[1] - 0.05)
            sound.play_note("REST", 0.05)

        sound.close()
