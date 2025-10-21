# From https://plotly.com/python/3d-scatter-plots/
import os
import tikzplotly

from tikzplotly._tex import tex_create_document, tex_begin_environment, tex_end_environment, tex_end_all_environment

import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def fig1():
    df = px.data.iris()
    fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width', color='species')
    # fig.show()
    return fig, "3D scatter plot with Plotly Express"

def fig2():
    df = px.data.iris()
    fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width', color='petal_length', symbol='species')
    # fig.show()
    return fig, "3D scatter plot with Plotly Express"

def fig3():
    df = px.data.iris()
    fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
                color='petal_length', size='petal_length', size_max=18,
                symbol='species', opacity=0.7)

    # tight layout
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    # fig.show()
    return fig, "Style 3d scatter plot"

def fig4():
    df = px.data.iris() # replace with your own data source
    low, high = 0, 2.5
    mask = (df.petal_width > low) & (df.petal_width < high)
    fig = px.scatter_3d(df[mask],
        x='sepal_length', y='sepal_width', z='petal_width',
        color="species", hover_data=['petal_width'])
    # fig.show()
    return fig, "Style 3d scatter plot"

def fig5():
    t = np.linspace(0, 10, 50)
    x, y, z = np.cos(t), np.sin(t), t
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers')])
    # fig.show()
    return fig, "Basic 3D Scatter Plot with go.Scatter3d"

def fig6():
    t = np.linspace(0, 20, 100)
    x, y, z = np.cos(t), np.sin(t), t

    fig = go.Figure(data=[go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=12,
            color=z,                # set color to an array/list of desired values
            colorscale='Viridis',   # choose a colorscale
            opacity=0.8
        )
    )])

    # tight layout
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    # fig.show()
    return fig, "3D Scatter Plot with Colorscaling and Marker Styling"

def fig7():
    fig = go.Figure(data=[go.Scatter3d(
        x=[1, 2, 3],
        y=[4, 5, 6],
        z=[7, 8, 9],
        mode='markers',
    )])
    fig.update_layout(
        scene=dict(
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            zaxis=dict(showgrid=True),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=0.5)
            )
        )
    )
    # fig.show()
    return fig, "3D plot with custom view"


if __name__ == "__main__":

    print("Tikzploty : ", tikzplotly.__version__)
    print("Plotly : ", plotly.__version__)
    print("Test scatter 3d charts")

    file_directory = os.path.dirname(os.path.abspath(__file__))

    functions = [
        ("1", fig1),
        ("2", fig2),
        ("3", fig3),
        ("4", fig4),
        ("5", fig5),
        ("6", fig6),
        ("7", fig7),
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
        save_path = os.path.join(file_directory, "outputs", "test_scatter3d", "fig{}.tex".format(i))
        tikzplotly.save(save_path, fig)
        main_tex_content += tex_begin_environment("figure", stack_env)
        main_tex_content += "  \\input{fig" + str(i) + ".tex}\n"
        main_tex_content += "  \\caption{" + title + "}\n"
        main_tex_content += tex_end_environment(stack_env) + '\n'

    main_tex_content += "\n" + tex_end_all_environment(stack_env)

    main_tex_path = os.path.join(file_directory, "outputs", "test_scatter3d", "main.tex")
    print("Save main tex file : ", main_tex_path)
    with open(main_tex_path, "w") as f:
        f.write(main_tex_content)
