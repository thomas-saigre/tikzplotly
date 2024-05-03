# From https://plotly.com/python/heatmaps/
import os
import tikzplotly

from tikzplotly._tex import tex_create_document, tex_begin_environment, tex_end_environment, tex_end_all_environment

import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def fig1():
    fig = px.imshow([[1, 20, 30],
                    [20, 1, 60],
                    [30, 60, 1]])
    # fig.show()
    return fig, "Heatmaps with Plotly Express"


if __name__ == "__main__":

    print("Tikzploty : ", tikzplotly.__version__)
    print("Plotly : ", plotly.__version__)
    print("Test line charts")

    file_directory = os.path.dirname(os.path.abspath(__file__))

    functions = [
        ("1", fig1)
    ]

    main_tex_content = tex_create_document(options="twocolumn", compatibility="newest")
    main_tex_content += "\\usepackage[left=1cm, right=1cm, top=1cm, bottom=1cm]{geometry}\n"
    main_tex_content += "\n"
    stack_env = []
    main_tex_content += tex_begin_environment("document", stack_env) + '\n'

    for i, f in functions:
        print(f"Figure {i}")
        fig, title = f()
        data = fig.data
        save_path = os.path.join(file_directory, "outputs", "test_heatmap", "fig{}.tex".format(i))
        tikzplotly.save(save_path, fig, img_name=os.path.join(file_directory, "outputs", "test_heatmap", "fig{}.png".format(i)))
        main_tex_content += tex_begin_environment("figure", stack_env)
        main_tex_content += "  \\input{fig" + str(i) + ".tex}\n"
        main_tex_content += "  \\caption{" + title + "}\n"
        main_tex_content += tex_end_environment(stack_env) + '\n'

    main_tex_content += "\\begin{figure}\n  \\input{tmp.tex}\n  \\caption{Heatmaps with Plotly Express}\n\\end{figure}\n"

    main_tex_content += "\n" + tex_end_all_environment(stack_env)

    main_tex_path = os.path.join(file_directory, "outputs", "test_heatmap", "main.tex")
    print("Save main tex file : ", main_tex_path)
    with open(main_tex_path, "w") as f:
        f.write(main_tex_content)
