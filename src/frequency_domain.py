import numpy as np
from constants import Constants as c


class FrequencyDomain:
    def __init__(self):
        pass

    def shift_signal(self, signal, doppler_signal):
        shifted_x = np.zeros(
            signal.X.size + int(doppler_signal.center_freq_doppler_shift)
        )
        shifted_x = shifted_x.astype(complex)
        for i, x in enumerate(signal.X):
            shifted_f = (
                i * signal.sampling_rate / signal.samples_number
                + doppler_signal.center_freq_doppler_shift
            )
            shifted_i = int(shifted_f / signal.sampling_rate * signal.samples_number)
            print(
                f"i: {i}, shifted_i: {shifted_i}, f: {i * signal.sampling_rate / signal.samples_number}, shifted_f = {shifted_f}"
            )
            shifted_x[shifted_i] = x
        print("")

        # To trzeba przesuwac jakos na podstawie freqa
        N = len(shifted_x)
        T = N / signal.sampling_rate
        freq = np.fft.fftfreq(N, 1 / N) / T
        shifted_xabs = np.abs(shifted_x) / (N / 2)

        return freq, shifted_x, shifted_xabs
