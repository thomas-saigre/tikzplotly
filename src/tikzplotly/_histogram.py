from ._axis import Axis
from ._utils import get_ticks_str, option_dict_to_str
from ._tex import tex_addplot
import numbers

def formalize_data(data, axis:Axis, row_sep="\\\\"):
    """Formalize the data for the histogram trace.

    Parameters
    ----------
    data
        data from Plotly figure

    Returns
    -------
        formalized data
    """

    data_str = f"data{row_sep}\n"
    if isinstance(data[0], numbers.Number):
        for x in data:
            data_str += "{}{} ".format(x, row_sep)

    else:
        flag_axis = True
        if axis.xticks is not None:
            flag_axis = False
            data_names = axis.xticks
            print(data_names)
        else: data_names = []

        for x in data:
            if x not in data_names:
                data_names.append(x)
            data_str += f"{data_names.index(x)}{row_sep} "
        if flag_axis:
            ticks, ticklabels = get_ticks_str(data_names)
            axis.add_option("xtick", ticks)
            axis.add_option("xticklabels", ticklabels)


    return data_str

def draw_histogram(trace, axis: Axis, colors_set, row_sep="\\\\"):
    """Draw a heatmap, and return the tikz code.

    Parameters
    ----------
    TODO

    Returns
    -------
        string of tikz code for the scatter trace
    """

    code = ""
    axis.add_option("ybar", None)

    data_str = formalize_data(trace.x, axis, row_sep=row_sep)

    plot_options = {"hist": None}
    type_options = {"row sep": row_sep, "y index": 0}
    hist_options = {}

    if trace.nbinsx is not None:
        hist_options["bins"] = trace.nbinsx
        plot_options["hist"] = f"{{{option_dict_to_str(hist_options)}}}"

    code += tex_addplot(data_str, type="table",
                        options=option_dict_to_str(plot_options), type_options=option_dict_to_str(type_options))


    return code