"""
Provides functionality to convert Plotly 3D polar plots into TikZ/PGFPlots code for LaTeX documents.
"""
from warnings import warn
import numpy as np
from ._axis import Axis
from ._utils import option_dict_to_str
from ._tex import tex_addplot
from ._color import convert_color
from ._dataContainer import DataContainer

def get_polar_coord(trace, axis: Axis, data_container: DataContainer):
    """Get polar coordinates from the trace

    Parameters
    ----------
    trace
        polar trace from Plotly figure
    axis
        axis object previously created
    data_container
        Data table, created before

    Returns
    -------
        Tuple (data_name_macro, theta_col_name, r_col_name):
            - data_name_macro: name of the data in LaTeX
            - theta_col_name: name of the theta column
            - r_col_name: name of the r column
    """
    polar_layout = getattr(axis.layout, 'polar')
    if polar_layout:
        # Angular Axis
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
            angular_categoryorder = getattr(angularaxis, 'categoryorder', 'trace')
            angular_categoryarray = getattr(angularaxis, 'categoryarray', None)

        # Radial Axis
        radialaxis = getattr(polar_layout, 'radialaxis')
        if radialaxis:
            # Type
            radial_axis_type = getattr(radialaxis, 'type', None)
            if radial_axis_type is not None and radial_axis_type not in ['-', 'linear', 'category']:
                warn(f"Polar: Radial axis type {radial_axis_type} is not supported yet.")

            # Category
            radial_categoryorder = getattr(radialaxis, 'categoryorder', 'trace')
            radial_categoryarray = getattr(radialaxis, 'categoryarray', None)

            # Range
            sector = getattr(radialaxis, 'range')
            if sector and len(sector) > 1:
                axis.add_option("ymin", sector[0])
                axis.add_option("ymax", sector[1])

        # Sector
        sector = getattr(polar_layout, 'sector')
        if sector and len(sector) > 1:
            axis.add_option("xmin", sector[0])
            axis.add_option("xmax", sector[1])

    theta = [t if t is not None else '' for t in trace.theta]
    r = [val if val is not None else 'nan' for val in trace.r]

    thetaunit = getattr(trace, "thetaunit", "degrees")

    # Angular Axis
    if all(isinstance(t, str) for t in theta):
        if angular_categoryarray is not None:
            symbolic_theta = list(angular_categoryarray)
        else:
            symbolic_theta = list(dict.fromkeys(theta))

        if angular_categoryorder is not None:
            if angular_categoryorder == "category ascending":
                symbolic_theta = sorted(set(symbolic_theta))
            elif angular_categoryorder == "category descending":
                symbolic_theta = sorted(set(symbolic_theta), reverse=True)
            else:
                warn(f"Polar: Angular category order {angular_categoryorder} is not supported yet.")

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

    # Radial Axis
    if all(isinstance(v, str) for v in r):
        if radial_categoryarray is not None:
            symbolic_r = list(radial_categoryarray)
        else:
            symbolic_r = list(dict.fromkeys(r))
        if radial_categoryorder is not None:
            if radial_categoryorder == "category ascending":
                symbolic_r = sorted(set(symbolic_r))
            elif radial_categoryorder == "category descending":
                symbolic_r = sorted(set(symbolic_r), reverse=True)
            else:
                warn(f"Polar: Radial category order {radial_categoryorder} is not supported yet.")

        axis.add_option("symbolic y coords", "{" + ",".join(symbolic_r) + "}")
        axis.add_option("ytick", "data")

    data_name_macro, r_col_name = data_container.add_data(numeric_theta, r, trace.name)
    theta_col_name = data_container.data[-1].name

    return data_name_macro, theta_col_name, r_col_name

def draw_scatterpolar(data_name_macro, theta_col_name, r_col_name, trace, axis: Axis, colors_set):
    """
    Draw a scatterpolar plot using pgfplots polaraxis environment.

    Parameters
    ----------
    data_name_macro : str
        The LaTeX macro for the data table (e.g. '\\data0').
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

    Returns
    -------
    str
        LaTeX/pgfplots code for scatterpolar plot
    """

    plot_options = {}

    mode = trace.mode if trace.mode else "lines"

    if "markers" not in mode:
        plot_options["no markers"] = None
    elif "lines" not in mode:
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
                warn("Polar: Individual marker sizes in a trace are not supported yet.")
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
        plot_type="table",
        options=option_dict_to_str(plot_options),
        type_options=f"x={theta_col_name}, y={r_col_name}"
    )

    return code
