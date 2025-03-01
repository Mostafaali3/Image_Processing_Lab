import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QVBoxLayout, QSlider, QComboBox, QPushButton, \
    QStackedWidget, QWidget, QFileDialog, QRadioButton, QDialog, QLineEdit, QHBoxLayout
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
from enums.type import Type
from classes.filter import Filters
from classes.noiser import Noiser
from classes.edgeDetector import Edge_detector
from enums.graphType import GraphType
from enums.colors import Color
from enums.mode import Mode
import cv2


# compile_qrc()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.r_histogram_viewer = Viewer(Color.R, GraphType.HISTO)
        self.g_histogram_viewer = Viewer(Color.G, GraphType.HISTO)
        self.b_histogram_viewer = Viewer(Color.B, GraphType.HISTO)
        self.gray_histogram_viewer = Viewer(Color.GRAY, GraphType.HISTO)
        self.r_cdf_viewer = Viewer(Color.R, GraphType.CDF)
        self.g_cdf_viewer = Viewer(Color.G, GraphType.CDF)
        self.b_cdf_viewer = Viewer(Color.B, GraphType.CDF)
        self.gray_cdf_viewer = Viewer(Color.GRAY, GraphType.CDF)
        
        self.gray_histogram_widget = self.findChild(QWidget, "widget_17")
        self.gray_histogram_layout = self.gray_histogram_widget.layout()
        self.gray_histogram_layout.addWidget(self.gray_histogram_viewer)
        
        self.gray_cdf_widget = self.findChild(QWidget, "widget_18")
        self.gray_cdf_layout = self.gray_cdf_widget.layout()
        self.gray_cdf_layout.addWidget(self.gray_cdf_viewer)
        
        self.gray_cdf_layout = self.findChild(QVBoxLayout, "gray_cdf")
        self.gray_cdf_layout.addWidget(self.gray_cdf_viewer)
        
        self.gray_histogram_layout = self.findChild(QVBoxLayout, "gray_histogram")
        self.gray_histogram_layout.addWidget(self.gray_histogram_viewer)
        
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
        self.main_page_browse_button.clicked.connect(lambda : self.browse_image(Mode.REGULAR))
        
        self.input_image_viewer_layout = self.findChild(QVBoxLayout, "input")
        self.input_image_viewer = ImageViewer()
        self.input_image_viewer_layout.addWidget(self.input_image_viewer)
        self.input_image_viewer.viewer_type = ViewerType.INPUT
        
        self.output_image_viewer_layout = self.findChild(QVBoxLayout, "output")
        self.output_image_viewer = ImageViewer()
        self.output_image_viewer_layout.addWidget(self.output_image_viewer)
        self.output_image_viewer.viewer_type = ViewerType.OUTPUT
        
        self.input_hybrid_image_viewer_1_layout = self.findChild(QVBoxLayout, "input_1")
        self.input_hybrid_image_viewer_1 = ImageViewer()
        self.input_hybrid_image_viewer_1_layout.addWidget(self.input_hybrid_image_viewer_1)
        
        self.filtered_hybrid_image_viewer_1_layout = self.findChild(QVBoxLayout, "output_1")
        self.filtered_hybrid_image_viewer_1 = ImageViewer()
        self.filtered_hybrid_image_viewer_1.viewer_type = ViewerType.OUTPUT
        self.filtered_hybrid_image_viewer_1_layout.addWidget(self.filtered_hybrid_image_viewer_1)
        
        self.input_hybrid_image_viewer_2_layout = self.findChild(QVBoxLayout, "input_2")
        self.input_hybrid_image_viewer_2 = ImageViewer()
        self.input_hybrid_image_viewer_2_layout.addWidget(self.input_hybrid_image_viewer_2)
        
        self.filtered_hybrid_image_viewer_2_layout = self.findChild(QVBoxLayout, "output_2")
        self.filtered_hybrid_image_viewer_2 = ImageViewer()
        self.filtered_hybrid_image_viewer_2.viewer_type = ViewerType.OUTPUT
        self.filtered_hybrid_image_viewer_2_layout.addWidget(self.filtered_hybrid_image_viewer_2)
        
        self.final_hybrid_image_viewer_layout = self.findChild(QVBoxLayout, "final_output")
        self.final_hybrid_image_viewer = ImageViewer()
        self.final_hybrid_image_viewer.viewer_type = ViewerType.HYBRID
        self.final_hybrid_image_viewer_layout.addWidget(self.final_hybrid_image_viewer)
        
        self.gray_scale_output_button = self.findChild(QPushButton, "grayscale_button")
        self.gray_scale_output_button.clicked.connect(self.on_gray_scale_button_clicked)

        self.local_threshold = self.findChild(QRadioButton, "local_threshold")
        self.global_threshold = self.findChild(QRadioButton, "global_threshold")

        self.local_threshold.toggled.connect(self.on_threshold_selected)
        self.global_threshold.toggled.connect(self.on_threshold_selected)
        self.thresholder = Thresholder(self.output_image_viewer)

        self.global_threshold_slider = self.findChild(QSlider, "threshold_slider")
        self.global_threshold_slider.setRange(1, 256)
        self.global_threshold_slider.setValue(127)
        # self.global_threshold_slider.valueChanged.connect(self.thresholder.update_global_threshold_val)
        self.global_threshold_slider.valueChanged.connect(self.update_global_threshold_val)

        self.filters_comboBox = self.findChild(QComboBox, "filter_combobox")
        self.filters_comboBox.addItem("Select a filter")
        self.filters_comboBox.addItem("Average Filter")
        self.filters_comboBox.addItem("Median Filter")
        self.filters_comboBox.addItem("Gaussiann Filter")
        self.filter = Filters(self.output_image_viewer, self.filtered_hybrid_image_viewer_1, self.filtered_hybrid_image_viewer_2)
        self.filters_comboBox.model().item(0).setFlags(Qt.NoItemFlags)
        self.filters_comboBox.currentIndexChanged.connect(self.on_filter_type_change)

        self.noise_combobox = self.findChild(QComboBox, "noise_combobox")
        self.noise_combobox.addItem("Select noise type")
        self.noise_combobox.addItem("Salt & Pepper noise")
        self.noise_combobox.addItem("Uniform noise")
        self.noise_combobox.addItem("Gaussian noise")
        self.noise = Noiser(self.output_image_viewer)
        self.noise_combobox.currentIndexChanged.connect(self.on_noise_type_change)

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
                                     self.gray_cdf_viewer, self.input_image_viewer, self.output_image_viewer, self.input_hybrid_image_viewer_1, self.input_hybrid_image_viewer_2
                                     ,self.filtered_hybrid_image_viewer_1, self.filtered_hybrid_image_viewer_2, self.final_hybrid_image_viewer)
        
        self.main_stacked_widget = self.findChild(QStackedWidget, "stackedWidget")
        self.histogram_stacked_widget = self.findChild(QStackedWidget, "stackedWidget_2")
        
        self.hybrid_mode_button = self.findChild(QPushButton, "hybrid_button")
        self.hybrid_mode_button.clicked.connect(self.on_hybrid_mode_button_clicked)

        self.show_histogram_button = self.findChild(QPushButton, "histograms_button")
        self.show_histogram_button.clicked.connect(self.on_show_histogram_button_clicked)

        self.back_from_histogram_button = self.findChild(QPushButton, "back_histo_button")
        self.back_from_histogram_button.clicked.connect(self.on_back_to_main_button_clicked)
        
        self.back_from_hybrid_mode_button = self.findChild(QPushButton, "pushButton_5")
        self.back_from_hybrid_mode_button.clicked.connect(self.on_back_to_main_button_clicked)

        self.equalize_image_button = self.findChild(QPushButton, "equalizer_button")
        self.equalize_image_button.clicked.connect(self.on_equalized_button_cliked)

        self.normalize_image_button = self.findChild(QPushButton, "normalizer_button")
        self.normalize_image_button.clicked.connect(self.on_normalize_button_clicked)
        
        self.reset_button = self.findChild(QPushButton, "reset_button")
        self.reset_button.clicked.connect(self.on_reset_button_clicked)
        
        self.browse_hybrid_image_1_button = self.findChild(QPushButton, "browse_1")
        self.browse_hybrid_image_1_button.clicked.connect(lambda : self.browse_image(Mode.HYBRID, 1))
        
        self.browse_hybrid_image_2_button = self.findChild(QPushButton, "browse_2")
        self.browse_hybrid_image_2_button.clicked.connect(lambda : self.browse_image(Mode.HYBRID, 2))
        
        self.low_high_filters_slider_1 = self.findChild(QSlider, "pass_filter_1")
        self.low_high_filters_slider_1.setRange(0,1)
        
        self.filtering_slider_1 = self.findChild(QSlider, "verticalSlider_3")
        self.filtering_slider_1.setRange(0,10)
        self.filtering_slider_1.valueChanged.connect(lambda x : self.on_filter_slider_value_changed(x,1))
        
        self.filtering_slider_2 = self.findChild(QSlider, "value_slider_2")
        self.filtering_slider_2.setRange(0,10)
        self.filtering_slider_2.valueChanged.connect(lambda x : self.on_filter_slider_value_changed(x,2))
        
        self.low_high_filters_slider_2 = self.findChild(QSlider, "pass_filter_2")
        self.low_high_filters_slider_2.setRange(0,1)


        # fix
        
    def browse_image(self, mode = Mode.REGULAR, viewer_index = 1):
        print("pushed")
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Image Files (*.jpeg *.jpg *.png *.bmp *.gif);;All Files (*)')
        
        if file_path:
            if file_path.endswith('.jpeg') or file_path.endswith('.jpg'):
                temp_image = cv2.imread(file_path)
                image = Image(temp_image)
                
                if mode == Mode.REGULAR:
                    self.input_image_viewer.current_image = image 
                    self.output_image_viewer.current_image = image
                    # make the viewer track the output image
                    self.r_histogram_viewer.output_image = image
                    self.r_cdf_viewer.output_image = image
                    self.g_histogram_viewer.output_image = image
                    self.g_cdf_viewer.output_image = image
                    self.b_histogram_viewer.output_image = image
                    self.b_cdf_viewer.output_image = image
                    self.gray_histogram_viewer.output_image = image
                    self.gray_cdf_viewer.output_image = image
                    # update
                    self.controller.update()
                else:
                    image.transfer_to_gray_scale()
                    if viewer_index == 1:
                        self.input_hybrid_image_viewer_1.current_image = image
                        self.filtered_hybrid_image_viewer_1.current_image = image
                        self.final_hybrid_image_viewer.current_image = image
                    else: 
                        self.input_hybrid_image_viewer_2.current_image = image
                        self.filtered_hybrid_image_viewer_2.current_image = image
                        self.final_hybrid_image_viewer.other_image = image
                    self.controller.update_hybrid()
                        

    def on_gray_scale_button_clicked(self):
        self.output_image_viewer.current_image.transfer_to_gray_scale()
        self.controller.update()
        
    def on_hybrid_mode_button_clicked(self):
        page_index = self.main_stacked_widget.indexOf(self.findChild(QWidget, "page_2"))
        if page_index != -1:
            self.main_stacked_widget.setCurrentIndex(page_index)
            
    def on_show_histogram_button_clicked(self):
        page_index = self.main_stacked_widget.indexOf(self.findChild(QWidget, "page_3"))
        if page_index != -1:
            self.main_stacked_widget.setCurrentIndex(page_index)
            # conditions for gray scale or rgb

            if len(self.output_image_viewer.current_image.modified_image.shape )==2:
                histogram_index = self.histogram_stacked_widget.indexOf(self.findChild(QWidget, "page_5"))
            else:
                histogram_index = self.histogram_stacked_widget.indexOf(self.findChild(QWidget, "page_4"))

            if histogram_index != -1:
                self.histogram_stacked_widget.setCurrentIndex(histogram_index)

    
    def on_back_to_main_button_clicked(self):
        page_index = self.main_stacked_widget.indexOf(self.findChild(QWidget, "page"))
        if page_index != -1:
            self.main_stacked_widget.setCurrentIndex(page_index)
        
    def on_equalized_button_cliked(self):
        self.output_image_viewer.current_image.equalize_image()
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

    def on_normalize_button_clicked(self):
        self.output_image_viewer.current_image.normalize_image()
        self.controller.update()

    def on_threshold_selected(self):
        # never calling it twice
        if self.sender().isChecked():
            last_img_copy = self.input_image_viewer.current_image.modified_image
            if self.sender() == self.local_threshold:
                self.thresholder.threshold_type = "LOCAL"
                self.thresholder.check_global_selection = False
            elif self.sender() == self.global_threshold:
                print("global")
                self.thresholder.threshold_type = "GLOBAL"
                self.thresholder.check_global_selection = True
            img = self.output_image_viewer.current_image.modified_image
            self.thresholder.apply_thresholding(self.thresholder.threshold_type)
            self.controller.update()
            self.input_image_viewer.current_image.modified_image = last_img_copy



    def update_global_threshold_val(self, value):
        last_img_copy = self.input_image_viewer.current_image.modified_image
        self.thresholder.global_threshold_val = value
        # self.thresholder.apply_global_thresholding()
        self.thresholder.apply_thresholding("GLOBAL")
        self.controller.update()
        self.input_image_viewer.current_image.modified_image = last_img_copy

    def on_noise_type_change(self):
        noise_type = self.noise_combobox.currentText()
        if noise_type == "Salt & Pepper noise":
            self.open_salt_and_pepper_pop_up_window()
        elif noise_type == "Uniform noise":
            self.open_uniform_pop_up_window()
        elif noise_type == "Gaussian noise":
            self.open_gaussian_pop_up_window()
        self.controller.update()

    def open_salt_and_pepper_pop_up_window(self):
        popup = QDialog()
        popup.setWindowTitle("Salt & Pepper Noise Parameters")
        popup.setGeometry(700, 400, 300, 150)

        layout = QVBoxLayout()

        # Title Label
        label = QLabel("Enter Salt & Pepper Noise Ratios")
        label.setStyleSheet("font-weight:500")
        layout.addWidget(label)

        # Salt to pepper Ratio Input
        salt_layout = QHBoxLayout()
        salt_label = QLabel("Salt Ratio (0-1):")
        self.salt_edit = QLineEdit()
        self.salt_edit.setPlaceholderText("e.g. 0.1")
        salt_layout.addWidget(salt_label)
        salt_layout.addWidget(self.salt_edit)
        layout.addLayout(salt_layout)

        pepper_layout = QHBoxLayout()
        pepper_label = QLabel("Pepper Ratio (0-1):")
        self.pepper_edit = QLineEdit()
        self.pepper_edit.setPlaceholderText("e.g. 0.1")
        pepper_layout.addWidget(pepper_label)
        pepper_layout.addWidget(self.pepper_edit)
        layout.addLayout(pepper_layout)

        # Apply Button
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(lambda: self.apply_salt_and_pepper_noise(popup))
        layout.addWidget(apply_button)

        popup.setLayout(layout)
        popup.exec_()

    def apply_salt_and_pepper_noise(self, popup):
        self.salt_input = float(self.salt_edit.text())
        self.pepper_input = float(self.pepper_edit.text())
        popup.close()
        self.noise.apply_salt_and_pepper_noise(self.salt_input, self.pepper_input)


    def open_uniform_pop_up_window(self):
        popup = QDialog()
        popup.setWindowTitle("Uniform Noise Parameters")
        popup.setGeometry(700, 400, 300, 150)

        layout = QVBoxLayout()

        # Title Label
        label = QLabel("Choose noise Intensity")
        label.setStyleSheet("font-weight:500")
        layout.addWidget(label)

        # Uniform Intensity Ratio
        uniform_layout = QHBoxLayout()
        uniform_noise_label = QLabel("Noise Intensity")
        self.uniform_noise_intensity_edit = QLineEdit()
        self.uniform_noise_intensity_edit.setPlaceholderText("e.g. 10")
        uniform_layout.addWidget(uniform_noise_label)
        uniform_layout.addWidget(self.uniform_noise_intensity_edit)
        layout.addLayout(uniform_layout)

        # Apply Button
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(lambda: self.apply_uniform_noise(popup))
        layout.addWidget(apply_button)

        popup.setLayout(layout)
        popup.exec_()

    def apply_uniform_noise(self,popup):
        self.uniform_noise_intensity = int(self.uniform_noise_intensity_edit.text())
        popup.close()
        self.noise.apply_uniform_noise(self.uniform_noise_intensity)

    def open_gaussian_pop_up_window(self):
        popup = QDialog()
        popup.setWindowTitle("Gaussian Noise Parameters")
        popup.setGeometry(700, 400, 300, 200)

        layout = QVBoxLayout()

        # Title Label
        label = QLabel("Choose gaussian parameters")
        label.setStyleSheet("font-weight:500")
        layout.addWidget(label)

        # Gaussian Mean
        gaussian_mean_layout = QHBoxLayout()
        gaussian_mean_label = QLabel("Gaussian Mean:")
        self.gaussian_mean_edit = QLineEdit()
        self.gaussian_mean_edit.setPlaceholderText("e.g. 10")
        gaussian_mean_layout.addWidget(gaussian_mean_label)
        gaussian_mean_layout.addWidget(self.gaussian_mean_edit)
        layout.addLayout(gaussian_mean_layout)

        # Gaussian ST
        gaussian_st_layout = QHBoxLayout()
        gaussian_st_label = QLabel("Gaussian st:")
        self.gaussian_st_edit = QLineEdit()
        self.gaussian_st_edit.setPlaceholderText("e.g. 10")
        gaussian_st_layout.addWidget(gaussian_st_label)
        gaussian_st_layout.addWidget(self.gaussian_st_edit)
        layout.addLayout(gaussian_st_layout)


        # Apply Button
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(lambda: self.apply_gaussian_noise(popup))
        layout.addWidget(apply_button)

        popup.setLayout(layout)
        popup.exec_()

    def apply_gaussian_noise(self,popup):
        self.gaussian_mean = int(self.gaussian_mean_edit.text())
        self.gaussian_st = int(self.gaussian_st_edit.text())
        popup.close()
        self.noise.apply_gaussian_noise(self.gaussian_mean, self.gaussian_st)



    def on_filter_type_change(self):
        filter_type = self.filters_comboBox.currentText()
        self.filter.apply_filters(filter_type)
        self.controller.update()

    def on_detector_type_change(self):
        detector_type = self.edge_detectors_comboBox.currentText()
        self.edge_detector.apply_edge_detectors(detector_type)
        self.controller.update()
        
    def on_reset_button_clicked(self):
        self.output_image_viewer.current_image.reset()
        self.controller.update()
        
    def get_filter_slider_value(self, index):
        values = [x/10 for x in range(11)]
        return values[index]
    
    def on_filter_slider_value_changed(self, index, slider_number):
        current_filtering_ratio = self.get_filter_slider_value(index)
        # print(slider_number)
        if slider_number == 1:
            if self.low_high_filters_slider_1.value() == 0: #low
                self.filter.apply_low_pass_filter(current_filtering_ratio,1)
            else:
                self.filter.apply_high_pass_filter(current_filtering_ratio,1)
        else:
            if self.low_high_filters_slider_2.value() == 0: #low
                self.filter.apply_low_pass_filter(current_filtering_ratio,2)
            else:
                self.filter.apply_high_pass_filter(current_filtering_ratio,2)
        self.controller.update_hybrid()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())