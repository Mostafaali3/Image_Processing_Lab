import pyqtgraph as pg

class ImageViewer(pg.ImageView):
    def __init__(self):
        super().__init__()
        self.getView().setBackgroundColor("#1E293B")
        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.getView().invertY(False)
        self.getView().setAspectLocked(False)
        self.current_mode = "Transmitting Mode"
        
    def plot_image(self):
        pass