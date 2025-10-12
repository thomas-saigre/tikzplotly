"""
Provides functionality to convert Plotly 3D scatter traces into TikZ/PGFPlots code for LaTeX documents.
"""
from warnings import warn
import numpy as np
from ._color import convert_color
from ._marker import marker_symbol_to_tex
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

    # Markers only
    if mode == "markers":
        if marker.symbol is not None:
            symbol, symbol_options = marker_symbol_to_tex(marker.symbol)
            options_dict["mark"] = symbol
            options_dict["only marks"] = None
            if symbol_options is not None:
                mark_option_dict[symbol_options[0]] = symbol_options[1]
        else:
            options_dict["only marks"] = None

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

        if (line := marker.line) is not None:
            if line.color is not None:
                color_set.add(convert_color(line.color)[:3])
                mark_option_dict["draw"] = convert_color(line.color)[0]
            if line.width is not None:
                mark_option_dict["line width"] = px_to_pt(line.width)

        if (opacity := scatter.opacity) is not None:
            options_dict["opacity"] = opacity
        if (opacity := marker.opacity) is not None:
            mark_option_dict["opacity"] = opacity

        if mark_option_dict:
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
        warn(f"Scatter3d : Mode {mode} is not supported yet.")

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
