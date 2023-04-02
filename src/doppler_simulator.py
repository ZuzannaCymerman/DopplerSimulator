from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import sys
import numpy as np
from broadband_signal import BroadbandSignal
from doppler_signal import DopplerSignal
import pandas as pd
from constants import Constants as c

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow): 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.label = QLabel("Doppler simulator")
        self.button = QPushButton("Press Me!")
        self.slider = QSlider(Qt.Horizontal)
        self.timeChart = MplCanvas(self, width=8, height=4, dpi=100)
        self.spectrumChart = MplCanvas(self, width=8, height=4, dpi=100)
        self.dopplerTimeChart=  MplCanvas(self, width=8, height=4, dpi=100)
        self.dopplerSpectrumChart = MplCanvas(self, width=8, height=4, dpi=100) 
        self.timeLabel =QLabel("Velocity") 
        self.layout = QGridLayout()
        self.container = QWidget()
        self.init_Qt_components()
        
        params = {
            "F0": 1*c.kHz,
            "FMAX": 100*c.kHz,
            "SAMPLING_RATE": 96*c.kHz,
            "SIGNAL_DURATION": 1,
            "NUMBER_OF_COMPONENTS": 10,
            "OBSERVER_VELOCITY": 50,
            "OBSERVER_DIRECTION": c.OBSERVER_COMMING_CLOSER,
            "SOURCE_VELOCITY": 0,
            "SOURCE_DIRECTION": c.SOURCE_COMMING_CLOSER,
            "CENTER_FREQUENCY": 30*c.kHz,
            "ANGLE_BETWEEN_V_VECTOR_AND_WAVE_VECTOR": 30,
            "TEMPERATURE": 10,
            "MODE": c.ALL_FREQUENCIES_MODE,
            "SIGNAL_SOURCE": c.SIGNAL_SOURCE_GENERATED
        }
                            
        self.simulate_doppler_effect(params)
    
    def simulate_doppler_effect(self, params):
        DT = 1/params["SAMPLING_RATE"]
        SAMPLES_NUMBER = params["SIGNAL_DURATION"]*params["SAMPLING_RATE"]
        SOUND_VELOCITY = 331 + 0.6*params["TEMPERATURE"]
        signal = BroadbandSignal(params["F0"],
                            params["FMAX"],
                            DT,
                            params["SIGNAL_DURATION"], 
                            params["SAMPLING_RATE"], 
                            params["CENTER_FREQUENCY"])
        
        self.create_signal(signal,
                           params["SIGNAL_SOURCE"], 
                           SAMPLES_NUMBER,
                           params["F0"], 
                           params["FMAX"], 
                           params["NUMBER_OF_COMPONENTS"])
        
        dopplerSignal = DopplerSignal(signal, 
                                params["OBSERVER_VELOCITY"], 
                                params["SOURCE_VELOCITY"], 
                                SOUND_VELOCITY, 
                                params["OBSERVER_DIRECTION"], 
                                params["SOURCE_DIRECTION"], 
                                params["ANGLE_BETWEEN_V_VECTOR_AND_WAVE_VECTOR"], 
                                params["MODE"])
 
        self.plot_signals(signal, dopplerSignal, params["F0"], params["FMAX"])
        self.set_layout()
        
    def plot_signals(self, signal, dopplerSignal, f0, fmax):
        self.timeChart.axes.plot(signal.t,signal.y)
        self.spectrumChart.axes.stem(signal.freq, signal.Xabs, 'b', markerfmt=" ")
        self.spectrumChart.axes.set_xlim(xmin=f0,xmax=fmax)
        self.dopplerTimeChart.axes.plot(signal.t,dopplerSignal.y)
        self.dopplerSpectrumChart.axes.stem(dopplerSignal.freq, dopplerSignal.Xabs, 'b', markerfmt=" ")
        self.dopplerSpectrumChart.axes.set_xlim(xmin=f0,xmax=fmax)

    def create_signal(self, signal, signal_source, samples_number, f0,fmax, number_of_components):
        if signal_source == c.SIGNAL_SOURCE_FROM_FILE:
            samples_from_file  = pd.read_csv(c.SIGNAL_FILENAME)
            signal.y =  np.array(samples_from_file.loc[1:samples_number,'data'])
        elif signal_source == c.SIGNAL_SOURCE_GENERATED:
            signal.y = signal.generate_random_signal(signal.t,f0,fmax,number_of_components)
        signal.freq, signal.X, signal.Xabs = signal.fourier(signal.y,signal.sampling_rate)
        signal.fourier_components = signal.get_fourier_components_from_fourier(signal.X, signal.fmax)

    def init_Qt_components(self):
            self.setWindowTitle("Doppler simulator")
            self.label.setAlignment(Qt.AlignCenter)
            self.button.clicked.connect(self.the_button_was_toggled)   
            self.slider.valueChanged.connect(self.slider_moved)
            self.timeChart.axes.grid(color='black', linestyle='-', linewidth=0.3)
            self.dopplerTimeChart.axes.grid(color='black', linestyle='-', linewidth=0.3)
            self.spectrumChart.axes.grid(color='black', linestyle='-', linewidth=0.3)
            self.dopplerSpectrumChart.axes.grid(color='black', linestyle='-', linewidth=0.3)

    def set_layout(self):
        self.layout.addWidget(self.timeLabel, 0,1)        
        self.layout.addWidget(self.slider,1,1)
        self.layout.addWidget(self.label, 0,0)
        self.layout.addWidget(self.timeChart,2,0)
        self.layout.addWidget(self.spectrumChart,2,1)
        self.layout.addWidget(self.dopplerTimeChart,3,0)
        self.layout.addWidget(self.dopplerSpectrumChart,3,1)
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        
    def the_button_was_toggled(self, checked):
        print("Button was toggled")
    
    def slider_moved(self):
        print("slider moved")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    
