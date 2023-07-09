from broadband_signal import BroadbandSignal
import numpy as np
from constants import Constants as c
from time_domain import TimeDomain
from frequency_domain import FrequencyDomain


class DopplerSignal(BroadbandSignal):
    def __init__(self, signal, vo, v_sound, direction_o, angle, domain):
        self.doppler_shifts = []
        self.sampling_rate = signal.sampling_rate
        self.samples_number = signal.samples_number
        self.scale_factor = self.count_scale_factor(direction_o, vo, v_sound, angle)
        self.center_freq_doppler_shift = self.count_doppler_shift(
            direction_o, signal.center_frequency, vo, v_sound
        )

        if domain == c.FREQUENCY_DOMAIN:
            self.domain = FrequencyDomain()
            self.freq, self.X, self.Xabs = self.domain.shift_signal(signal, self)
            self.y = np.fft.irfft(self.X)
            t = np.arange(
                0,
                signal.duration,
                1 / self.y.size * signal.duration,
            )
            self.t = t[0 : self.y.size]
        else:
            self.domain = TimeDomain()
            self.y, self.t = self.domain.shift_signal(signal, self)
        filtered = self.y[0 : int(self.samples_number)]
        self.freq, self.X, self.Xabs = self.fourier(
            filtered, self.sampling_rate, hamming=False
        )

    def count_doppler_shift(self, direction_o, frequency, vo, v_sound):
        # doppler_shift = direction_o * frequency * (vo / v_sound)
        doppler_shift = frequency * self.scale_factor - frequency
        return doppler_shift

    def count_scale_factor(self, direction_o, vo, v_sound, angle):
        scale_factor = round((v_sound + direction_o * vo) / (v_sound), 5)
        return scale_factor
