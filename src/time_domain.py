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
        doppler_time_vector = np.arange(
            0, signal.duration, signal.dt * doppler_signal.scale_factor
        )
        interpolated_y = np.interp(doppler_time_vector, signal.t, signal.y)
        y_out = [0] * signal.t.size
        y_out[0 : doppler_time_vector.size] = interpolated_y
        doppler_signal.samples_number = doppler_time_vector.size
        return y_out

    def broaden_whole_signal(self, signal, doppler_signal):
        doppler_time_vector = np.arange(
            0, signal.duration, signal.dt * doppler_signal.scale_factor
        )
        interpolated_y = np.interp(doppler_time_vector, signal.t, signal.y)
        t_out = np.arange(0, signal.duration / doppler_signal.scale_factor, signal.dt)
        y_out = [0] * t_out.size
        y_out[0 : doppler_time_vector.size] = interpolated_y
        doppler_signal.samples_number = doppler_time_vector.size
        return y_out, t_out
