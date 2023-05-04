class Axis():

    def __init__(self, xaxis_layout, yaxis_layout):
        self.x_label = xaxis_layout['title']['text']
        self.y_label = yaxis_layout['title']['text']

    def set_x_label(self, xlabel):
        self.xlabel = xlabel
    
    def set_y_label(self, ylabel):
        self.ylabel = ylabel

    def get_options(self):
        return f"xlabel={self.x_label},\nylabel={self.y_label}"