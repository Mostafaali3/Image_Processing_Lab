import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QVBoxLayout, QSlider, QComboBox, QPushButton, \
    QStackedWidget, QWidget, QFileDialog, QRadioButton
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from helper_function.compile_qrc import compile_qrc
from icons_setup.compiledIcons import *
from classes.viewer import Viewer
from classes.image import Image
from classes.imageViewer import ImageViewer
from enums.viewerType import ViewerType
from classes.controller import Controller
from classes.thresholder import Thresholder
from classes.noiser import Noiser
from enums.thresholdType import Threshold_type
from classes.filter import Filters
from classes.edgeDetector import Edge_detector

import cv2


compile_qrc()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.r_histogram_viewer = Viewer()
        self.g_histogram_viewer = Viewer()
        self.b_histogram_viewer = Viewer()
        self.gray_histogram_viewer = Viewer()
        self.r_cdf_viewer = Viewer()
        self.g_cdf_viewer = Viewer()
        self.b_cdf_viewer = Viewer()
        self.gray_cdf_viewer = Viewer()
        
        self.gray_histogram_widget = self.findChild(QWidget, "widget_17")
        self.gray_histogram_layout = self.gray_histogram_widget.layout()
        self.gray_histogram_layout.addWidget(self.gray_histogram_viewer)
        
        self.gray_cdf_widget = self.findChild(QWidget, "widget_18")
        self.gray_cdf_layout = self.gray_cdf_widget.layout()
        self.gray_cdf_layout.addWidget(self.gray_cdf_viewer)
        
        self.r_histogram_layout = self.findChild(QVBoxLayout, "red_histogram")
        self.r_histogram_layout.addWidget(self.r_histogram_viewer)

        self.r_cdf_layout = self.findChild(QVBoxLayout, "red_cdf")
        self.r_cdf_layout.addWidget(self.r_cdf_viewer)
        
        self.g_histogram_layout = self.findChild(QVBoxLayout, "green_histogram")
        self.g_histogram_layout.addWidget(self.g_histogram_viewer)

        self.g_cdf_layout = self.findChild(QVBoxLayout, "green_cdf")
        self.g_cdf_layout.addWidget(self.g_cdf_viewer)
        
        self.b_histogram_layout = self.findChild(QVBoxLayout, "blue_histogram")
        self.b_histogram_layout.addWidget(self.b_histogram_viewer)

        self.b_cdf_layout = self.findChild(QVBoxLayout, "blue_cdf")
        self.b_cdf_layout.addWidget(self.b_cdf_viewer)
        
        self.main_page_browse_button = self.findChild(QPushButton, "browse")
        self.main_page_browse_button.clicked.connect(self.browse_image)
        
        self.input_image_viewer_layout = self.findChild(QVBoxLayout, "input")
        self.input_image_viewer = ImageViewer()
        self.input_image_viewer_layout.addWidget(self.input_image_viewer)
        self.input_image_viewer.viewer_type = ViewerType.INPUT
        
        self.output_image_viewer_layout = self.findChild(QVBoxLayout, "output")
        self.output_image_viewer = ImageViewer()
        self.output_image_viewer_layout.addWidget(self.output_image_viewer)
        self.output_image_viewer.viewer_type = ViewerType.OUTPUT
        
        self.gray_scale_output_button = self.findChild(QPushButton, "grayscale_button")
        self.gray_scale_output_button.clicked.connect(self.on_gray_scale_button_clicked)

        self.local_threshold = self.findChild(QRadioButton, "local_threshold")
        self.global_threshold = self.findChild(QRadioButton, "global_threshold")

        self.local_threshold.toggled.connect(self.on_threshold_selected)
        self.global_threshold.toggled.connect(self.on_threshold_selected)
        self.thresholder = Thresholder(self.output_image_viewer)

        self.global_threshold_slider = self.findChild(QSlider, "threshold_slider")
        self.global_threshold_slider.setRange(0, 255)
        self.global_threshold_slider.setValue(127)
        # self.global_threshold_slider.valueChanged.connect(self.thresholder.update_global_threshold_val)
        self.global_threshold_slider.valueChanged.connect(self.update_global_threshold_val)

        self.filters_comboBox = self.findChild(QComboBox, "filter_combobox")
        self.filters_comboBox.addItem("Select a filter")
        self.filters_comboBox.addItem("Average Filter")
        self.filters_comboBox.addItem("Median Filter")
        self.filters_comboBox.addItem("Gaussiann Filter")
        self.filter = Filters(self.output_image_viewer)
        self.filters_comboBox.model().item(0).setFlags(Qt.NoItemFlags)
        self.filters_comboBox.currentIndexChanged.connect(self.on_filter_type_change)

        self.noise_combobox = self.findChild(QComboBox, "noise_combobox")
        self.noise_combobox.addItem("Select noise type")
        self.noise_combobox.addItem("Salt & Pepper noise")
        self.noise_combobox.addItem("Uniform noise")
        self.noise_combobox.addItem("Gaussian noise")
        self.noise_combobox.model().item(0).setFlags(Qt.NoItemFlags)
        self.noise = Noiser(self.output_image_viewer)
        self.noise_combobox.currentIndexChanged.connect(self.on_filter_type_change)

        self.edge_detectors_comboBox = self.findChild(QComboBox, "mask_combobox")
        self.edge_detectors_comboBox.addItem("Select edge detector type")
        self.edge_detectors_comboBox.addItem("Sobel detector")
        self.edge_detectors_comboBox.addItem("Roberts detector")
        self.edge_detectors_comboBox.addItem("Prewitt detector")
        self.edge_detectors_comboBox.addItem("Canny detector")
        self.edge_detector = Edge_detector(self.output_image_viewer)
        self.edge_detectors_comboBox.currentIndexChanged.connect(self.on_detector_type_change)


        self.controller = Controller(self.r_histogram_viewer,self.g_histogram_viewer,self.b_histogram_viewer,
                                     self.gray_histogram_viewer, self.r_cdf_viewer, self.g_cdf_viewer, self.b_cdf_viewer,
                                     self.gray_cdf_viewer, self.input_image_viewer, self.output_image_viewer )
        
    
        
    def browse_image(self):
        print("pushed")
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Image Files (*.jpeg *.jpg *.png *.bmp *.gif);;All Files (*)')
        
        if file_path:
            if file_path.endswith('.jpeg') or file_path.endswith('.jpg'):
                temp_image = cv2.imread(file_path)
                print(temp_image.shape[0],temp_image.shape[1],temp_image.shape[2])
                image = Image(temp_image)
                self.input_image_viewer.current_image = image 
                self.output_image_viewer.current_image = image
                self.controller.update()

    def on_gray_scale_button_clicked(self):
        self.output_image_viewer.current_image.transfer_to_gray_scale()
        self.controller.update()

    # def on_threshold_selected(self):
    #     # never calling it twice
    #     if self.sender().isChecked():
    #         if self.sender() == self.local_threshold:
    #             print("local")
    #             self.thresholder.apply_local_thresholding()
    #         elif self.sender() == self.global_threshold:
    #             print("global")
    #             self.thresholder.apply_global_thresholding()
    #     self.controller.update()

    def on_threshold_selected(self):
        # never calling it twice
        if self.sender().isChecked():
            if self.sender() == self.local_threshold:
                self.thresholder.threshold_type = "LOCAL"
                self.thresholder.check_global_selection = False
            elif self.sender() == self.global_threshold:
                print("global")
                self.thresholder.threshold_type = "GLOBAL"
                self.thresholder.check_global_selection = True
        self.thresholder.apply_thresholding(self.thresholder.threshold_type)
        self.controller.update()

    def update_global_threshold_val(self, value):
        self.thresholder.global_threshold_val = value
        # self.thresholder.apply_global_thresholding()
        self.thresholder.apply_thresholding("GLOBAL")
        self.controller.update()

    def on_noise_type_change(self):
        noise_type = self.noise_combobox.currentText()
        if noise_type == "Salt & Pepper noise":
            pass
    def on_filter_type_change(self):
        filter_type = self.filters_comboBox.currentText()
        self.filter.apply_filters(filter_type)
        self.controller.update()

    def on_detector_type_change(self):
        detector_type = self.edge_detectors_comboBox.currentText()
        self.edge_detector.apply_edge_detectors(detector_type)
        self.controller.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())