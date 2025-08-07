import tikzplotly
from tikzplotly._tex import *
import os
import plotly.express as px
import pytest
import pathlib
from .helpers import compare_two_files

this_dir = pathlib.Path(__file__).resolve().parent

@pytest.mark.parametrize("axis_options", ["None", "dict", "str"])
def test_tikzplotly(axis_options):
    fig = px.scatter(x=[1, 2, 3], y=[1, 2, 3])
    if axis_options == "dict":
        tikzplotly.save("/tmp/tikzplotly/test_tikzplotly_dict.tex", fig, axis_options={"xlabel": "x", "ylabel": "y"})
    elif axis_options == "str":
        tikzplotly.save("/tmp/tikzplotly/test_tikzplotly_str.tex", fig, axis_options="xlabel=x, ylabel=y, xmajorgrids")
    else:
        tikzplotly.save("/tmp/tikzplotly/test_tikzplotly_none.tex", fig)

@pytest.mark.parametrize("options", [None, "a4paper"])
def test_create_document(options):
    main_tex_content = tex_create_document(compatibility="newest", options=options)
    main_tex_content += "\\usepackage{graphicx}\n"
    main_tex_content += "\n"
    stack_env = []
    main_tex_content += tex_begin_environment("document", stack_env) + '\n'

    main_tex_content += tex_begin_environment("figure", stack_env)
    main_tex_content += "  \\includegraphics{example-image-a}\n"
    main_tex_content += "  \\caption{Test figure}\n"
    main_tex_content += tex_end_environment(stack_env) + '\n'

    main_tex_content += "\n" + tex_end_all_environment(stack_env)

    main_tex_path = os.path.join("/tmp/tikzplotly", "test_create_document.tex")
    with open(main_tex_path, "w") as f:
        f.write(main_tex_content)

    compare_two_files(main_tex_path, os.path.join(this_dir, "test_tikzplotly", f"test_create_document_{options}.tex"))
