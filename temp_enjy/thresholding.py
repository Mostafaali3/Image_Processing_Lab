import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog, QSlider
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class Image_processing_lab(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thresholding_ui()

    def thresholding_ui(self):
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.img_upload_button = QPushButton('Upload Image',self)
        self.img_upload_button.clicked.connect(self.upload_image)
        layout.addWidget(self.img_upload_button)

        self.global_threshold_button = QPushButton('global thresholding', self)
        self.global_threshold_button.clicked.connect(self.apply_global_thresholding)
        layout.addWidget(self.global_threshold_button)

        self.global_threshold_slider = QSlider(Qt.Horizontal, self)
        self.global_threshold_slider.setRange(-1,255)
        self.global_threshold_slider.setValue(127)
        self.global_threshold_slider.valueChanged.connect(self.apply_global_thresholding)
        layout.addWidget(self.global_threshold_slider)



        self.local_threshold_button = QPushButton('local Thresholding',self)
        self.local_threshold_button.clicked.connect(self.apply_local_thresholding)


        layout.addWidget(self.local_threshold_button)

        self.image_label = QLabel(self)
        # self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        central_widget.setLayout(layout)


        self.image = None
        self.global_threshold_val = 127

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Images (*.png *.jpg *.bmp *.jpeg);;All Files (*)", options=options)

        if file_name:
            self.image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
            self.display_image(self.image)

    def apply_global_thresholding(self):
        if self.image is not None:
            # if it was gradiant --> any pixel below 127 is black and above 127 is white

            # ret returns true of false (whether we can apply thresholding aslan or not) --> not significant
            # thresh_val = 0
            self.global_threshold_val = self.global_threshold_slider.value()
            ret, global_thresholded_img = cv2.threshold(self.image, self.global_threshold_val, 255,cv2.THRESH_BINARY)
            self.display_image(global_thresholded_img)

    def apply_local_thresholding(self):
        if self.image is not None:
            local_thresholded_img = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                      cv2.THRESH_BINARY, 11, 2)
            # sum of el mean of each block (11 blocks) - C
            # block size should be odd --> the greater the size, less noise
            self.display_image(local_thresholded_img)

    def display_image(self, image):
        # el conversion to QImage
        height, width = image.shape
        bytes_per_line = width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        # pixmap for displaying
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(),Qt.KeepAspectRatio))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Image_processing_lab()
    window.show()
    sys.exit(app.exec_())