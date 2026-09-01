# From https://plotly.com/python/heatmaps/
import os
import tikzplotly

from tikzplotly._tex import tex_create_document, tex_begin_environment, tex_end_environment, tex_end_all_environment

import plotly
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import datetime
np.random.seed(1)

def fig1():
    fig = px.imshow([[1, 20, 30],
                    [20, 1, 60],
                    [30, 60, 1]])
    # fig.show()
    return fig, "Heatmaps with Plotly Express"

def fig2():
    df = px.data.medals_wide(indexed=True)
    fig = px.imshow(df)
    # fig.show()
    return fig, "Heatmaps with Plotly Express 2"

def fig3():
    z = [[.1, .3, .5, .7, .9],
        [1, .8, .6, .4, .2],
        [.2, 0, .5, .7, .9],
        [.9, .8, .4, .2, 0],
        [.3, .4, .5, .7, 1]]

    fig = px.imshow(z, text_auto=True)
    # fig.show()
    return fig, "Displaying Text on Heatmaps"

def fig4():
    z = [[.1, .3, .5, .7, .9],
     [1, .8, .6, .4, .2],
     [.2, 0, .5, .7, .9],
     [.9, .8, .4, .2, 0],
     [.3, .4, .5, .7, 1]]

    fig = px.imshow(z, text_auto=True, aspect="auto")
    # fig.show()
    return fig, "Controlling Aspect Ratio"

def fig5():
    data=[[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
    fig = px.imshow(data,
                    labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
                    x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                    y=['Morning', 'Afternoon', 'Evening']
                )
    fig.update_xaxes(side="top")
    # fig.show()
    return fig, "Customizing the axes and labels on a heatmap"

def fig6():

    fig = go.Figure(data=go.Heatmap(
                        z=[[1, 20, 30],
                        [20, 1, 60],
                        [30, 60, 1]]))
    # fig.show()
    return fig, "Basic Heatmap with plotly.graph\\_objects"

def fig7():
    fig = go.Figure(data=go.Heatmap(
                   z=[[1, None, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, -10, 20]],
                   x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                   y=['Morning', 'Afternoon', 'Evening'],
                   hoverongaps = False))
    # fig.show()
    return fig, "Heatmap with Categorical Axis Labels"

def fig8():
    import plotly.graph_objects as go

    # Build the rectangles as a heatmap
    # specify the edges of the heatmap squares
    phi = (1 + np.sqrt(5) )/2. # golden ratio
    xe = [0, 1, 1+(1/(phi**4)), 1+(1/(phi**3)), phi]
    ye = [0, 1/(phi**3), 1/phi**3+1/phi**4, 1/(phi**2), 1]

    z = [ [13,3,3,5],
        [13,2,1,5],
        [13,10,11,12],
        [13,8,8,8]
        ]

    fig = go.Figure(data=go.Heatmap(
            x = np.sort(xe),
            y = np.sort(ye),
            z = z,
            type = 'heatmap',
            colorscale = 'Viridis'))

    # Add spiral line plot

    def spiral(th):
        a = 1.120529
        b = 0.306349
        r = a*np.exp(-b*th)
        return (r*np.cos(th), r*np.sin(th))

    theta = np.linspace(-np.pi/13,4*np.pi,1000); # angle
    (x,y) = spiral(theta)

    fig.add_trace(go.Scatter(x= -x+x[0], y= y-y[0],
        line =dict(color='white',width=3)))

    axis_template = dict(range = [0,1.6], autorange = False,
                showgrid = False, zeroline = False,
                linecolor = 'black', showticklabels = False,
                ticks = '' )

    fig.update_layout(margin = dict(t=200,r=200,b=200,l=200),
        xaxis = axis_template,
        yaxis = axis_template,
        showlegend = False,
        width = 700, height = 700,
        autosize = False )

    # fig.show()
    return fig, "Heatmap with Unequal Block Sizes"


def fig9():
    import plotly.graph_objects as go


    programmers = ['Alex','Nicole','Sara','Etienne','Chelsea','Jody','Marianne']

    base = datetime.datetime.today()
    dates = base - np.arange(180) * datetime.timedelta(days=1)
    z = np.random.poisson(size=(len(programmers), len(dates)))

    fig = go.Figure(data=go.Heatmap(
            z=z,
            x=dates,
            y=programmers,
            colorscale='Viridis'))

    fig.update_layout(
        title='GitHub commits per day',
        xaxis_nticks=36)

    # fig.show()
    return fig, "Heatmap with Datetime Axis"


def fig11():    # from @JasonGross, see issue https://github.com/thomas-saigre/tikzplotly/issues/6
    data = np.random.rand(10,10)
    fig = px.imshow(data, color_continuous_scale='Viridis', title='Heatmap Example with Plotly Express')
    # fig.show()
    return fig, "Heatmap Example with Plotly Express"

if __name__ == "__main__":

    print("Tikzploty : ", tikzplotly.__version__)
    print("Plotly : ", plotly.__version__)
    print("Test line charts")

    file_directory = os.path.dirname(os.path.abspath(__file__))

    functions = [
        ("1", fig1),
        ("2", fig2),
        # ("3", fig3),          # texttemplate not supported
        ("4", fig4),
        ("5", fig5),
        ("6", fig6),
        ("7", fig7),
        # ("8", fig8),          # Not supported
        ("9", fig9),
        ("11", fig11)
    ]

    main_tex_content = tex_create_document(options="twocolumn", compatibility="newest")
    main_tex_content += "\\usepackage[left=1cm, right=1cm, top=1cm, bottom=1cm]{geometry}\n"
    main_tex_content += "\n"
    stack_env = []
    main_tex_content += tex_begin_environment("document", stack_env) + '\n'

    for i, f in functions:
        print(f"Figure {i}")
        fig, title = f()
        save_path = os.path.join(file_directory, "outputs", "test_heatmap", "fig{}.tex".format(i))
        tikzplotly.save(save_path, fig, img_name=os.path.join(file_directory, "outputs", "test_heatmap", "fig{}.png".format(i)))
        main_tex_content += tex_begin_environment("figure", stack_env)
        main_tex_content += "  \\input{fig" + str(i) + ".tex}\n"
        main_tex_content += "  \\caption{" + title + "}\n"
        main_tex_content += tex_end_environment(stack_env) + '\n'

    main_tex_content += "\n" + tex_end_all_environment(stack_env)

    main_tex_path = os.path.join(file_directory, "outputs", "test_heatmap", "main.tex")
    print("Save main tex file : ", main_tex_path)
    with open(main_tex_path, "w") as f:
        f.write(main_tex_content)
