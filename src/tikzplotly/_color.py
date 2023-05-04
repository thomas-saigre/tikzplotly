from warnings import warn
import hashlib

def convert_color(color):
    """Convert a color from html to tikz format."""
    if color[0] == "#":
        return color[1:], "HTML", color[1:]
    elif color[0:3] == "rgb":
        color = color[4:-1].replace("[", "{").replace("]", "}")
        return hashlib.sha1(color.encode('UTF-8')).hexdigest()[:10], "RGB", color
    else:
        warn(f"Color {color} type is not supported yet. Returning the same color.")
        return color