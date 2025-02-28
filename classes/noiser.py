import cv2
import numpy as np


class Noiser():
    def __init__(self, output_image_viewer):
        self.output_image_viewer = output_image_viewer
    def apply_salt_and_pepper_noise(self, salt_ratio, pepper_ratio):
        image = self.output_image_viewer.current_image
        pixels = image.modified_image.size

        no_of_salts = int(pixels * salt_ratio)
        no_of_pepper = int(pixels * pepper_ratio)

        coords = [np.random.randint(0, i, no_of_salts) for i in image.modified_image.shape[:2]]
        image.modified_image[coords[0], coords[1]] = 255

        coords = [np.random.randint(0, i, no_of_pepper) for i in image.modified_image.shape[:2]]
        image.modified_image[coords[0], coords[1]] = 0

    def apply_uniform_noise(self,  noise_intensity):
        image = self.output_image_viewer.current_image
        uniform_noise = np.random.uniform(-noise_intensity, noise_intensity, image.modified_image.shape).astype(np.uint8)
        modified_image = cv2.add(image.modified_image, uniform_noise)
        image.modified_image = modified_image
    def apply_gaussian_noise(self, mean, standard_deviation):
        image = self.output_image_viewer.current_image
        gaussian_noise = np.random.normal(mean, standard_deviation, image.modified_image.shape).astype(np.uint8)
        modified_image = cv2.add(image.modified_image, gaussian_noise)
        image.modified_image = modified_image