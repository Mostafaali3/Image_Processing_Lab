import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QVBoxLayout, QSlider, QComboBox, QPushButton, QStackedWidget
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from helper_function.compile_qrc import compile_qrc
from icons_setup.compiledIcons import *
from classes.viewer import Viewer


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
        
        
        
        
        
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())