import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QVBoxLayout, QSlider, QComboBox, QPushButton, QStackedWidget, QWidget, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from helper_function.compile_qrc import compile_qrc
from icons_setup.compiledIcons import *
from classes.viewer import Viewer
from classes.image import Image
import cv2


compile_qrc()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.r_histogram_viewer = Viewer()
        self.g_histogram_viewer = Viewer()
        self.b_histogram_viewer = Viewer()
        self.gray_histogram_viewer = Viewer()
        self.r_cdf_viewer = Viewer()
        self.g_cdf_viewer = Viewer()
        self.b_cdf_viewer = Viewer()
        self.gray_cdf_viewer = Viewer()
        
        self.gray_histogram_widget = self.findChild(QWidget, "widget_17")
        self.gray_histogram_layout = self.gray_histogram_widget.layout()
        self.gray_histogram_layout.addWidget(self.gray_histogram_viewer)
        
        self.gray_cdf_widget = self.findChild(QWidget, "widget_18")
        self.gray_cdf_layout = self.gray_cdf_widget.layout()
        self.gray_cdf_layout.addWidget(self.gray_cdf_viewer)
        
        self.r_histogram_layout = self.findChild(QVBoxLayout, "red_histogram")
        self.r_histogram_layout.addWidget(self.r_histogram_viewer)

        self.r_cdf_layout = self.findChild(QVBoxLayout, "red_cdf")
        self.r_cdf_layout.addWidget(self.r_cdf_viewer)
        
        self.g_histogram_layout = self.findChild(QVBoxLayout, "green_histogram")
        self.g_histogram_layout.addWidget(self.g_histogram_viewer)

        self.g_cdf_layout = self.findChild(QVBoxLayout, "green_cdf")
        self.g_cdf_layout.addWidget(self.g_cdf_viewer)
        
        self.b_histogram_layout = self.findChild(QVBoxLayout, "blue_histogram")
        self.b_histogram_layout.addWidget(self.b_histogram_viewer)

        self.b_cdf_layout = self.findChild(QVBoxLayout, "blue_cdf")
        self.b_cdf_layout.addWidget(self.b_cdf_viewer)
        
        self.main_page_browse_button = self.findChild(QPushButton, "browse")
        self.main_page_browse_button.clicked.connect(self.browse_image)
    
        
    def browse_image(self):
        print("pushed")
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Image Files (*.jpeg *.jpg *.png *.bmp *.gif);;All Files (*)')
        
        if file_path:
            if file_path.endswith('.jpeg') or file_path.endswith('.jpg'):
                temp_image = cv2.imread(file_path)
                print(temp_image.shape[0],temp_image.shape[1],temp_image.shape[2])
                image = Image(temp_image)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())