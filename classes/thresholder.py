import cv2
from enums.thresholdType import Threshold_type


class Thresholder():
    def __init__(self, output_image_viewer):
        self.output_image_viewer = output_image_viewer
        self.threshold_type = None
        self.check_global_selection = False
        self.global_threshold_val = 127


    def apply_thresholding(self, threshold_type):
        if self.output_image_viewer.current_image is not None:
            if threshold_type == "LOCAL":
                self.output_image_viewer.current_image.transfer_to_gray_scale()
                self.apply_local_thresholding()
            elif threshold_type == "GLOBAL" and self.check_global_selection:
                self.output_image_viewer.current_image.transfer_to_gray_scale()
                self.apply_global_thresholding()



    def apply_global_thresholding(self):
        # if it was gradiant --> any pixel below 127 is black and above 127 is white
        # ret returns true of false (whether we can apply thresholding aslan or not) --> not significant
        # thresh_val = 0
        print(f"new threshold {self.global_threshold_val}")
        ret, global_thresholded_img = cv2.threshold(self.output_image_viewer.current_image.modified_image, self.global_threshold_val, 255,cv2.THRESH_BINARY)
        self.output_image_viewer.current_image.modified_image = global_thresholded_img


    def apply_local_thresholding(self):
        local_thresholded_img = cv2.adaptiveThreshold(self.output_image_viewer.current_image.modified_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                  cv2.THRESH_BINARY, 11, 2)
        # sum of el mean of each block (11 blocks) - C
        # block size should be odd --> the greater the size, less noise
        print("gwa el local_thresholding")
        self.output_image_viewer.current_image.modified_image = local_thresholded_img





    # def update_global_threshold_val(self, value):
    #     self.global_threshold_val = value
    #     print(f"slider value {value}")
    #     self.apply_global_thresholding()











