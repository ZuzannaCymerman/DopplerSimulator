import numpy as np
from constants import Constants as c


class TimeDomain:
    def __init__(self):
        pass

    def shrink_signal(
        self,
        doppler_signal,
        signal_t,
        signal_y,
        dt,
        duration,
        shifted_frequency,
        signal_frequency,
    ):
        ratio = float("{:.3f}".format(shifted_frequency / signal_frequency))
        interp_ratio = ratio * c.INTERP_SAMPLE_NUMBER_INCREASE
        doppler_signal.ratio = int(interp_ratio) / c.INTERP_SAMPLE_NUMBER_INCREASE

        doppler_dt = dt / c.INTERP_SAMPLE_NUMBER_INCREASE
        doppler_time_vector = np.arange(0, duration, doppler_dt)
        y_doppler = [0] * signal_t.size
        interpolated_y = np.interp(doppler_time_vector, signal_t, signal_y)
        y_cut_ratio_samples = interpolated_y[:: int(interp_ratio)]
        y_doppler[0 : y_cut_ratio_samples.size] = y_cut_ratio_samples
        # doppler_signal.sampling_rate = int(
        #     doppler_signal.sampling_rate * interp_ratio / c.INTERP_SAMPLE_NUMBER_INCREASE
        # )
        doppler_signal.samples_number = y_cut_ratio_samples.size
        return y_doppler, signal_t

    def broaden_signal(
        self,
        doppler_signal,
        signal_t,
        signal_y,
        dt,
        duration,
        shifted_frequency,
        signal_frequency,
    ):
        ratio = float("{:.3f}".format(signal_frequency / shifted_frequency))
        interp_ratio = ratio * c.INTERP_SAMPLE_NUMBER_INCREASE
        doppler_signal.ratio = int(interp_ratio) / c.INTERP_SAMPLE_NUMBER_INCREASE
        doppler_dt = dt / c.INTERP_SAMPLE_NUMBER_INCREASE
        t_out = np.arange(0, duration * c.BROADEN_SIGNAL_PLOT_T_LENGTH, doppler_dt)
        doppler_time_vector = np.arange(0, duration, dt / int(interp_ratio))
        interpolated_y = np.interp(doppler_time_vector, signal_t, signal_y)
        y_out = [0] * t_out.size
        y_out[0 : doppler_time_vector.size] = interpolated_y
        # find how many samples are in 1s
        # self.sampling_rate = np.where(t_out == min(t_out, key=lambda x: abs(x - 1)))[0]
        doppler_signal.samples_number = doppler_time_vector.size
        return y_out, t_out

    def get_doppler_signal_from_all_frequencies(
        self, doppler_signal, signal, direction_o, vo, v_sound
    ):
        y_out = []
        for idx, unit_frequency in enumerate(signal.fourier_components["freq"]):
            doppler_shift = doppler_signal.count_doppler_shift(
                direction_o, unit_frequency, vo, v_sound
            )
            shifted_frequency = unit_frequency + doppler_shift
            print(
                f"\033[92m{idx}. f0: {unit_frequency}, fout: {unit_frequency+doppler_shift}, ds: {doppler_shift}\033[0m"
            )
            unit_frequency_signal_y = self.get_unit_frequency_signal_y(
                signal, unit_frequency
            )
            unit_frequency_signal_shifted_y, doppler_t = self.shift_signal(
                doppler_signal,
                doppler_shift,
                shifted_frequency,
                signal,
                unit_frequency,
                unit_frequency_signal_y,
            )
            if idx == 0:
                y_out = unit_frequency_signal_shifted_y
            else:
                y_out = list(
                    np.array(y_out) + np.array(unit_frequency_signal_shifted_y)
                )
        return y_out, doppler_t

    def get_doppler_signal_from_center_frequency(
        self, doppler_signal, signal, direction_o, vo, v_sound
    ):
        y_out = []
        doppler_shift = doppler_signal.count_doppler_shift(
            direction_o, signal.center_frequency, vo, v_sound
        )
        shifted_frequency = signal.center_frequency + doppler_shift
        y_out, doppler_t = self.shift_signal(
            doppler_signal,
            doppler_shift,
            shifted_frequency,
            signal,
            signal.center_frequency,
            signal.y,
        )
        return y_out, doppler_t

    def get_unit_frequency_signal_y(self, signal, frequency):
        filtered_x = np.zeros(signal.X.size)
        filtered_x = filtered_x.astype(complex)

        fourier_components_freqs = signal.fourier_components["freq"]
        fourier_components_args = signal.fourier_components["arg"]
        fourier_components_starts = signal.fourier_components["start"]
        fourier_components_ends = signal.fourier_components["end"]

        freq_index = fourier_components_freqs.index(frequency)
        frequency_x_arg = fourier_components_args[freq_index]
        frequency_start = fourier_components_starts[freq_index]
        frequency_end = fourier_components_ends[freq_index]

        for i in range(frequency_start, frequency_end):
            filtered_x[i] = signal.X[i]
        filtered_y = np.fft.irfft(filtered_x)
        filtered_y = filtered_y / np.hamming(filtered_y.size)
        return filtered_y

    def shift_signal(
        self,
        doppler_signal,
        doppler_shift,
        shifted_frequency,
        signal,
        unit_frequency,
        unit_frequency_signal_y,
    ):
        if doppler_shift >= 0:
            y, t = self.shrink_signal(
                doppler_signal,
                signal.t,
                unit_frequency_signal_y,
                signal.dt,
                signal.duration,
                shifted_frequency,
                unit_frequency,
            )
        elif doppler_shift < 0:
            y, t = self.broaden_signal(
                self,
                doppler_signal,
                signal.t,
                unit_frequency_signal_y,
                signal.dt,
                signal.duration,
                shifted_frequency,
                unit_frequency,
            )
        return y, t
