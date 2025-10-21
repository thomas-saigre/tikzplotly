# From https://plotly.com/python/radar-chart/
# From https://plotly.com/python/polar-chart/
import os
import tikzplotly

from tikzplotly._tex import tex_create_document, tex_begin_environment, tex_end_environment, tex_end_all_environment

import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def fig_radar1():
    df = pd.DataFrame(dict(
        r=[1, 5, 2, 2, 3],
        theta=['processing cost','mechanical properties','chemical stability',
            'thermal stability', 'device integration']))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)

    # fig.show()
    return fig, "Radar Chart with Plotly Express"

def fig_radar2():
    df = pd.DataFrame(dict(
        r=[1, 5, 2, 2, 3],
        theta=['processing cost','mechanical properties','chemical stability',
            'thermal stability', 'device integration']))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself')

    # fig.show()
    return fig, "Filled Radar Chart with Plotly Express"

def fig_radar3():
    fig = go.Figure(data=go.Scatterpolar(
    r=[1, 5, 2, 2, 3],
    theta=['processing cost','mechanical properties','chemical stability', 'thermal stability',
            'device integration'],
    fill='toself'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=False
    )

    # fig.show()
    return fig, "Basic Filled Radar Chart with go.Scatterpolar"

def fig_radar4():
    categories = ['processing cost','mechanical properties','chemical stability',
                'thermal stability', 'device integration']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[1, 5, 2, 2, 3],
        theta=categories,
        fill='toself',
        name='Product A'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[4, 3, 2.5, 1, 2],
        theta=categories,
        fill='toself',
        name='Product B'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 5]
            )),
        showlegend=False
    )

    # fig.show()
    return fig, "Multiple Trace Radar Chart"


def fig_polar1():

    df = px.data.wind()
    fig = px.scatter_polar(df, r="frequency", theta="direction")

    # fig.show()
    return fig, "Polar chart with Plotly Express"

def fig_polar2():
    df = px.data.wind()
    fig = px.scatter_polar(df, r="frequency", theta="direction",
                           color="strength", symbol="strength", size="frequency",
                           color_discrete_sequence=px.colors.sequential.Plasma_r)

    # fig.show()
    return fig, "Polar chart with Plotly Express"

def fig_polar3():
    df = px.data.wind()
    fig = px.line_polar(df, r="frequency", theta="direction", color="strength", line_close=True,
                        color_discrete_sequence=px.colors.sequential.Plasma_r,
                        template="plotly_dark",)

    # fig.show()
    return fig, "Polar chart with Plotly Express"

def fig_polar4():
    fig = px.scatter_polar(r=range(0,90,10), theta=range(0,90,10),
                           range_theta=[0,90], start_angle=0, direction="counterclockwise")

    # fig.show()
    return fig, "Range polar chart with Plotly Express"

def fig_polar5():
    fig = go.Figure(data=
        go.Scatterpolar(
            r = [0.5,1,2,2.5,3,4],
            theta = [35,70,120,155,205,240],
            mode = 'markers',
        ))

    fig.update_layout(showlegend=False)

    # fig.show()
    return fig, "Basic Polar Chart"

def fig_polar6():
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/polar_dataset.csv")

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
            r = df['x1'],
            theta = df['y'],
            mode = 'lines',
            name = 'Figure 8',
            line_color = 'peru'
        ))
    fig.add_trace(go.Scatterpolar(
            r = df['x2'],
            theta = df['y'],
            mode = 'lines',
            name = 'Cardioid',
            line_color = 'darkviolet'
        ))
    fig.add_trace(go.Scatterpolar(
            r = df['x3'],
            theta = df['y'],
            mode = 'lines',
            name = 'Hypercardioid',
            line_color = 'deepskyblue'
        ))


    fig.update_layout(
        title = 'Basic Polar Chart',
        showlegend = False
    )

    # fig.show()
    return fig, "Mic Patterns"

def fig_polar7():
    fig = go.Figure(go.Barpolar(
        r=[3.5, 1.5, 2.5, 4.5, 4.5, 4, 3],
        theta=[65, 15, 210, 110, 312.5, 180, 270],
        width=[20,15,10,20,15,30,15,],
        marker_color=["#E4FF87", '#709BFF', '#709BFF', '#FFAA70', '#FFAA70', '#FFDF70', '#B6FFB4'],
        marker_line_color="black",
        marker_line_width=2,
        opacity=0.8
    ))

    fig.update_layout(
        template=None,
        polar = dict(
            radialaxis = dict(range=[0, 5], showticklabels=False, ticks=''),
            angularaxis = dict(showticklabels=False, ticks='')
        )
    )

    # fig.show()
    return fig, "Polar Bar Chart"

def fig_polar8a():

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        name = "angular categories",
        r = [5, 4, 2, 4, 5],
        theta = ["a", "b", "c", "d", "a"],
        ))

    fig.update_traces(fill='toself')

    fig.update_layout(
        polar = dict(
        radialaxis_angle = -45,
        angularaxis = dict(
            direction = "clockwise",
            period = 6)
        ),
    )

    # fig.show()

    return fig, "Categorical Polar Chart"

def fig_polar8b():

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        name = "radial categories",
        r = ["a", "b", "c", "d", "b", "f", "a"],
        theta = [1, 4, 2, 1.5, 1.5, 6, 5],
        thetaunit = "radians",
        ))

    fig.update_traces(fill='toself')

    fig.update_layout(
        polar = dict(
            radialaxis = dict(
                angle = 180,
                tickangle = -180 # so that tick labels are not upside down
            )
        )
    )

    # fig.show()

    return fig, "Categorical Polar Chart"

def fig_polar8c():

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        name = "angular categories (w/ categoryarray)",
        r = [5, 4, 2, 4, 5],
        theta = ["a", "b", "c", "d", "a"],
        ))

    fig.update_traces(fill='toself')

    fig.update_layout(
        polar = dict(
            sector = [80, 400],
            radialaxis_angle = -45,
            angularaxis_categoryarray = ["d", "a", "c", "b"]
        ),
    )

    # fig.show()

    return fig, "Categorical Polar Chart"

def fig_polar8d():

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        name = "radial categories (w/ category descending)",
        r = ["a", "b", "c", "d", "b", "f", "a", "a"],
        theta = [45, 90, 180, 200, 300, 15, 20, 45],
        ))

    fig.update_traces(fill='toself')
    fig.update_layout(
        polar = dict(
        radialaxis_categoryorder = "category descending",
        angularaxis = dict(
            thetaunit = "radians",
            dtick = 0.3141592653589793
        ))
    )

    # fig.show()
    return fig, "Categorical Polar Chart"

def fig_polar9a():

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar())
    fig.update_traces(mode = "lines+markers",
        r = [1,2,3,4,5],
        theta = [0,90,180,360,0],
        line_color = "magenta",
        marker = dict(
            color = "royalblue",
            symbol = "square",
            size = 8
        ))

    fig.update_layout(
        showlegend = False,
        polar = dict(
            sector = [150,210],
        ))

    # fig.show()
    return fig, "Polar Chart Sector"

def fig_polar9b():

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar())
    fig.update_traces(mode = "lines+markers",
        r = [1,2,3,4,5],
        theta = [0,90,180,360,0],
        line_color = "magenta",
        marker = dict(
            color = "royalblue",
            symbol = "square",
            size = 8
        ))

    fig.update_layout(
        showlegend = False,
    )

    # fig.show()
    return fig, "Polar Chart Sector"

def fig_polar10a():

    fig = go.Figure()

    r = [1,2,3,4,5]
    theta = [0,90,180,360,0]

    fig.add_trace(go.Scatterpolar())
    fig.update_traces(r= r, theta=theta,
                    mode="lines+markers", line_color='indianred',
                    marker=dict(color='lightslategray', size=8, symbol='square'))
    fig.update_layout(
        showlegend = False,
        polar = dict(
            radialaxis_tickfont_size = 8,
            angularaxis = dict(
                tickfont_size=8,
                rotation=90, # start position of angular axis
                direction="counterclockwise"
            )
        )
    )

    # fig.show()
    return fig, "Polar Chart Directions"

def fig_polar10b():

    fig = go.Figure()

    r = [1,2,3,4,5]
    theta = [0,90,180,360,0]

    fig.add_trace(go.Scatterpolar())
    fig.update_traces(r= r, theta=theta,
                    mode="lines+markers", line_color='indianred',
                    marker=dict(color='lightslategray', size=8, symbol='square'))
    fig.update_layout(
        showlegend = False,
        polar = dict(
            radialaxis_tickfont_size = 8,
            angularaxis = dict(
                tickfont_size = 8,
                rotation = 90,
                direction = "clockwise"
            )
        )
    )

    # fig.show()
    return fig, "Polar Chart Directions"

def fig_polar10c():

    fig = go.Figure()

    r = [1,2,3,4,5]
    theta = [0,90,180,360,0]

    fig.add_trace(go.Scatterpolar())
    fig.update_traces(r= r, theta=theta,
                    mode="lines+markers", line_color='indianred',
                    marker=dict(color='lightslategray', size=8, symbol='square'))
    fig.update_layout(
        showlegend = False,
        polar = dict(
            radialaxis_tickfont_size = 8,
            angularaxis = dict(
                tickfont_size=8,
                rotation=180, # start position of angular axis
                direction="counterclockwise"
            )
        )
    )

    # fig.show()
    return fig, "Polar Chart Directions"

def fig_polar10d():

    fig = go.Figure()

    r = [1,2,3,4,5]
    theta = [0,90,180,360,0]

    fig.add_trace(go.Scatterpolar())
    fig.update_traces(r= r, theta=theta,
                    mode="lines+markers", line_color='indianred',
                    marker=dict(color='lightslategray', size=8, symbol='square'))
    fig.update_layout(
        showlegend = False,
        polar = dict(
            radialaxis_tickfont_size = 8,
            angularaxis = dict(
                tickfont_size = 8,
                rotation = 180,
                direction = "clockwise"
            )
        )
    )

    # fig.show()
    return fig, "Polar Chart Directions"

def fig_polar11():

    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/hobbs-pearson-trials.csv")

    fig = go.Figure()

    fig.add_trace(go.Scatterpolargl(
        r = df.trial_1_r,
        theta = df.trial_1_theta,
        name = "Trial 1",
        marker=dict(size=15, color="mediumseagreen")
        ))
    fig.add_trace(go.Scatterpolargl(
        r = df.trial_2_r,
        theta = df.trial_2_theta,
        name = "Trial 2",
        marker=dict(size=20, color="darkorange")
        ))
    fig.add_trace(go.Scatterpolargl(
        r = df.trial_3_r,
        theta = df.trial_3_theta,
        name = "Trial 3",
        marker=dict(size=12, color="mediumpurple")
        ))
    fig.add_trace(go.Scatterpolargl(
        r = df.trial_4_r,
        theta = df.trial_4_theta,
        name = "Trial 4",
        marker=dict(size=22, color = "magenta")
        ))
    fig.add_trace(go.Scatterpolargl(
        r = df.trial_5_r,
        theta = df.trial_5_theta,
        name = "Trial 5",
        marker=dict(size=19, color = "limegreen")
        ))
    fig.add_trace(go.Scatterpolargl(
        r = df.trial_6_r,
        theta = df.trial_6_theta,
        name = "Trial 6",
        marker=dict(size=10, color = "gold")
        ))

    # Common parameters for all traces
    fig.update_traces(mode="markers", marker=dict(line_color='white', opacity=0.7))

    fig.update_layout(
        title = "Hobbs-Pearson Trials",
        font_size = 15,
        showlegend = False,
        polar = dict(
        bgcolor = "rgb(223, 223, 223)",
        angularaxis = dict(
            linewidth = 3,
            showline=True,
            linecolor='black'
        ),
        radialaxis = dict(
            side = "counterclockwise",
            showline = True,
            linewidth = 2,
            gridcolor = "white",
            gridwidth = 2,
        )
        ),
        paper_bgcolor = "rgb(223, 223, 223)"
    )

    # print(f"fig = {fig}")

    # fig.show()
    return fig, "Webgl Polar Chart"

def fig_polar12a():

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r = [1, 2, 3],
        theta = [50, 100, 200],
        marker_symbol = "square"
    ))
    fig.add_trace(go.Scatterpolar(
        r = [1, 2, 3],
        theta = [1, 2, 3],
        thetaunit = "radians"
    ))

    fig.update_layout(
        polar = dict(
            radialaxis_range = [1, 4],
            angularaxis_thetaunit = "radians"
        ),
        showlegend = False
    )

    # fig.show()
    return fig, "Polar Chart Subplots"

def fig_polar12b():

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r = ["a", "b", "c", "b"],
        theta = ["D", "C", "B", "A"],
    ))

    fig.update_layout(
        showlegend = False
    )
    # fig.show()
    return fig, "Polar Chart Subplots"

def fig_polar12c():

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r = [50, 300, 900],
        theta = [0, 90, 180],
    ))

    fig.update_layout(
        polar = dict(
            radialaxis = dict(type = "log", tickangle = 45),
            sector = [0, 180]
        ),
        showlegend = False
    )

    # fig.show()
    return fig, "Polar Chart Subplots"

def fig_polar12d():

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        mode = "lines",
        r = [3, 3, 4, 3],
        theta = [0, 45, 90, 270],
        fill = "toself",
        subplot = "polar4"
    ))

    fig.update_layout(
        polar = dict(
            radialaxis = dict(visible = False, range = [0, 6])
        ),
        showlegend = False
    )

    # fig.show()
    return fig, "Polar Chart Subplots"

if __name__ == "__main__":

    print("Tikzploty : ", tikzplotly.__version__)
    print("Plotly : ", plotly.__version__)
    print("Test polar/radar charts")

    file_directory = os.path.dirname(os.path.abspath(__file__))

    functions = [
        ("radar1", fig_radar1),
        ("radar2", fig_radar2),    # Individual marker sizes in a trace are not supported yet
        ("radar3", fig_radar3),
        ("radar4", fig_radar4),

        ("polar1", fig_polar1),
        ("polar2", fig_polar2),
        ("polar3", fig_polar3),
        ("polar4", fig_polar4),
        ("polar5", fig_polar5),
        ("polar6", fig_polar6),
        ("polar7", fig_polar7),     # Polar bar charts are not supported yet.
        ("polar8a", fig_polar8a),
        ("polar8b", fig_polar8b),
        ("polar8c", fig_polar8c),
        ("polar8d", fig_polar8d),
        ("polar9a", fig_polar9a),
        ("polar9b", fig_polar9b),
        ("polar10a", fig_polar10a),
        ("polar10b", fig_polar10b),
        ("polar10c", fig_polar10c),
        ("polar10d", fig_polar10d),
        ("polar11", fig_polar11),   # Webgl polar charts are treated as normal polar charts.
        ("polar12a", fig_polar12a), # Radial axis range does not look the same with pgfplots.
        ("polar12b", fig_polar12b),
        ("polar12c", fig_polar12c), # Radial axis type log is not supported yet.
        ("polar12d", fig_polar12d),
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
