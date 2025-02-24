from copy import deepcopy
import numpy as np



class Image():
    def __init__(self, data = None):
        self.original_data = data
        self.modified_image = deepcopy(data)
        self.gray = False
        self.frequency_data = None
        if data:
            pass #get the fast fourier transform of this image only once
        
    def get_histogram(self):
        pass
    
    def transfer_to_gray_scale(self):
        pass
    
    def mix(self, other):
        if isinstance(self, other):
            pass