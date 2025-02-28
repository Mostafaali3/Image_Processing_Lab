import numpy as np
import cv2
import matplotlib.pyplot as plt


image = cv2.imread('data\diane.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
noise = np.random.normal(0, 25, image.shape).astype(np.uint8)  # Mean=0, Std=25
noisy_image = cv2.add(image, noise)

plt.imshow(noisy_image)

plt.show()

