# Image Processing Lab

## Description
This project focuses on various image processing techniques using OpenCV, including noise addition, filtering, edge detection, thresholding, histogram analysis, and hybrid image creation. The results from different methods and parameter variations are analyzed and presented in a UI for easy testing and comparison.

![Application Overview](assets/Group%2016.png "Overview of the Fourier Transform Mixer")

## Features
- **Image Acquisition**: Supports both RGB and grayscale images.
- **Noise Addition**: Implements uniform, Gaussian, and salt & pepper noise to simulate real-world image distortions.
- **Noise Reduction Filters**: Includes average, Gaussian, and median filters to clean noisy images.
- **Edge Detection**: Implements Sobel, Roberts, Prewitt, and Canny edge detection methods (custom implementations for Sobel, Roberts, and Prewitt).
- **Histogram Analysis**: Generates histograms for R, G, and B channels, along with cumulative distribution function plots.
- **Image Equalization and Normalization**: Enhances image contrast and standardizes pixel intensity values.
- **Thresholding Techniques**: Supports both local and global thresholding methods.
- **Frequency Domain Filtering**: Implements high-pass and low-pass filters for frequency-based image enhancements.
- **Hybrid Image Generation**: Combines low and high-frequency components to create hybrid images.
- **UI Integration**: Interactive interface for testing different image processing techniques.
- **Comparative Analysis**: Provides a structured report detailing the impact of different methods and parameter variations.

## Dependencies

The image processing lab relies on the following technologies and libraries:

| **Dependency**       | **Description**                                       |
|-----------------------|-------------------------------------------------------|
| Python 3.x           | Core programming language.                            |
| NumPy                | Numerical computations for signal processing.         |
| PyQt5                | GUI framework for building desktop applications.      |
| pyqtgraph            | Fast plotting and 2D visualization in PyQt.           |
| matplotlib           | Visualization library for plotting and analysis.      |
| OpenCV (cv2)         | Computer vision library for image manipulation.       |        |


## How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/Mostafaali3/image_processing_lab
   cd image_processing_lab
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the main script:
   ```bash
   python main.py
   ```

## Contributors
<div align="center">
  <table style="border-collapse: collapse; border: none;">
    <tr>
      <td align="center" style="border: none;">
        <img src="https://avatars.githubusercontent.com/Mostafaali3" alt="Mostafa Ali" width="150" height="150"><br>
        <a href="https://github.com/Mostafaali3"><b>Mostafa Ali</b></a>
      </td>
      <td align="center" style="border: none;">
        <img src="https://avatars.githubusercontent.com/habibaalaa123" alt="Habiba Alaa" width="150" height="150"><br>
        <a href="https://github.com/habibaalaa123"><b>Habiba Alaa</b></a>
      </td>
      <td align="center" style="border: none;">
        <img src="https://avatars.githubusercontent.com/enjyashraf18" alt="Anjy Ashraf" width="150" height="150"><br>
        <a href="https://github.com/enjyashraf18"><b>Enjy Ashraf</b></a>
      </td>
      </td>
      <td align="center" style="border: none;">
        <img src="https://avatars.githubusercontent.com/Shahd-A-Mahmoud" alt="Shahd Ahmed" width="150" height="150"><br>
        <a href="https://github.com/Shahd-A-Mahmoud"><b>Shahd Ahmed</b></a>
      </td>
  </table>
</div>

## License
This project is open-source and available under the [MIT License](LICENSE).

