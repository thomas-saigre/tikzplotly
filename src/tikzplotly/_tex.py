
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
    else:
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

def tex_addplot(data_str, type="table", options=None):
    """Create a LaTeX addplot command.

    Parameters
    ----------
    data_str
        string containing the data
    type, optional
        type of data, by default "table"
    options, optional
        options given to the addplot command, by default None

    Returns
    -------
        LaTeX code for the addplot command
    """
    code = "\\addplot+ "
    if options is not None:
        code += f"[{options}] "
    code += type + " {%\n"
    code += data_str
    code += "};\n"
    return code

def tex_add_text(x, y, text, color="black"):
    """Create a LaTeX node command.

    Parameters
    ----------
    x
        x coordinate of the node
    y
        y coordinate of the node
    text
        text of the node
    color, optional
        color of the node, by default "black"

    Returns
    -------
        LaTeX code for the node command
    """
    return f"\draw (axis cs:{x},{y}) node[scale=0.5, anchor=south east, text={color}, rotate=0.0]{{{text}}};\n"

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
    else:
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
    else:
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
    code += "\\usepackage{pgf, tikz}\n\\usepackage{pgfplots}\n"
    code += "\\pgfplotsset{compat=" + compatibility + "}\n\n"
    return code
