# -*- coding: utf-8 -*-
"""
Provides functionality to convert Plotly figures into TikZ/PGFPlots code for LaTeX documents.
It includes utilities to process different Plotly trace types (scatter, heatmap, histogram), handle axis and color
configuration, manage data containers, and export the resulting TikZ code to a file or stream.
"""

from pathlib import Path
from warnings import warn
import re
from .__about__ import __version__
from ._tex import tex_add_legendentry, tex_comment, tex_begin_environment, tex_add_color, tex_end_all_environment
from ._scatter import draw_scatter2d
from ._heatmap import draw_heatmap
from ._histogram import draw_histogram
from ._axis import Axis
from ._color import convert_color
from ._annotations import str_from_annotation
from ._dataContainer import DataContainer
from ._utils import sanitize_tex_text

def get_tikz_code(
        fig,
        tikz_options = None,
        axis_options = None,
        include_disclamer = True,
        img_name = "heatmap.png",
    ):
    """Get the tikz code of a figure.

    Parameters
    ----------
    fig
        Plotly figure
    tikz_options, optional
        options given to the tikzpicture environment, by default None
    axis_options, optional
        options given to the axis environment, by default None
    include_disclamer, optional
        include a disclamer in the code, by default True
    img_name, optional
        name of the PNG file for heatmap, by default "heatmap.png"

    Returns
    -------
        string of tikz code
    """
    figure_data = fig.data
    figure_layout = fig.layout
    colors_set = set()
    data_str = []

    axis = Axis(figure_layout, colors_set, axis_options=axis_options)
    data_container = DataContainer()

    if len(figure_data) == 0:
        warn("No data in figure.")

    for trace in figure_data:

        if trace.type == "scatter":
            # Handle the case where x or y is empty
            if trace.x is None and trace.y is None:
                warn("Adding empty trace.")
                data_str.append( "\\addplot coordinates {};\n" )
                continue

            if trace.x is None:
                trace.x = list(range(len(trace.y)))
            if trace.y is None:
                trace.y = list(range(len(trace.x)))

            data_name_macro, y_name = data_container.add_data(trace.x, trace.y, trace.name)
            data_str.append( draw_scatter2d(data_name_macro, trace, y_name, axis, colors_set) )
            if trace.name and trace['showlegend'] is not False:
                data_str.append( tex_add_legendentry(sanitize_tex_text(trace.name)) )
            if trace.line.color is not None:
                colors_set.add(convert_color(trace.line.color)[:3])
            if trace.fillcolor is not None:
                colors_set.add(convert_color(trace.fillcolor)[:3])

        elif trace.type == "heatmap":
            # Handle the case where x, y or z is empty
            if trace.z is None:
                warn("Adding empty trace.")
                data_str.append( "\\addplot coordinates {};\n" )
                continue
            data_str.append( draw_heatmap(trace, fig, img_name, axis) )

        elif trace.type == "histogram":

            data_str.append( draw_histogram(trace, axis, colors_set) )
            if trace.name and trace['showlegend'] is not False:
                data_str.append( tex_add_legendentry(sanitize_tex_text(trace.name)) )

        else:
            warn(f"Trace type {trace.type} is not supported yet.")

    annotation_str = str_from_annotation(figure_layout.annotations, axis, colors_set)

    code = """"""
    stack_env = []

    if include_disclamer:
        code += tex_comment(f"This file was created with tikzplotly version {__version__}.")

    if len(data_container.data) > 0:
        code += data_container.export_data()
        code += "\n"

    code += tex_begin_environment("tikzpicture", stack_env, options=tikz_options)

    if bool(colors_set):
        code += "\n"
    color_list = list(colors_set)
    color_list.sort()
    for color in color_list:
        code += tex_add_color(color[0], color[1], color[2])
    if bool(colors_set):
        code += "\n"

    code += axis.open_environment(stack_env)

    if figure_layout.legend.title.text is not None and figure_layout.showlegend:
        code += "\\addlegendimage{empty legend}\n"
        code += tex_add_legendentry(sanitize_tex_text(fig.layout.legend.title.text), options="yshift=5pt")

    for trace_str in data_str:
        code += trace_str

    code += annotation_str

    if figure_layout.showlegend is False:
        code = re.sub(r"\\addlegendentry{.+}\n", "", code)

    code += tex_end_all_environment(stack_env)

    return code


def save(filepath, *args, **kwargs):
    """Save a figure to a file or a stream.

    Parameters
    ----------
    filepath : str or Path
        A string containing a path to a filename, or a Path object.
    *args, **kwargs
        Additional arguments are passed to the backend.
    """
    code = get_tikz_code(*args, **kwargs)
    directory = Path(filepath).parent
    if not directory.exists():
        directory.mkdir(parents=True)
    with open(filepath, "w", encoding='utf-8') as fd:
        fd.write(code)
