---
title: Supported plots
subtitle: Convert plotly figures to TikZ code
---


# Supported plots

The plots type supported by tikzplotly are presented in this page.


## Scatter plots

The code has been constructed to export (almost all) the figures of the page [Line Charts in Python](https://plotly.com/python/line-charts/) of Plotly documentation.

??? example "Scatter plot Example"

    ```python
    import plotly.express as px
    import tikzplotly

    df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(df, x="year", y="lifeExp", color='country')

    tikzplotly.save("line.tex", fig)
    ```
    ![Scatter plot Example](../assets/examples/line_chart.png)


## Heat maps

The code has been constructed to export (almost all) the figures of the page [Heatmaps in Python](https://plotly.com/python/heatmaps/) of Plotly documentation.

??? example "Heatmap Example"
    ```python
    import plotly.express as px
    import tikzplotly
    fig = px.imshow([[1, 20, 30],
                    [20, 1, 60],
                    [30, 60, 1]])
    tikzplotly.save("heatmap.tex", fig)
    ```

    ![Heatmap Example](../assets/examples/heatmap.png)

!!! Note
    - If possible, TikzPlotly try to save the heatmap as a png of the smallest size possible, namely 1 pixel for each value of the heatmap. But in some case, such export does not work. In this case, the image is saved in the original size of the Plotly figure.


## Histograms

The examples of the page [Histograms in Python](https://plotly.com/python/histograms/) of Plotly documentation are supported.

??? example "Histogram Example"
    ```python
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill")
    tikzplotly.save("histogram.tex", fig)
    ```

    ![Histogram Example](../assets/examples/histogram.png)

!!! Note
    - There may be issues when many histograms are plotted on the same figure...