"""
Mini library for generating a tone on the system.
"""

import math
import time

from note_table import notes
from pyaudio import PyAudio


def stopwatch(func):
    def decorator(*args, **kwargs):
        t0 = time.time()
        func(*args, **kwargs)
        t1 = time.time()
        print(f"Function took {t1 - t0} seconds.")
    return decorator


class Sound(object):
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        self.audio = None

    def open(self):
        self.audio = PyAudio()
        self.stream = self.audio.open(format=self.audio.get_format_from_width(1), # 8bit
                                      channels=1,                                 # mono
                                      rate=self.sample_rate,
                                      output=True)

    def play_tone(self, freq, duration, volume=0.5):
        n_samples = int(self.sample_rate * duration)
        print(f"{n_samples} samples, duration={duration}s")

        wave = lambda t: volume * math.sin(2 * math.pi * freq * t / self.sample_rate)

        # Generate a list of samples.
        samples = [
            int(wave(t) * 0x7f + 0x80)
            for t in range(n_samples)
        ]

        self.stream.write(bytes(bytearray(samples)))

    def play_tones(self, freqs, duration, volume=0.5):
        n_samples = int(self.sample_rate * duration)
        print(f"{n_samples} samples, duration={duration}s")

        wave = lambda freq, t: volume * math.sin(2 * math.pi * freq * t / self.sample_rate)

        # Generate a list of samples. Combine frequencies for chords.
        samples = [
            int(sum([
                wave(freq, t)
                for freq in freqs
            ]) * 0x7f + 0x80)
            for t in range(n_samples)
        ]

        self.stream.write(bytes(bytearray(samples)))

    def play_note(self, note, duration, volume=0.1):
        freq = notes[note]
        self.play_tone(freq, duration, volume=volume)

    def play_chord(self, chord, duration, volume=0.1):
        freqs = [notes[note] for note in chord]
        self.play_tones(freqs, duration, volume=volume)

    def close(self):
        # Brief sleep to let the last note ring out.
        # I'm better than this.
        time.sleep(0.2)
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()


sound = Sound()
sound.open()
sound.play_chord(["A4", "C#5"], 1.0)
sound.close()