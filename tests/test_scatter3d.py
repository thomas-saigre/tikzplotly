"""
Test of 3D scatter plots https://plotly.com/python/3d-scatter-plots/
"""
import os, pathlib
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pytest
from .helpers import assert_equality

this_dir = pathlib.Path(__file__).resolve().parent
test_name = "test_scatter3d"

def plot_scatter_3d_1():
    df = px.data.iris()
    fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width', color='species')
    return fig

def plot_scatter_3d_2(mode):
    t = np.linspace(0, 20, 100)
    x, y, z = np.cos(t), np.sin(t), t

    fig = go.Figure(data=[go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode=mode,
        marker=dict(
            size=12,
            color=z,                # set color to an array/list of desired values
            colorscale='Viridis',   # choose a colorscale
            opacity=0.8,
            symbol="diamond"
        ),
    )])
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    return fig

def plot_scatter_3d_3():
    t = np.linspace(0, 20, 100)
    x, y, z = np.cos(t), np.sin(t), t

    fig = go.Figure(data=[go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='lines',
        line=dict(
            color='darkblue',
            width=4
        ),
        showlegend=False
    )])
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    return fig

def plot_scatter_3d_view():
    fig = go.Figure(data=[go.Scatter3d(
        x=[1, 2, 3],
        y=[4, 5, 6],
        z=[7, 8, 9],
        mode='markers',
        marker=dict(size=6, color='red')
    )])
    fig.update_layout(
        scene=dict(
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=0.5)
            ),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            zaxis=dict(showgrid=False)
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )
    return fig


def plot_scatter_3d_empty():
    return go.Figure(data=[go.Scatter3d(
        x=None,
        y=None,
        z=None,
    )])

def test_scatter_3d_1():
    assert_equality(plot_scatter_3d_1(), os.path.join(this_dir, test_name, test_name + "_1_reference.tex"))

@pytest.mark.parametrize("mode", ["markers", "markers+lines", "lines"])
def test_scatter_3d_2(mode):
    assert_equality(plot_scatter_3d_2(mode), os.path.join(this_dir, test_name, test_name + f"_2_{mode}_reference.tex"))

def test_scatter_3d_3():
    assert_equality(plot_scatter_3d_3(), os.path.join(this_dir, test_name, test_name + "_3_reference.tex"))

def test_scatter_3d_view():
    assert_equality(plot_scatter_3d_view(), os.path.join(this_dir, test_name, test_name + "_view_reference.tex"))

def test_scatter_3d_empty():
    assert_equality(plot_scatter_3d_empty(), os.path.join(this_dir, test_name, test_name + "_empty_reference.tex"))
