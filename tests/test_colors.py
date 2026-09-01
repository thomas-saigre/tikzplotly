import os
import pathlib
from contextlib import nullcontext

import numpy
import plotly.graph_objects as go
import plotly.express as px
import pytest

from .helpers import assert_equality


this_dir = pathlib.Path(__file__).resolve().parent
test_name = "test_colors"


def plot_color(color_scheme):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16], marker_color=color_scheme))
    return fig

def plot_transparent_background():
    fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
    fig.update_layout(plot_bgcolor='rgba(255, 182, 193, .5)')

    return fig


@pytest.mark.parametrize(
    "color, warning_match",
    [
        pytest.param(None, None, id="none"),
        pytest.param(numpy.array([1, 2, 3]), "Color from data is not supported yet", id="numpy-array"), # ("blue", "HTML", "0000ff", 1)
        pytest.param(123, "Color 123 type 'int' is not supported yet", id="non-string"), # ("blue", "HTML", "0000ff", 1)
        pytest.param("#ffb6c1", None, id="hex"),
        pytest.param("rgba(255, 182, 193, .2)", None, id="rgba-with-opacity"),
        pytest.param("rgba(255, 182, 193)", None, id="rgba-without-opacity"),
        pytest.param("rgb(255, 182, 193)", None, id="rgb"),
        pytest.param("red", None, id="named-color"),
        pytest.param("LightBlue", None, id="colors-dict-hit"),
    ],
)
def test_color(color, warning_match, request):
    id = request.node.callspec.id
    if warning_match is None:
        context = nullcontext()
    else:
        context =  pytest.warns(UserWarning, match=warning_match)
    with context:
        assert_equality(plot_color(color), os.path.join(this_dir, test_name, f"{test_name}_{id}_reference.tex"))

def test_transparent_background():
    assert_equality(plot_transparent_background(), os.path.join(this_dir, test_name, test_name + "_transparent_background_reference.tex"))
