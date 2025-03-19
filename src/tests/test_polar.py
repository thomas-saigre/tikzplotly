# From https://plotly.com/python/polar-chart/
import os
import tikzplotly

from tikzplotly._tex import tex_create_document, tex_begin_environment, tex_end_environment, tex_end_all_environment

import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def fig1():

    df = px.data.wind()
    fig = px.scatter_polar(df, r="frequency", theta="direction")
    # print(f"fig = {fig}")

    # fig.show()
    return fig, "Polar chart with Plotly Express"

def fig2():
    df = px.data.wind()
    fig = px.scatter_polar(df, r="frequency", theta="direction",
                           color="strength", symbol="strength", size="frequency",
                           color_discrete_sequence=px.colors.sequential.Plasma_r)

    # fig.show()
    return fig, "Polar chart with Plotly Express"

def fig3():
    df = px.data.wind()
    fig = px.line_polar(df, r="frequency", theta="direction", color="strength", line_close=True,
                        color_discrete_sequence=px.colors.sequential.Plasma_r,
                        template="plotly_dark",)

    # fig.show()
    return fig, "Polar chart with Plotly Express"

def fig4():
    fig = px.scatter_polar(r=range(0,90,10), theta=range(0,90,10),
                           range_theta=[0,90], start_angle=0, direction="counterclockwise")

    # fig.show()
    return fig, "Range polar chart with Plotly Express"

def fig5():
    fig = go.Figure(data=
        go.Scatterpolar(
            r = [0.5,1,2,2.5,3,4],
            theta = [35,70,120,155,205,240],
            mode = 'markers',
        ))

    fig.update_layout(showlegend=False)
    
    # fig.show()
    return fig, "Basic Polar Chart"

if __name__ == "__main__":

    print("Tikzploty : ", tikzplotly.__version__)
    print("Plotly : ", plotly.__version__)
    print("Test line charts")

    file_directory = os.path.dirname(os.path.abspath(__file__))

    functions = [
        ("1", fig1),
        ("2", fig2),
        ("3", fig3),
        ("4", fig4),
        ("5", fig5),
    ]

    main_tex_content = tex_create_document(options="twocolumn", compatibility="newest")
    main_tex_content += "\\usepackage[left=1cm, right=1cm, top=1cm, bottom=1cm]{geometry}\n"
    main_tex_content += "\\usetikzlibrary{pgfplots.dateplot}\n"
    main_tex_content += "\\usepgfplotslibrary{polar}\n"
    main_tex_content += "\n"
    stack_env = []
    main_tex_content += tex_begin_environment("document", stack_env) + '\n'

    for i, f in functions:
        print(f"Figure {i}")
        fig, title = f()
        data = fig.data
        save_path = os.path.join(file_directory, "outputs", "test_polar", "fig{}.tex".format(i))
        tikzplotly.save(save_path, fig)
        main_tex_content += tex_begin_environment("figure", stack_env)
        main_tex_content += "  \\input{fig" + str(i) + ".tex}\n"
        main_tex_content += "  \\caption{" + title + "}\n"
        main_tex_content += tex_end_environment(stack_env) + '\n'

    main_tex_content += "\n" + tex_end_all_environment(stack_env)

    main_tex_path = os.path.join(file_directory, "outputs", "test_polar", "main.tex")
    print("Save main tex file : ", main_tex_path)
    with open(main_tex_path, "w") as f:
        f.write(main_tex_content)
