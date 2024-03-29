from broadband_signal import BroadbandSignal
from doppler_signal import DopplerSignal
from constants import Constants as c
import numpy as np
import pandas as pd


class DopplerSimulator:
    def __init__(self, params):
        DT = 1 / params["SAMPLING_RATE"]
        SAMPLES_NUMBER = params["SIGNAL_DURATION"] * params["SAMPLING_RATE"]
        # SOUND_VELOCITY = 331 + 0.6 * params["TEMPERATURE"]
        SOUND_VELOCITY = 1500
        self.signal = BroadbandSignal(
            params["F0"],
            params["FMAX"],
            DT,
            params["SIGNAL_DURATION"],
            params["SAMPLING_RATE"],
            params["CENTER_FREQUENCY"],
            SAMPLES_NUMBER,
        )

        self.create_signal(
            self.signal,
            params["SIGNAL_SOURCE"],
            SAMPLES_NUMBER,
            params["F0"],
            params["FMAX"],
            params["NUMBER_OF_COMPONENTS"],
        )

        self.dopplerSignal = DopplerSignal(
            self.signal,
            params["OBSERVER_VELOCITY"],
            SOUND_VELOCITY,
            params["OBSERVER_DIRECTION"],
            params["ANGLE_BETWEEN_V_VECTOR_AND_WAVE_VECTOR"],
            params["DOMAIN"],
        )

    def create_signal(
        self, signal, signal_source, samples_number, f0, fmax, number_of_components
    ):
        if signal_source == c.SIGNAL_SOURCE_FROM_FILE:
            samples_from_file = pd.read_csv(c.SIGNAL_FILENAME)
            signal.y = np.array(samples_from_file.loc[0 : (samples_number - 1), "data"])
        elif signal_source == c.SIGNAL_SOURCE_GENERATED:
            signal.y = signal.generate_random_signal(
                signal.t, f0, fmax, number_of_components
            )
            signal.samples_number = signal.y.size
        signal.freq, signal.X, signal.Xabs = signal.fourier(
            signal.y, signal.sampling_rate, hamming=False
        )
