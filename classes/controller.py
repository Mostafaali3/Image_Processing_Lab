class Controller():
    def __init__(self, r_histogram_viewer,g_histogram_viewer,b_histogram_viewer, gray_histogram_viewer, r_cdf_viewer, g_cdf_viewer, b_cdf_viewer,gray_cdf_viewer, input_image_viewer, output_image_viewer, input_hybrid_image_viewer_1, input_hybrid_image_viewer_2, filtered_hybrid_image_viewer_1, filtered_hybrid_image_viewer_2,final_hybrid_image_viewer):
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
        self.input_hybrid_image_viewer_1 = input_hybrid_image_viewer_1
        self.input_hybrid_image_viewer_2 = input_hybrid_image_viewer_2
        self.filtered_hybrid_image_viewer_1 = filtered_hybrid_image_viewer_1
        self.filtered_hybrid_image_viewer_2 = filtered_hybrid_image_viewer_2
        self.final_hybrid_image_viewer = final_hybrid_image_viewer
        
        
    def update(self): #fix
        self.input_image_viewer.update_plot()
        self.output_image_viewer.update_plot()
        self.r_histogram_viewer.output_image.get_histogram() # to update the calculations
        self.r_histogram_viewer.update_histogram()
        self.g_histogram_viewer.update_histogram()
        self.b_histogram_viewer.update_histogram()
        self.gray_histogram_viewer.update_histogram()
        self.gray_cdf_viewer.update_histogram()
        self.r_cdf_viewer.update_histogram()
        self.b_cdf_viewer.update_histogram()
        self.g_cdf_viewer.update_histogram()
        
    def update_hybrid(self):#fix 
        self.input_hybrid_image_viewer_1.update_plot()
        self.input_hybrid_image_viewer_2.update_plot()
        self.filtered_hybrid_image_viewer_1.update_plot()
        self.filtered_hybrid_image_viewer_2.update_plot()
        self.final_hybrid_image_viewer.update_plot()

    
    
    