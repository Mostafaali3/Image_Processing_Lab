import pyqtgraph as pg
from enums.graphType import GraphType
from enums.type import Type
from enums.colors import Color
import cv2
import numpy as np
class Viewer(pg.PlotWidget):
    def __init__(self,color: Color, graph_type: GraphType):
        super().__init__()
        self.__channels = []
        self.setLimits(xMin = 0, xMax = 1000)
        self.setBackground('w')
        self.showGrid(x= True, y= True , alpha = 0.25)
        self.current_graph_type = graph_type
        self.x_range = np.arange(256)
        self.output_image =  None
        self.color = color
    def update_histogram(self):
        # self.output_image.get_histogram() # calling for histograms calculations
        if self.output_image is not None :
            self.clear()
            if self.current_graph_type == GraphType.HISTO :
                histo_name = f"{self.color.name()}_histo_vector"
                histo_vector = getattr(self.output_image, histo_name, None)
                if histo_vector is not None:
                    self.addItem(pg.BarGraphItem(
                        x = self.x_range,
                        height = histo_vector,
                        width = 1,
                        brush = self.color.brush()
                    ))
            else : # it will be cdf
                cdf_name = f"{self.color.name()}_cum_vector"
                cdf_vector = getattr(self.output_image, cdf_name, None)
                if cdf_vector is not None :
                    self.plot(self.x_range, cdf_vector, pen=self.color.brush())







