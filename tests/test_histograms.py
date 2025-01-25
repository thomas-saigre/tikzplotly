import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from .helpers import assert_equality
import pathlib
import pytest

this_dir = pathlib.Path(__file__).resolve().parent
test_name = "test_histograms"
pathlib.Path("/tmp/tikzplotly").mkdir(parents=True, exist_ok=True)

def plot_1():
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill", nbins=20)
    return fig

def plot_2():
    np.random.seed(0)
    y = np.random.randn(100)
    fig = go.Figure(data=[go.Histogram(y=y)])
    return fig

def plot_3():
    df = px.data.tips()
    fig = px.histogram(df, x="day", category_orders=dict(day=["Thur", "Fri", "Sat", "Sun"]))
    return fig

def plot_4(histnorm):
    np.random.seed(0)
    x = np.random.randn(100)
    fig = go.Figure(data=[go.Histogram(x=x, histnorm=histnorm)])
    return fig

def plot_5():
    np.random.seed(0)
    x = np.random.randn(100)
    fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True)])
    return fig

def test_1():
    assert_equality(plot_1(), os.path.join(this_dir, test_name, test_name + "_1_reference.tex"))

def test_2():
    assert_equality(plot_2(), os.path.join(this_dir, test_name, test_name + "_2_reference.tex"))

def test_3():
    assert_equality(plot_3(), os.path.join(this_dir, test_name, test_name + "_3_reference.tex"))

@pytest.mark.parametrize("histnorm", ["percent", "probability", "density", "probability density"])
def test_4(histnorm):
    assert_equality(plot_4(histnorm), os.path.join(this_dir, test_name, test_name + "_4_reference.tex"))