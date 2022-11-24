

import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack as fftpack # We use this one to perform Fourier transforms
import random
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import sys
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        
class MainWindow(QMainWindow):
    def the_button_was_toggled(self, checked):
        print("Button was toggled")
        
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Doppler simulator")
    
        #label
        label = QLabel("Doppler simulator")
        label.setAlignment(Qt.AlignCenter)
        
        #button
        button = QPushButton("Press Me!")
        button.clicked.connect(self.the_button_was_toggled)
        
        #plot
        pi = np.pi
        points = 1000
        x = np.linspace(0, 3*pi,points)
        chart = MplCanvas(self, width=8, height=4, dpi=100)
        chart.axes.plot(x,f(x))
        
        #layout 
        layout = QVBoxLayout()        
        layout.addWidget(button)
        layout.addWidget(label)
        layout.addWidget(chart)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
def f(x):
    
    #sygnal szerokopasmowy 6 Hz - 6000 Hz 
    f0 = 6
    fmax = 6e3
    npx = np.sin(f0*x)
    for i in range(10):
        r = random.randint(f0,fmax)
        npx = npx + np.sin(r*x)
    return npx
    
if __name__ == "__main__":
    
    # plt.show()
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    
