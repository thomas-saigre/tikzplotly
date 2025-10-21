"""This module provides utilities for generating LaTeX document headers,
    specifically for documents using the pgfplots package.
    It includes functions to create document classes, environments, and TikZ commands.
"""
from ._color import hex2rgb
from ._utils import sanitize_tex_text

def tex_comment(text):
    """Create a LaTeX comment.

    Parameters
    ----------
    text :
        text to be inserted in the comment

    Returns
    -------
        LaTeX comment
    """
    return f"% {text}\n"

def tex_begin_environment(environment, stack_env, options=None):
    """Open a LaTeX environment.

    Parameters
    ----------
    environment
        name of the environment
    stack_env
        stack of opened environments
    options, optional
        option given to the environment, by default None

    Returns
    -------
        LaTeX code for the beginning of the environment
    """
    stack_env.append(environment)
    if options is not None:
        return f"\\begin{{{environment}}}[\n{options}\n]\n"
    return f"\\begin{{{environment}}}\n"

def tex_end_environment(stack_env):
    """Close the last opened LaTeX environment.

    Parameters
    ----------
    stack_env
        stack of opened environments

    Returns
    -------
        LaTeX code for the end of the environment
    """
    environment = stack_env.pop()
    return f"\\end{{{environment}}}\n"

def tex_end_all_environment(stack_env):
    """Close all opened LaTeX environments.

    Parameters
    ----------
    stack_env
        stack of opened environments

    Returns
    -------
        LaTeX code for the end of all environments
    """
    code = ""
    while len(stack_env) > 0:
        code += tex_end_environment(stack_env)
    return code

def tex_addplot(data_str, plot_type="table", options=None, type_options=None):
    """Create a LaTeX addplot command.

    Parameters
    ----------
    data_str
        string containing the data
    plot_type, optional
        type of data, by default "table"
    options, optional
        options given to the addplot command, by default None
    type_options, optional
        options given to the type of data, by default None

    Returns
    -------
        LaTeX code for the addplot command
    """
    code = "\\addplot+ "
    if options is not None:
        code += f"[{options}] "
    code += plot_type
    if type_options is not None:
        code += f"[{type_options}]"
    code += " {" + data_str + "};\n"
    return code

def tex_add_text(x, y, text, options=None, relative=False):
    """Create a LaTeX node command.

    Parameters
    ----------
    x
        x coordinate of the node
    y
        y coordinate of the node
    text
        text of the node
    options, optional
        options given to the node command, by default None
    relative, optional
        boolean indicating if the coordinates are relative to the axis, by default False

    Returns
    -------
        LaTeX code for the node command
    """
    relative_text = ["", "rel "][relative]
    if options is not None:
        return f"\\node[{options}] at ({relative_text}axis cs:{x}, {y}) {{{tex_text(text)}}};\n"
    return f"\\node at (axis cs:{x},{y}) {{{tex_text(text)}}};\n"

def tex_add_color(color_name, type_color, color):
    """Create a LaTeX color definition.

    Parameters
    ----------
    color_name
        name of the color
    type_color
        type of the color
    color
        color string

    Returns
    -------
        LaTeX code for the color definition
    """
    if type_color is not None:
        return f"\\definecolor{{{color_name}}}{{{type_color}}}{{{color}}}\n"
    return ""

def tex_add_legendentry(legend, options=None):
    """Create a LaTeX legend entry.

    Parameters
    ----------
    legend
        legend text
    options, optional
        options given to the legend entry, by default None

    Returns
    -------
        LaTeX code for the legend entry
    """
    if options is not None:
        return f"\\addlegendentry[{options}]{{{legend}}}\n"
    return f"\\addlegendentry{{{legend}}}\n"

def tex_create_document(document_class="article", options=None, compatibility="newest"):
    """Create a LaTeX document.

    Parameters
    ----------
    document_class, optional
        document class, by default "article"
    options, optional
        options given to the document class, by default None
    compatibility, optional
        compatibility of the pgfplots package, by default "newest"

    Returns
    -------
        LaTeX code for the document
    """
    if options is not None:
        code = f"\\documentclass[{options}]{{{document_class}}}\n"
    else:
        code = f"\\documentclass{{{document_class}}}\n"
    code += "\\usepackage{pgfplots}\n"
    code += "\\pgfplotsset{compat=" + compatibility + "}\n\n"
    return code

# Pushed by error, not used yet
# def tex_add_fill_pattern(name, pattern, color, options=None):
#     """Create a LaTeX fill pattern.

#     Parameters
#     ----------
#     pattern
#         pattern name
#     color
#         color string
#     options, optional
#         options given to the pattern, by default None

#     Returns
#     -------
#         LaTeX code for the fill pattern
#     """
#     print("pattern: ", pattern)
#     code = f"\\addplot[color={color}]\n"
#     code += "fill between[of={name} and axis"
#     if options is not None:
#         code += f",{options}"
#     code += f"];\n"
#     return code

def tex_text(text):
    """Convert a string to LaTeX,
    escaping the special characters %, _, &, #, $, {, }, ~.
    """
    text_san = sanitize_tex_text(text)
    return (
        text_san.replace("%", "\\%")
        .replace("&", "\\&")
        .replace("#", "\\#")
        .replace("$", "\\$")
        # .replace("{", "\\{")  # Already done in sanitize_tex_text
        # .replace("}", "\\}")  #
        # .replace("_", "\\_")
        .replace("~", "\\textasciitilde ")
    )

def get_tikz_colorscale(colorscale, name="mycolor"):
    """Get TikZ code for a colorscale.

    Arguments:
        colorscale {tuple} -- tuple of (dist, color) pairs (e.g. ((0.0, '#0d0887'), (1.0, '#f0f921')))

    Keyword Arguments:
        name {str} -- name of the colorscale (default: {"mycolor"})

    Returns:
        str -- code for the TikZ colorscale definition
    """

    code = "{" + str(name) + "}{\n"
    for dist, color in colorscale:
        rgb_color = hex2rgb(color)
        code += f"  rgb255({dist}cm)=({rgb_color})".replace(" ", "") + ";\n"
    code += "}"
    return code
