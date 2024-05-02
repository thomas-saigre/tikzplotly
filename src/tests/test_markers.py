# From https://plotly.com/python/marker-style/
import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import tikzplotly
import os
import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator
from warnings import warn
from tikzplotly._tex import tex_create_document, tex_begin_environment, tex_end_environment, tex_end_all_environment

def fig1():

    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

    fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
    # fig.show()

    return fig, "add marker border"

def fig2():
    np.random.seed(1)

    x = np.random.uniform(low=3, high=6, size=(500,))
    y = np.random.uniform(low=3, high=6, size=(500,))

    # Build figure
    fig = go.Figure()

    # Add scatter trace with medium sized markers
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=x,
            y=y,
            marker=dict(
                color='LightSkyBlue',
                size=20,
                line=dict(
                    color='MediumPurple',
                    width=2
                )
            ),
            showlegend=False
        )
    )

    # Add trace with large marker
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=[2],
            y=[4.5],
            marker=dict(
                color='LightSkyBlue',
                size=120,
                line=dict(
                    color='MediumPurple',
                    width=12
                )
            ),
            showlegend=False
        )
    )

    return fig, "Add marker border 2"


def fig3():
    x = np.random.uniform(low=3, high=6, size=(500,))
    y = np.random.uniform(low=3, high=4.5, size=(500,))
    x2 = np.random.uniform(low=3, high=6, size=(500,))
    y2 = np.random.uniform(low=4.5, high=6, size=(500,))

    # Build figure
    fig = go.Figure()

    # Add first scatter trace with medium sized markers
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=x,
            y=y,
            opacity=0.5,
            marker=dict(
                color='LightSkyBlue',
                size=3,
                line=dict(color='MediumPurple')
            ),
            name='Opacity 0.5'
        )
    )

    # Add second scatter trace with medium sized markers
    # and opacity 1.0
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=x2,
            y=y2,
            marker=dict(
                color='LightSkyBlue',
                size=3,
                line=dict(color='MediumPurple')
            ),
            name='Opacity 1.0'
        )
    )

    # Add trace with large markers
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=[2, 2],
            y=[4.25, 4.75],
            marker=dict(
                opacity=0.5,
                color='LightSkyBlue',
                size=10,
                line=dict(color='MediumPurple')
            ),
            showlegend=False
        )
    )

    return fig, "Opacity"

def fig3bis():
    x = np.random.uniform(low=3, high=6, size=(500,))
    y = np.random.uniform(low=3, high=6, size=(500,))

    # Build figure
    fig = go.Figure()

    # Add scatter trace with medium sized markers
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=x,
            y=y,
            marker=dict(
                color='LightSkyBlue',
                size=20,
                opacity=0.5,
                line=dict(
                    color='MediumPurple',
                    width=2
                )
            ),
            showlegend=False
        )
    )


    # Add trace with large markers
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=[2, 2],
            y=[4.25, 4.75],
            marker=dict(
                color='LightSkyBlue',
                size=80,
                opacity=0.5,
                line=dict(
                    color='MediumPurple',
                    width=8
                )
            ),
            showlegend=False
        )
    )

    return fig, "Marker Opacity"

def fig3ter():
    x = np.random.uniform(low=3, high=6, size=(500,))
    y = np.random.uniform(low=3, high=6, size=(500,))


    # Build figure
    fig = go.Figure()

    # Add scatter trace with medium sized markers
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=x,
            y=y,
            marker=dict(
                color='rgba(135, 206, 250, 0.5)',
                size=20,
                line=dict(
                    color='MediumPurple',
                    width=2
                )
            ),
            showlegend=False
        )
    )


    # Add trace with large markers
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=[2, 2],
            y=[4.25, 4.75],
            marker=dict(
                color='rgba(135, 206, 250, 0.5)',
                size=80,
                line=dict(
                    color='MediumPurple',
                    width=8
                )
            ),
            showlegend=False
        )
    )
    return fig, "Color opacity"

def fig4():
    warn("This example is not exactly the one online, but has been changed as this kind of data is not yet supported.")
    raw_symbols = SymbolValidator().values
    namestems = []
    namevariants = []
    symbols = []
    names = []
    for i in range(0, len(raw_symbols), 3):
        name = raw_symbols[i+2]
        symbols.append(raw_symbols[i])
        namestems.append(name.replace("-open", "").replace("-dot", ""))
        namevariants.append(name[len(namestems[-1]):])
        names.append(name)

    fig = go.Figure()

    i = 0

    names = ["circle", "square", "diamond", "cross", "x", "triangle-up", "triangle-down", "triangle-left", "triangle-right", "triangle-ne", "triangle-se", "triangle-sw", "triangle-nw", "pentagon", "hexagon", "hexagon2", "octagon", "star", "hexagram", "star-triangle-up", "star-triangle-down", "star-square", "star-diamond", "diamond-tall", "diamond-wide", "hourglass", "bowtie", "circle-cross", "circle-x", "square-cross", "square-x", "diamond-cross", "diamond-x", "cross-thin", "x-thin", "asterisk", "hash", "y-up", "y-down", "y-left", "y-right", "line-ew", "line-ns", "line-ne", "line-nw", "arrow-up", "arrow-down", "arrow-left", "arrow-right", "arrow-bar-up", "arrow-bar-down", "arrow-bar-left", "arrow-bar-right", "arrow", "arrow-wide"]
    types = ["", "-open"]
    for name in names:
        for type in types:
            name = name + type
            fig.add_trace(go.Scatter(mode="markers", x=[i%2], y=[-(i//2)], marker_symbol=name,
                                     marker_line_color="midnightblue", marker_color="lightskyblue",
                                     marker_line_width=2, marker_size=8,
                                     showlegend=False,
                                     hovertemplate="name: %{y}%{x}<br>number: %{marker.symbol}<extra></extra>"))
            i += 1

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[0, 1],
            ticktext=types
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=list(range(0, -55, -1)),
            ticktext=names
        )
    )

    # fig.show()
    return fig, "Custom Marker Symbols"


def fig5():
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

    fig.update_traces(
        marker=dict(size=8, symbol="diamond", line=dict(width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )

    return fig, "Using a custom marker "

def fig6():
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

    fig.update_traces(
        marker=dict(
            size=8,
            symbol="diamond-open",
            line=dict(
                width=2,
    #             color="DarkSlateGrey" Line colors don't apply to open markers
            )
        ),
        selector=dict(mode="markers"),
    )
    return fig, "Open Marker Colors"


def fig7():
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

    fig.update_traces(
        marker=dict(
            size=12, symbol="triangle-up", angle=45, line=dict(width=2, color="DarkSlateGrey")
        ),
        selector=dict(mode="markers"),
    )
    return fig, "Setting marker angle"

def fig8():
    df = px.data.gapminder()
    fig = go.Figure()

    for x in df.loc[df.continent.isin(["Europe"])].country.unique()[:5]:
        fil = df.loc[(df.country.str.contains(x))]
        fig.add_trace(
            go.Scatter(
                x=fil["year"],
                y=fil["pop"],
                mode="lines+markers",
                marker=dict(
                    symbol="arrow",
                    size=15,
                    angleref="previous",
                ),
                name=x,
            )
        )
    return fig, "Setting Angle Reference"



if __name__ == "__main__":

    print("Tikzploty : ", tikzplotly.__version__)
    print("Plotly : ", plotly.__version__)
    print("Test markers")


    file_directory = os.path.dirname(os.path.abspath(__file__))

    functions = [
        ("1", fig1),
        ("2", fig2),
        ("3", fig3),
        ("3bis", fig3bis),
        # ("3ter", fig3ter),
        ("5", fig5),
        ("6", fig6),
        ("7", fig7),
        # ("8", fig8),      # angle reference not supported yet
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
        save_path = os.path.join(file_directory, "outputs", "test_markers", "fig{}.tex".format(i))
        tikzplotly.save(save_path, fig)
        main_tex_content += tex_begin_environment("figure", stack_env)
        main_tex_content += "  \\input{fig" + str(i) + ".tex}\n"
        main_tex_content += "  \\caption{" + title + "}\n"
        main_tex_content += tex_end_environment(stack_env) + '\n'

    main_tex_content += "\n" + tex_end_all_environment(stack_env)

    main_tex_path = os.path.join(file_directory, "outputs", "test_markers", "main.tex")
    print("Save main tex file : ", main_tex_path)
    with open(main_tex_path, "w") as f:
        f.write(main_tex_content)

    ## Separately handling the case with all markers types
    tex_markers = tex_create_document(document_class="standalone")
    tex_markers += tex_begin_environment("document", stack_env) + '\n'
    fig, title = fig4()
    tikzplotly.save(os.path.join(file_directory, "outputs", "test_markers", "markers_fig.tex"), fig, axis_options="height=35cm, ymajorgrids, width=5cm")
    tex_markers += "\\input{markers_fig.tex}\n"
    tex_markers += tex_end_all_environment(stack_env)
    with open(os.path.join(file_directory, "outputs", "test_markers", "markers.tex"), "w") as f:
        f.write(tex_markers)
