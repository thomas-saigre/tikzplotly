import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from .helpers import assert_equality
import pathlib
import pytest

this_dir = pathlib.Path(__file__).resolve().parent
test_name = "test_scatter"

def plot_1():
    df = px.data.gapminder().query("continent == 'Oceania'")
    fig = px.line(df, x='year', y='lifeExp', color='country', markers=True)
    return fig

def plot_transparent_color():
    # TODO move into color tests
    fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16], opacity=0.5)
    return fig

def plot_transparent_color_rgba():
    # TODO
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16], marker_color='rgba(255, 182, 193, .5)'))
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

def plot_4():
    labels = ['Television', 'Newspaper', 'Internet', 'Radio']
    colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

    mode_size = [4, 4, 6, 4]
    line_size = [2, 2, 4, 2]

    x_data = np.vstack((np.arange(2001, 2013),)*4)

    y_data = np.array([
        [74, 82, 80, 74, 73, 72, 74, 70, 70, 66, 66, 69],
        [45, 42, 50, 46, 36, 36, 34, 35, 32, 31, 31, 28],
        [13, 14, 20, 24, 20, 24, 24, 40, 35, 41, 43, 50],
        [18, 21, 18, 21, 16, 14, 13, 18, 17, 16, 19, 23],
    ])

    fig = go.Figure()

    for i in range(0, 4):
        fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
            name=labels[i],
            line=dict(color=colors[i], width=line_size[i]),
            connectgaps=True,
        ))

        # endpoints
        fig.add_trace(go.Scatter(
            x=[x_data[i][0], x_data[i][-1]],
            y=[y_data[i][0], y_data[i][-1]],
            mode='markers',
            marker=dict(color=colors[i], size=mode_size[i])
        ))

    fig.update_layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    annotations = []

    # Adding labels
    for y_trace, label, color in zip(y_data, labels, colors):
        # labeling the left_side of the plot
        annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                    xanchor='right', yanchor='middle',
                                    text=label + ' {}%'.format(y_trace[0]),
                                    font=dict(family='Arial',
                                                size=16),
                                    showarrow=False))
        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.95, y=y_trace[11],
                                    xanchor='left', yanchor='middle',
                                    text='{}%'.format(y_trace[11]),
                                    font=dict(family='Arial',
                                                size=16),
                                    showarrow=False))
    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                xanchor='left', yanchor='bottom',
                                text='Main Source for News',
                                font=dict(family='Arial',
                                            size=30,
                                            color='rgb(37,37,37)'),
                                showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                xanchor='center', yanchor='top',
                                text='Source: PewResearch Center & ' +
                                    'Storytelling with data',
                                font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                showarrow=False))

    fig.update_layout(annotations=annotations)

    # fig.show()
    return fig

def plot_5():
    df = px.data.stocks()
    fig = px.line(df, x='date', y="GOOG")
    return fig

def plot_6(x=True, y=True):
    fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
    if x: fig.data[0].x = None
    if y: fig.data[0].y = None
    return fig

def plot_7():
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
            'August', 'September', 'October', 'November', 'December']
    high_2000 = [32.5, 37.6, 49.9, 53.0, 69.1, 75.4, 76.5, 76.6, 70.7, 60.6, 45.1, 29.3]
    low_2000 = [13.8, 22.3, 32.5, 37.2, 49.9, 56.1, 57.7, 58.3, 51.2, 42.8, 31.6, 15.9]
    high_2007 = [36.5, 26.6, 43.6, 52.3, 71.5, 81.4, 80.5, 82.2, 76.0, 67.3, 46.1, 35.0]
    low_2007 = [23.6, 14.0, 27.0, 36.8, 47.6, 57.7, 58.9, 61.2, 53.3, 48.5, 31.0, 23.6]
    high_2014 = [28.8, 28.5, 37.0, 56.8, 69.7, 79.7, 78.5, 77.8, 74.1, 62.6, 45.3, 39.9]
    low_2014 = [12.7, 14.3, 18.6, 35.5, 49.9, 58.0, 60.0, 58.6, 51.7, 45.2, 32.2, 29.1]

    fig = go.Figure()
    # Create and style traces
    fig.add_trace(go.Scatter(x=month, y=high_2014, name='High 2014',
                            line=dict(color='firebrick', width=1.5)))
    fig.add_trace(go.Scatter(x=month, y=low_2014, name = 'Low 2014',
                            line=dict(color='royalblue', width=1.5)))
    fig.add_trace(go.Scatter(x=month, y=high_2007, name='High 2007',
                            line=dict(color='firebrick', width=1.5,
                                dash='dash') # dash options include 'dash', 'dot', and 'dashdot'
    ))
    fig.add_trace(go.Scatter(x=month, y=low_2007, name='Low 2007',
                            line = dict(color='royalblue', width=1.5, dash='dash')))
    fig.add_trace(go.Scatter(x=month, y=high_2000, name='High 2000',
                            line = dict(color='firebrick', width=1.5, dash='dot')))
    fig.add_trace(go.Scatter(x=month, y=low_2000, name='Low 2000',
                            line=dict(color='royalblue', width=1.5, dash='dot')))

    fig.update_layout(title='Average High and Low Temperatures in New York',
                    xaxis_title='Month',
                    yaxis_title='Temperature (degrees F)')
    return fig

def plot_8():
    df = px.data.gapminder().query("year == 2007")
    fig = px.scatter(df, x="gdpPercap", y="lifeExp", hover_name="country",
                    log_x=True, range_x=[1,100000], range_y=[0,100])
    fig.update_xaxes(showgrid=True, minor=dict(ticks="inside", ticklen=6, showgrid=True), ticklen=6)
    fig.update_yaxes(showgrid=True, ticklen=6)
    return fig

def plot_9():
    np.random.seed(0)
    x = np.random.lognormal(mean=0.0, sigma=1.0, size=50)
    y = np.random.lognormal(mean=0.0, sigma=1.0, size=50)
    fig = px.scatter(x=x, y=y, labels={'x':'log(x)', 'y':'log(y)'})
    fig.update_xaxes(type="log", visible=False)
    fig.update_yaxes(type="log", visible=False)
    return fig

def plot_10():
    df = px.data.gapminder().query("continent == 'Oceania'")
    fig = px.line(df, x='year', y='lifeExp', color='country', markers=True)
    fig.update_xaxes(autorange="reversed")
    fig.update_yaxes(autorange="reversed")
    return fig


def test_1():
    assert_equality(plot_1(), os.path.join(this_dir, test_name, test_name + "_1_reference.tex"))

def test_2():
    assert_equality(plot_2(), os.path.join(this_dir, test_name, test_name + "_2_reference.tex"))

def test_tranparent_color():
    assert_equality(plot_transparent_color(), os.path.join(this_dir, test_name, test_name + "_transparent_color_reference.tex"))

# def test_tranparent_color_rgba():
    # assert_equality(plot_transparent_color_rgba(), os.path.join(this_dir, test_name, test_name + "_transparent_color_rgba_reference.tex"))

def test_3():
    assert_equality(plot_3(), os.path.join(this_dir, test_name, test_name + "_3_reference.tex"))

def test_4():
    assert_equality(plot_4(), os.path.join(this_dir, test_name, test_name + "_4_reference.tex"))

def test_5():
    assert_equality(plot_5(), os.path.join(this_dir, test_name, test_name + "_5_reference.tex"))

@pytest.mark.parametrize("x, y", [(True, True), (True, False), (False, True)])
def test_6(x, y):
    assert_equality(plot_6(x, y), os.path.join(this_dir, test_name, test_name + f"_6_{x}_{y}_reference.tex"))

def test_7():
    assert_equality(plot_7(), os.path.join(this_dir, test_name, test_name + "_7_reference.tex"))

def test_8():
    assert_equality(plot_8(), os.path.join(this_dir, test_name, test_name + "_8_reference.tex"))

def test_9():
    assert_equality(plot_9(), os.path.join(this_dir, test_name, test_name + "_9_reference.tex"))

def test_10():
    assert_equality(plot_10(), os.path.join(this_dir, test_name, test_name + "_10_reference.tex"))
