import numpy as np
from constants import Constants as c


class FrequencyDomain:
    def __init__(self):
        pass

    def shift_spectrum_unit(self, signal, frequency, doppler_shift):
        shifted_x = np.zeros(signal.X.size)
        shifted_x = shifted_x.astype(complex)
        target_frequency = frequency + doppler_shift
        fourier_components_freqs = signal.fourier_components["freq"]
        fourier_components_starts = signal.fourier_components["start"]
        fourier_components_ends = signal.fourier_components["end"]
        fourier_components_args = signal.fourier_components["arg"]
        target_frequency_arg = int(
            target_frequency / signal.sampling_rate * signal.samples_number
        )
        freq_index = fourier_components_freqs.index(frequency)

        frequency_x_arg = fourier_components_args[freq_index]
        frequency_start = fourier_components_starts[freq_index]
        frequency_end = fourier_components_ends[freq_index]
        freq_arg_shift = target_frequency_arg - frequency_x_arg
        for i in range(frequency_start, frequency_end):
            target_arg = i + freq_arg_shift
            if target_arg < shifted_x.size:
                shifted_x[target_arg] = signal.X[i]
        return shifted_x

    def get_doppler_signal_from_all_frequencies(
        self, doppler_signal, signal, direction_o, vo, v_sound
    ):
        for idx, unit_frequency in enumerate(signal.fourier_components["freq"]):
            doppler_shift = doppler_signal.count_doppler_shift(
                direction_o, unit_frequency, vo, v_sound
            )
            print(
                f"\033[92m{idx}. f0: {unit_frequency}, fout: {unit_frequency+doppler_shift}, ds: {doppler_shift}\033[0m"
            )
            shifted_unit_spectrum = self.shift_spectrum_unit(
                signal, unit_frequency, doppler_shift
            )
            if idx == 0:
                x_out = shifted_unit_spectrum
            else:
                x_out = list(np.array(x_out) + np.array(shifted_unit_spectrum))
        y_out = np.fft.irfft(x_out)
        y_out = y_out / np.hamming(y_out.size)
        return y_out, signal.t

    def get_doppler_signal_from_center_frequency(
        self, doppler_signal, signal, direction_o, vo, v_sound
    ):
        doppler_shift = doppler_signal.count_doppler_shift(
            direction_o, signal.center_frequency, vo, v_sound
        )
        for idx, unit_frequency in enumerate(signal.fourier_components["freq"]):
            print(
                f"\033[92m{idx}. f0: {unit_frequency}, fout: {unit_frequency+doppler_shift}, ds: {doppler_shift}\033[0m"
            )
            shifted_unit_spectrum = self.shift_spectrum_unit(
                signal, unit_frequency, doppler_shift
            )
            if idx == 0:
                x_out = shifted_unit_spectrum
            else:
                x_out = list(np.array(x_out) + np.array(shifted_unit_spectrum))
        y_out = np.fft.irfft(x_out)
        y_out = y_out / np.hamming(y_out.size)
        return y_out, signal.t
