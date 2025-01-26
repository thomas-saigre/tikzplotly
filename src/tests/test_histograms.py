# From https://plotly.com/python/histograms/
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np
import tikzplotly
import os
from warnings import warn
from tikzplotly._tex import tex_create_document, tex_begin_environment, tex_end_environment, tex_end_all_environment

def fig1():
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill")
    # fig.show()
    return fig, "Histogram of total bill"

def fig2():
    df = px.data.tips()
    # Here we use a column with categorical data
    fig = px.histogram(df, x="day")
    # fig.show()
    return fig, "Histogram of days"

def fig3():
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill", nbins=20)
    # fig.show()
    return fig, "Choose the number of bins"

def fig4():
    warn("NB: This example is quite not working because of the high number of different dates present in the data set")
    df = px.data.stocks()
    fig = px.histogram(df, x="date")
    fig.update_layout(bargap=0.2)
    # fig.show()
    return fig, "Histogram on date data"

def fig5():
    df = px.data.tips()
    fig = px.histogram(df, x="day", category_orders=dict(day=["Thur", "Fri", "Sat", "Sun"]))
    # fig.show()
    return fig, "Histograms on Categorical Data"

def fig6():
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill", histnorm='probability density')
    # fig.show()
    return fig, "Type of normalization"

def fig7():
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill",
                    title='Histogram of bills',
                    labels={'total_bill':'total bill'}, # can specify one label per df column
                    opacity=0.8,
                    log_y=True, # represent bars with log scale
                    color_discrete_sequence=['indianred'] # color of histogram bars
                    )
    # fig.show()
    return fig, "Aspect of the histogram plot"

def fig8():
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill", color="sex")
    # fig.show()
    return fig, "Several histograms for different values of one column"

def fig9():
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill", color="sex", marginal="rug", # can be `box`, `violin`
                       hover_data=df.columns)
    return fig, "Histograms with pattern shapes"

def fig10():
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill", y="tip", histfunc="avg", nbins=8, text_auto=True)
    return fig, "Adding text labels"

def fig11():
    np.random.seed(1)
    x = np.random.randn(500)
    fig = go.Figure(data=[go.Histogram(x=x)])
    return fig, "Basic Histogram"

def fig12():
    x = np.random.randn(500)
    fig = go.Figure(data=[go.Histogram(x=x, histnorm='probability')])
    return fig, "Normalized Histogram"

def fig13():
    y = np.random.randn(500)
    fig = go.Figure(data=[go.Histogram(y=y)])
    return fig, "Horizontal Histogram"

def fig14():

    x0 = np.random.randn(500)
    x1 = np.random.randn(500) + 1

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=x0))
    fig.add_trace(go.Histogram(x=x1))

    # Overlay both histograms
    fig.update_layout(barmode='overlay')
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.75)
    return fig, "Overlay Histograms"

def fig15():
    x0 = np.random.randn(500)
    x1 = np.random.randn(500)

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=x0))
    fig.add_trace(go.Histogram(x=x1))

    # The two histograms are drawn on top of another
    fig.update_layout(barmode='stack')
    return fig, "Stacked Histograms"

def fig16():
    x0 = np.random.randn(500)
    x1 = np.random.randn(500) + 1

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=x0,
        histnorm='percent',
        name='control', # name used in legend and hover labels
        xbins=dict( # bins used for histogram
            start=-4.0,
            end=3.0,
            size=0.5
        ),
        marker_color='#EB89B5',
        opacity=0.75
    ))
    fig.add_trace(go.Histogram(
        x=x1,
        histnorm='percent',
        name='experimental',
        xbins=dict(
            start=-3.0,
            end=4,
            size=0.5
        ),
        marker_color='#330C73',
        opacity=0.75
    ))

    fig.update_layout(
        title_text='Sampled Results', # title of plot
        xaxis_title_text='Value', # xaxis label
        yaxis_title_text='Count', # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1 # gap between bars of the same location coordinates
    )
    return fig, "Styled Histogram"

def fig17():
    numbers = ["5", "10", "3", "10", "5", "8", "5", "5"]
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=numbers, name="count", texttemplate="%{x}", textfont_size=20))
    return fig, "Histogram Bar Text"

def fig18():
    x = np.random.randn(500)
    fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True)])
    return fig, "Cumulative Histogram"

def fig19():
    x = ["Apples","Apples","Apples","Oranges", "Bananas"]
    y = ["5","10","3","10","5"]

    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="count", y=y, x=x, name="count"))
    fig.add_trace(go.Histogram(histfunc="sum", y=y, x=x, name="sum"))
    return fig, "Specify Aggregation Function"

def fig20():
    x = ['1970-01-01', '1970-01-01', '1970-02-01', '1970-04-01', '1970-01-02',
     '1972-01-31', '1970-02-13', '1971-04-19']

    fig = make_subplots(rows=3, cols=2)

    trace0 = go.Histogram(x=x, nbinsx=4)
    trace1 = go.Histogram(x=x, nbinsx = 8)
    trace2 = go.Histogram(x=x, nbinsx=10)
    trace3 = go.Histogram(x=x,
                        xbins=dict(
                        start='1969-11-15',
                        end='1972-03-31',
                        size='M18'), # M18 stands for 18 months
                        autobinx=False
                        )
    trace4 = go.Histogram(x=x,
                        xbins=dict(
                        start='1969-11-15',
                        end='1972-03-31',
                        size='M4'), # 4 months bin size
                        autobinx=False
                        )
    trace5 = go.Histogram(x=x,
                        xbins=dict(
                        start='1969-11-15',
                        end='1972-03-31',
                        size= 'M2'), # 2 months
                        autobinx = False
                        )

    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 1, 2)
    fig.append_trace(trace2, 2, 1)
    fig.append_trace(trace3, 2, 2)
    fig.append_trace(trace4, 3, 1)
    fig.append_trace(trace5, 3, 2)

    return fig, "Custom Binning"

def fig21():
    df = px.data.tips()
    fig = px.histogram(df, x="day").update_xaxes(categoryorder='total ascending')
    return fig, "Sort Histogram by Category Order"


if __name__ == "__main__":

    print("Tikzploty : ", tikzplotly.__version__)
    print("Plotly : ", plotly.__version__)
    print("Test histograms")


    file_directory = os.path.dirname(os.path.abspath(__file__))

    functions = [
        ("1", fig1),
        ("2", fig2),
        ("3", fig3),
        # ("4", fig4),
        ("5", fig5),
        ("6", fig6),
        ("7", fig7),
        ("8", fig8),
        # ("9", fig9),    # Trace type box is not yet supported
        # ("10", fig10),  # Text template is not supported yet.
        ("11", fig11),
        ("12", fig12),
        ("13", fig13),
        ("14", fig14),
        ("15", fig15),
        # ("16", fig16),  # Layout of this example not supported yet
        ("17", fig17),    # Text template is not supported yet.
        ("18", fig18),
        ("19", fig19),
        # ("20", fig20),  # Subplots not supported yet
        ("21", fig21)     # Category order not supported yet
    ]

    main_tex_content = tex_create_document(options="twocolumn", compatibility="newest")
    main_tex_content += "\\usepackage[left=1cm, right=1cm, top=1cm, bottom=1cm]{geometry}\n"
    main_tex_content += "\n"
    stack_env = []
    main_tex_content += tex_begin_environment("document", stack_env) + '\n'

    for i, f in functions:
        print(f"Figure {i}")
        fig, title = f()
        data = fig.data
        save_path = os.path.join(file_directory, "outputs", "test_histograms", "fig{}.tex".format(i))
        tikzplotly.save(save_path, fig)
        main_tex_content += tex_begin_environment("figure", stack_env)
        main_tex_content += "  \\input{fig" + str(i) + ".tex}\n"
        main_tex_content += "  \\caption{" + title + "}\n"
        main_tex_content += tex_end_environment(stack_env) + '\n'

    main_tex_content += "\n" + tex_end_all_environment(stack_env)

    main_tex_path = os.path.join(file_directory, "outputs", "test_histograms", "main.tex")
    print("Save main tex file : ", main_tex_path)
    with open(main_tex_path, "w") as f:
        f.write(main_tex_content)
