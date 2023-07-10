from PySide2 import QtWidgets
from qrange_slider import QRangeSlider


class RangeSliderDialog(QtWidgets.QDialog):
    def __init__(self, num_sliders, truncation_range: list, parent=None):
        super().__init__(parent)

        self.min_threshold = truncation_range[0]
        self.max_threshold = truncation_range[1]
        self.range_threshold = truncation_range[1] - truncation_range[0]
        self.setWindowTitle("Range Slider Dialog")
        self.resize(400, 200)
        self.sliders = []

        # Create the range sliders
        for i in range(num_sliders):
            slider = QRangeSlider(self)
            slider.setRange(0, 100)
            self.sliders.append(slider)

        # Create layout
        layout = QtWidgets.QVBoxLayout(self)

        # Add sliders to layout
        for i, slider in enumerate(self.sliders):
            #slider_label = QtWidgets.QLabel(f"Slider {i + 1}:")
            sli=''
            if i == 0:
                sli='TLS markers'
            elif i == 1:
                sli='Chemokine'
            elif i == 2:
                sli='Hotspot'
            slider_label = QtWidgets.QLabel(f"{sli}:") 
            layout.addWidget(slider_label)
            layout.addWidget(slider)

        # Connect signals
        for slider in self.sliders:
            slider.startValueChanged.connect(self.handleStartValueChanged)
            slider.endValueChanged.connect(self.handleEndValueChanged)

    def handleStartValueChanged(self):
        sender = self.sender()
        index = self.sliders.index(sender)
        self.updateSliderValue(index)

    def handleEndValueChanged(self):
        sender = self.sender()
        index = self.sliders.index(sender)
        self.updateSliderValue(index)

    def updateSliderValue(self, index):
        slider = self.sliders[index]
        slider_label = self.layout().itemAt(2 * index).widget()
        sli=''
        if index == 0:
            sli='TLS markers'
        elif index == 1:
            sli='Chemokine'
        elif index == 2:
            sli='Hotspot'
        #slider_label.setText(f"Slider {index + 1}: [{slider._start * self.range_threshold / self.max_threshold + self.min_threshold:.2f}, {slider._end * self.range_threshold / self.max_threshold + self.min_threshold:.2f}]")
        slider_label.setText(f"{sli}: [{slider._start * self.range_threshold / self.max_threshold + self.min_threshold:.2f}, {slider._end * self.range_threshold / self.max_threshold + self.min_threshold:.2f}]")

