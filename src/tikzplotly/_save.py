from pathlib import Path
from .__about__ import __version__
from ._tex import *
from ._scatter import draw_scatter2d
from ._heatmap import draw_heatmap
from ._histogram import draw_histogram
from ._bar import draw_bar
from ._polar import get_polar_coord, draw_scatterpolar
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
            else:
                if trace.x is None:
                    trace.x = list(range(len(trace.y)))
                if trace.y is None:
                    trace.y = list(range(len(trace.x)))

            data_name_macro, y_name = data_container.addData(trace.x, trace.y, trace.name)
            
            # If x is textual => symbolic x coords
            if all(isinstance(v, str) for v in trace.x):
                axis.add_option("symbolic x coords", "{" + ",".join(trace.x) + "}")
                axis.add_option("xtick", "data")

            # If y is textual => symbolic y coords
            if all(isinstance(v, str) for v in trace.y):
                axis.add_option("symbolic y coords", "{" + ",".join(trace.y) + "}")
                axis.add_option("ytick", "data")

            data_str.append( draw_scatter2d(data_name_macro, trace, y_name, axis, colors_set) )
            if trace.name and trace['showlegend'] != False:
                data_str.append( tex_add_legendentry(sanitize_TeX_text(trace.name)) )
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
            if trace.name and trace['showlegend'] != False:
                data_str.append( tex_add_legendentry(sanitize_TeX_text(trace.name)) )

        elif trace.type == "bar":
            orientation = getattr(trace, "orientation", None)
            if orientation == "h":
                cat_list = trace.y
                val_list = trace.x
            else:
                cat_list = trace.x
                val_list = trace.y

            # If x or y is empty
            if trace.x is None and trace.y is None:
                warn("Adding empty bar trace.")
                data_str.append("\\addplot coordinates {};\n")
                continue
            else:
                if trace.x is None:
                    trace.x = list(range(len(trace.y)))
                if trace.y is None:
                    trace.y = list(range(len(trace.x)))

            data_name_macro, val_col_name = data_container.addData(cat_list, val_list, trace.name)
            x_col_name = data_container.data[-1].name  # 'data0

            if all(isinstance(value, str) for value in cat_list):
                if orientation == "h":
                    # Categories go on the y-axis
                    axis.add_option("symbolic y coords", sanitize_TeX_text(",".join(cat_list)))
                    axis.add_option("ytick", "data")
                else:
                    # Categories go on the x-axis
                    axis.add_option("symbolic x coords", sanitize_TeX_text(",".join(cat_list)))
                    axis.add_option("xtick", "data")

            # Build the bar code
            bar_code = draw_bar(data_name_macro, x_col_name, val_col_name, trace, axis, colors_set)
            data_str.append(bar_code)

            if trace.name and trace['showlegend'] != False:
                data_str.append(tex_add_legendentry(sanitize_TeX_text(trace.name)))

        elif trace.type == "scatterpolar" or trace.type == "scatterpolargl":
            data_name_macro, theta_col_name, r_col_name = get_polar_coord(trace, axis, data_container)
           
            if all(isinstance(v, str) for v in trace.r):
                unique_r_vals = list(dict.fromkeys(trace.r))
                axis.add_option("symbolic y coords", "{" + ",".join(unique_r_vals) + "}")
                axis.add_option("ytick", "data")
           
            polar_code = draw_scatterpolar(data_name_macro, theta_col_name, r_col_name, trace, axis, colors_set)
            data_str.append(polar_code)

            if trace.name and trace['showlegend'] != False:
                data_str.append(tex_add_legendentry(sanitize_TeX_text(trace.name)))

        else:
            warn(f"Trace type {trace.type} is not supported yet.")

    annotation_str = str_from_annotation(figure_layout.annotations, axis, colors_set)

    code = """"""
    stack_env = []

    if include_disclamer:
        code += tex_comment(f"This file was created with tikzplotly version {__version__}.")

    if len(data_container.data) > 0:
        code += data_container.exportData()
        code += "\n"

    code += tex_begin_environment("tikzpicture", stack_env, options=tikz_options)

    if bool(colors_set): code += "\n"
    color_list = list(colors_set)
    color_list.sort()
    for color in color_list:
        code += tex_add_color(color[0], color[1], color[2])
    if bool(colors_set): code += "\n"

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
    with open(filepath, "w") as fd:
        fd.write(code)
