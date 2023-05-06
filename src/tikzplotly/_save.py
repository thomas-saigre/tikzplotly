from pathlib import Path
from .__about__ import __version__
from ._tex import *
from ._scatter import draw_scatter2d
from ._axis import Axis
from ._color import *
from warnings import warn

def get_tikz_code(
        fig,
        tikz_options = None,
        include_disclamer = True,
    ):

    figure_data = fig.data

    colors_set = set()
    data_str = []

    if len(figure_data) == 0:
        warn("No data in figure.")

    for trace in figure_data:
        if trace.type == "scatter":
            data_str.append( draw_scatter2d(trace) )
            if 'name' in trace and trace['showlegend'] != False:
                data_str.append( tex_add_legendentry(trace.name) )
            if trace.line.color is not None:
                colors_set.add(convert_color(trace.line.color))
        else:
            warn(f"Trace type {trace.type} is not supported yet.")


    code = """"""
    stack_env = []

    if include_disclamer:
        code += tex_comment(f"This file was created with tikzplotly version {__version__}.")

    
    code += tex_begin_environment("tikzpicture", stack_env, options=tikz_options)

    code += "\n"
    for color in colors_set:
        code += tex_add_color(color[0], color[1], color[2])
    code += "\n"

    axis = Axis(fig.layout)

    code += tex_begin_environment("axis", stack_env, options=axis.get_options())

    if fig.layout.legend.title.text is not None:
        code += "\\addlegendimage{empty legend}\n"
        code += tex_add_legendentry(fig.layout.legend.title.text, options="yshift=5pt")

    for trace_str in data_str:
        code += trace_str

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