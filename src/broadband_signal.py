import numpy as np
import scipy.fftpack as fftpack # We use this one to perform Fourier transforms
from scipy.fft import fft, ifft, fftfreq, fftshift
import random
import math as m

class BroadbandSignal:
    def __init__(self, f0, fmax, dt, duration, sampling_rate, center_frequency):
        self.dt = dt
        self.duration = duration
        self.f0 = f0
        self.fmax = fmax
        self.y = []
        self.X = []
        self.Xabs = []
        self.freq = []
        self.t = np.arange(0, duration, dt)
        self.sampling_rate = sampling_rate
        self.fourier_components = []
        self.center_frequency = center_frequency

    def generate_random_signal(self, t, f0, fmax, numOfComponents):
        y = np.sin(2*np.pi*f0*t)
        r=0
        for i in range(numOfComponents-1):
            r = random.randint(f0,fmax)
            y = y + np.sin(2*np.pi*r*t)
            print(r)
        return y
    
    def fourier(self,y,sampling_rate):
        X = np.fft.fft(y)
        N = len(X)
        n = np.arange(N)
        T = N/sampling_rate
        freq = n/T 
        Xabs = np.abs(X)
        print(f"\033[92mSignal length: {len(y)}\033[0m")
        return freq, X, Xabs
    
    def get_fourier_components_from_fourier(self, X, fmax):
        Xabs = np.abs(X)
        fourier_components = []
        for frequency,amplitude in np.ndenumerate(Xabs):
            if amplitude > 0.1 and 0 < frequency[0] <= fmax:
                fourier_components.append(float(frequency[0]))
        return fourier_components
    
    def cut_noise(self):
        sig_fft_filtered = self.X.copy()
        freq = fftfreq(self.y.size, d=self.dt)
        sig_fft_filtered[np.abs(freq) < self.f0] = 0
        sig_fft_filtered[np.abs(freq) > self.fmax] = 0
        filtered = ifft(sig_fft_filtered)
        return np.real(filtered)
        
        