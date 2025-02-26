class Controller():
    def __init__(self, r_histogram_viewer,g_histogram_viewer,b_histogram_viewer, gray_histogram_viewer, r_cdf_viewer, g_cdf_viewer, b_cdf_viewer,gray_cdf_viewer, input_image_viewer, output_image_viewer ):
        self.r_histogram_viewer = r_histogram_viewer
        self.g_histogram_viewer = g_histogram_viewer
        self.b_histogram_viewer = b_histogram_viewer
        self.gray_histogram_viewer = gray_histogram_viewer
        self.r_cdf_viewer = r_cdf_viewer
        self.g_cdf_viewer = g_cdf_viewer
        self.b_cdf_viewer = b_cdf_viewer
        self.gray_cdf_viewer = gray_cdf_viewer
        self.input_image_viewer = input_image_viewer 
        self.output_image_viewer = output_image_viewer
        
        
    def update(self):
        self.input_image_viewer.update_plot()
        self.output_image_viewer.update_plot()
    
    
    