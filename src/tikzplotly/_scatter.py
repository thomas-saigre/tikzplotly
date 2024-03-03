from warnings import warn

from ._tex import *
from ._color import *
from ._marker import marker_symbol_to_tex
from ._dash import *
from ._axis import Axis
from ._data import *
from ._utils import px_to_pt, option_dict_to_str, sanitize_text
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

    options_dict = {}
    mark_option_dict = {}

    if mode == "markers":
        if marker.symbol is not None:
            symbol, symbol_options = marker_symbol_to_tex(marker.symbol)
            options_dict["mark"] = symbol
            options_dict["only marks"] = None
            if symbol_options is not None:
                mark_option_dict[symbol_options[0]] = symbol_options[1]
        else:
            options_dict["only marks"] = None

        mark_options = ""
        if scatter.marker.size is not None:
            options_dict["mark size"] = px_to_pt(marker.size)

        if scatter.marker.color is not None:
            color_set.add(convert_color(scatter.marker.color)[:3])
            mark_option_dict["solid"] = None
            mark_option_dict["fill"] = convert_color(scatter.marker.color)[0]

        if (line:=scatter.marker.line) is not None:
            if line.color is not None:
                color_set.add(convert_color(line.color)[:3])
                mark_option_dict["draw"] = convert_color(line.color)[0]
            if line.width is not None:
                mark_option_dict["line width"] = px_to_pt(line.width)

        if (angle:=scatter.marker.angle) is not None:
            mark_option_dict["rotate"] = -angle

        if (opacity:=scatter.opacity) is not None:
            options_dict["opacity"] = round(opacity, 2)
        if (opacity:=scatter.marker.opacity) is not None:
            mark_option_dict["opacity"] = round(opacity, 2)

        if mark_option_dict != {}:
            mark_options = option_dict_to_str(mark_option_dict)
            options_dict["mark options"] = f"{{{mark_options}}}"

    elif mode == "lines":
        options_dict["mark"] = "none"

    elif "lines" in mode and "markers" in mode:
        if marker.symbol is not None:
            symbol, symbol_options = marker_symbol_to_tex(marker.symbol)
            options_dict["mark"] = symbol
            if symbol_options is not None:
                mark_option_dict[symbol_options[0]] = symbol_options[1]

    else:
        warn(f"Scatter : Mode {mode} is not supported yet.")

    if scatter.line.width is not None:
        options_dict["line width"] = px_to_pt(scatter.line.width)
    if scatter.line.dash is not None:
        options_dict[DASH_PATTERN[scatter.line.dash]] = None
    if scatter.connectgaps in [False, None] and None in scatter.x:
        options_dict["unbounded coords"] = "jump"


    if scatter.line.color is not None:
        options_dict["color"] = convert_color(scatter.line.color)[0]
        if "mark" in mode:
            mark_option_dict["draw"] = convert_color(scatter.line.color)[0]
            mark_option_dict["solid"] = None

    if scatter.fill is not None:
        fill_color = convert_color(scatter.fillcolor)
        opacity = fill_color[-1]
        options_dict["fill"] = fill_color[0]
        if opacity < 1:
            options_dict["fill opacity"] = opacity

    if scatter.showlegend is False:
        options_dict["forget plot"] = None

    options = option_dict_to_str(options_dict)
    code += tex_addplot(data_name, type="table", options=options, type_options=f"y={sanitize_text(y_name)}")

    if scatter.text is not None:
        for x_data, y_data, text_data in zip(scatter.x, scatter.y, scatter.text):
            code += tex_add_text(x_data, y_data, str(text_data).rstrip('.0'))

    return code