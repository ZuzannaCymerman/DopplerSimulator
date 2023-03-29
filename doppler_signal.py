
from broadband_signal import BroadbandSignal
from scipy.fft import fft, ifft, fftfreq, fftshift
import numpy as np
from scipy.interpolate import interp1d
from operator import add
import math


class DopplerSignal(BroadbandSignal):
    def __init__(self, signal, vo, vs, temperature, direction_o, direction_g, angle):
        v_sound = 331 + 0.6*temperature
        self.y= self.get_doppler_signal_from_all_frequencies(signal, direction_o, direction_g, vo, vs, v_sound,angle)
        filtered = list(filter(lambda y: y != 0, self.y))
        self.freq, self.X, self.Xabs = self.fourier(filtered,signal.sampling_rate) 
        # self.t_center_f, self.y_center_f, self.xf_center_f, self.yf_center_f = self.get_doppler_signal_from_center_frequency(signal, direction_o, direction_g, vo, vs, v_sound)

    def get_doppler_signal_from_all_frequencies(self, signal, direction_o, direction_s, vo, vs, v_sound, angle):
        y_out =[]
        for idx, unit_frequency in enumerate(signal.fourier_components):
            # wzor na odchylke kiedy observer sie porusza
            doppler_shift = direction_o*unit_frequency*(vo/v_sound)
            # przesunieta czestotliwosc 
            shifted_frequency = unit_frequency + doppler_shift
            print(shifted_frequency)
            if doppler_shift > 0:
                unit_frequency_signal_y = self.get_unit_frequency_signal_y(signal, unit_frequency)
                unit_frequency_signal_shifted_y = self.shrink_signal(signal.t, unit_frequency_signal_y, signal.dt,signal.duration, shifted_frequency, unit_frequency)
            if idx == 0:
                 y_out = unit_frequency_signal_shifted_y
            else:
                 y_out = list( np.array(y_out) + np.array(unit_frequency_signal_shifted_y))
        return y_out
    
    def get_unit_frequency_signal_y(self, signal, frequency):
        sig_fft_filtered = signal.X.copy()
        freq = fftfreq(signal.y.size, d=signal.dt)
        sig_fft_filtered[np.abs(freq) != frequency] = 0
        filtered = ifft(sig_fft_filtered)
        return np.real(filtered)
        
    def get_doppler_signal_from_center_frequency(self, signal, direction_o, direction_s, vo, vs, v_sound):
        pass
    
    def shrink_signal(self, signal_t, signal_y, dt, duration, shifted_frequency, signal_frequency):
        # liczymy proporcje jak skurczy sie sygnal, np dla sygnalu wezszego 2 razy bedzie ratio = 2
        ratio = float("{:.3f}".format(shifted_frequency/signal_frequency))*10
        doppler_dt = dt/10
        doppler_time_vector = np.arange(0, duration, doppler_dt)
        y_doppler=[0]*signal_t.size
        interpolated_y = np.interp(doppler_time_vector, signal_t, signal_y)
        y_cut_ratio_samples = interpolated_y[::int(ratio)]
        y_doppler[0:y_cut_ratio_samples.size] = y_cut_ratio_samples
        return y_doppler
    
    def broaden_signal(self, signal, fd, fs):
        pass
    
    def signal_in_db_scale(self, signal):
        pass