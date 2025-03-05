import cv2
import numpy as np
# import cv2
# from enums.thresholdType import Threshold_type

class Thresholder():
    def __init__(self,output_image_viewer):
        self.output_image_viewer = output_image_viewer
        self.threshold_type = None
        self.check_global_selection = False
        self.global_threshold_val = 127

    def apply_thresholding(self, threshold_type):
        if self.output_image_viewer.current_image is not None:
            if threshold_type == "LOCAL":
                self.restore_original_img()
                self.apply_local_thresholding()
            elif threshold_type == "GLOBAL" and self.check_global_selection:
                self.restore_original_img()
                self.apply_global_thresholding()

    def apply_global_thresholding(self):
        height, width = self.output_image_viewer.current_image.modified_image.shape
        thresholded_img = np.zeros((height, width), dtype=np.uint8)

        for row in range(height):
            for col in range(width):
                if self.output_image_viewer.current_image.modified_image[row, col] < self.global_threshold_val:
                    thresholded_img[row, col] = 0
                else:
                    thresholded_img[row, col] = 255
        print(f"thresh img {thresholded_img}")

        self.output_image_viewer.current_image.modified_image = thresholded_img


    def apply_local_thresholding(self):
        block_size =11
        c= 2
        height, width = self.output_image_viewer.current_image.modified_image.shape
        thresholded_img = np.zeros((height, width), dtype=np.uint8)
        img = self.output_image_viewer.current_image.modified_image
        for i in range(height):
            for j in range(width):
                x_min = max(0, i - block_size // 2)
                y_min = max(0, j - block_size // 2)
                x_max = min(height -1, i + block_size // 2)
                y_max = min(width - 1, j + block_size // 2)
                block = img[x_min:x_max + 1, y_min:y_max + 1]
                thresh = np.mean(block) - c
                if img[i, j] >= thresh:
                    thresholded_img[i, j] = 255

        self.output_image_viewer.current_image.modified_image= thresholded_img


    def restore_original_img(self):
        imported_image_gray_scale = cv2.cvtColor(self.output_image_viewer.current_image.original_image, cv2.COLOR_BGR2GRAY)
        self.output_image_viewer.current_image.modified_image= np.array(imported_image_gray_scale, dtype=np.uint8)



# import cv2
# from enums.thresholdType import Threshold_type
#
#
# class Thresholder():
#     def __init__(self, output_image_viewer):
#         self.output_image_viewer = output_image_viewer
#         self.threshold_type = None
#         self.check_global_selection = False
#         self.global_threshold_val = 127
#
#
#     def apply_thresholding(self, threshold_type):
#         if self.output_image_viewer.current_image is not None:
#             if threshold_type == "LOCAL":
#                 self.output_image_viewer.current_image.transfer_to_gray_scale()
#                 self.apply_local_thresholding()
#             elif threshold_type == "GLOBAL" and self.check_global_selection:
#                 self.output_image_viewer.current_image.transfer_to_gray_scale()
#                 self.apply_global_thresholding()
#
#
#
#     def apply_global_thresholding(self):
#         # if it was gradiant --> any pixel below 127 is black and above 127 is white
#         # ret returns true of false (whether we can apply thresholding aslan or not) --> not significant
#         # thresh_val = 0
#         print(f"new threshold {self.global_threshold_val}")
#         ret, global_thresholded_img = cv2.threshold(self.output_image_viewer.current_image.modified_image, self.global_threshold_val, 255,cv2.THRESH_BINARY)
#         self.output_image_viewer.current_image.modified_image = global_thresholded_img
#
#
#     def apply_local_thresholding(self):
#         local_thresholded_img = cv2.adaptiveThreshold(self.output_image_viewer.current_image.modified_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
#                                                   cv2.THRESH_BINARY, 11, 2)
#         # sum of el mean of each block (11 blocks) - C
#         # block size should be odd --> the greater the size, less noise
#         print("gwa el local_thresholding")
#         self.output_image_viewer.current_image.modified_image = local_thresholded_img
#
#
#
#
#
#
#
#
#
#

