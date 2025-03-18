from ._axis import Axis
from ._utils import option_dict_to_str
from ._tex import tex_addplot
from ._color import convert_color
from warnings import warn

def draw_bar(data_name_macro, x_col_name, y_col_name, trace, axis: Axis, colors_set, row_sep="\\\\"):
    """
    Draw a bar chart (vertical or horizontal) referencing the data table
    created by DataContainer.addData(...).

    If trace.orientation == 'h', we do xbar (horizontal).
    Otherwise, we do ybar (vertical).

    Parameters
    ----------
    data_name_macro : str
        The LaTeX macro name for the data table (e.g. '\\data0').
    x_col_name : str
        The name of the column for x in the data table (e.g. 'data0').
    y_col_name : str
        The name of the column for y in the data table (e.g. 'y0').
    trace : plotly.graph_objs._bar.Bar
        The bar trace object containing data and style information.
    axis : Axis
        The axis object to which the bar chart will be added.
    colors_set : set
        A set to keep track of colors used in the plot (for \\definecolor).
    row_sep : str, optional
        The row separator for the data table in TikZ, by default "\\\\"
    """
    code = ""
    plot_options = {}
    type_options = {"row sep": row_sep}

    orientation = getattr(trace, "orientation", None)
    barmode = getattr(trace, "barmode", None)
    stack = " stacked" if axis.layout.barmode in ("stack", "relative") else ""

    if orientation == "h":
        plot_options["xbar"] = None
        axis.add_option("xbar" + stack, None)
        type_options["x"] = y_col_name
        type_options["y"] = x_col_name
    else:
        plot_options["ybar"] = None
        axis.add_option("ybar" + stack, None)
        type_options["x"] = x_col_name
        type_options["y"] = y_col_name

    # Handle marker style (color, opacity, line)
    if trace.marker is not None:
        m = trace.marker
        if m.color is not None:
            c = convert_color(m.color)
            colors_set.add(c[:3])
            plot_options["fill"] = c[0]
            plot_options["color"] = c[0]
        if m.opacity is not None:
            plot_options["opacity"] = m.opacity
        if m.line is not None:
            if m.line.width is not None:
                plot_options["line width"] = m.line.width
            if m.line.color is not None:
                linecol = convert_color(m.line.color)
                colors_set.add(linecol[:3])
                plot_options["draw"] = linecol[0]

    if trace.text is not None:
        warn("Text display for bar chart is not supported yet (ignored).")

    # Build the final addplot referencing the table
    code += tex_addplot(
        data_str=data_name_macro,
        type="table",
        options=option_dict_to_str(plot_options),
        type_options=option_dict_to_str(type_options)
    )

    return code
