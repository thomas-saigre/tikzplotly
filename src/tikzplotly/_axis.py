class Axis():

    def __init__(self, layout):
        self.x_label = layout.xaxis.title.text
        self.y_label = layout.yaxis.title.text
        self.title = layout.title.text

    def set_x_label(self, xlabel):
        self.xlabel = xlabel
    
    def set_y_label(self, ylabel):
        self.ylabel = ylabel

    def get_options(self):
        options_str = ""
        if self.title is not None:
            options_str += f"title={self.title},\n"
        if self.x_label is not None:
            options_str += f"xlabel={self.x_label},\n"
        if self.y_label is not None:
            options_str += f"ylabel={self.y_label},\n"
        return options_str[:-1]