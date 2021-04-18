"""
Plays one or more tracks.
"""

import engine.player.sample as sample

from engine import debug, info
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

    def __init__(self, waveforms: list, sample_rate: int, sample_width: int):
        """
        Initialize a wave collapser with the following attributes.

        Args:
            waveforms: A list of waveforms that are to be played.
            sample_rate: The sample rate.
            sample_width: The bit width of each sample.
        """
        self.waveforms = waveforms
        self.sample_rate = sample_rate
        self.sampler = sample.get_sampler_from_width(sample_width)

    def collapse(self, t0: float, duration: float, volume: float) -> list:
        """
        Returns the sum of all waveforms between [t0, t0 + duration). This is
        guts of the algorithm that allows us to play many sounds at the same
        time, even when the sounds have different start/stop times.

        Args:
            t0: The start time of this collapse interval.
            duration: The chunk size to collapse.
            volume: The volume to play at, expressed as a multiplier in the
                    range [0.0, 1.0]. Audio that exceeds the max amplitude of
                    our bit width will be truncated.

        Returns:
            A series of bytes that can be passed to pyaudio as frames.

        Note that volume is passed in on each call to `collapse()`. This allows
        the user the flexibility to change the volume in the middle of playback.
        """
        debug(f"Collapsing interval {t0}")

        # First, add all of the waves that are in this range.
        waves = []
        reached_end = True
        for i in range(len(self.waveforms)):
            reached_end = i == len(self.waveforms) - 1

            if self.waveforms[i].time + self.waveforms[i].waveform.duration < t0:
                continue
            elif self.waveforms[i].time < t0 + duration:
                waves.append(self.waveforms[i])
            else:
                break

        ###################################
        # Main wave generation algorithm. #
        ###################################

        # Step 1. If t0 is beyond the end of our samples, return an empty list.
        # This is a signal to our caller that we are done playing music.
        if len(waves) == 0 and reached_end:
            return []

        # Step 2. Initialize an empty sample array for each sample in the
        # duration.
        samples = [0] * int(self.sample_rate * duration)

        # Step 3. For each wave, sum up each sample against the existing samples.
        # This is accomplished by calculating the start point within the sample
        # interval and the start point within the waveform. Sum up samples until
        # either the end of the interval or the end of the waveform.
        for wave in waves:
            interval_start_idx = max(0,
                                     int((wave.time - t0) * self.sample_rate))
            wave_start_idx = max(0,
                                 int((t0 - wave.time) * self.sample_rate))
            wave_end_idx = min(wave.waveform.num_samples,
                               wave_start_idx + len(samples) - interval_start_idx)

            debug(f"Playing wave: {wave.waveform.freq} t={wave.time}, " +
                  f"wave sample: [{wave_start_idx}, {wave_end_idx}) " +
                  f"chunk offset: {interval_start_idx}")

            # Add this sample to our array of samples.
            wave_samples = wave.waveform.get_samples(wave_start_idx, wave_end_idx)
            for i in range(len(wave_samples)):
                samples[i + interval_start_idx] += wave_samples[i]

        # Step 4. Initialize an empty array of "frames". Frames are one byte, so
        # we need to create a list of size (bit_width * samples).
        num_bytes = self.sampler.bytes_per_sample()
        frames = bytearray(len(samples) * num_bytes)

        # Step 5. For each sample, convert the floating point representation to
        # a frame of the correct bit width. See engine.player.sample.Sampler.
        for i in range(len(samples)):
            full_frame = self.sampler.convert(volume * samples[i])
            for j in range(num_bytes):
                b = (full_frame >> (8 * j)) & 0xFF
                frames[i * num_bytes + j] = b

        return frames


class Player(object):
    """
    Plays a list of tracks.
    """
    def __init__(self,
                 tracks: list,
                 sample_rate: int,
                 volume=0.5,
                 sample_width=16):
        """
        Initialize an audio player.

        Args:
            tracks: A list of Tracks to play.
            sample_rate: The sample rate (samples per second).
            volume: Volume between [0.0, 1.0) at which to play the audio.
                    Combined audio will be truncated if it exceeds 1.0.
            sample_width: The bit width at which to play the tracks. Supported
                          widths include 8-bit, 16-bit, 24-bit.
        """
        self.tracks = tracks
        self.sample_rate = sample_rate
        self.audio = PyAudio()
        self.volume = volume
        self.sample_width = sample_width

        debug("Added tracks: " + str([track.name for track in self.tracks]))

    @contextmanager
    def _open_stream(self):
        # Open the stream.
        debug("Opening stream.")
        self.stream = self.audio.open(
            format=self.audio.get_format_from_width(self.sample_width / 8), # 8bit
            channels=1,                                                     # mono
            rate=self.sample_rate,
            output=True
        )

        try:
            yield
        finally:
            debug("Closing stream")
            self.stream.stop_stream()
            self.stream.close()

    def play(self):
        compiled_track = sum(self.tracks)
        waveforms = compiled_track.waveforms

        # Main play algorithm.
        wave_collapser = WaveCollapser(waveforms,
                                       self.sample_rate,
                                       self.sample_width)

        with self._open_stream():
            info("Beginning playback...")

            t = 0.0
            samples = wave_collapser.collapse(t, CHUNK_SIZE, self.volume)
            while len(samples) > 0:
                self.stream.write(bytes(bytearray(samples)))
                t += CHUNK_SIZE
                samples = wave_collapser.collapse(t, CHUNK_SIZE, self.volume)

        info("Playback complete.")
