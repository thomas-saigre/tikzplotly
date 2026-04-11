"""Shared helpers for Plotly trace to TikZ conversion."""

from warnings import warn

from ._color import convert_color
from ._marker import marker_symbol_to_tex
from ._utils import px_to_pt, option_dict_to_str


def configure_marker_options(mode, marker, options_dict, mark_option_dict, color_set):
    """Populate common marker options for scatter-like traces."""

    if marker.symbol is not None:
        symbol, symbol_options = marker_symbol_to_tex(marker.symbol)
        options_dict["mark"] = symbol
        if "lines" not in mode:
            options_dict["only marks"] = None
        if symbol_options is not None:
            mark_option_dict[symbol_options[0]] = symbol_options[1]
    elif "lines" not in mode:
        options_dict["only marks"] = None

    if marker.line is not None:
        if marker.line.color is not None:
            color = convert_color(marker.line.color)
            color_set.add(color[:3])
            mark_option_dict["draw"] = color[0]
        if marker.line.width is not None:
            mark_option_dict["line width"] = px_to_pt(marker.line.width)


def finalize_marker_options(mode, options_dict, mark_option_dict, trace_name):
    """Finalize common marker options for scatter-like traces."""

    if "markers" in mode:
        if mark_option_dict:
            mark_options = option_dict_to_str(mark_option_dict)
            options_dict["mark options"] = f"{{{mark_options}}}"
        return

    if mode == "lines":
        options_dict["mark"] = "none"
    else:
        warn(f"{trace_name} : Mode {mode} is not supported yet.")
