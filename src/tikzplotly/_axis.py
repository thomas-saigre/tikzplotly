"""
tikzplotly._axis

This module provides the Axis class, which manages the TikZ axis environment for converting Plotly figures to TikZ/PGFPlots code.
It handles axis options, labels, ticks, background, and bar layout, supporting customization via Plotly figure layout and color sets.
"""

from warnings import warn
from ._color import convert_color
from ._tex import tex_begin_environment
from ._utils import sanitize_tex_text, option_dict_to_str, get_ticks_str

class Axis():
    """Class to handle the axis environment in TikZ.
    This class manages the options and environment for the TikZ axis, including labels, ticks, and background.
    """

    def __init__(self, layout, colors_set, axis_options=None):
        """Initialize an Axis.

        Parameters
        ----------
        layout
            layout of the figure
        colors_set
            set of colors used in the figure, to be filled with the colors of the axis
        axis_options
            options given to the axis environment, by default None.
            Can be a dict ({option: value}) or a string ("option1=value1, option2=value2").
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
        self.x_label = None
        self.y_label = None

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
            self.options["title"] = sanitize_tex_text(self.title)
        if self.x_label is not None:
            self.options["xlabel"] = sanitize_tex_text(self.x_label)
        if self.y_label is not None:
            self.options["ylabel"] = sanitize_tex_text(self.y_label)
        options_str = option_dict_to_str(self.options, sep="\n")
        return options_str

    def treat_axis_layout(self):
        """Treat the layout of the axis."""

        self.set_x_label(self.layout.xaxis.title.text)
        self.set_y_label(self.layout.yaxis.title.text)
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
            self.add_option("xmin", self.layout.xaxis.range[0] if self.layout.xaxis.type != "log" else 10**self.layout.xaxis.range[0])
            self.add_option("xmax", self.layout.xaxis.range[1] if self.layout.xaxis.type != "log" else 10**self.layout.xaxis.range[1])
        if self.layout.yaxis.autorange is False or self.layout.yaxis.range is not None:
            self.add_option("ymin", self.layout.yaxis.range[0] if self.layout.yaxis.type != "log" else 10**self.layout.yaxis.range[0])
            self.add_option("ymax", self.layout.yaxis.range[1] if self.layout.yaxis.type != "log" else 10**self.layout.yaxis.range[1])
        if self.layout.xaxis.autorange == "reversed":
            self.add_option("x dir", "reverse")
        if self.layout.yaxis.autorange == "reversed":
            self.add_option("y dir", "reverse")

        if self.layout.xaxis.showline is False:
            self.add_option("axis x line", "none")
        if self.layout.yaxis.showline is False:
            self.add_option("axis y line", "none")
        if self.layout.xaxis.categoryorder == "array":
            self.xticks = self.layout.xaxis.categoryarray
            ticks, ticklabels = get_ticks_str(self.layout.xaxis.categoryarray)
            self.add_option("xtick", ticks)
            self.add_option("xticklabels", ticklabels)

        # At this point, only layout.xaxis.categoryarray = "array" is supported
        if self.layout.xaxis.categoryorder is not None and self.layout.xaxis.categoryorder not in ["array"]:
            warn(
            f"The xaxis categoryorder option {self.layout.xaxis.categoryorder} is not supported (yet 🤞) for the axis environment."
            )
        if self.layout.yaxis.categoryorder is not None and self.layout.yaxis.categoryorder not in []:
            warn(
            f"The yaxis categoryorder option {self.layout.yaxis.categoryorder} is not supported (yet 🤞) for the axis environment."
            )

        if self.layout.xaxis.showgrid:
            self.add_option("xmajorgrids", None)
        if self.layout.yaxis.showgrid:
            self.add_option("ymajorgrids", None)
        if self.layout.xaxis.ticklen is not None:
            self.add_option("tickwidth", self.layout.xaxis.ticklen)
        if self.layout.yaxis.ticklen is not None:
            self.add_option("tickwidth", self.layout.yaxis.ticklen)

        if (m := self.layout.xaxis.minor) is not None:
            if m.showgrid:
                self.add_option("xminorgrids", None)
            if m.ticklen is not None:
                self.add_option("subtickwidth", m.ticklen)

    def treat_background_layout(self, colors_set):
        """Treat the background layout of the axis.
        Parameters
        ----------
        colors_set : set
            Set of colors used in the figure, to be filled with the background color of the axis.
        """
        if self.layout.plot_bgcolor is not None:
            bg_color = convert_color(self.layout.plot_bgcolor)
            colors_set.add(bg_color[:3])
            opacity = bg_color[-1]
            options = f"fill={bg_color[0]}"
            if opacity != 1:
                options += f", opacity={opacity}"
            self.add_option("axis background/.style", f"{{{options}}}")

    def treat_bar_layout(self):
        """Treat the bar layout of the axis.
        This method handles the bar mode and adds the appropriate options to the axis.
        """
        if (barmode := self.layout.barmode) is not None:
            if barmode == "stack":
                self.add_option("ybar stacked", None)
