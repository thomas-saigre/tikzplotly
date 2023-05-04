from warnings import warn

from ._util import *
from ._tex import *
from ._color import *
from ._marker import marker_symbol_to_tex

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
    elif mode == "lines+markers" or mode == "markers+lines":
        options = f"mark={marker_symbol_to_tex(marker.symbol)}"
    else:
        warn(f"Mode {mode} is not supported yet.")

    if scatter.line.color is not None:
        options += f", color={convert_color(scatter.line.color)[0]}"

    code += tex_addplot(data_string, type="table", options=options)

    return code