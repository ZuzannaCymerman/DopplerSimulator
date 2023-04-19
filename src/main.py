from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import sys
from doppler_simulator import DopplerSimulator
import numpy as np
from constants import Constants as c
from doppler_simulator_window import DopplerSimulatorWindow, MplCanvas


class MainWindow(DopplerSimulatorWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.params = {
            "F0": 10,
            "FMAX": 100,
            "SAMPLING_RATE": 30,
            "SIGNAL_DURATION": 1,
            "NUMBER_OF_COMPONENTS": 1,
            "OBSERVER_VELOCITY": 50,
            "OBSERVER_DIRECTION": c.OBSERVER_COMMING_FURTHER,
            "CENTER_FREQUENCY": 50,
            "ANGLE_BETWEEN_V_VECTOR_AND_WAVE_VECTOR": 30,
            "TEMPERATURE": 20,
            "MODE": c.CENTER_FREQUENCY_MODE,
            "SIGNAL_SOURCE": c.SIGNAL_SOURCE_GENERATED,
        }
        self.setDefaults(self.params)
        self.setInputParams()

    def the_button_was_toggled(self):
        self.setInputParams()
        doppler_simulator = DopplerSimulator(self.params)
        self.plot_signals(
            doppler_simulator.signal,
            doppler_simulator.dopplerSignal,
            self.params["F0"],
            self.params["FMAX"],
            self.params["OBSERVER_DIRECTION"],
        )
        self.ratioLabel.setText(f"Ratio: {doppler_simulator.dopplerSignal.ratio}")

    def adjustBroadenSignalPlot(self, signal):
        t = np.arange(0, signal.duration * c.BROADEN_SIGNAL_PLOT_T_LENGTH, signal.dt)
        y = [0] * t.size
        y[0 : signal.y.size] = signal.y
        return t, y

    def plot_signals(self, signal, dopplerSignal, f0, fmax, direction_o):
        self.clearAxes()
        self.adjustAxesGrid()

        if self.params["OBSERVER_DIRECTION"] == c.OBSERVER_COMMING_FURTHER:
            t, y = self.adjustBroadenSignalPlot(signal)
        else:
            t, y = signal.t, signal.y

        self.timeChart.axes.plot(t, y)
        self.dopplerTimeChart.axes.plot(dopplerSignal.t, dopplerSignal.y)

        self.spectrumChart.axes.plot(signal.freq, signal.Xabs)
        self.dopplerSpectrumChart.axes.plot(dopplerSignal.freq, dopplerSignal.Xabs)

        # self.spectrumChart.axes.stem(signal.freq, signal.Xabs, "b", markerfmt=" ")
        # self.dopplerSpectrumChart.axes.stem(
        # dopplerSignal.freq, dopplerSignal.Xabs, "b", markerfmt=" "
        # )

        self.setAxesXlim(fmax)
        self.drawAxes()

    def setInputParams(self):
        self.params["F0"] = int(self.f0_input.text())
        self.params["FMAX"] = int(self.fmax_input.text())
        self.params["SAMPLING_RATE"] = int(self.sampling_rate_input.text())
        self.params["SIGNAL_DURATION"] = float(self.signal_duration_input.text())
        self.params["NUMBER_OF_COMPONENTS"] = int(
            self.number_of_components_input.text()
        )
        if self.observer_direction_combobox.currentText() == "Observer comming closer":
            self.params["OBSERVER_DIRECTION"] = c.OBSERVER_COMMING_CLOSER
        elif (
            self.observer_direction_combobox.currentText() == "Observer comming further"
        ):
            self.params["OBSERVER_DIRECTION"] = c.OBSERVER_COMMING_FURTHER

        self.params["OBSERVER_VELOCITY"] = int(self.slider.value())
        self.params["SIGNAL_SOURCE"] = self.signal_source_combobox.currentText()
        self.params["MODE"] = self.modeCombobox.currentText()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
