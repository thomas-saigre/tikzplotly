from warnings import warn

from ._util import *
from ._tex import *
from ._color import *
from ._marker import marker_symbol_to_tex
from numpy import round

def draw_scatter2d(scatter):
    """Draw scatter plot."""
    code = ""

    # Create a new axis if necessary
    data_string = data_to_string(scatter.x, scatter.y)

    mode = scatter.mode
    marker = scatter.marker

    if mode == "markers":
        options = f"only marks, mark={marker_symbol_to_tex(marker.symbol)}"
    elif mode == "lines":
        options = f"mark=none"
    elif "lines" in mode and "markers" in mode:
        options = f"mark={marker_symbol_to_tex(marker.symbol)}"
    else:
        warn(f"Mode {mode} is not supported yet.")
        options = ""


    if scatter.line.color is not None:
        options += f", color={convert_color(scatter.line.color)[0]}"

    code += tex_addplot(data_string, type="table", options=options)

    if scatter.text is not None:
        for x_data, y_data, text_data in zip(scatter.x, scatter.y, scatter.text):
            code += tex_add_text(x_data, y_data, str(text_data).rstrip('.0'))
        

    return code