from ._axis import Axis
from ._utils import option_dict_to_str
from ._tex import tex_addplot
from ._color import convert_color
from ._dataContainer import DataContainer
from warnings import warn
import numpy as np

def get_polar_coord(trace, axis: Axis, data_container: DataContainer):
    polar_layout = getattr(axis.layout, 'polar')
    if polar_layout:
        angularaxis = getattr(polar_layout, 'angularaxis')
        if angularaxis:
            # Rotation
            rotation = getattr(angularaxis, 'rotation')
            if rotation is None:
                rotation = 0
            else:
                axis.add_option("rotate", rotation)
                axis.add_option("xticklabel style", f"{{anchor=\\tick+{rotation}+180}}")
                axis.add_option("yticklabel style", f"{{anchor=\\tick-{rotation}-90}}")

            # Direction
            direction = getattr(angularaxis, "direction", "counterclockwise")
            if direction == "clockwise":
                axis.add_option("y dir", "reverse")
                axis.add_option("xticklabel style", f"{{anchor={rotation}-\\tick+180}}")
            
            # Period
            period = getattr(angularaxis, "period")

            # Category
            categoryarray = getattr(angularaxis, 'categoryarray')

    theta = [t if t is not None else '' for t in trace.theta]
    r = [val if val is not None else 'nan' for val in trace.r]

    thetaunit = getattr(trace, "thetaunit", "degrees")

    if all(isinstance(t, str) for t in theta):
        if categoryarray is not None:
            symbolic_theta = list(categoryarray)
        else:
            symbolic_theta = list(dict.fromkeys(theta))

        n_theta = len(symbolic_theta)
        if period is not None:
            n_theta = max(period, n_theta)

        numeric_theta = [symbolic_theta.index(t) * (360 / n_theta) for t in theta]

        axis.environment = "polaraxis"
        axis.add_option("xtick", f"{{{','.join(str( i * (360 / n_theta)) for i in range(n_theta))}}}")
        axis.add_option("xticklabels", "{" + ",".join(symbolic_theta) + "}")
    else:
        symbolic_theta = None        
        if thetaunit == "radians":
            numeric_theta = [t * (180 / 3.141592653589793) for t in theta]
        else:
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

    if not "markers" in mode:
        plot_options["no markers"] = None
    elif not "lines" in mode:
        plot_options["only marks"] = None

    # Marker style
    if trace.marker is not None:
        marker = trace.marker
        if marker.color is not None:
            col = convert_color(marker.color)
            plot_options["color"] = col[0]
            mark_opts = {"solid": None, "fill": col[0]}
            colors_set.add(col[:3])
            plot_options["mark options"] = "{" + option_dict_to_str(mark_opts) + "}"
        if marker.size is not None:
            if isinstance(marker.size, np.ndarray):
                warn(f"Individual marker sizes in a trace are not supported yet.")
            else:
                plot_options["mark size"] = marker.size/4

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

    # Axis options for polar plot
    axis.environment = "polaraxis"

    # Construct TikZ addplot
    code = tex_addplot(
        data_str=data_name_macro,
        type="table",
        options=option_dict_to_str(plot_options),
        type_options=f"x={theta_col_name}, y={r_col_name}"
    )

    return code
