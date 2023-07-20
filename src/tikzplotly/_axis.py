from ._color import convert_color
from ._tex import tex_begin_environment
class Axis():

    def __init__(self, layout, colors_set):
        """Initialize an Axis.

        Parameters
        ----------
        layout
            layout of the figure
        colors_set
            set of colors used in the figure, to be filled with the colors of the axis
        """
        self.x_label = layout.xaxis.title.text
        self.y_label = layout.yaxis.title.text
        self.title = layout.title.text
        self.options = {}
        self.environment = "axis"

        if layout.xaxis.visible is False:
            self.x_label = None
            self.add_option("hide x axis", None)
        if layout.yaxis.visible is False:
            self.y_label = None
            self.add_option("hide y axis", None)

        # Handle log axes
        if layout.xaxis.type == "log":
            self.add_option("xmode", "log")
        if layout.yaxis.type == "log":
            self.add_option("ymode", "log")

        if layout.plot_bgcolor is not None:
            bg_color = convert_color(layout.plot_bgcolor)
            colors_set.add(bg_color[:3])
            opacity = bg_color[3]
            if opacity < 1:
                self.add_option("axis background/.style", f"{{fill={bg_color[0]}, opacity={opacity}}}")
            else:
                self.add_option("axis background/.style", f"{{fill={bg_color[0]}}}")

    def set_x_label(self, x_label):
        """Set the x label.

        Parameters
        ----------
        x_label
            x label
        """
        self.x_label = x_label

    def set_y_label(self, y_label):
        """Set the y label.

        Parameters
        ----------
        y_label
            y label
        """
        self.y_label = y_label

    def add_option(self, option, value):
        """Add an option to the axis, to be used in the axis environment.

        Parameters
        ----------
        option
            name of the option
        value
            value of the option, can be None
        """
        self.options[option] = value

    def open_environment(self, stack_env):
        """Open the axis environment.

        Parameters
        ----------
        stack_env
            stack of environments, to be filled with the axis environment
        """
        return tex_begin_environment(self.environment, stack_env, options=self.get_options())


    def get_options(self):
        """Get options string for the axis environment.

        Returns
        -------
            string of all options with their values
        """
        content = False
        options_str = ""
        if self.title is not None:
            options_str += f"title={self.title},\n"
            content = True
        if self.x_label is not None:
            options_str += f"xlabel={self.x_label},\n"
            content = True
        if self.y_label is not None:
            options_str += f"ylabel={self.y_label},\n"
            content = True
        if len(self.options) > 0:
            for option, value in self.options.items():
                if value is None:
                    options_str += f"{option},\n"
                else:
                    options_str += f"{option}={value},\n"
            content = True
        if content:
            return options_str[:-1]
        else:
            return None