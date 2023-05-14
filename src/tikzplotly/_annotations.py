from ._axis import Axis
from ._tex import *
from ._color import convert_color

anchor_dict = {
    "left": "west",
    "right": "east",
    "top": "north",
    "bottom": "south",
    "middle": "",
    "center": "",
    None: ""
}


def get_coordinates(x, y, x_ref, y_ref):
    """Computed the coordinates of an annotation. The coordinates can be relative to the axis or absolute.
    If only one coordinate is relative and the other is absolute, the relative coordinate is converted to absolute,
    using the axis limits : x_return = xmin + x * (xmax - xmin) (idem for y)

    Parameters
    ----------
    x
        input x coordinate
    y
        input y coordinate
    x_ref
        reference of the x coordinate
    y_ref
        reference of the y coordinate

    Returns
    -------
        x coordinate, y coordinate, relative (boolean indicating if the coordinates are relative to the axis)
    """
    if x_ref == "paper" and y_ref == "paper":
        return x, y, True
    elif x_ref == "paper" and y_ref != "paper":
        x_text = "\\pgfkeysvalueof{/pgfplots/xmin} + " + str(x) + "*\\pgfkeysvalueof{/pgfplots/xmax}-" + str(x) + "*\\pgfkeysvalueof{/pgfplots/xmin}"
        return x_text, y, False
    elif x_ref != "paper" and y_ref == "paper":
        y_text = "\\pgfkeysvalueof{/pgfplots/ymin} + " + str(y) + "*\\pgfkeysvalueof{/pgfplots/ymax}-" + str(y) + "*\\pgfkeysvalueof{/pgfplots/ymin}"
        return x, y_text, False
    else:
        return x, y, False

def str_from_annotation(annotation_list, axis: Axis, colors_set):
    """Create a string of LaTeX code for the annotations of a figure.

    Parameters
    ----------
    annotation_list
        list of annotations from Plotly figure, in fig.layout.annotations
    axis
        Axis object previously created
    colors_set
        colors used in the figure, to be filled with the colors of the annotations

    Returns
    -------
        string of LaTeX code for the annotations
    """
    annotation_str = ""
    if len(annotation_list) > 0:
        axis.add_option("clip", "false")
    for annotation in annotation_list:
        x_anchor = anchor_dict[annotation.xanchor]
        y_anchor = anchor_dict[annotation.yanchor]
        x_ref = annotation.xref
        y_ref = annotation.yref
        x_coordinate, y_coordinate, relative = get_coordinates(annotation.x, annotation.y, x_ref, y_ref)
        anchor_option = f"{y_anchor} {x_anchor}".rstrip()

        if anchor_option != "":
            anchor_option = f"anchor={anchor_option}"
        node_options = anchor_option
        if annotation.font.color is not None:
            color_converted = convert_color(annotation.font.color)
            colors_set.add(color_converted[:3])
            node_options += f", color={color_converted[0]}"
        annotation_str += tex_add_text(x_coordinate, y_coordinate, annotation.text, options=node_options, relative=relative)
    return annotation_str
