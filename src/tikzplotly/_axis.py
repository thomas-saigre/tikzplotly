from ._color import convert_color
from ._tex import tex_begin_environment
from ._utils import sanitize_TeX_text, option_dict_to_str, get_ticks_str
from warnings import warn

class Axis():

    def __init__(self, layout, colors_set, axis_options=None):
        """Initialize an Axis.

        Parameters
        ----------
        layout
            layout of the figure
        colors_set
            set of colors used in the figure, to be filled with the colors of the axis
        axis_options
            options given to the axis environment, by default None. Can be a dict ({option: value}) or a string ("option1=value1, option2=value2").
        """
        self.layout = layout

        self.options = {}
        if isinstance(axis_options, dict):
            self.options = axis_options
        elif isinstance(axis_options, str):
            for option in axis_options.split(","):
                option = option.strip()
                if "=" in option:
                    key, value = option.split("=")
                    self.options[key] = value
                else:
                    self.options[option] = None
        self.environment = "axis"

        self.xticks = None

        self.treat_axis_layout()
        self.treat_background_layout(colors_set)
        self.treat_bar_layout()




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
        if self.title is not None:
            self.options["title"] = sanitize_TeX_text(self.title)
        if self.x_label is not None:
            self.options["xlabel"] = sanitize_TeX_text(self.x_label)
        if self.y_label is not None:
            self.options["ylabel"] = sanitize_TeX_text(self.y_label)
        options_str = option_dict_to_str(self.options, sep="\n")
        return options_str


    def treat_axis_layout(self):
        """Treat the layout of the axis."""

        self.x_label = self.layout.xaxis.title.text
        self.y_label = self.layout.yaxis.title.text
        self.title = self.layout.title.text

        if self.layout.xaxis.visible is False:
            self.x_label = None
            self.add_option("hide x axis", None)
        if self.layout.yaxis.visible is False:
            self.y_label = None
            self.add_option("hide y axis", None)

        # Handle log axes
        if self.layout.xaxis.type == "log":
            self.add_option("xmode", "log")
        if self.layout.yaxis.type == "log":
            self.add_option("ymode", "log")

        # Handle range
        # In log mode, the range is the exponent of the range : https://plotly.com/python/reference/layout/xaxis/#layout-xaxis-range
        # For more information, refer to documentation https://plotly.com/python/reference/layout/xaxis/#layout-xaxis-autorange
        if self.layout.xaxis.autorange is False or self.layout.xaxis.range is not None:
            self.add_option("xmin", self.layout.xaxis.range[0] if self.layout.xaxis.type != "log" else 10**layout.xaxis.range[0])
            self.add_option("xmax", self.layout.xaxis.range[1] if self.layout.xaxis.type != "log" else 10**layout.xaxis.range[1])
        if self.layout.yaxis.autorange is False or self.layout.yaxis.range is not None:
            self.add_option("ymin", self.layout.yaxis.range[0] if self.layout.yaxis.type != "log" else 10**layout.yaxis.range[0])
            self.add_option("ymax", self.layout.yaxis.range[1] if self.layout.yaxis.type != "log" else 10**layout.yaxis.range[1])
        if self.layout.xaxis.autorange == "reversed":
            self.add_option("x dir", "reverse")
        if self.layout.yaxis.autorange == "reversed":
            self.add_option("y dir", "reverse")

        if self.layout.xaxis.showline == False:
            self.add_option("axis x line", "none")
        if self.layout.yaxis.showline == False:
            self.add_option("axis y line", "none")
        if self.layout.xaxis.categoryorder == "array":
            self.xticks = self.layout.xaxis.categoryarray
            ticks, ticklabels = get_ticks_str(self.layout.xaxis.categoryarray)
            self.add_option("xtick", ticks)
            self.add_option("xticklabels", ticklabels)

        if self.layout.xaxis.categoryorder != "trace" or self.layout.yaxis.categoryorder != "trace" or self.layout.xaxis.categoryorder != "total descending":
            warn("The categoryorder option is not supported (yet 🤞) for the axis environment.")

    def treat_background_layout(self, colors_set):
        if self.layout.plot_bgcolor is not None:
            bg_color = convert_color(self.layout.plot_bgcolor)
            colors_set.add(bg_color[:3])
            opacity = bg_color[3]
            if opacity < 1:
                self.add_option("axis background/.style", f"{{fill={bg_color[0]}, opacity={opacity}}}")
            else:
                self.add_option("axis background/.style", f"{{fill={bg_color[0]}}}")

    def treat_bar_layout(self):
        if (barmode := self.layout.barmode) is not None:
            if barmode == "stack":
                self.add_option("ybar stacked", None)