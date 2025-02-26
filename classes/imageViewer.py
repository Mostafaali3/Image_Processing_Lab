import pyqtgraph as pg
from enums.viewerType import ViewerType
import cv2
class ImageViewer(pg.ImageView):
    def __init__(self):
        super().__init__()
        self.getView().setBackgroundColor("#edf6f9")
        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.getView().setAspectLocked(False)
        self.viewer_type = ViewerType.INPUT
        self.current_image = None
        
    def update_plot(self):
        if self.current_image is not None:
            self.clear()
            if self.viewer_type == ViewerType.INPUT:
                self.setImage(cv2.transpose(self.current_image.original_image))
                print("gwa update_plot input")
            elif self.viewer_type == ViewerType.OUTPUT:
                self.setImage(cv2.transpose(self.current_image.modified_image))
                print("gwa update_plot output")