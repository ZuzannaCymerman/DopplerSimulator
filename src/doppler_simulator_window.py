from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from doppler_simulator import DopplerSimulator
import numpy as np
from constants import Constants as c


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class DopplerSimulatorWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(DopplerSimulatorWindow, self).__init__(*args, **kwargs)
        self.addQtComponents()
        self.init_Qt_components()
        self.set_layout()

    def slider_moved(self):
        self.velocityLabel.setText(f"Velocity: {int(self.slider.value())}")
        self.slider.setValue(int(self.slider.value() / 10) * 10)

    def addQtComponents(self):
        self.label = QLabel("Doppler simulator")
        self.button = QPushButton("Run")
        self.f0_input = QLineEdit()
        self.fmax_input = QLineEdit()
        self.sampling_rate_input = QLineEdit()
        self.signal_duration_input = QLineEdit()
        self.number_of_components_input = QLineEdit()
        self.observer_direction_combobox = QComboBox()
        self.signal_source_combobox = QComboBox()
        self.domain_combobox = QComboBox()
        self.domain_label = QLabel("Shift domain")
        self.f0_label = QLabel("F0")
        self.fmax_label = QLabel("Fmax")
        self.sampling_rate_label = QLabel("Sampling rate")
        self.signal_duration_label = QLabel("Signal duration")
        self.number_of_components_label = QLabel("Number of components")
        self.observer_direction_label = QLabel("Observer direction")
        self.signal_source_label = QLabel("Signal source")
        self.slider = QSlider(Qt.Horizontal)
        self.timeChart = MplCanvas(self, width=8, height=4, dpi=100)
        self.spectrumChart = MplCanvas(self, width=8, height=4, dpi=100)
        self.dopplerTimeChart = MplCanvas(self, width=8, height=4, dpi=100)
        self.dopplerSpectrumChart = MplCanvas(self, width=8, height=4, dpi=100)
        self.velocityLabel = QLabel("Velocity: 0")
        self.layout = QGridLayout()
        self.chart_layout = QGridLayout()
        self.chart_layout2 = QGridLayout()
        self.control_layout = QGridLayout()
        self.container = QWidget()
        self.chart_container = QWidget()
        self.chart_container2 = QWidget()
        self.control_container = QWidget()
        self.ratioLabel = QLabel("Ratio: 0")
        self.centerFrequencyLabel = QLabel("Center frequency")
        self.centerFrequencyInput = QLineEdit()

    def set_layout(self):
        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.button, 0, 1)
        self.layout.addWidget(self.ratioLabel, 0, 2)

        self.control_layout.addWidget(self.velocityLabel, 1, 0)
        self.control_layout.addWidget(self.slider, 1, 1)
        self.control_layout.addWidget(self.observer_direction_label, 2, 0)
        self.control_layout.addWidget(self.signal_source_label, 3, 0)
        self.control_layout.addWidget(self.f0_label, 4, 0)
        self.control_layout.addWidget(self.fmax_label, 5, 0)
        self.control_layout.addWidget(self.sampling_rate_label, 6, 0)
        self.control_layout.addWidget(self.signal_duration_label, 7, 0)
        self.control_layout.addWidget(self.number_of_components_label, 8, 0)
        self.control_layout.addWidget(self.observer_direction_combobox, 2, 1)
        self.control_layout.addWidget(self.signal_source_combobox, 3, 1)
        self.control_layout.addWidget(self.f0_input, 4, 1)
        self.control_layout.addWidget(self.fmax_input, 5, 1)
        self.control_layout.addWidget(self.sampling_rate_input, 6, 1)
        self.control_layout.addWidget(self.signal_duration_input, 7, 1)
        self.control_layout.addWidget(self.number_of_components_input, 8, 1)
        self.control_layout.addWidget(self.centerFrequencyLabel, 10, 0)
        self.control_layout.addWidget(self.centerFrequencyInput, 10, 1)
        self.control_layout.addWidget(self.domain_label, 11, 0)
        self.control_layout.addWidget(self.domain_combobox, 11, 1)

        self.chart_layout.addWidget(self.timeChart, 1, 0)
        self.chart_layout2.addWidget(self.spectrumChart, 1, 0)
        self.chart_layout.addWidget(self.dopplerTimeChart, 2, 0)
        self.chart_layout2.addWidget(self.dopplerSpectrumChart, 2, 0)

        self.chart_container.setLayout(self.chart_layout)
        self.chart_container2.setLayout(self.chart_layout2)
        self.control_container.setLayout(self.control_layout)

        self.layout.addWidget(self.control_container, 1, 0)
        self.layout.addWidget(self.chart_container, 1, 1)
        self.layout.addWidget(self.chart_container2, 1, 2)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def init_Qt_components(self):
        self.setWindowTitle("Doppler simulator")
        self.label.setAlignment(Qt.AlignCenter)
        self.f0_label.setAlignment(Qt.AlignRight)
        self.fmax_label.setAlignment(Qt.AlignRight)
        self.velocityLabel.setAlignment(Qt.AlignRight)
        self.sampling_rate_label.setAlignment(Qt.AlignRight)
        self.signal_source_label.setAlignment(Qt.AlignRight)
        self.signal_duration_label.setAlignment(Qt.AlignRight)
        self.observer_direction_label.setAlignment(Qt.AlignRight)
        self.number_of_components_label.setAlignment(Qt.AlignRight)
        self.domain_label.setAlignment(Qt.AlignRight)
        self.button.clicked.connect(self.the_button_was_toggled)
        self.slider.valueChanged.connect(self.slider_moved)
        self.slider.setMaximum(100)
        self.observer_direction_combobox.addItems(
            ["Observer comming closer", "Observer comming further"]
        )
        self.signal_source_combobox.addItems(["Generated", "From file"])
        self.ratioLabel.setAlignment(Qt.AlignCenter)
        self.domain_combobox.addItems(["Time domain", "Frequency domain"])
        self.centerFrequencyLabel.setAlignment(Qt.AlignRight)

    def clearAxes(self):
        self.timeChart.axes.clear()
        self.spectrumChart.axes.clear()
        self.dopplerTimeChart.axes.clear()
        self.dopplerSpectrumChart.axes.clear()

    def drawAxes(self):
        self.timeChart.draw()
        self.spectrumChart.draw()
        self.dopplerTimeChart.draw()
        self.dopplerSpectrumChart.draw()

    def adjustAxesGrid(self):
        self.timeChart.axes.grid(color="black", linestyle="-", linewidth=0.3)
        self.dopplerTimeChart.axes.grid(color="black", linestyle="-", linewidth=0.3)
        self.spectrumChart.axes.grid(color="black", linestyle="-", linewidth=0.3)
        self.dopplerSpectrumChart.axes.grid(color="black", linestyle="-", linewidth=0.3)

    def setDefaults(self, params):
        self.f0_input.setText(f"{params['F0']}")
        self.fmax_input.setText(f"{params['FMAX']}")
        self.sampling_rate_input.setText(f"{params['SAMPLING_RATE']}")
        self.signal_duration_input.setText(f"{params['SIGNAL_DURATION']}")
        self.number_of_components_input.setText(f"{params['NUMBER_OF_COMPONENTS']}")
        self.slider.setValue(params["OBSERVER_VELOCITY"])
        if self.params["OBSERVER_DIRECTION"] == c.OBSERVER_COMMING_CLOSER:
            self.observer_direction_combobox.setCurrentText("Observer comming closer")
        elif self.params["OBSERVER_DIRECTION"] == c.OBSERVER_COMMING_FURTHER:
            self.observer_direction_combobox.setCurrentText("Observer comming further")
        self.signal_source_combobox.setCurrentText(f"{params['SIGNAL_SOURCE']}")
        self.centerFrequencyInput.setText(f"{params['CENTER_FREQUENCY']}")
        self.domain_combobox.setCurrentText(f"{params['DOMAIN']}")

    def setAxesXlim(self, fmax):
        # self.spectrumChart.axes.set_xlim(xmin=0, xmax=fmax * 1.5)
        # self.dopplerSpectrumChart.axes.set_xlim(xmin=0, xmax=fmax * 1.5)
        pass
