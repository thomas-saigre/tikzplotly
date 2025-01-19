---
title: Supported plots
subtitle: Convert plotly figures to tikz code
---


# Supported plots

The plots type supported by tikzplotly are presented in this page.


## Scatter plots

The code has been constructed to export (almost all) the figures of the page [Line Charts in Python](https://plotly.com/python/line-charts/) of Plotly documentation.

```python
import plotly.express as px
import tikzplotly

df = px.data.gapminder().query("continent=='Oceania'")
fig = px.line(df, x="year", y="lifeExp", color='country')

tikzplotly.save("line.tex", fig)
```
![Marker Style Example](../assets/examples/line_chart.png)


## Heat maps

The code has been constructed to export (almost all) the figures of the page [Heatmaps in Python](https://plotly.com/python/heatmaps/) of Plotly documentation.


```python
import plotly.express as px
import tikzplotly
fig = px.imshow([[1, 20, 30],
                [20, 1, 60],
                [30, 60, 1]])
tikzplotly.save("heatmap.tex", fig)
```

![Marker Style Example](../assets/examples/heatmap.png)
