from warnings import warn

from ._tex import *
from ._color import *
from ._marker import marker_symbol_to_tex
from ._dash import *
from ._axis import Axis
from ._data import *
from ._utils import px_to_pt
from numpy import round

def draw_scatter2d(data_name, scatter, y_name, axis: Axis, color_set):
    """Get code for a scatter trace.

    Parameters
    ----------
    data_name
        name of the data imported in LaTeX
    scatter
        scatter trace from Plotly figure
    y_name
        name of the y data imported in LaTeX
    axis
        axis object previously created
    color_set
        set of colors used in the figure

    Returns
    -------
        string of tikz code for the scatter trace
    """
    code = ""

    mode = scatter.mode
    marker = scatter.marker

    if data_type(scatter.x[0]) == "date":
        axis.add_option("date coordinates in", "x")
    if data_type(scatter.x[0]) == "month":
        scatter_x_str = "{" + ", ".join([x for x in scatter.x]) + "}"
        axis.add_option("xticklabels", scatter_x_str)

    if mode is None:
        # by default, plot markers and lines
        mode = "markers+lines"

    if mode == "markers":
        if marker.symbol is not None:
            options = f"only marks, mark={marker_symbol_to_tex(marker.symbol)}"
        else:
            options = f"only marks"
        mark_options = ""
        if scatter.marker.size is not None:
            options += f", mark size={px_to_pt(marker.size)}"
        if scatter.marker.color is not None:
            color_set.add(convert_color(scatter.marker.color)[:3])
            mark_options += f"solid, fill={convert_color(scatter.marker.color)[0]}"
        if (line:=scatter.marker.line) is not None:
            if line.color is not None:
                color_set.add(convert_color(line.color)[:3])
                mark_options += f", draw={convert_color(line.color)[0]}"
            if line.width is not None:
                mark_options += f", line width={px_to_pt(line.width)}"
        if (opacity:=scatter.opacity) is not None:
            options += f", opacity={round(opacity, 2)}"
        if (opacity:=scatter.marker.opacity) is not None:
            mark_options += f", opacity={round(opacity, 2)}"

        if mark_options != "":
            options += f", mark options={{{mark_options}}}"

    elif mode == "lines":
        options = f"mark=none"
    elif "lines" in mode and "markers" in mode and marker.symbol is not None:
        options = f"mark={marker_symbol_to_tex(marker.symbol)}"
    else:
        warn(f"Mode {mode} is not supported yet.")
        options = ""

    if scatter.line.width is not None:
        options += f", line width={px_to_pt(scatter.line.width)}"
    if scatter.line.dash is not None:
        options += ", " + DASH_PATTERN[scatter.line.dash]
    if scatter.connectgaps in [False, None] and None in scatter.x:
        options += ", unbounded coords=jump"


    if scatter.line.color is not None:
        options += f", color={convert_color(scatter.line.color)[0]}"
        if "mark" in mode:
            options += f", mark options={{solid, draw={convert_color(scatter.line.color)[0]}}}"

    if scatter.fill is not None:
        fill_color = convert_color(scatter.fillcolor)
        opacity = fill_color[-1]
        options += f", fill={fill_color[0]}"
        if opacity < 1:
            options += f", opacity={opacity}"

    if scatter.showlegend is False:
        options += ", forget plot"

    code += tex_addplot(data_name, type="table", options=options, type_options=f"y={y_name}")

    if scatter.text is not None:
        for x_data, y_data, text_data in zip(scatter.x, scatter.y, scatter.text):
            code += tex_add_text(x_data, y_data, str(text_data).rstrip('.0'))

    return code