from copy import deepcopy
import numpy as np
import cv2
from enums.type import Type


class Image():
    def __init__(self, data=None, calculate_fourier = True):
        self.__original_image = data
        self.__modified_image = deepcopy(data)
        self.is_loaded = False

        self.current_type = Type.NONE #fix 
        if data is not None:
            self.is_loaded = True
            if len(self.__original_image.shape) == 2:
                self.current_type = Type.GRAY
                # imported_image_gray_scale = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
                self.__original_image = np.array(data, dtype=np.uint8)
            else:
                self.current_type = Type.RGB
                image_rgb = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
                self.__original_image = image_rgb
                self.r_channel, self.g_channel, self.b_channel = cv2.split(self.__original_image)
            self.__modified_image = deepcopy(self.__original_image)
            
            if calculate_fourier:
                self.transfer_to_gray_scale()
                self.__image_fourier_components = np.fft.fft2(self.__modified_image)
                self.__image_fourier_components = np.fft.fftshift(self.__image_fourier_components)
                self.reset()

            self.original_image_distributions = []
            self.modified_image_distributions = []

            self.gray_histo_vector = np.zeros(256)
            self.gray_cum_vector = np.zeros(256)
            self.blue_histo_vector, self.green_histo_vector, self.red_histo_vector = np.zeros(256), np.zeros(
                256), np.zeros(256)
            self.blue_cum_vector, self.green_cum_vector, self.red_cum_vector = np.zeros(256), np.zeros(256), np.zeros(
                256)

            # self.__modified_image_fourier_components = deepcopy(self.__original_image)

    @property
    def original_image(self):
        return self.__original_image

    @property
    def modified_image(self):
        return self.__modified_image

    @property
    def image_fourier_components(self):
        return self.__image_fourier_components
    
    @modified_image.setter
    def modified_image(self, value):
        self.__modified_image = value

    def calculate_sigle_dim_historgram(self, single_dim_image_mat, histo_vector, cumulative_vector):
        total_num_of_pixel = 0
        print(single_dim_image_mat.shape)
        for row in range(len(single_dim_image_mat)):
            for col in range(len(single_dim_image_mat[row])):
                histo_vector[int(single_dim_image_mat[row][col])] += 1
                total_num_of_pixel += 1

        cumulative_sum = 0
        for i, val in enumerate(histo_vector):
            cumulative_sum += val
            cumulative_vector[i] = float(cumulative_sum / total_num_of_pixel)

    def calculate_Rgb_histograms(self):
        self.reset_histo_vector()
        blue_channel, green_channel , red_channel = cv2.split(self.__modified_image)

        self.calculate_sigle_dim_historgram(blue_channel, self.blue_histo_vector, self.blue_cum_vector)
        self.calculate_sigle_dim_historgram(green_channel, self.green_histo_vector, self.green_cum_vector)
        self.calculate_sigle_dim_historgram(red_channel, self.red_histo_vector, self.red_cum_vector)

    def reset_histo_vector(self):
        self.gray_histo_vector = np.zeros(256)
        self.red_histo_vector = np.zeros(256)
        self.green_histo_vector = np.zeros(256)
        self.blue_histo_vector = np.zeros(256)
        self.red_cum_vector = np.zeros(256)
        self.blue_cum_vector = np.zeros(256)
        self.green_cum_vector = np.zeros(256)
    def get_histogram(self):
        self.reset_histo_vector()
        if len(self.__modified_image.shape) == 2:
            self.calculate_sigle_dim_historgram(self.__modified_image, self.gray_histo_vector, self.gray_cum_vector)
        else:
            self.calculate_Rgb_histograms()
    def equalize_image(self):
        if  len(self.__modified_image.shape) != 2:
            self.transfer_to_gray_scale()
            self.get_histogram()
        gray_cum_vector_normalized = np.round(self.gray_cum_vector * 255).astype(np.uint8)
        for row in range(self.__modified_image.shape[0]):
            for col in range(self.__modified_image.shape[1]):
                old_intensity = self.__modified_image[row, col]
                new_intensity = gray_cum_vector_normalized[old_intensity]
                self.__modified_image[row, col] = new_intensity

    def normalize_image(self):
        self.transfer_to_gray_scale()
        min_pixel = self.__modified_image[0,0]
        max_pixel = 0
        for row in range(self.__modified_image.shape[0]):
            for col in range(self.__modified_image.shape[1]):
                if self.__modified_image[row, col] <= min_pixel:
                    min_pixel = self.__modified_image[row, col]
                elif self.__modified_image[row, col] >= max_pixel:
                    max_pixel = self.__modified_image[row, col]

        if max_pixel == min_pixel:
            print ("Normalization can't be done")
            return

        self.__modified_image = self.__modified_image.astype(np.float32)
        # Normalization Formula
        self.__modified_image = 255 * (self.__modified_image - min_pixel) / (max_pixel - min_pixel)
        # Convert Back to uint8
        self.__modified_image = np.clip(self.__modified_image, 0, 255).astype(np.uint8)
        # for row in range(self.__modified_image.shape[0]):
        #     for col in range(self.__modified_image.shape[1]):
        #         self.__modified_image[row, col] = float( 255 * (self.__modified_image[row, col] - min_pixel) / (max_pixel - min_pixel))
        #
        # self.modified_image = self.__modified_image.astype(np.uint8)

    # @property
    # def original_image_fourier_components(self):
    #     return self.__original_image_fourier_components

    def transfer_to_gray_scale(self):
        if  len(self.__modified_image.shape) != 2:
            imported_image_gray_scale = np.dot(self.__modified_image[...,:3], [0.2989, 0.570, 0.1140])
            self.__modified_image = np.array(imported_image_gray_scale, dtype=np.uint8)
        #
        #
        # if len(self.__modified_image.shape) != 2:
        #     imported_image_gray_scale = cv2.cvtColor(self.__modified_image, cv2.COLOR_BGR2GRAY)
        #     self.__modified_image = np.array(imported_image_gray_scale, dtype=np.uint8)
            print(f"modified img shape {self.__modified_image.shape}")
        
    def reset(self):
        self.__modified_image = deepcopy(self.__original_image)

    def mix(self, other):
        print(f"{self.__modified_image.shape}")
        print(f"{other.modified_image.shape}")
        
        rows_1, cols_1 = self.__modified_image.shape
        rows_2, cols_2 = other.modified_image.shape
        rows = min(rows_1, rows_2)
        cols = min(cols_1, cols_2)
        first_image = self.modified_image[:rows,:cols]
        sec_image = other.modified_image[:rows,:cols]
        
        result_sum = first_image.astype(np.float32) + sec_image.astype(np.float32)
        result = (result_sum/2).astype(np.uint8)
        new_image = Image(result)
        return new_image
