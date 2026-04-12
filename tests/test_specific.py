"""
In this file are present the test of some very specific usage case, that should occur very rarely.
"""
import os, pathlib
import pytest
import plotly.graph_objects as go
import plotly.express as px
from .helpers import assert_equality

this_dir = pathlib.Path(__file__).resolve().parent
test_name = "test_specific"

def plot_sanitized_text():
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16], name="[test​]")
    )
    annotations = []
    # add label at top of the plot
    annotations.append(dict(yref='paper', x=2, y=1.05,
                            xanchor='left', yanchor='bottom',
                            text='==[{𝕋op text}]==	'  # special characters u1d54b (blackbold T, should appear x1d54b), and
                                                       # u9 (horizontal tabulation, should appear as x9 in exported code)
    ))
    annotations.append(dict(x=2, y=2,
                            xanchor='left', yanchor='bottom',
                            text="Ouais c'est pas faux"
    ))
    fig.update_layout(annotations=annotations)

    return fig



def plot_empty_figure():
    fig = go.Figure()
    return fig

def plot_empty_histogram():
    # Normally user shouldn't create this kind on figure, but we never know !
    fig = px.histogram(x=[1])
    fig.data[0].x = None
    return fig


def test_sanitized_text():
    with pytest.warns(UserWarning, match="Character .+ has been replaced by \"x[0-9a-f]+\" in output file"):
        assert_equality(plot_sanitized_text(), os.path.join(this_dir, test_name, test_name + "_sanitized_text_reference.tex"))

def test_empty_figure():
    with pytest.warns(UserWarning, match="No data in figure."):
        assert_equality(plot_empty_figure(), os.path.join(this_dir, "empty_plot.tex"))

def test_empty_histogram():
    with pytest.warns(UserWarning, match="Empty histogram.*"):
        assert_equality(plot_empty_histogram(), os.path.join(this_dir, test_name, test_name + "_empty_histogram_reference.tex"))
