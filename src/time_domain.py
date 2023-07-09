import numpy as np
from constants import Constants as c


class TimeDomain:
    def __init__(self):
        pass

    def shift_signal(self, signal, doppler_signal):
        if doppler_signal.scale_factor >= 1:
            y = self.shrink_whole_signal(signal, doppler_signal)
            t = signal.t
        elif doppler_signal.scale_factor <= 1:
            y, t = self.broaden_whole_signal(signal, doppler_signal)
        return y, t

    def shrink_whole_signal(self, signal, doppler_signal):
        interp_scale_factor = (
            doppler_signal.scale_factor * c.INTERP_SAMPLE_NUMBER_INCREASE
        )
        doppler_dt = signal.dt / c.INTERP_SAMPLE_NUMBER_INCREASE
        doppler_time_vector = np.arange(0, signal.duration, doppler_dt)
        y_doppler = [0] * signal.t.size
        interpolated_y = np.interp(doppler_time_vector, signal.t, signal.y)
        y_cut_scale_factor_samples = interpolated_y[:: int(interp_scale_factor)]
        y_doppler[0 : y_cut_scale_factor_samples.size] = y_cut_scale_factor_samples
        doppler_signal.sampling_rate = int(
            doppler_signal.sampling_rate
            * interp_scale_factor
            / c.INTERP_SAMPLE_NUMBER_INCREASE
        )
        doppler_signal.samples_number = y_cut_scale_factor_samples.size
        return y_doppler

    def broaden_whole_signal(self, signal, doppler_signal):
        interp_scale_factor = (
            doppler_signal.scale_factor * c.INTERP_SAMPLE_NUMBER_INCREASE
        )
        doppler_signal.scale_factor = (
            int(interp_scale_factor) / c.INTERP_SAMPLE_NUMBER_INCREASE
        )
        doppler_dt = signal.dt / c.INTERP_SAMPLE_NUMBER_INCREASE
        t_out = np.arange(
            0, signal.duration * c.BROADEN_SIGNAL_PLOT_T_LENGTH, doppler_dt
        )
        doppler_time_vector = np.arange(
            0, signal.duration, signal.dt / int(interp_scale_factor)
        )
        interpolated_y = np.interp(doppler_time_vector, signal.t, signal.y)
        y_out = [0] * t_out.size
        y_out[0 : doppler_time_vector.size] = interpolated_y
        doppler_signal.samples_number = doppler_time_vector.size
        return y_out, t_out
