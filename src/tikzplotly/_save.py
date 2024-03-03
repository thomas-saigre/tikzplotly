from pathlib import Path
from .__about__ import __version__
from ._tex import *
from ._scatter import draw_scatter2d
from ._axis import Axis
from ._color import *
from ._annotations import str_from_annotation
from ._dataContainer import DataContainer
from ._utils import sanitize_TeX_text
from warnings import warn
import re

def get_tikz_code(
        fig,
        tikz_options = None,
        axis_options = None,
        include_disclamer = True,
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

    if figure_layout.xaxis.showline == False:
        axis.add_option("axis x line", "none")
    if figure_layout.yaxis.showline == False:
        axis.add_option("axis y line", "none")

    if len(figure_data) == 0:
        warn("No data in figure.")

    for trace in figure_data:
        if trace.type == "scatter":
            data_name_macro, y_name = data_container.addData(trace.x, trace.y, trace.name)
            data_str.append( draw_scatter2d(data_name_macro, trace, y_name, axis, colors_set) )
            if trace.name and trace['showlegend'] != False:
                data_str.append( tex_add_legendentry(sanitize_TeX_text(trace.name)) )
            if trace.line.color is not None:
                colors_set.add(convert_color(trace.line.color)[:3])
            if trace.fillcolor is not None:
                colors_set.add(convert_color(trace.fillcolor)[:3])
        else:
            warn(f"Trace type {trace.type} is not supported yet.")

    annotation_str = str_from_annotation(figure_layout.annotations, axis, colors_set)

    code = """"""
    stack_env = []

    if include_disclamer:
        code += tex_comment(f"This file was created with tikzplotly version {__version__}.")

    code += data_container.exportData()
    code += "\n"

    code += tex_begin_environment("tikzpicture", stack_env, options=tikz_options)

    code += "\n"
    for color in colors_set:
        code += tex_add_color(color[0], color[1], color[2])
    code += "\n"

    code += axis.open_environment(stack_env)

    if figure_layout.legend.title.text is not None and figure_layout.showlegend:
        code += "\\addlegendimage{empty legend}\n"
        code += tex_add_legendentry(sanitize_TeX_text(fig.layout.legend.title.text), options="yshift=5pt")

    for trace_str in data_str:
        code += trace_str

    code += annotation_str

    if figure_layout.showlegend == False:
        code = re.sub(r"\\addlegendentry{.+}\n", "", code)

    code += tex_end_all_environment(stack_env)

    return code


def save(filepath: str | Path, *args, encoding: str | None = None, **kwargs):
    """Save a figure to a file or a stream.

    Parameters
    ----------
    filepath : str or Path
        A string containing a path to a filename, or a Path object.
    *args, **kwargs
        Additional arguments are passed to the backend.
    """
    code = get_tikz_code(*args, **kwargs)
    with open(filepath, "w") as fd:
        fd.write(code)