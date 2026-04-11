"""
Provides functionality to convert Plotly 3D scatter traces into TikZ/PGFPlots code for LaTeX documents.
"""

import numpy as np
from ._color import convert_color
from ._trace_utils import configure_marker_options, finalize_marker_options
from ._utils import px_to_pt, option_dict_to_str


def draw_scatter3d(data_name, scatter, color_set):
    """
    Get code for a scatter3d trace.

    Parameters
    ----------
    data_name
        name of the data imported in LaTeX
    scatter
        scatter trace from Plotly figure
    color_set
        set of colors used in the figure
    """
    code = ""

    mode = scatter.mode or "markers+lines"
    marker = scatter.marker

    options_dict = {}
    mark_option_dict = {}

    if "markers" in mode:
        configure_marker_options(mode, marker, options_dict, mark_option_dict, color_set)

        if marker.size is not None:
            size = marker.size
            if isinstance(size, (list, tuple)) or (hasattr(size, "shape") and hasattr(size, "__len__")):
                try:
                    size = float(np.mean(size))
                except (TypeError, ValueError):
                    size = float(size[0])
            options_dict["mark size"] = px_to_pt(size)

        if (c := marker.color) is not None:
            color_set.add(convert_color(c)[:3])
            mark_option_dict["solid"] = None
            mark_option_dict["fill"] = convert_color(c)[0]

        if (opacity := scatter.opacity) is not None:
            options_dict["opacity"] = opacity
        if (opacity := marker.opacity) is not None:
            mark_option_dict["opacity"] = opacity

    finalize_marker_options(mode, options_dict, mark_option_dict, "Scatter3d")

    if scatter.line is not None:
        if scatter.line.width is not None:
            options_dict["line width"] = px_to_pt(scatter.line.width)
        if scatter.line.color is not None:
            options_dict["color"] = convert_color(scatter.line.color)[0]
            color_set.add(convert_color(scatter.line.color)[:3])

    if scatter.showlegend is False:
        options_dict["forget plot"] = None

    options = option_dict_to_str(options_dict)
    if scatter.name:
        code += f"\n% {scatter.name}\n"

    code += "\\addplot3+ "
    if options is not None:
        code += f"[{options}] "
    code += f"table[x=x, y=y, z=z] {{\\{data_name}}};\n"

    return code
