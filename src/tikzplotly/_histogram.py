"""
Functions to convert Plotly histogram traces into TikZ/PGFPlots code.

Notes:
------
- Some advanced Plotly histogram features (such as normalization modes and text templates) are not fully supported and will issue warnings.
- Only the 'count' aggregation function is supported; other functions require pre-processing of data.
"""
import numbers
from warnings import warn
from ._axis import Axis
from ._utils import get_ticks_str, option_dict_to_str
from ._tex import tex_addplot
from ._color import convert_color

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
            data_str += f"{x}{row_sep} "

    else:
        flag_axis = True
        if axis.xticks is not None:
            flag_axis = False
            data_names = axis.xticks
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
    """
    Draw a histogram and return the TikZ code.

    Parameters
    ----------
    trace : plotly.graph_objs._histogram.Histogram
        The histogram trace object containing data and style information.
    axis : Axis
        The axis object to which the histogram will be added.
    colors_set : set
        A set to keep track of colors used in the plot.
    row_sep : str, optional
        The row separator for the data table in TikZ, by default "\\\\"

    Returns
    -------
    str
        A string containing the TikZ code for the histogram.

    Notes
    -----
    - The function currently does not support 'percent', 'probability', and 'density' normalization for histograms.
    - Text templates are not supported.
    - Only 'count' aggregation function is supported; other functions need pre-treatment of data.
    """

    code = ""

    plot_options = {"hist": None}
    type_options = {"row sep": row_sep, "y index": 0}
    hist_options = {}

    if trace.x is not None:
        data_str = formalize_data(trace.x, axis, row_sep=row_sep)
        axis.add_option("ybar", None)
    elif trace.y is not None:
        data_str = formalize_data(trace.y, axis, row_sep=row_sep)
        axis.add_option("ybar", None)
        axis.add_option("x filter/.expression", "rawy")
        axis.add_option("y filter/.expression", "rawx")
        hist_options["handler/.style"] = "{xbar interval}"



    if trace.nbinsx is not None:
        hist_options["bins"] = trace.nbinsx

    if trace.histnorm == "percent":
        warn(
            f"Sorry, I did not find an equivalent for histnorm='{trace.histnorm}' in TikZ. "
            "If you need this feature implemented, please open an issue, if possible with a MWE pgfplots code "
            "that would plot this :).\nFor now, the histogram will be plotted without normalization "
            "(as if histnorm='probability density')."
        )
        hist_options["density"] = None
    elif trace.histnorm == "probability":
        warn(
            f"Sorry, I did not find an equivalent for histnorm='{trace.histnorm}' in TikZ. "
            "If you need this feature implemented, please open an issue, if possible with a MWE pgfplots code that would plot this :).\n"
            "For now, the histogram will be plotted without normalization (as if histnorm='probability density')."
        )
        hist_options["density"] = None
    elif trace.histnorm == "density":
        warn(
            f"Sorry, I did not find an equivalent for histnorm='{trace.histnorm}' in TikZ. "
            "If you need this feature implemented, please open an issue, if possible with a MWE pgfplots code that would plot this :).\n"
            "For now, the histogram will be plotted without normalization (as if histnorm='probability density')."
        )
        hist_options["density"] = None
    elif trace.histnorm == "probability density":
        hist_options["density"] = None

    if trace.cumulative.enabled:
        hist_options["cumulative"] = None

    if bool(hist_options):
        plot_options["hist"] = f"{{{option_dict_to_str(hist_options)}}}"

    if trace.texttemplate is not None:
        warn("Text template is not supported yet.")

    if (m := trace.marker) is not None:

        if (c := m.color) is not None:
            colors_set.add(convert_color(c))
            plot_options["fill"] = convert_color(c)[0]
            plot_options["color"] = convert_color(c)[0]

        if m.opacity is not None:
            plot_options["opacity"] = m.opacity

    if (f := trace.histfunc) is not None:
        if f != "count":
            warn(
                "To the best of our knowledge, other aggregate function than 'count' are not supported in pgfplots. "
                "Please pre-treat your data to display what you want. Sorry for the inconvenience."
            )

    code += tex_addplot(data_str, plot_type = "table",
                        options = option_dict_to_str(plot_options), type_options=option_dict_to_str(type_options))


    return code
