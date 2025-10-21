import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from .helpers import assert_equality
import pathlib
import pytest

this_dir = pathlib.Path(__file__).resolve().parent
test_name = "test_bars"


def plot_vertical1():
    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(data_canada, x='year', y='pop')
    return fig

def plot_vertical2():
    wide_df = px.data.medals_wide()
    fig = px.bar(
        wide_df,
        x="nation",
        y=["gold", "silver", "bronze"],
        title="Wide-Form Input",
        color_discrete_map={
            "gold": "gold",
            "silver": "silver",
            "bronze": "#cd7f32"
        }
    )
    fig.update_traces(marker_line_width=2, marker_line_color="black")
    return fig

def plot_horizontal1():
    fig = go.Figure(go.Bar(
            x=[20, 14, 23],
            y=['giraffes', 'orangutans', 'monkeys'],
            orientation='h'))
    return fig

def plot_horizontal2():
    df = px.data.tips()
    fig = px.bar(df, x="total_bill", y="day", orientation='h')
    return fig


def test_vertical1():
    assert_equality(plot_vertical1(), os.path.join(this_dir, test_name, test_name + "_vertical1_reference.tex"))

def test_vertical2():
    assert_equality(plot_vertical2(), os.path.join(this_dir, test_name, test_name + "_vertical2_reference.tex"))

def test_horizontal1():
    assert_equality(plot_horizontal1(), os.path.join(this_dir, test_name, test_name + "_horizontal1_reference.tex"))

def test_horizontal2():
    assert_equality(plot_horizontal2(), os.path.join(this_dir, test_name, test_name + "_horizontal2_reference.tex"))
