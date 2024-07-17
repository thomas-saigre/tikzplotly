import tikzplotly
import plotly.express as px

def test_tikzplotly():
    fig = px.scatter(x=[1, 2, 3], y=[1, 2, 3])
    tikzplotly.save("/tmp/test_tikzplotly.tex", fig)