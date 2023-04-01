
from broadband_signal import BroadbandSignal
from scipy.fft import fft, ifft, fftfreq, fftshift
import numpy as np
from scipy.interpolate import interp1d
from operator import add
import math
from constants import Constants as c

class DopplerSignal(BroadbandSignal):
    def __init__(self, signal, vo, vs, temperature, direction_o, direction_g, angle, shift_mode ):
        v_sound = 331 + 0.6*temperature 
        if shift_mode == c.ALL_FREQUENCIES_MODE:
            self.y= self.get_doppler_signal_from_all_frequencies(signal, direction_o, direction_g, vo, vs, v_sound)
        elif shift_mode == c.CENTER_FREQUENCY_MODE:
            self.y= self.get_doppler_signal_from_center_frequency(signal, direction_o, direction_g, vo, vs, v_sound)
        
        filtered = list(filter(lambda y: y != 0, self.y))
        self.freq, self.X, self.Xabs = self.fourier(filtered,signal.sampling_rate) 

    def get_doppler_signal_from_all_frequencies(self, signal, direction_o, direction_s, vo, vs, v_sound):
        y_out =[]
        for idx, unit_frequency in enumerate(signal.fourier_components):
            doppler_shift = self.count_doppler_shift(direction_o, unit_frequency, vo, v_sound)
            shifted_frequency = unit_frequency + doppler_shift
            print(f"{idx}. Doppler shift: {doppler_shift} for frequency: {unit_frequency}")
            unit_frequency_signal_y = self.get_unit_frequency_signal_y(signal, unit_frequency)
            unit_frequency_signal_shifted_y = self.shift_signal(doppler_shift, shifted_frequency, signal, unit_frequency, unit_frequency_signal_y)
            # unit_frequency_signal_shifted_y = self.get_unit_frequency_signal_y(signal, unit_frequency)
            if idx == 0:
                 y_out = unit_frequency_signal_shifted_y
            else:
                 y_out = list( np.array(y_out) + np.array(unit_frequency_signal_shifted_y))
        return y_out
    
    def get_doppler_signal_from_center_frequency(self, signal, direction_o, direction_s, vo, vs, v_sound):
        y_out =[]
        doppler_shift = self.count_doppler_shift(direction_o, signal.center_frequency, vo, v_sound)
        for idx, unit_frequency in enumerate(signal.fourier_components):
            shifted_frequency = unit_frequency + doppler_shift
            unit_frequency_signal_y = self.get_unit_frequency_signal_y(signal, unit_frequency)
            unit_frequency_signal_shifted_y = self.shift_signal(doppler_shift, shifted_frequency, signal, unit_frequency, unit_frequency_signal_y)
            if idx == 0:
                 y_out = unit_frequency_signal_shifted_y
            else:
                 y_out = list( np.array(y_out) + np.array(unit_frequency_signal_shifted_y))
        return y_out
    
    def get_unit_frequency_signal_y(self, signal, frequency):
        X = signal.X
        filtered_x = np.zeros(X.size)
        filtered_x = filtered_x.astype(complex)
        filtered_x[int(frequency)] = X[int(frequency)]
        filtered_y = ifft(filtered_x)
        return np.real(filtered_y)
         
    def shift_signal(self, doppler_shift, shifted_frequency, signal, unit_frequency, unit_frequency_signal_y):
        if doppler_shift > 0:
            return self.shrink_signal(signal.t, unit_frequency_signal_y, signal.dt,signal.duration, shifted_frequency, unit_frequency)
        elif doppler_shift < 0:
            return self.broaden_signal(self)
    
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
    
    def count_doppler_shift(self, direction_o, frequency, vo, v_sound):
        doppler_shift = direction_o*frequency*(vo/v_sound)
        #tylko dla przyblizajacergo sie? wzory dodam pozniej. 
        return doppler_shift
        
    def broaden_signal(self):
        return []
    
    def signal_in_db_scale(self, signal):
        pass