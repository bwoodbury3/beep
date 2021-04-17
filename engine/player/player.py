"""
Plays one or more tracks.
"""

from engine.tracks import Track

from contextlib import contextmanager
from pyaudio import PyAudio
from sortedcontainers import SortedList

CHUNK_SIZE = 1.0
"""
Cache in 1 second increments.
"""

class WaveCollapser(object):
    """
    Engine which takes a series of tracks and can be iterated on to produce the
    N seconds of playtime.
    """
    def __init__(self, waveforms: list, sample_rate: int):
        self.waveforms = waveforms
        self.sample_rate = sample_rate

    def collapse(self, t0: float, duration: float) -> SortedList:
        """
        returns a collapsed wave from t0 for the specified duration. Returns
        an empty list if the wave requested is past the last wave.
        """
        print(f"Collapsing interval {t0}")

        # First, add all of the waves that are in this range.
        waves = SortedList()
        reached_end = True
        for i in range(len(self.waveforms)):
            reached_end = i == len(self.waveforms) - 1

            if self.waveforms[i].time + self.waveforms[i].waveform.duration < t0:
                continue
            elif self.waveforms[i].time < t0 + duration:
                waves.add(self.waveforms[i])
            else:
                break

        # We seeked past the end of the list of waveforms and found nothing.
        # Return an empty list, per the function description.
        if len(waves) == 0 and reached_end:
            return []

        # Otherwise, add all of the parts of the wave that apply to this time
        # range.
        samples = [0] * int(self.sample_rate * duration)
        for wave in waves:
            # sample_start either the start or partway through.
            sample_start_idx = max(0, int((wave.time - t0) * self.sample_rate))

            # Waveform start is either the start or partway through.
            wave_start_idx = max(0, int((t0 - wave.time) * self.sample_rate))
            # Waveform end is the duration of this waveform, truncated by the
            # length of the sample.
            wave_end_idx = min(wave.waveform.num_samples,
                               wave_start_idx + len(samples) - sample_start_idx)

            print(f"Playing wave: {wave.waveform.freq} t={wave.time}, "
                + f"seq [{wave_start_idx}, {wave_end_idx}) "
                + f"starting at: {sample_start_idx}")

            # Cool, now just add this sample to our array of samples.
            wave_samples = wave.waveform.get_samples(wave_start_idx, wave_end_idx)
            for i in range(len(wave_samples)):
                samples[i + sample_start_idx] += wave_samples[i]

        for i in range(len(samples)):
            # What is this even doing?
            samples[i] = int(samples[i] * 0x7f + 0x80)

        # print(samples)
        return samples


class Player(object):
    def __init__(self, tracks: list, sample_rate: int):
        self.tracks = tracks
        self.sample_rate = sample_rate
        self.audio = PyAudio()

    @contextmanager
    def open_stream(self):
        # Open the stream.
        print("Opening stream.")
        self.stream = self.audio.open(format=self.audio.get_format_from_width(1), # 8bit
                                      channels=1,                                 # mono
                                      rate=self.sample_rate,
                                      output=True)
        try:
            yield
        finally:
            print("Closing stream")
            self.stream.stop_stream()
            self.stream.close()

    def play(self):
        compiled_track = sum(self.tracks)
        waveforms = compiled_track.waveforms

        # Main play algorithm.
        wave_collapser = WaveCollapser(waveforms, self.sample_rate)

        with self.open_stream():
            t = 0.0
            samples = wave_collapser.collapse(t, CHUNK_SIZE)
            while len(samples) > 0:
                self.stream.write(bytes(bytearray(samples)))
                t += CHUNK_SIZE
                samples = wave_collapser.collapse(t, CHUNK_SIZE)
