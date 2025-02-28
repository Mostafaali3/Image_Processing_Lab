import math
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog, QSlider
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class Image_processing_lab(QMainWindow):
    def __init__(self):
        super().__init__()
        self.filters_ui()

    def filters_ui(self):
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.img_upload_button = QPushButton('Upload Image',self)
        self.img_upload_button.clicked.connect(self.upload_image)
        layout.addWidget(self.img_upload_button)

        self.avg_filter_button = QPushButton('avg filter', self)
        self.avg_filter_button.clicked.connect(self.apply_average_filter)
        layout.addWidget(self.avg_filter_button)

        self.median_filter_button = QPushButton('median filter', self)
        self.median_filter_button.clicked.connect(self.apply_median_filter)
        layout.addWidget(self.median_filter_button)

        self.guassian_filter_button = QPushButton('gaussian', self)
        self.guassian_filter_button.clicked.connect(self.apply_gaussian_filter)
        layout.addWidget(self.guassian_filter_button)

        self.low_pass_filter_button = QPushButton('low pass', self)
        self.low_pass_filter_button.clicked.connect(self.apply_low_pass_filter)
        layout.addWidget(self.low_pass_filter_button)

        self.high_pass_filter_button = QPushButton('high pass', self)
        self.high_pass_filter_button.clicked.connect(self.apply_high_pass_filter)
        layout.addWidget(self.high_pass_filter_button)

        self.image_label = QLabel(self)
        # self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        central_widget.setLayout(layout)
        self.image = None

    def apply_average_filter(self):
        if self.image is None:
            return
        image_height, image_width = self.image.shape
        kernel_size = 5  # odd num input passed mn el func
        filtered_img = np.zeros_like(self.image, dtype=np.float32)

        # creating the kernel
        kernel = np.ones((kernel_size, kernel_size), dtype=np.float32)
        norm_factor = kernel_size * kernel_size
        kernel /= norm_factor

        # creating padding (fake pixels to handle edges)
        pad_size = kernel_size // 2
        padded_image = cv2.copyMakeBorder(self.image, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT)
        # print(f"hena padded_img {padded_image}")

        for i in range(pad_size, image_height + pad_size):
            for j in range(pad_size, image_width + pad_size):
                # instead of looping 3la kol pixel (gonna take forever) we apply the process mat by mat
                region = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1]
                filtered_img[i - pad_size, j - pad_size] = np.sum(region * kernel)

        filtered_img = filtered_img.astype(np.uint8)
        print(f"hena filtered_img using avg {filtered_img}")
        self.display_image(filtered_img)

    def apply_median_filter(self):
        if self.image is None:
            return
        image_height, image_width = self.image.shape
        kernel_size = 5  # odd num input passed mn el func
        filtered_img = np.zeros_like(self.image, dtype=np.uint8)

        # creating padding (fake pixels to handle edges)
        pad_size = kernel_size // 2
        padded_image = cv2.copyMakeBorder(self.image, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT)
        # print(f"hena padded_img {padded_image}")

        for i in range(pad_size, image_height + pad_size):
            for j in range(pad_size, image_width + pad_size):
                # instead of looping 3la kol pixel (gonna take forever) we apply the process mat by mat
                region = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1]
                filtered_img[i - pad_size, j - pad_size] = np.median(region)  # obtaining median of the selected region

        print(f"hena filtered_img using median{filtered_img}")
        self.display_image(filtered_img)

    def create_gaussian_kernel(self, kernel_size):
        sigma = 0.3 * ((kernel_size - 1) * 0.5 - 1) + 0.8
        gaussian_kernel = []
        total_sum = 0
        for i in range(int(-(kernel_size - 1) / 2), int((kernel_size - 1) / 2 + 1)):
            filter_row = []
            for j in range(int(-(kernel_size - 1) / 2), int((kernel_size - 1) / 2 + 1)):
                G = math.exp(-(i ** 2 + j ** 2) / (2 * sigma ** 2))
                filter_row.append(G)
                total_sum += G
            gaussian_kernel.append(filter_row)

        gaussian_kernel = np.array(gaussian_kernel) / total_sum
        return gaussian_kernel

    def apply_gaussian_filter(self):
        if self.image is None:
            return

        image_height, image_width = self.image.shape
        kernel_size = 13  # odd num input passed mn el func
        filtered_img = np.zeros_like(self.image, dtype=np.float32)

        # creating the Gaussian kernel
        kernel = self.create_gaussian_kernel(kernel_size)
        # creating padding (fake pixels to handle edges)
        pad_size = kernel_size // 2
        padded_image = cv2.copyMakeBorder(self.image, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT)
        # print(f"hena padded_img {padded_image}")

        for i in range(pad_size, image_height + pad_size):
            for j in range(pad_size, image_width + pad_size):
                # instead of looping 3la kol pixel (gonna take forever) we apply the process mat by mat
                region = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1]
                # apply the Gaussian kernel
                filtered_img[i - pad_size, j - pad_size] = np.sum(region * kernel)

        filtered_img = filtered_img.astype(np.uint8)
        print(f"hena filtered_img {filtered_img}")
        self.display_image(filtered_img)

    def apply_low_pass_filter(self):
        if self.image is None:
            return
        region_factor = 0.5
        low_pass_mat = self.create_fourier_filter_mask(region_factor)
        img_fourier = np.fft.fft2(self.image)
        image_fourier_shifted = np.fft.fftshift(img_fourier)
        filtered_fourier = image_fourier_shifted *low_pass_mat
        filtered_img = np.fft.ifftshift(filtered_fourier)
        filtered_img = np.fft.ifft2(filtered_img)
        filtered_img = np.abs(filtered_img).astype(np.uint8)
        self.display_image(filtered_img)

    def apply_high_pass_filter(self):
        if self.image is None:
            return
        region_factor = 0
        high_pass_mat = 1 - self.create_fourier_filter_mask(region_factor)
        img_fourier = np.fft.fft2(self.image)
        image_fourier_shifted = np.fft.fftshift(img_fourier)
        filtered_fourier = image_fourier_shifted *high_pass_mat
        filtered_img = np.fft.ifftshift(filtered_fourier)
        filtered_img = np.fft.ifft2(filtered_img)
        filtered_img = np.abs(filtered_img).astype(np.uint8)
        self.display_image(filtered_img)

    def create_fourier_filter_mask(self, region_factor):
        rows, cols = self.image.shape
        center_row, center_col = rows // 2, cols // 2
        kernel = np.zeros((rows, cols), np.uint8)
        limiting_factor = min(center_row, center_col)
        radius = region_factor * limiting_factor

        for i in range(rows):
            for j in range(cols):
                dis = np.sqrt((i - center_row) ** 2 + (j - center_col) ** 2)
                if dis <= radius:
                    kernel[i, j] = 1

        return kernel


    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Images (*.png *.jpg *.bmp *.jpeg);;All Files (*)", options=options)
        if file_name:
            self.image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
            self.display_image(self.image)


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





# def apply_average_filter(self):
    #     image_width, image_height = self.image.shape
    #     filtered_img = np.zeros([image_width, image_height])
    #     kernel_size = 3
    #
    #
    #     #creating the kernel
    #     kernel = np.ones([kernel_size, kernel_size], dtype= int)
    #     avg_factor = kernel_size * kernel_size
    #     kernel = kernel / avg_factor
    #     print("inside avg filter")

    #     #temp assuming kernal size b 3
    #     for i in range(1, image_width - 1):
    #         for j in range(1, image_height - 1):
    #             temp_img = self.image[i - 1, j - 1] * kernal[0, 0] + self.image[i - 1, j] * kernal[0, 1] + self.image[i - 1, j + 1] * kernal[0, 2] + \
    #                    self.image[i, j - 1] * kernal[1, 0] + self.image[i, j] * kernal[1, 1] + self.image[i, j + 1] * kernal[1, 2] + self.image[
    #                        i + 1, j - 1] * kernal[2, 0] + self.image[i + 1, j] * kernal[2, 1] + self.image[i + 1, j + 1] * kernal[2, 2]
    #
    #             filtered_img[i, j] = temp_img
    #             print(f"hena temp_img {temp_img}")
    #
    #     filtered_img = filtered_img.astype(np.uint8)
    #     self.display_image(filtered_img)




    # def create_gaussian_kernel(self, kernel_size):
    #     sigma = 0.3 * ((kernel_size -1)*0.5 -1) +0.8
    #     guassian = []
    #     sum = 0
    #     G = 0
    #
    #     for i in range( int(-(kernel_size -1) /2), int((kernel_size -1) /2 +1)):
    #         filter_list = []
    #         for j in range(int(-(kernel_size - 1) / 2), int((kernel_size - 1) / 2 + 1)):
    #             G = math.exp(-(i**2 + j**2) / (2*sigma **2))
    #             filter_list.append(G)
    #             sum += G
    #             guassian += [filter_list]
    #
    #     guassian = np.array(guassian) / sum
    #     return guassian