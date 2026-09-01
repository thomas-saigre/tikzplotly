# https://plotly.com/python/filled-area-plots/
import plotly.express as px
import plotly.graph_objects as go

import os
import tikzplotly, plotly
from tikzplotly._tex import tex_create_document, tex_begin_environment, tex_end_environment, tex_end_all_environment


def f1():
    df = px.data.gapminder()
    fig = px.area(df, x="year", y="pop", color="continent", line_group="country")
    # fig.show()
    return fig, "Filled area plot with plotly.express"

def f2():
    df = px.data.medals_long()
    fig = px.area(df, x="medal", y="count", color="nation",
                pattern_shape="nation", pattern_shape_sequence=[".", "x", "+"])
    # fig.show()
    return fig, "Pattern Fills"

def f3():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[0, 2, 3, 5], fill='tozeroy')) # fill down to xaxis
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[3, 5, 1, 7], fill='tonexty')) # fill to trace0 y
    # fig.show()
    return fig, "Basic Overlaid Area Chart"

def f4():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[0, 2, 3, 5], fill='tozeroy',
                        mode='none' # override default markers+lines
                        ))
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[3, 5, 1, 7], fill='tonexty',
                        mode= 'none'))
    # fig.show()
    return fig, "Overlaid Area Chart Without Boundary Lines"

def f5():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[3, 4, 8, 3],
        fill=None,
        mode='lines',
        line_color='indigo',
        ))
    fig.add_trace(go.Scatter(
        x=[1, 2, 3, 4],
        y=[1, 6, 2, 6],
        fill='tonexty', # fill area between trace0 and trace1
        mode='lines', line_color='indigo'))
    # fig.show()
    return fig, "Interior Filling for Area Chart"

def f6():
    x=['Winter', 'Spring', 'Summer', 'Fall']

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=[40, 60, 40, 10],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(131, 90, 241)'),
        stackgroup='one' # define stack group
    ))
    fig.add_trace(go.Scatter(
        x=x, y=[20, 10, 10, 60],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=[40, 30, 50, 30],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(184, 247, 212)'),
        stackgroup='one'
    ))

    fig.update_layout(yaxis_range=(0, 100))
    # fig.show()
    return fig, "Stacked Area Chart"

def f7():
    x=['Winter', 'Spring', 'Summer', 'Fall']
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x, y=[40, 20, 30, 40],
        mode='lines',
        line=dict(width=0.5, color='rgb(184, 247, 212)'),
        stackgroup='one',
        groupnorm='percent' # sets the normalization for the sum of the stackgroup
    ))
    fig.add_trace(go.Scatter(
        x=x, y=[50, 70, 40, 60],
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=[70, 80, 60, 70],
        mode='lines',
        line=dict(width=0.5, color='rgb(127, 166, 238)'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=[100, 100, 100, 100],
        mode='lines',
        line=dict(width=0.5, color='rgb(131, 90, 241)'),
        stackgroup='one'
    ))

    fig.update_layout(
        showlegend=True,
        xaxis_type='category',
        yaxis=dict(
            type='linear',
            range=[1, 100],
            ticksuffix='%'))

    # fig.show()
    return fig, "Stacked Area Chart with Normalized Values"

def f8():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0,0.5,1,1.5,2], y=[0,1,2,1,0],
                        fill='toself', fillcolor='darkviolet',
                        hoveron = 'points+fills', # select where hover is active
                        line_color='darkviolet',
                        text="Points + Fills",
                        hoverinfo = 'text+x+y'))

    fig.add_trace(go.Scatter(x=[3,3.5,4,4.5,5], y=[0,1,2,1,0],
                        fill='toself', fillcolor = 'violet',
                        hoveron='points',
                        line_color='violet',
                        text="Points only",
                        hoverinfo='text+x+y'))

    fig.update_layout(
        title = "hover on <i>points</i> or <i>fill</i>",
        xaxis_range = [0,5.2],
        yaxis_range = [0,3]
    )

    # fig.show()
    return fig, "Hover on Points or Fill"



if __name__ == "__main__":

    print("Tikzploty : ", tikzplotly.__version__)
    print("Plotly : ", plotly.__version__)
    print("Test line charts")

    file_directory = os.path.dirname(os.path.abspath(__file__))

    functions = [
        f1,
        f2,
        f3,
        f4,
        f5,
        f6,
        f7,
        f8,
    ]
    NbFigures = len(functions)

    main_tex_content = tex_create_document(options="twocolumn", compatibility="newest")
    main_tex_content += "\\usepackage[left=1cm, right=1cm, top=1cm, bottom=1cm]{geometry}\n"
    main_tex_content += "\\usetikzlibrary{pgfplots.dateplot}\n"
    main_tex_content += "\n"
    stack_env = []
    main_tex_content += tex_begin_environment("document", stack_env) + '\n'

    if not os.path.exists(os.path.join(file_directory, "outputs", "test_area_plots")):
        os.makedirs(os.path.join(file_directory, "outputs", "test_area_plots"))

    for i, f in enumerate(functions):
        print(f"Figure {i+1} / {NbFigures}")
        fig, title = f()
        data = fig.data
        save_path = os.path.join(file_directory, "outputs", "test_area_plots", "fig{}.tex".format(i+1))
        tikzplotly.save(save_path, fig)
        main_tex_content += tex_begin_environment("figure", stack_env)
        main_tex_content += "  \\input{fig" + str(i+1) + ".tex}\n"
        main_tex_content += "  \\caption{" + title + "}\n"
        main_tex_content += tex_end_environment(stack_env) + '\n'

    main_tex_content += "\n" + tex_end_all_environment(stack_env)

    main_tex_path = os.path.join(file_directory, "outputs", "test_area_plots", "main.tex")
    print("Save main tex file : ", main_tex_path)
    with open(main_tex_path, "w") as f:
        f.write(main_tex_content)