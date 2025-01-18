# From https://plotly.com/python/histograms/
import plotly
import plotly.express as px
import plotly.graph_objects as go
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
        # ("9", fig9), # Trace type box is not yet supported
        # ("10", fig10),  # Text template is not supported yet.
        ("11", fig11),
        ("12", fig12),
        ("13", fig13),
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
