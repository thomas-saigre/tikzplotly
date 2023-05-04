from ._util import *
from ._tex import *
from ._color import *

def draw_scatter2d(scatter):
    """Draw scatter plot."""
    code = ""

    # Create a new axis if necessary
    data_string = data_to_string(scatter.x, scatter.y)
    plot_color = convert_color(scatter.line.color)

    options = f"color={plot_color}, mark=*"

    code += tex_addplot(data_string, type="table", options=options)

    return code