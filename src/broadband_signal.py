import numpy as np
import random
from constants import Constants as c

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
    
    def fourier(self,y, sr):
        X = np.fft.fft(y)
        fs = len(X)
        if fs > sr:
            T = fs/sr/c.INTERP_SAMPLE_NUMBER_INCREASE
        else:
            T = fs/sr
        freq = np.fft.fftfreq(fs, 1/fs) /T
        Xabs = np.abs(np.fft.fft(y)) /(fs/2)
        return freq, X, Xabs
    
    def get_fourier_components_from_fourier(self, Xabs, fmax):
        fourier_components = []
        for frequency, magnitude in np.ndenumerate(Xabs):
            if magnitude > 1e-3 and 0 < frequency[0] <= fmax:
                fourier_components.append(float(frequency[0]))
        return fourier_components
        