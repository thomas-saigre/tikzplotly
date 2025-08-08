"""
Test of 3D scatter plots https://plotly.com/python/3d-scatter-plots/
"""
import os, pathlib
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from .helpers import assert_equality

this_dir = pathlib.Path(__file__).resolve().parent
test_name = "test_scatter3d"

def plot_scatter_3d_1():
    df = px.data.iris()
    fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width', color='species')
    return fig

def plot_scatter_3d_2():
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
        )
    )])
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    return fig

def test_scatter_3d_1():
    assert_equality(plot_scatter_3d_1(), os.path.join(this_dir, test_name, test_name + "_1_reference.tex"))

def test_scatter_3d_2():
    assert_equality(plot_scatter_3d_2(), os.path.join(this_dir, test_name, test_name + "_2_reference.tex"))

def test_scatter_3d_3():
    assert_equality(plot_scatter_3d_3(), os.path.join(this_dir, test_name, test_name + "_3_reference.tex"))
