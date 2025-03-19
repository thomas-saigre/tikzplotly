from ._axis import Axis
from ._utils import option_dict_to_str
from ._tex import tex_addplot
from ._color import convert_color
from ._dataContainer import DataContainer
from warnings import warn

def get_polar_coord(trace, axis: Axis, data_container: DataContainer):
    # rotation
    polar_layout = getattr(axis.layout, 'polar', None)
    if polar_layout:
        angularaxis = getattr(polar_layout, 'angularaxis', None)
        if angularaxis:
            rotation = getattr(angularaxis, 'rotation', None)
            if rotation is not None and rotation != 0:
                axis.add_option("rotate", rotation)
                axis.add_option("xticklabel style", f"{{anchor=\\tick-{rotation}}}")

    theta = [t if t is not None else '' for t in trace.theta]
    r = [val if val is not None else 'nan' for val in trace.r]

    if all(isinstance(t, str) for t in theta):
        symbolic_theta = list(dict.fromkeys(theta))
        numeric_theta = [symbolic_theta.index(t) * (360 / len(symbolic_theta)) for t in theta]

        axis.environment = "polaraxis"
        axis.add_option("xtick", f"{{{','.join(str(i*(360/len(symbolic_theta))) for i in range(len(symbolic_theta)))}}}")
        axis.add_option("xticklabels", "{" + ",".join(symbolic_theta) + "}")
    else:
        symbolic_theta = None
        numeric_theta = theta

    data_name_macro, r_col_name = data_container.addData(numeric_theta, r, trace.name)
    theta_col_name = data_container.data[-1].name

    return data_name_macro, theta_col_name, r_col_name


def draw_scatterpolar(data_name_macro, theta_col_name, r_col_name, trace, axis: Axis, colors_set, row_sep="\\"):
    """
    Draw a scatterpolar plot using pgfplots polaraxis environment.

    Parameters
    ----------
    data_name_macro : str
        The LaTeX macro for the data table (e.g. '\data0').
    theta_col_name : str
        Name of the column for theta values (angles).
    r_col_name : str
        The name of the column for radial values in the data table.
    trace : plotly.graph_objs._scatterpolar.Scatterpolar
        Plotly Scatterpolar trace
    axis : Axis
        Axis object (to add axis-level options)
    colors_set : set
        Set of colors defined
    row_sep : str, optional
        Row separator in LaTeX, default "\\"

    Returns
    -------
    str
        LaTeX/pgfplots code for scatterpolar plot
    """

    plot_options = {}
    mark_options = {}

    mode = trace.mode if trace.mode else "lines"

    if "markers" in mode:
        plot_options["only marks"] = None

    if "lines" in mode:
        plot_options["no markers"] = None

    # Marker style
    if trace.marker is not None:
        marker = trace.marker
        if marker.color is not None:
            col = convert_color(marker.color)
            plot_options["color"] = col[0]
            mark_opts = {"solid": None, "fill": col[0]}
            colors_set.add(col[:3])
            # plot_options["mark options"] = "{" + option_dict_to_str(mark_option_dict=mark_opts) + "}"

    # Line style
    if trace.line is not None:
        line = trace.line
        if line.color is not None:
            color = convert_color(line.color)
            colors_set.add(color[:3])
            plot_options["color"] = color[0]
        if line.width is not None:
            plot_options["line width"] = line.width

     # Fill
    if trace.fill is not None:
        if trace.fill == 'toself':
            plot_options["fill"] = ".!50"
            plot_options["opacity"] = 0.6

    # axis options for polar plot
    axis.environment = "polaraxis"

    # Construct TikZ addplot
    code = tex_addplot(
        data_str=data_name_macro,
        type="table",
        options=option_dict_to_str(plot_options),
        type_options=f"x={theta_col_name}, y={r_col_name}"
    )

    return code
