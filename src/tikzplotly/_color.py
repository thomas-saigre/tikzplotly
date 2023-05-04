from warnings import warn

def convert_color(color):
    """Convert a color from html to tikz format."""
    if color[0] == "#":
        return color[1:]
    else:
        warn(f"Color {color} is not in html format. Returning the same color.")
        return color