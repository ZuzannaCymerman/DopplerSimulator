from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import sys
from doppler_simulator import DopplerSimulator
import numpy as np
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
            "F0": 10,
            "FMAX":100 ,
            "SAMPLING_RATE": 400,
            "SIGNAL_DURATION": 1,
            "NUMBER_OF_COMPONENTS": 3,
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
        
        doppler_simulator = DopplerSimulator(params)
        self.plot_signals(doppler_simulator.signal, doppler_simulator.dopplerSignal, params["F0"], params["FMAX"])
        self.set_layout()                         

    def the_button_was_toggled(self, checked):
        print("Button was toggled")
    
    def slider_moved(self):
        print("slider moved")
    
    def plot_signals(self, signal, dopplerSignal, f0, fmax):
        if dopplerSignal.t[-1] > signal.t[-1]:
            t = np.arange(0, signal.duration*c.BROADEN_SIGNAL_PLOT_T_LENGTH, signal.dt)
            y = [0]*t.size
            y[0:signal.y.size] = signal.y
            self.timeChart.axes.plot(t,y)
        else:
            self.timeChart.axes.plot(signal.t,signal.y)
        self.dopplerTimeChart.axes.plot(dopplerSignal.t,dopplerSignal.y)    
        self.spectrumChart.axes.stem(signal.freq, signal.Xabs, 'b', markerfmt=" ")
        # self.spectrumChart.axes.plot(signal.freq, signal.Xabs)
        self.spectrumChart.axes.set_xlim(xmin=0,xmax=fmax)
        # self.dopplerSpectrumChart.axes.plot(dopplerSignal.freq, dopplerSignal.Xabs)
        self.dopplerSpectrumChart.axes.stem(dopplerSignal.freq, dopplerSignal.Xabs, 'b', markerfmt=" ")
        self.spectrumChart.axes.set_xlim(xmin=0,xmax=fmax*1.2)
        self.dopplerSpectrumChart.axes.set_xlim(xmin=0,xmax=fmax*1.2)
    
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
    
    def init_Qt_components(self):
        self.setWindowTitle("Doppler simulator")
        self.label.setAlignment(Qt.AlignCenter)
        self.button.clicked.connect(self.the_button_was_toggled)   
        self.slider.valueChanged.connect(self.slider_moved)
        self.timeChart.axes.grid(color='black', linestyle='-', linewidth=0.3)
        self.dopplerTimeChart.axes.grid(color='black', linestyle='-', linewidth=0.3)
        self.spectrumChart.axes.grid(color='black', linestyle='-', linewidth=0.3)
        self.dopplerSpectrumChart.axes.grid(color='black', linestyle='-', linewidth=0.3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    
