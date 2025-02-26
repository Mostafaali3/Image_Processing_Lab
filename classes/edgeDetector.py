import math
import cv2
import numpy as np


class Edge_detector():
    def __init__(self, output_image_viewer):
        self.output_image_viewer = output_image_viewer


    def apply_edge_detectors(self, detector_type):
        if self.output_image_viewer.current_image is not None:
            self.output_image_viewer.current_image.transfer_to_gray_scale()
            print(f"detector type {detector_type}")



    def sobel_edge_detector(self):
        pass

    def roberts_edge_detector(self):
        pass

    def prewitt_edge_detector(self):
        pass

    def canny_edge_detector(self):
        pass


