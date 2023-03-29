from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import sys
import numpy as np
from broadband_signal import BroadbandSignal
from doppler_signal import DopplerSignal
from scipy.interpolate import interp1d
import math
import pandas as pd

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        
class MainWindow(QMainWindow):
    def the_button_was_toggled(self, checked):
        print("Button was toggled")
    
    def slider_moved(self):
        print("slider moved")
        
    def __init__(self, *args, **kwargs):
        # parameters
        # for environment temperature 10 °C
        TEMPERATURE = 10
        F0 = 1000
        FMAX = 10000
        # cz. probkowania
        SAMPLING_RATE = 96000
        DT = 1/SAMPLING_RATE 
        SIGNAL_DURATION = 0.1
        SAMPLES_NUMBER = SIGNAL_DURATION*SAMPLING_RATE
        NUMBER_OF_COMPONENTS = 3
        OBSERVER_VELOCITY = 50
        SOURCE_VELOCITY = 0
        SOURCE_COMMING_CLOSER = -1
        SOURCE_COMMING_FURTHER = 1
        OBSERVER_COMMING_CLOSER = 1
        OBSERVER_COMMING_FURTHER = -1
        ANGLE_BETWEEN_V_VECTOR_AND_WAVE_VECTOR = 30
        SIGNAL_FILENAME = "dsss_m4_B8000_data3_ks5_0_1s.csv"
        
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Doppler simulator")
    
        # labels
        label = QLabel("Doppler simulator")
        label.setAlignment(Qt.AlignCenter)
        timeLabel =QLabel("Velocity") 
        
        # button
        button = QPushButton("Press Me!")
        button.clicked.connect(self.the_button_was_toggled)
        
        # slider
        slider = QSlider(Qt.Horizontal)
        slider.valueChanged.connect(self.slider_moved)
        # charts
        timeChart = MplCanvas(self, width=8, height=4, dpi=100)
        spectrumChart = MplCanvas(self, width=8, height=4, dpi=100)
        
        dopplerTimeChart=  MplCanvas(self, width=8, height=4, dpi=100)
        dopplerSpectrumChart = MplCanvas(self, width=8, height=4, dpi=100) 
        
        signal = BroadbandSignal(F0,FMAX,DT,SIGNAL_DURATION, SAMPLING_RATE)
        # signal.y = signal.generate_random_signal(signal.t,F0,FMAX,NUMBER_OF_COMPONENTS)
        samples_from_file  = pd.read_csv(SIGNAL_FILENAME)
        signal.y =  np.array(samples_from_file.loc[1:SAMPLES_NUMBER,'data'])
        signal.freq, signal.X, signal.Xabs = signal.fourier(signal.y,signal.sampling_rate)
        signal.fourier_components = signal.get_fourier_components_from_fourier(signal.X, signal.fmax)
        
        dopplerSignal = DopplerSignal(signal, OBSERVER_VELOCITY, SOURCE_VELOCITY, TEMPERATURE, OBSERVER_COMMING_CLOSER, SOURCE_COMMING_CLOSER, ANGLE_BETWEEN_V_VECTOR_AND_WAVE_VECTOR)

        timeChart.axes.plot(signal.t,signal.y)
        spectrumChart.axes.stem(signal.freq, signal.Xabs, 'b', markerfmt=" ", basefmt="-b")
        spectrumChart.axes.set_xlim(xmin=0,xmax=FMAX)
        spectrumChart.axes.set_ylim(ymin=0,ymax=30)
        dopplerTimeChart.axes.plot(signal.t,dopplerSignal.y)
        dopplerSpectrumChart.axes.stem(dopplerSignal.freq, dopplerSignal.Xabs, 'b', markerfmt=" ", basefmt="-b")
        dopplerSpectrumChart.axes.set_xlim(xmin=0,xmax=FMAX)
    
        timeChart.axes.grid(color='black', linestyle='-', linewidth=0.3)
        dopplerTimeChart.axes.grid(color='black', linestyle='-', linewidth=0.3)
        spectrumChart.axes.grid(color='black', linestyle='-', linewidth=0.3)
        dopplerSpectrumChart.axes.grid(color='black', linestyle='-', linewidth=0.3)
         
        #layout 
        layout = QGridLayout()
        layout.addWidget(timeLabel, 0,1)        
        layout.addWidget(slider,1,1)
        layout.addWidget(label, 0,0)
        layout.addWidget(timeChart,2,0)
        layout.addWidget(spectrumChart,2,1)
        layout.addWidget(dopplerTimeChart,3,0)
        layout.addWidget(dopplerSpectrumChart,3,1)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    
if __name__ == "__main__":
    
    # plt.show()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    
