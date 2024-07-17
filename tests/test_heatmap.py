import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from .helpers import assert_equality
import pathlib
import datetime

this_dir = pathlib.Path(__file__).resolve().parent
test_name = "test_heatmap"
pathlib.Path("/tmp/tikzplotly").mkdir(parents=True, exist_ok=True)

def plot_1():
    fig = px.imshow([[1, 20, 30],
                    [20, 1, 60],
                    [30, 60, 1]])
    return fig

def plot_2():
    df = px.data.medals_wide(indexed=True)
    fig = px.imshow(df)
    return fig

def plot_3():
    fig = go.Figure(data=go.Heatmap(
                   z=[[1, None, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, -10, 20]],
                   x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                   y=['Morning', 'Afternoon', 'Evening'],
                   hoverongaps = False))
    return fig

def plot_4():
    import plotly.graph_objects as go

    programmers = ['Alex','Nicole','Sara','Etienne','Chelsea','Jody','Marianne']

    base = datetime.datetime(2021, 7, 20, 19, 30, 0)
    dates = base - np.arange(180) * datetime.timedelta(days=1)
    np.random.seed(43)
    z = np.random.poisson(size=(len(programmers), len(dates)))

    fig = go.Figure(data=go.Heatmap(
            z=z,
            x=dates,
            y=programmers,
            colorscale='Viridis'))

    fig.update_layout(
        title='GitHub commits per day',
        xaxis_nticks=36)

    return fig

def plot_5():
    fig = px.imshow([[1, 20, 30],
                    [20, 1, 60],
                    [30, 60, 1]])
    fig.data[0].z = None
    return fig

def test_1():
    assert_equality(plot_1(), os.path.join(this_dir, test_name, test_name + "_1_reference.tex"), img_name="/tmp/tikzplotly/fig1.png")

def test_2():
    assert_equality(plot_2(), os.path.join(this_dir, test_name, test_name + "_2_reference.tex"), img_name="/tmp/tikzplotly/fig2.png")

def test_3():
    assert_equality(plot_3(), os.path.join(this_dir, test_name, test_name + "_3_reference.tex"), img_name="/tmp/tikzplotly/fig3.png")

def test_4():
    assert_equality(plot_4(), os.path.join(this_dir, test_name, test_name + "_4_reference.tex"), img_name="/tmp/tikzplotly/fig4.png")

def test_5():
    assert_equality(plot_5(), os.path.join(this_dir, test_name, test_name + "_5_reference.tex"))