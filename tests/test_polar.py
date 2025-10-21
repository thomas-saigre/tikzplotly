"""
Test of polar plots https://plotly.com/python/radar-chart/ and https://plotly.com/python/polar-chart/
"""
import os, pathlib
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .helpers import assert_equality

this_dir = pathlib.Path(__file__).resolve().parent
test_name = "test_polar"

def plot_radar_1():
    df = pd.DataFrame(dict(
        r=[1, 5, 2, 2, 3],
        theta=['processing cost','mechanical properties','chemical stability',
            'thermal stability', 'device integration']))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    return fig

def plot_radar_2():
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
            line_color = 'darkviolet',
            line_width=2
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
    return fig

def fig_polar_categorial_angular():

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
    return fig

def fig_polar_categorial_radial():

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
    return fig

def fig_polar_categorial_angularcategories():

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
    return fig

def fig_polar_categorial_radialcategories():

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
    return fig

def fig_polar_range_1():
    fig = px.scatter_polar(r=range(0,90,10), theta=range(0,90,10),
                           range_theta=[0,90], start_angle=0, direction="counterclockwise")
    return fig

def fig_polar_range_2():
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        mode = "lines",
        r = [3, 3, 4, 3],
        theta = [0, 45, 90, 270],
        fill = "toself",
        subplot = "polar4",
    ))
    fig.update_layout(
        polar = dict(
            radialaxis = dict(visible = False, range = [0, 6])
        ),
        showlegend = False
    )
    return fig

def fig_polar_1():
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
    return fig

def fig_polar_matplotlib(): # not supported yet
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
    return fig


def test_radar_1():
    assert_equality(plot_radar_1(), os.path.join(this_dir, test_name, test_name + "_radar_1_reference.tex"))

def test_radar_2():
    assert_equality(plot_radar_2(), os.path.join(this_dir, test_name, test_name + "_radar_2_reference.tex"))

def test_polar_categorial_angular():
    assert_equality(fig_polar_categorial_angular(), os.path.join(this_dir, test_name, test_name + "_categorical_angular_reference.tex"))

def test_polar_categorial_radial():
    assert_equality(fig_polar_categorial_radial(), os.path.join(this_dir, test_name, test_name + "_categorical_radial_reference.tex"))

def test_polar_categorial_angularcategories():
    assert_equality(fig_polar_categorial_angularcategories(), os.path.join(this_dir, test_name, test_name + "_categorical_angularcategories_reference.tex"))

def test_polar_categorial_radialcategories():
    assert_equality(fig_polar_categorial_radialcategories(), os.path.join(this_dir, test_name, test_name + "_categorical_radialcategories_reference.tex"))

def test_polar_range_1():
    assert_equality(fig_polar_range_1(), os.path.join(this_dir, test_name, test_name + "_radar_range_1_reference.tex"))

def test_polar_range_2():
    assert_equality(fig_polar_range_2(), os.path.join(this_dir, test_name, test_name + "_radar_range_2_reference.tex"))

def test_polar_1():
    assert_equality(fig_polar_1(), os.path.join(this_dir, test_name, test_name + "_1_reference.tex"))

def test_polar_matplotlib():
    assert_equality(fig_polar_matplotlib(), os.path.join(this_dir, "empty_plot.tex"))
