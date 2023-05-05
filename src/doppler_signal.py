from broadband_signal import BroadbandSignal
import numpy as np
from constants import Constants as c
from time_domain import TimeDomain
from frequency_domain import FrequencyDomain


class DopplerSignal(BroadbandSignal):
    def __init__(self, signal, vo, v_sound, direction_o, angle, shift_mode, domain):
        self.doppler_shifts = []
        self.sampling_rate = signal.sampling_rate
        self.samples_number = signal.samples_number
        self.ratio = 1
        if domain == c.FREQUENCY_DOMAIN:
            self.domain = FrequencyDomain()
        else:
            self.domain = TimeDomain()

        if shift_mode == c.ALL_FREQUENCIES_MODE:
            (
                self.y,
                self.t,
            ) = self.domain.get_doppler_signal_from_all_frequencies(
                self, signal, direction_o, vo, v_sound
            )
        elif shift_mode == c.CENTER_FREQUENCY_MODE:
            self.y, self.t = self.domain.get_doppler_signal_from_center_frequency(
                self, signal, direction_o, vo, v_sound
            )
        filtered = self.y[0 : int(self.samples_number)]
        self.freq, self.X, self.Xabs = self.fourier(
            filtered, self.sampling_rate, hamming=True
        )

    def count_doppler_shift(self, direction_o, frequency, vo, v_sound):
        doppler_shift = direction_o * frequency * (vo / v_sound)
        return doppler_shift
