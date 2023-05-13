from ._color import convert_color
class Axis():

    def __init__(self, layout, colors_set):
        self.x_label = layout.xaxis.title.text
        self.y_label = layout.yaxis.title.text
        self.title = layout.title.text
        self.options = {}

        if layout.xaxis.visible is False:
            self.x_label = None
            self.add_option("hide x axis", None)
        if layout.yaxis.visible is False:
            self.y_label = None
            self.add_option("hide y axis", None)

        if layout.plot_bgcolor is not None:
            bg_color = convert_color(layout.plot_bgcolor)
            colors_set.add(bg_color[:3])
            opacity = bg_color[3]
            if opacity < 1:
                self.add_option("axis background/.style", f"{{fill={bg_color[0]}, opacity={opacity}}}")
            else:
                self.add_option("axis background/.style", f"{{fill={bg_color[0]}}}")

    def set_x_label(self, x_label):
        self.x_label = x_label
    
    def set_y_label(self, y_label):
        self.y_label = y_label

    def add_option(self, option, value):
        self.options[option] = value


    def get_options(self):
        something = False
        options_str = ""
        if self.title is not None:
            options_str += f"title={self.title},\n"
            something = True
        if self.x_label is not None:
            options_str += f"xlabel={self.x_label},\n"
            something = True
        if self.y_label is not None:
            options_str += f"ylabel={self.y_label},\n"
            something = True
        if len(self.options) > 0:
            for option, value in self.options.items():
                if value is None:
                    options_str += f"{option},\n"
                else:
                    options_str += f"{option}={value},\n"
            something = True
        if something:
            return options_str[:-1]
        else:
            return None