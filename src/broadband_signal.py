import numpy as np
import random
from constants import Constants as c


class BroadbandSignal:
    def __init__(
        self, f0, fmax, dt, duration, sampling_rate, center_frequency, samples_number
    ):
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
        self.samples_number = samples_number

    def generate_random_signal(self, t, f0, fmax, numOfComponents):
        y = np.sin(2 * np.pi * f0 * t)
        r = 0
        for i in range(numOfComponents - 1):
            r = random.randint(f0, fmax)
            y = y + np.sin(2 * np.pi * r * t)
            print(r)
        return y

    def fourier(self, y, sr):
        N = len(y)
        Xabs = np.abs(np.fft.rfft(y * np.hamming(N))) / (N / 2)
        # X = np.fft.fft(y)
        X = np.fft.rfft(y * np.hamming(N))
        # Xabs = np.abs(np.fft.rfft(y)) / (N / 2)
        # N = len(X)
        if N > sr:
            T = N / sr / c.INTERP_SAMPLE_NUMBER_INCREASE
        else:
            T = N / sr
        freq = np.fft.rfftfreq(N, 1 / N) / T
        # Xabs = np.abs(np.fft.fft(y)) /(N/2)
        return freq, X, Xabs

    # def fourier_windowed(self,y, sr):
    #     X = np.fft.fft(y)
    #     N = len(X)
    #     if N > sr:
    #         T = N/sr/c.INTERP_SAMPLE_NUMBER_INCREASE
    #     else:
    #         T = N/sr
    #     freq = np.fft.fftfreq(N, 1/N) /T
    #     windowed_y = np.hamming(N) * y
    #     # windowed_y = y
    #     Xabs = np.abs(np.fft.fft(windowed_y)) /(N/2)
    #     return freq, X, Xabs

    def get_fourier_components_from_fourier(self, signal):
        fs = signal.sampling_rate
        Xabs_dB = 20 * np.log10(signal.Xabs)
        treshhold = -45
        ponad = (Xabs_dB >= treshhold).astype(np.int)
        diff = np.diff(ponad)
        starts = np.where(diff == 1)[0] + 1
        ends = np.where(diff == -1)[0] + 1
        fourier_components = dict({"freq": [], "arg": []})
        for start, end in zip(starts, ends):
            p = np.argmax(Xabs_dB[start:end]) + start
            fourier_components["freq"].append(p * fs / signal.samples_number)
            fourier_components["arg"].append(p)
        return fourier_components
