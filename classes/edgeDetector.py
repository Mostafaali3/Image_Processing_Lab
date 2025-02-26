import math
import cv2
import numpy as np


class Edge_detector():
    def __init__(self, output_image_viewer):
        self.output_image_viewer = output_image_viewer


    def apply_edge_detectors(self, detector_type):
        if self.output_image_viewer.current_image is not None:
            if len(self.output_image_viewer.current_image.modified_image.shape) == 3:
                self.output_image_viewer.current_image.transfer_to_gray_scale()
            print(f"detector type {detector_type}")
            if detector_type == "Sobel detector":
                self.sobel_edge_detector()



    def sobel_edge_detector(self):
        image_height, image_width = self.output_image_viewer.current_image.modified_image.shape
        # default and most common is 3 for now
        kernel_size = 3
        Gx, Gy = self.create_sobel_kernel(kernel_size)

        # gradiants for x and y
        G_x = np.zeros_like(self.output_image_viewer.current_image.modified_image, dtype=np.float32)
        G_y = np.zeros_like(self.output_image_viewer.current_image.modified_image, dtype=np.float32)

        pad_size = kernel_size // 2
        # gpt shit so 7arfyan no diff --> instead of opencv
        padded_image = np.pad(self.output_image_viewer.current_image.modified_image,((pad_size, pad_size), (pad_size, pad_size)), mode='reflect')

        for i in range(pad_size, image_height + pad_size):
            for j in range(pad_size, image_width + pad_size):
                region = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1]
                G_x[i - pad_size,j - pad_size] = np.sum(region * Gx)
                G_y[i -pad_size, j - pad_size] =np.sum(region * Gy)

        gradient_magnitude =np.sqrt(G_x ** 2 + G_y ** 2)
        threshold = 50
        # edges = gradient_magnitude > threshold
        #normailzation
        gradient_magnitude = (gradient_magnitude / np.max(gradient_magnitude)) * 255
        gradient_magnitude = gradient_magnitude.astype(np.uint8)
        self.output_image_viewer.current_image.modified_image = gradient_magnitude

    def create_sobel_kernel(self, kernel_size):
        gradiant_x = np.array([[-1, 0, 1],
                       [-2, 0, 2],
                       [-1, 0, 1]])

        gradiant_y = np.array([[-1, -2, -1],
                       [0, 0, 0],
                       [1, 2, 1]])
        return gradiant_x, gradiant_y

    def roberts_edge_detector(self):
        pass


    def prewitt_edge_detector(self):
        pass

    def canny_edge_detector(self):
        pass

    def kernel_restrictions(self, kernel_size):
        if kernel_size <3 :
            raise ValueError("kernel size must be >= 3")
        if kernel_size %2 ==0:
            raise ValueError("kernel size must be odd")
        if (kernel_size * kernel_size) < len(self.output_image_viewer):
            raise ValueError("pick a smaller kernel size")


import numpy as np
import cv2



