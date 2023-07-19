# From https://plotly.com/python/line-charts/
import os
import tikzplotly

from tikzplotly._tex import tex_create_document, tex_begin_environment, tex_end_environment, tex_end_all_environment

import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def fig1():
    df = px.data.gapminder().query("country=='Canada'")
    fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')

    # fig.show()
    return fig, "Line Plots with plotly.express"

def fig2():
    df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(df, x="year", y="lifeExp", color='country')

    # fig.show()
    return fig, "Line Plots with column encoding color"

def fig3():
    df = pd.DataFrame(dict(
        x = [1, 3, 2, 4],
        y = [1, 2, 3, 4]
    ))
    df = df.sort_values(by="x")
    fig = px.line(df, x="x", y="y", title="Sorted Input")

    # fig.show()
    return fig, "Data Order in Line Charts : sorted input"

def fig4():
    df = px.data.gapminder().query("country in ['Canada', 'Botswana']")
    fig = px.line(df, x="lifeExp", y="gdpPercap", color="country", text="year")
    fig.update_traces(textposition="bottom right")

    # fig.show()
    return fig, "Connected Scatterplots"

def fig5():
    df = px.data.gapminder().query("continent == 'Oceania'")
    fig = px.line(df, x='year', y='lifeExp', color='country', markers=True)

    # fig.show()
    return fig, "Line charts with markers 1/2"

def fig6():
    df = px.data.gapminder().query("continent == 'Oceania'")
    fig = px.line(df, x='year', y='lifeExp', color='country', symbol="country")
    # fig.show()
    return fig, "Line charts with markers 2/2"

def fig7():
    df = px.data.stocks()
    fig = px.line(df, x='date', y="GOOG")
    # fig.show()
    return fig, "Line plots on Date axes"

def fig8():
    df = px.data.stocks(indexed=True)
    fig = px.line(df, facet_row="company", facet_row_spacing=0.01, height=200, width=200)

    # hide and lock down axes
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)

    # remove facet/subplot labels
    fig.update_layout(annotations=[], overwrite=True)

    # strip down the rest of the plot
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(t=10,l=10,b=10,r=10)
    )

    # disable the modebar for such a small plot
    # fig.show(config=dict(displayModeBar=False))
    return fig, "Sparklines with Plotly Express"

def fig9():
    x = np.arange(10)
    fig = go.Figure(data=go.Scatter(x=x, y=x**2))
    return fig, "Simple Line Plot"

def fig10():
    np.random.seed(1)

    N = 100
    random_x = np.linspace(0, 1, N)
    random_y0 = np.random.randn(N) + 5
    random_y1 = np.random.randn(N)
    random_y2 = np.random.randn(N) - 5

    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                        mode='lines',
                        name='lines'))
    fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                        mode='lines+markers',
                        name='lines+markers'))
    fig.add_trace(go.Scatter(x=random_x, y=random_y2,
                        mode='markers', name='markers'))

    # fig.show()
    return fig, "Line Plot Modes"

def fig11():
    # Add data
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

    # Edit the layout
    fig.update_layout(title='Average High and Low Temperatures in New York',
                    xaxis_title='Month',
                    yaxis_title='Temperature (degrees F)')
    # fig.show()
    return fig, "Style Line Plots"

def fig12():
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=[10, 20, None, 15, 10, 5, 15, None, 20, 10, 10, 15, 25, 20, 10],
        name='No Gaps',
        connectgaps=True # override default to connect the gaps
    ))
    fig.add_trace(go.Scatter(
        x=x,
        y=[5, 15, None, 10, 5, 0, 10, None, 15, 5, 5, 10, 20, 15, 5],
        name='Gaps',
    ))

    # fig.show()
    return fig, "Connect Data Gaps"

def fig13():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([1, 3, 2, 3, 1])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, name="linear",
                        line_shape='linear'))
    fig.add_trace(go.Scatter(x=x, y=y + 5, name="spline",
                        text=["tweak line smoothness<br>with 'smoothing' in line object"],
                        hoverinfo='text+name',
                        line_shape='spline'))
    fig.add_trace(go.Scatter(x=x, y=y + 10, name="vhv",
                        line_shape='vhv'))
    fig.add_trace(go.Scatter(x=x, y=y + 15, name="hvh",
                        line_shape='hvh'))
    fig.add_trace(go.Scatter(x=x, y=y + 20, name="vh",
                        line_shape='vh'))
    fig.add_trace(go.Scatter(x=x, y=y + 25, name="hv",
                        line_shape='hv'))

    fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))

    # fig.show()
    return fig, "Interpolation with Line Plots"

def fig14():
    title = 'Main Source for News'
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
            showline=True,
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
    return fig, "Label Lines with Annotations"

def fig15():
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    x_rev = x[::-1]

    # Line 1
    y1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y1_upper = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    y1_lower = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y1_lower = y1_lower[::-1]

    # Line 2
    y2 = [5, 2.5, 5, 7.5, 5, 2.5, 7.5, 4.5, 5.5, 5]
    y2_upper = [5.5, 3, 5.5, 8, 6, 3, 8, 5, 6, 5.5]
    y2_lower = [4.5, 2, 4.4, 7, 4, 2, 7, 4, 5, 4.75]
    y2_lower = y2_lower[::-1]

    # Line 3
    y3 = [10, 8, 6, 4, 2, 0, 2, 4, 2, 0]
    y3_upper = [11, 9, 7, 5, 3, 1, 3, 5, 3, 1]
    y3_lower = [9, 7, 5, 3, 1, -.5, 1, 3, 1, -1]
    y3_lower = y3_lower[::-1]


    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x+x_rev,
        y=y1_upper+y1_lower,
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='Fair',
    ))
    fig.add_trace(go.Scatter(
        x=x+x_rev,
        y=y2_upper+y2_lower,
        fill='toself',
        fillcolor='rgba(0,176,246,0.2)',
        line_color='rgba(255,255,255,0)',
        name='Premium',
        showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=x+x_rev,
        y=y3_upper+y3_lower,
        fill='toself',
        fillcolor='rgba(231,107,243,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='Ideal',
    ))
    fig.add_trace(go.Scatter(
        x=x, y=y1,
        line_color='rgb(0,100,80)',
        name='Fair',
    ))
    fig.add_trace(go.Scatter(
        x=x, y=y2,
        line_color='rgb(0,176,246)',
        name='Premium',
    ))
    fig.add_trace(go.Scatter(
        x=x, y=y3,
        line_color='rgb(231,107,243)',
        name='Ideal',
    ))

    fig.update_traces(mode='lines')
    # fig.show()
    return fig, "Filled Lines"


if __name__ == "__main__":

    print("Tikzploty : ", tikzplotly.__version__)
    print("Plotly : ", plotly.__version__)
    print("Test line charts")

    file_directory = os.path.dirname(os.path.abspath(__file__))

    functions = [
        ("1", fig1),
        ("2", fig2),
        ("3", fig3),
        ("4", fig4),
        ("5", fig5),
        ("6", fig6),
        ("7", fig7),
        ("8", fig8),
        ("9", fig9),
        ("10", fig10),
        ("11", fig11),
        # ("12", fig12),
        ("14", fig14),
        ("15", fig15)
    ]

    main_tex_content = tex_create_document(options="twocolumn", compatibility="newest")
    main_tex_content += "\\usepackage[left=1cm, right=1cm, top=1cm, bottom=1cm]{geometry}\n"
    main_tex_content += "\\usetikzlibrary{pgfplots.dateplot}\n"
    main_tex_content += "\n"
    stack_env = []
    main_tex_content += tex_begin_environment("document", stack_env) + '\n'

    for i, f in functions:
        print(f"Figure {i}")
        fig, title = f()
        data = fig.data
        save_path = os.path.join(file_directory, "outputs", "test_line_charts", "fig{}.tex".format(i))
        tikzplotly.save(save_path, fig)
        main_tex_content += tex_begin_environment("figure", stack_env)
        main_tex_content += "  \\input{fig" + str(i) + ".tex}\n"
        main_tex_content += "  \\caption{" + title + "}\n"
        main_tex_content += tex_end_environment(stack_env) + '\n'

    main_tex_content += "\n" + tex_end_all_environment(stack_env)

    main_tex_path = os.path.join(file_directory, "outputs", "test_line_charts", "main.tex")
    print("Save main tex file : ", main_tex_path)
    with open(main_tex_path, "w") as f:
        f.write(main_tex_content)
