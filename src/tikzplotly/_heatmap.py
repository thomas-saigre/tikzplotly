"""
This module contains the code to draw a heatmap in TikZ using Plotly data.
"""
from warnings import warn
import io
import os
from copy import deepcopy
import numpy as np
from PIL import Image
from ._tex import tex_addplot, get_tikz_colorscale
from ._axis import Axis
from ._color import DEFAULT_COLORSCALE
from ._utils import get_ticks_str

def crop_image(img_data):
    """Crops an image to the smallest bounding box that contains all non-white pixels.

    Parameters
    ----------
    img_data
        A PIL Image object.

    Returns
    -------
        cropped_image : PIL Image
    """
    image_np = np.array(img_data)
    non_white_rows = np.any(image_np != [255, 255, 255, 255], axis=1)
    non_white_cols = np.any(image_np != [255, 255, 255, 255], axis=0)

    top, bottom = np.where(non_white_rows)[0][[0, -1]]
    left, right = np.where(non_white_cols)[0][[0, -1]]
    cropped_image = Image.fromarray(image_np[top:bottom+1, left:right+1])

    return cropped_image

def resize_image(img, nb_row, nb_col):
    """Resizes an image to a given number of rows and columns.

    Parameters
    ----------
    img
        A PIL Image object.
    nb_row
        The number of rows of the resized image.
    nb_col
        The number of columns of the resized image.

    Returns
    -------
        resized_image : PIL Image
    """
    resized_image = Image.new("RGBA", size = (nb_col, nb_row))
    block_size = (img.width // nb_col, img.height // nb_row)

    if block_size[0] != img.width / nb_col or block_size[1] != img.height / nb_row:
        warn("png image has not been reduced, see https://github.com/thomas-saigre/tikzplotly/issues/6#issuecomment-2106180586")
        return img

    for i in range(nb_row):
        for j in range(nb_col):
            color = img.getpixel((j * block_size[0], i * block_size[1]))
            resized_image.putpixel((j, i), color)

    return resized_image

def draw_heatmap(data, fig, img_name, axis: Axis):
    """Draw a heatmap, and return the tikz code.

    Parameters
    ----------
    data
        data array to be plotted
    fig
        whole plotly figure
    img_name
        name of the image file to be created
    axis
        axis object previously created

    Returns
    -------
        string of tikz code for the scatter trace
    """

    code = ""

    figure_data = np.array(data.z)

    # We create a new figure with only the data, and export it as a png
    fig_copy = deepcopy(fig)
    fig_copy.update_layout(coloraxis_showscale=False, coloraxis_colorbar=None, xaxis_visible=False, yaxis_visible=False)
    try:
        fig_copy.update_traces(showscale=False)
    except ValueError as _:
        pass

    if data.texttemplate is not None:
        warn("Text template is not supported yet.")
        fig_copy.update_traces(texttemplate=None)
    fig_copy.update_layout(title=None)

    img_bytes = fig_copy.to_image(format="png")  # The image created by plotly keeps places around the heatmap
    cropped_image = crop_image(Image.open(io.BytesIO(img_bytes)))   # so we crop all the white around the figure
    resized_image = resize_image(cropped_image, *figure_data.shape)  # and we resize it so each square is a 1px x 1px square

    os.makedirs(os.path.dirname(img_name), exist_ok=True) # Make sure the directory exists
    resized_image.save(img_name)


    xmin = -0.5
    xmax = -0.5 + figure_data.shape[1]
    ymin = -0.5 + figure_data.shape[0]
    ymax = -0.5         # NB : the axis is reversed


    if not fig.layout.coloraxis.showscale is False:   # If the value is True or None
        axis.add_option("colorbar", None)

    if (x := data.x) is not None:
        xtick, xticklabels = get_ticks_str(x, fig.layout.xaxis.nticks)
        axis.add_option("xtick", xtick)
        axis.add_option("xticklabels", xticklabels)

    if (y := data.y) is not None:
        ytick, yticklabels = get_ticks_str(y, fig.layout.yaxis.nticks)
        axis.add_option("ytick", ytick)
        axis.add_option("yticklabels", yticklabels)

    if (colorscale := data.colorscale) is not None:
        axis.add_option("colormap", get_tikz_colorscale(colorscale))
    elif (colorscale := fig.layout.coloraxis.colorscale) is not None:
        axis.add_option("colormap", get_tikz_colorscale(colorscale))
    elif data.showscale is not False:
        warn("No colorscale found, using default")
        axis.add_option("colormap", get_tikz_colorscale(DEFAULT_COLORSCALE))

    tmp = np.where(figure_data == None, np.nan, figure_data)
    axis.add_option("point meta max", np.nanmax(tmp))
    axis.add_option("point meta min", np.nanmin(tmp))
    axis.add_option("xmin", xmin)
    axis.add_option("xmax", xmax)
    axis.add_option("ymin", ymax)
    axis.add_option("ymax", ymin)
    axis.add_option("tick align", "outside")
    axis.add_option("tick pos", "left")

    code += tex_addplot(img_name, plot_type="graphics",
                        type_options=f"includegraphics cmd=\\pgfimage,xmin={xmin}, xmax={xmax}, ymin={ymin}, ymax={ymax}")

    return code
