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
                imported_image_gray_scale = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
                self.__original_image = np.array(imported_image_gray_scale, dtype=np.uint8)
            else:      
                self.current_type = Type.RGB
                image_rgb = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
                self.__original_image = image_rgb
                self.r_channel, self.g_channel, self.b_channel = cv2.split(self.__original_image)
            self.__modified_image = deepcopy(self.__original_image)
            self.transfer_to_gray_scale()
            
            self.__image_fourier_components = np.fft.fft2(self.__original_image)
            self.__image_fourier_components = np.fft.fftshift(self.__image_fourier_components)
            
            self.original_image_distributions = []
            self.modified_image_distributions = []
            
            # self.__modified_image_fourier_components = deepcopy(self.__original_image)

    @property
    def original_image(self):
        return self.__original_image
    
    @property
    def modified_image(self):
        return self.__modified_image
    

    @modified_image.setter
    def modified_image(self, value):
        self.__modified_image = value
    
    def get_histogram(self, index): # implementation from scratch 
        '''
        index: 0 or 1, 0 represents the histogram of the original image and 1 represents the histogram of the modified image
        note, you need to check if the output is 3 arrays or only one because of the rgb and the gray scale images 
        '''
        image_to_calculate = None
        if index == 0: # original image histograms
            image_to_calculate = self.__original_image
        elif index == 1:
            image_to_calculate = self.__modified_image
        # need to be completed
        pass
    
    @property
    def image_fourier_components(self):
        return self.__image_fourier_components
    
    # @property
    # def original_image_fourier_components(self):
    #     return self.__original_image_fourier_components
    
    def transfer_to_gray_scale(self):
        # if self.__modified_image is not None:
        #     imported_image_gray_scale = np.dot(self.__modified_image[...,:3], [0.2989, 0.570, 0.1140])
        #     self.__modified_image = np.array(imported_image_gray_scale, dtype=np.uint8)
        #
        #
        imported_image_gray_scale = cv2.cvtColor(self.__original_image , cv2.COLOR_BGR2GRAY)
        self.__modified_image = np.array(imported_image_gray_scale, dtype=np.uint8)
        print(f"modified img shape {self.__modified_image.shape}")
    
    def mix(self, other):
        if isinstance(self, other):
            pass