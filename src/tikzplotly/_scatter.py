from warnings import warn

from ._util import *
from ._tex import *
from ._color import *
from ._marker import marker_symbol_to_tex
from ._dash import *
from ._axis import Axis
from ._data import *
from numpy import round

def draw_scatter2d(scatter, axis: Axis):
    """Get code for a scatter trace.

    Parameters
    ----------
    scatter
        scatter trace from Plotly figure
    axis
        axis object previously created

    Returns
    -------
        string of tikz code for the scatter trace
    """
    code = ""

    # Create a new axis if necessary
    data_string = data_to_string(scatter.x, scatter.y)

    mode = scatter.mode
    marker = scatter.marker

    if data_type(scatter.x[0]) == "date":
        axis.add_option("date coordinates in", "x")
    if data_type(scatter.x[0]) == "month":
        scatter_x_str = "{" + ", ".join([x for x in scatter.x]) + "}"
        axis.add_option("xticklabels", scatter_x_str)
        data_string = data_string.replace("January", "1").replace("February", "2").replace("March", "3").replace("April", "4").replace("May", "5").replace("June", "6").replace("July", "7").replace("August", "8").replace("September", "9").replace("October", "10").replace("November", "11").replace("December", "12")
        data_string = data_string.replace("january", "1").replace("february", "2").replace("march", "3").replace("april", "4").replace("may", "5").replace("june", "6").replace("july", "7").replace("august", "8").replace("september", "9").replace("october", "10").replace("november", "11").replace("december", "12")

    if mode is None:
        # by default, plot markers and lines
        mode = "markers+lines"

    if mode == "markers":
        options = f"only marks, mark={marker_symbol_to_tex(marker.symbol)}"
        if scatter.marker.size is not None:
            options += f", mark size={marker.size}"
        if scatter.marker.color is not None:
            options += f", mark options={{solid, fill={convert_color(scatter.marker.color)[0]}, color={convert_color(scatter.marker.color)[0]}}}"
    elif mode == "lines":
        options = f"mark=none"
    elif "lines" in mode and "markers" in mode:
        options = f"mark={marker_symbol_to_tex(marker.symbol)}"
    else:
        warn(f"Mode {mode} is not supported yet.")
        options = ""

    if scatter.line.width is not None:
        options += f", line width={scatter.line.width}"
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

    code += tex_addplot(data_string, type="table", options=options)

    if scatter.text is not None:
        for x_data, y_data, text_data in zip(scatter.x, scatter.y, scatter.text):
            code += tex_add_text(x_data, y_data, str(text_data).rstrip('.0'))

    return code