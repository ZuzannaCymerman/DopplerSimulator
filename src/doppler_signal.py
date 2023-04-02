
from broadband_signal import BroadbandSignal
import numpy as np
from constants import Constants as c

class DopplerSignal(BroadbandSignal):
    def __init__(self, signal, vo, vs, v_sound, direction_o, direction_g, angle, shift_mode ):
        if shift_mode == c.ALL_FREQUENCIES_MODE:
            self.y= self.get_doppler_signal_from_all_frequencies(signal, direction_o, direction_g, vo, vs, v_sound)
        elif shift_mode == c.CENTER_FREQUENCY_MODE:
            self.y= self.get_doppler_signal_from_center_frequency(signal, direction_o, direction_g, vo, vs, v_sound)
        
        filtered = list(filter(lambda y: y != 0, self.y))
        self.freq, self.X, self.Xabs = self.fourier(filtered,signal.sampling_rate) 

    def get_doppler_signal_from_all_frequencies(self, signal, direction_o, direction_s, vo, vs, v_sound):
        y_out =[]
        for idx, unit_frequency in enumerate(signal.fourier_components):
            doppler_shift = self.count_doppler_shift(direction_o, unit_frequency, vo, vs, v_sound)
            shifted_frequency = unit_frequency + doppler_shift
            print(f"{idx}. Doppler shift: {doppler_shift} for frequency: {unit_frequency} with magnitude: {signal.Xabs[int(unit_frequency)]}")
            unit_frequency_signal_y = self.get_unit_frequency_signal_y(signal, unit_frequency)
            unit_frequency_signal_shifted_y = self.shift_signal(doppler_shift, shifted_frequency, signal, unit_frequency, unit_frequency_signal_y)
            # unit_frequency_signal_shifted_y = self.get_unit_frequency_signal_y(signal, unit_frequency)
            if idx == 0:
                 y_out = unit_frequency_signal_shifted_y
            else:
                 y_out = list( np.array(y_out) + np.array(unit_frequency_signal_shifted_y))
        return y_out+self.get_noise(signal)
    
    def get_doppler_signal_from_center_frequency(self, signal, direction_o, direction_s, vo, vs, v_sound):
        y_out =[]
        doppler_shift = self.count_doppler_shift(direction_o, signal.center_frequency, vo,vs, v_sound)
        for idx, unit_frequency in enumerate(signal.fourier_components):
            shifted_frequency = unit_frequency + doppler_shift
            unit_frequency_signal_y = self.get_unit_frequency_signal_y(signal, unit_frequency)
            unit_frequency_signal_shifted_y = self.shift_signal(doppler_shift, shifted_frequency, signal, unit_frequency, unit_frequency_signal_y)
            if idx == 0:
                 y_out = unit_frequency_signal_shifted_y
            else:
                 y_out = list( np.array(y_out) + np.array(unit_frequency_signal_shifted_y))
        return y_out+self.get_noise(signal)
    
    def get_noise(self, signal):
        noise_x = signal.X
        for component_frequency in signal.fourier_components:
               noise_x[int(component_frequency)] = 0j
        noise_y = np.fft.ifft(noise_x)
        return np.real(noise_y)
            
    def get_unit_frequency_signal_y(self, signal, frequency):
        filtered_x = np.zeros(signal.X.size)
        filtered_x = filtered_x.astype(complex)
        filtered_x[int(frequency)] = signal.X[int(frequency)]
        for component_frequency in signal.fourier_components:
            if component_frequency != frequency:
                filtered_x[int(component_frequency)] = 0j
        filtered_y = np.fft.ifft(filtered_x)
        return np.real(filtered_y)
         
    def shift_signal(self, doppler_shift, shifted_frequency, signal, unit_frequency, unit_frequency_signal_y):
        if doppler_shift > 0:
            return self.shrink_signal(signal.t, unit_frequency_signal_y, signal.dt,signal.duration, shifted_frequency, unit_frequency)
        elif doppler_shift < 0:
            return self.broaden_signal(self)
    
    def shrink_signal(self, signal_t, signal_y, dt, duration, shifted_frequency, signal_frequency):
        ratio = float("{:.3f}".format(shifted_frequency/signal_frequency))*10
        doppler_dt = dt/10
        doppler_time_vector = np.arange(0, duration, doppler_dt)
        y_doppler=[0]*signal_t.size
        interpolated_y = np.interp(doppler_time_vector, signal_t, signal_y)
        y_cut_ratio_samples = interpolated_y[::int(ratio)]
        y_doppler[0:y_cut_ratio_samples.size] = y_cut_ratio_samples
        return y_doppler
    
    def count_doppler_shift(self, direction_o, frequency, vo, vs, v_sound):
        doppler_shift = direction_o*frequency*(1+2*(vo+vs)/v_sound)
        #tylko dla przyblizajacergo sie? wzory dodam pozniej. 
        return doppler_shift
        
    def broaden_signal(self):
        return []
