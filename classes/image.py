from copy import deepcopy
import numpy as np
import cv2
from enums.type import Type


class Image():
    def __init__(self, data = None):
        self.__original_image = data
        self.__modified_image = deepcopy(data)
        self.is_loaded = False
        self.current_type = Type.NONE
        if data is not None:
            self.is_loaded = True
            if self.__original_image.shape[2] == 1:
                self.current_type = Type.GRAY
                imported_image_gray_scale = cv2.cvtColor(data , cv2.COLOR_BGR2GRAY)
                self.__original_image = np.array(imported_image_gray_scale, dtype=np.uint8)
            else:      
                self.current_type = Type.RGB
                image_rgb = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
                self.__original_image = image_rgb
                self.r_channel, self.g_channel, self.b_channel = cv2.split(self.__original_image)
            self.__modified_image = deepcopy(self.__original_image)
            
            # self.__original_image_fourier_components = np.fft.fft2(self.__original_image)
            # self.__original_image_fourier_components = np.fft.fftshift(self.__original_image_fourier_components)
            # self.__modified_image_fourier_components = deepcopy(self.__original_image)

    @property
    def original_image(self):
        return self.__original_image
    
    @property
    def modified_image(self):
        return self.__modified_image
    
    # @property
    # def modified_image_fourier_components(self):
    #     return self.__modified_image_fourier_components
    
    # @property
    # def original_image_fourier_components(self):
    #     return self.__original_image_fourier_components
    
    
    def get_histogram(self):
        pass
    
    def transfer_to_gray_scale(self):
        pass
    
    def mix(self, other):
        if isinstance(self, other):
            pass