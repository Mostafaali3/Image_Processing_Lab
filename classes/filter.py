import math
import cv2
import numpy as np


class Filters():
    def __init__(self, output_image_viewer, filtered_hybrid_image_viewer_1, filtered_hybrid_image_viewer_2):
        self.output_image_viewer = output_image_viewer
        self.filtered_hybrid_image_viewer_1 = filtered_hybrid_image_viewer_1
        self.filtered_hybrid_image_viewer_2 = filtered_hybrid_image_viewer_2


    def apply_filters(self, filter_type):
        if self.output_image_viewer.current_image is not None:
            # self.output_image_viewer.current_image.transfer_to_gray_scale()
            if len(self.output_image_viewer.current_image.modified_image.shape) == 3:
                self.output_image_viewer.current_image.transfer_to_gray_scale()
            print(f"filter type {filter_type}")
            if filter_type == "Average Filter":
                self.apply_average_filter()
            elif filter_type == "Median Filter":
                self.apply_median_filter()
            elif filter_type == "Gaussiann Filter":
                self.apply_gaussian_filter()


    def apply_average_filter(self):
        image_height, image_width = self.output_image_viewer.current_image.modified_image.shape
        kernel_size = 5  # odd num input passed mn el func
        filtered_img = np.zeros_like(self.output_image_viewer.current_image.modified_image, dtype=np.float32)

        # creating the kernel
        kernel = np.ones((kernel_size, kernel_size), dtype=np.float32)
        norm_factor = kernel_size * kernel_size
        kernel /= norm_factor

        # creating padding (fake pixels to handle edges)
        pad_size = kernel_size // 2
        padded_image = np.pad(self.output_image_viewer.current_image.modified_image,
                              ((pad_size, pad_size), (pad_size, pad_size)),
                              mode='reflect')  # print(f"hena padded_img {padded_image}")

        for i in range(pad_size, image_height + pad_size):
            for j in range(pad_size, image_width + pad_size):
                # instead of looping 3la kol pixel (gonna take forever) we apply the process mat by mat
                region = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1]
                filtered_img[i - pad_size, j - pad_size] = np.sum(region * kernel)

        filtered_img = filtered_img.astype(np.uint8)
        print(f"hena filtered_img using avg {filtered_img}")
        self.output_image_viewer.current_image.modified_image = filtered_img



    def apply_median_filter(self):

        image_height, image_width = self.output_image_viewer.current_image.modified_image.shape
        kernel_size = 5  # odd num input passed mn el func
        filtered_img = np.zeros_like(self.output_image_viewer.current_image.modified_image, dtype=np.uint8)

        # creating padding (fake pixels to handle edges)
        pad_size = kernel_size // 2
        padded_image = np.pad(self.output_image_viewer.current_image.modified_image,
                              ((pad_size, pad_size), (pad_size, pad_size)), mode='reflect')        # print(f"hena padded_img {padded_image}")

        for i in range(pad_size, image_height + pad_size):
            for j in range(pad_size, image_width + pad_size):
                # instead of looping 3la kol pixel (gonna take forever) we apply the process mat by mat
                region = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1]
                filtered_img[i - pad_size, j - pad_size] = np.median(
                    region)  # obtaining median of the selected region

        print(f"hena filtered_img using median{filtered_img}")
        self.output_image_viewer.current_image.modified_image = filtered_img

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

        image_height, image_width = self.output_image_viewer.current_image.modified_image.shape
        kernel_size = 13  # odd num input passed mn el func
        filtered_img = np.zeros_like(self.output_image_viewer.current_image.modified_image, dtype=np.float32)

        # creating the Gaussian kernel
        kernel = self.create_gaussian_kernel(kernel_size)
        # creating padding (fake pixels to handle edges)
        pad_size = kernel_size // 2
        padded_image = np.pad(self.output_image_viewer.current_image.modified_image,
                              ((pad_size, pad_size), (pad_size, pad_size)),
                              mode='reflect')  # print(f"hena padded_img {padded_image}")

        for i in range(pad_size, image_height + pad_size):
            for j in range(pad_size, image_width + pad_size):
                # instead of looping 3la kol pixel (gonna take forever) we apply the process mat by mat
                region = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1]
                # apply the Gaussian kernel
                filtered_img[i - pad_size, j - pad_size] = np.sum(region * kernel)

        filtered_img = filtered_img.astype(np.uint8)
        print(f"hena filtered_img {filtered_img}")
        self.output_image_viewer.current_image.modified_image = filtered_img

    def apply_low_pass_filter(self, region_factor, viewer_number = None):
        if viewer_number == 1:
            current_output_viewer_to_process = self.filtered_hybrid_image_viewer_1
        elif viewer_number == 2:
            current_output_viewer_to_process = self.filtered_hybrid_image_viewer_2
        else:
            current_output_viewer_to_process = self.output_image_viewer
        
        if current_output_viewer_to_process.current_image is not None:
            low_pass_mat = self.create_fourier_filter_mask(region_factor, viewer_number)
            filtered_fourier = current_output_viewer_to_process.current_image.image_fourier_components* low_pass_mat
            filtered_img = np.fft.ifftshift(filtered_fourier)
            filtered_img = np.fft.ifft2(filtered_img)
            filtered_img = np.abs(filtered_img).astype(np.uint8)
            current_output_viewer_to_process.current_image.modified_image = filtered_img
            # return filtered_img


    def apply_high_pass_filter(self, region_factor, viewer_number = None):
        if viewer_number == 1:
            current_output_viewer_to_process = self.filtered_hybrid_image_viewer_1
        elif viewer_number == 2:
            current_output_viewer_to_process = self.filtered_hybrid_image_viewer_2
        else:
            current_output_viewer_to_process = self.output_image_viewer
        
        if current_output_viewer_to_process.current_image is not None:
            high_pass_mat = 1 - self.create_fourier_filter_mask(region_factor, viewer_number)
            filtered_fourier = current_output_viewer_to_process.current_image.image_fourier_components * high_pass_mat
            filtered_img = np.fft.ifftshift(filtered_fourier)
            filtered_img = np.fft.ifft2(filtered_img)
            filtered_img = np.abs(filtered_img).astype(np.uint8)
            current_output_viewer_to_process.current_image.modified_image = filtered_img
            # return filtered_img

    def create_fourier_filter_mask(self,region_factor, viewer_number=None):
        if viewer_number == 1:
            current_output_viewer_to_process = self.filtered_hybrid_image_viewer_1
        elif viewer_number == 2:
            current_output_viewer_to_process = self.filtered_hybrid_image_viewer_2
        else:
            current_output_viewer_to_process = self.output_image_viewer
        
        rows, cols = current_output_viewer_to_process.current_image.image_fourier_components.shape
        center_row, center_col = rows// 2, cols// 2
        kernel = np.zeros((rows, cols), np.uint8)
        # choosing the min between el height wl width --> thus the region will never exceed the pic
        if region_factor != 0:
            limiting_factor = min(center_row, center_col)
            radius = region_factor * limiting_factor

            for i in range(rows):
                for j in range(cols):
                    dis = np.sqrt((i - center_row) ** 2 + (j - center_col) ** 2)
                    if dis <= radius:
                        kernel[i, j] = 1

        return kernel







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