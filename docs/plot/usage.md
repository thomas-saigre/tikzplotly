# Usage

```python
import plotly.express as px
import tikzplotly

df = px.data.gapminder().query("continent == 'Oceania'")
fig = px.line(df, x='year', y='lifeExp', color='country', markers=True)
tikzplotly.save("example.tex", fig)
```

The arguments of the function `tikzplotly.save` are:

* `filename` (`str`): The name of the file where the ti*k*z code will be saved.
* `fig` (`plotly.graph_objs.Figure`): The figure to be saved.
* `tikz_options` (`str`, optional): The options to be passed to the `tikzpicture` environment. Default is `None`.
    For example `tikz_options="scale=0.5"` will scale the figure by a factor 0.5.
* `axis_options` (`str`, optional): Option that you would like to manually add to the `axis` environment.
* `include_disclamer` (`bool`, optional): If `True`, the line `% This file was created with tikzplotly version XXX.` is added at the head of the generated code. Default is `True`.
* `img_name` (`str`, optional): only for the export of [heatmaps](supported.md#heat-maps), the name of the image that will be saved. Default is `heatmap.png`.
* `decimate` (`int|None`, optional): only for the exports of scatter plots (in [2D](supported.md#scatter-plots) and [3D](supported.md#3d-scatter-plots)), reduce the number of data exported to only get the `decimate`-th ones (and the last one). If `None`, then all the data are exported. This is the default behavior.


## Export from the browser window

Instead of calling `tikzplotly.save` in your script, you can open the figure in your web browser with an _Export to TikZ_ button (:material-content-save:) added to the Plotly mode bar:


```py
import plotly.express as px
import tikzplotly

df = px.data.gapminder().query("continent == 'Oceania'")
fig = px.line(df, x='year', y='lifeExp', color='country', markers=True)
tikzplotly.show(fig, "example.tex", axis_options="width=10cm")
```

Each click on the button exports the figure *as currently displayed*: if you have zoomed in, the axis limits are exported (`xmin`, `xmax`...), and the traces hidden by clicking on the legend are left out.

The default filename is `figure.tex`.
No file is overwritten: if `example.tex` already exists, `example_1.tex`, `example_2.tex`... are used.
For a [heatmap](supported.md#Heat-maps), the image is saved next to the `.tex` file with the same name, unless `img_name` is given.


Importing tikzplotly also registers a Plotly renderer named `tikzplotly`, so the button can be added through the usual `fig.show`:

```python
import plotly.io as pio
import tikzplotly

fig.show(renderer="tikzplotly")         # for one figure
pio.renderers.default = "tikzplotly"    # for every fig.show() of the script
pio.renderers["tikzplotly"] = tikzplotly.TikzBrowserRenderer("out.tex", axis_options="width=10cm")              # to choose the file name and the options in that case
```


