import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from .helpers import assert_equality
import pathlib

this_dir = pathlib.Path(__file__).resolve().parent
test_name = "test_scatter"

def plot_1():
    df = px.data.gapminder().query("continent == 'Oceania'")
    fig = px.line(df, x='year', y='lifeExp', color='country', markers=True)
    return fig

def plot_2():
    df = px.data.gapminder().query("country in ['Canada', 'Botswana']")
    fig = px.line(df, x="lifeExp", y="gdpPercap", color="country", text="year")
    fig.update_traces(textposition="bottom right")

    # fig.show()
    return fig

def plot_3():
    x = np.arange(10)
    fig = go.Figure(data=go.Scatter(x=x, y=x**2))
    return fig

def test_1():
    assert_equality(plot_1(), os.path.join(this_dir, test_name, test_name + "_1_reference.tikz"))

def test_2():
    assert_equality(plot_2(), os.path.join(this_dir, test_name, test_name + "_2_reference.tikz"))

def test_3():
    assert_equality(plot_3(), os.path.join(this_dir, test_name, test_name + "_3_reference.tikz"))