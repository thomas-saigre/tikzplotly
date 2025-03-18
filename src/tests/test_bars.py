# From https://plotly.com/python/bar-charts/
import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np
import tikzplotly
import os
from warnings import warn
from tikzplotly._tex import tex_create_document, tex_begin_environment, tex_end_environment, tex_end_all_environment

def fig1():

    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(data_canada, x='year', y='pop')

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig1.png"))

    return fig, "Bar chart with Plotly Express"

def fig2():

    long_df = px.data.medals_long()

    fig = px.bar(long_df, x="nation", y="count", color="medal", title="Long-Form Input")

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig2.png"))

    return fig, "Bar charts with Long Format Data"

def fig3():

    wide_df = px.data.medals_wide()

    fig = px.bar(wide_df, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input")

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig3.png"))

    return fig, "Bar charts with Wide Format Data"

def fig5():

    df = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(df, x='year', y='pop',
                hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
                labels={'pop':'population of Canada'}, height=400)

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig5.png"))

    return fig, "Colored Bars"

def fig5bis():

    df = px.data.gapminder().query("continent == 'Oceania'")
    fig = px.bar(df, x='year', y='pop',
                hover_data=['lifeExp', 'gdpPercap'], color='country',
                labels={'pop':'population of Canada'}, height=400)

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig5bis.png"))
    
    return fig, "Colored Bars"

def fig6():

    df = px.data.tips()
    fig = px.bar(df, x="sex", y="total_bill", color='time')

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig6.png"))

    return fig, "Stacked vs Grouped Bars"

def fig6bis():

    df = px.data.tips()
    fig = px.bar(df, x="sex", y="total_bill",
                color='smoker', barmode='group',
                height=400)

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig6bis.png"))

    return fig, "Stacked vs Grouped Bars"

def fig7():

    df = px.data.tips()
    fig = px.histogram(df, x="sex", y="total_bill",
                color='smoker', barmode='group',
                height=400)

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig7.png"))

    return fig, "Aggregating into Single Colored Bars"

def fig7bis():

    df = px.data.tips()
    fig = px.histogram(df, x="sex", y="total_bill",
                color='smoker', barmode='group',
                histfunc='avg',
                height=400)

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig7bis.png"))

    return fig, "Aggregating into Single Colored Bars"

def fig8():

    df = px.data.medals_long()

    fig = px.bar(df, x="medal", y="count", color="nation", text_auto=True)

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig8.png"))

    return fig, "Bar Charts with Text"

def fig8bis():

    df = px.data.medals_long()

    fig = px.bar(df, x="medal", y="count", color="nation", text="nation")

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig8bis.png"))

    return fig, "Bar Charts with Text"

def fig8ter():

    df = px.data.gapminder().query("continent == 'Europe' and year == 2007 and pop > 2.e6")
    fig = px.bar(df, y='pop', x='country', text_auto='.2s',
                title="Default: various text sizes, positions and angles")

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig8ter.png"))

    return fig, "Bar Charts with Text"

def fig8quater():

    df = px.data.gapminder().query("continent == 'Europe' and year == 2007 and pop > 2.e6")
    fig = px.bar(df, y='pop', x='country', text_auto='.2s',
                title="Controlled text sizes, positions and angles")
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig8quater.png"))

    return fig, "Bar Charts with Text"

def fig9():

    df = px.data.medals_long()

    fig = px.bar(df, x="medal", y="count", color="nation",
                pattern_shape="nation", pattern_shape_sequence=[".", "x", "+"])

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig9.png"))

    return fig, "Pattern fills"

def fig10():
    animals=['giraffes', 'orangutans', 'monkeys']

    fig = go.Figure([go.Bar(x=animals, y=[20, 14, 23])])

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig10.png"))

    return fig, "Basic Bar Charts with plotly graph objects"

def fig11():
    animals=['giraffes', 'orangutans', 'monkeys']

    fig = go.Figure(data=[
        go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23]),
        go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig11.png"))

    return fig, "Grouped Bar Chart"

def fig12():
    animals=['giraffes', 'orangutans', 'monkeys']

    fig = go.Figure(data=[
        go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23]),
        go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29])
    ])
    # Change the bar mode
    fig.update_layout(barmode='stack')

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig12.png"))

    return fig, "Stacked Bar Chart"

def fig13():
    x = [1, 2, 3, 4]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=[1, 4, 9, 16]))
    fig.add_trace(go.Bar(x=x, y=[6, -8, -4.5, 8]))
    fig.add_trace(go.Bar(x=x, y=[-15, -3, 4.5, -8]))
    fig.add_trace(go.Bar(x=x, y=[-1, 3, -3, -4]))

    fig.update_layout(barmode='relative', title_text='Relative Barmode')

    # fig.show()
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "fig13.png"))

    return fig, "Bar Chart with Relative Barmode"


def figa():
    """
    Creates a simple vertical grouped bar chart with categorical x-values.
    We have two series of data, each with 7 categories.
    """
    categories = ["04bits", "08bits", "16bits", "24bits", "32bits", "48bits", "64bits"]
    fmax_chisel = [1147, 277, 256, 220, 207, 186, 179]
    fmax_sv     = [375, 270, 235, 212, 205, 192, 190]
    
    df = pd.DataFrame({
        "Category": categories,
        "ALU1": fmax_chisel,
        "ALU2": fmax_sv
    })

    fig = px.bar(df, x="Category", y=["ALU1", "ALU2"], barmode="group",
                 title="Simple Vertical Bar Chart Example")

    fig.update_layout(xaxis_title="Configuration", yaxis_title="Fmax (MHz)")

    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "figa.png"))

    return fig, "Simple vertical grouped bar chart"

def figb():
    """
    Creates a simple horizontal grouped bar chart with categorical y-values.
    We have two series of data, each with 7 categories.
    """
    categories = ["04bits", "08bits", "16bits", "24bits", "32bits", "48bits", "64bits"]
    fmax_chisel = [1147, 277, 256, 220, 207, 186, 179]
    fmax_sv     = [375, 270, 235, 212, 205, 192, 190]
    
    df = pd.DataFrame({
        "Category": categories,
        "ALU1": fmax_chisel,
        "ALU2": fmax_sv
    })

    fig = px.bar(df, x=["ALU1", "ALU2"], y="Category", barmode="group",
                 title="Simple Horizontal Bar Chart Example")

    fig.update_layout(xaxis_title="Fmax (MHz)", yaxis_title="Configuration")
    
    # fig.write_image(os.path.join(file_directory, "outputs", "test_bars", "figb.png"))
    
    return fig, "Simple horizontal grouped bar chart"

if __name__ == "__main__":

    print("Tikzploty : ", tikzplotly.__version__)
    print("Plotly : ", plotly.__version__)
    print("Test histograms")


    file_directory = os.path.dirname(os.path.abspath(__file__))

    functions = [
        ("1", fig1),
        ("2", fig2),
        ("3", fig3),
        ("5", fig5),
        ("5bis", fig5bis),
        ("6", fig6),              # Stacked bars are not supported yet.
        ("6bis", fig6bis),        # Stacked bars are not supported yet.
        ("7", fig7),              # Aggregated bars are not supported yet.
        ("7bis", fig7bis),        # Aggregated bars are not supported yet.
        ("8", fig8),              # Text template is not supported yet.
        ("8bis", fig8bis),        # Text template is not supported yet.
        ("8ter", fig8ter),        # Text template is not supported yet.
        ("8quater", fig8quater),  # Text template is not supported yet.
        ("9", fig9),              # Pattern fills are not supported yet.
        ("10", fig10),
        ("11", fig11),
        ("12", fig12),
        ("13", fig13),
        ("a", figa),
        ("b", figb),
    ]

    main_tex_content = tex_create_document(options="twocolumn", compatibility="newest")
    main_tex_content += "\\usepackage[left=1cm, right=1cm, top=1cm, bottom=1cm]{geometry}\n"
    main_tex_content += "\n"
    stack_env = []
    main_tex_content += tex_begin_environment("document", stack_env) + '\n'

    output_path = os.path.join(file_directory, "outputs", "test_bars")
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for i, f in functions:
        print(f"Figure {i}")
        fig, title = f()
        data = fig.data
        save_path = os.path.join(file_directory, "outputs", "test_bars", "fig{}.tex".format(i))
        tikzplotly.save(save_path, fig)
        main_tex_content += tex_begin_environment("figure", stack_env)
        main_tex_content += "  \\input{fig" + str(i) + ".tex}\n"
        main_tex_content += "  \\caption{" + title + "}\n"
        main_tex_content += tex_end_environment(stack_env) + '\n'

    main_tex_content += "\n" + tex_end_all_environment(stack_env)

    main_tex_path = os.path.join(file_directory, "outputs", "test_bars", "main.tex")
    print("Save main tex file : ", main_tex_path)
    with open(main_tex_path, "w") as f:
        f.write(main_tex_content)
