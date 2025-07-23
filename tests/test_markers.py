import plotly.express as px
import plotly.graph_objects as go
import pytest
import numpy as np
import os
from .helpers import assert_equality
import pathlib

this_dir = pathlib.Path(__file__).resolve().parent
test_name = "test_markers"

def plot_1(symbol):

    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

    fig.update_traces(marker=dict(size=12,
                              symbol = symbol,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
    return fig

def plot_2():
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

    return fig

def plot_3():
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

    fig.update_traces(
        marker=dict(size=8, symbol="diamond", line=dict(width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )

    return fig

def plot_with_angle():
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

    fig.update_traces(
        marker=dict(
            size=12, symbol="arrow", angle=45, line=dict(width=2, color="DarkSlateGrey")
        ),
        selector=dict(mode="markers"),
    )
    # fig.show()
    return fig

@pytest.mark.parametrize("symbol", ["circle", 0, "0", "circle-dot"])
def test_1(symbol):
    assert_equality(plot_1(symbol), os.path.join(this_dir, test_name, test_name + "_1_reference.tex"))

def test_2():
    assert_equality(plot_2(), os.path.join(this_dir, test_name, test_name + "_2_reference.tex"))

def test_3():
    assert_equality(plot_3(), os.path.join(this_dir, test_name, test_name + "_3_reference.tex"))

def test_angle():
    assert_equality(plot_with_angle(), os.path.join(this_dir, test_name, test_name + "_angle_reference.tex"))
