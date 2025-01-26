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
    fig = px.histogram(df, x="day", category_orders=dict(day=["Thur", "Fri", "Sat", "Sun"]), opacity=0.8)
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

def plot_6():
    np.random.seed(0)
    x0 = np.random.randn(100)
    x1 = np.random.randn(100)

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=x0))
    fig.add_trace(go.Histogram(x=x1))

    fig.update_layout(barmode='stack')
    return fig

def plot_7():
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill", y="tip", histfunc="avg", nbins=8, text_auto=True)
    return fig

def plot_8():
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill", color="sex")
    return fig

def plot_9():
    np.random.seed(0)
    x_data = np.random.choice(["A", "B", "C", "D"], size=20, p=[0.4, 0.2, 0.3, 0.1])
    fig = px.histogram(x=x_data)
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

def test_5():
    assert_equality(plot_5(), os.path.join(this_dir, test_name, test_name + "_5_reference.tex"))

def test_6():
    assert_equality(plot_6(), os.path.join(this_dir, test_name, test_name + "_6_reference.tex"))

def test_7():
    assert_equality(plot_7(), os.path.join(this_dir, test_name, test_name + "_7_reference.tex"))

def test_8():
    assert_equality(plot_8(), os.path.join(this_dir, test_name, test_name + "_8_reference.tex"))

def test_9():
    assert_equality(plot_9(), os.path.join(this_dir, test_name, test_name + "_9_reference.tex"))