# Some differences between plotly ans pgfplots

We gather here some points that are different between a plotly figure and the corresponding Ti*k*Z figure generated with `tikzplotly`.

* Size of the objects: in plotly, the size is given in `px` unit, while in Ti*k*Z it is given in `pt`. A conversion is performed (`1 px = 0.75 pt`), but this still results in objects of different sizes.
* By default, the colors or the markers are not the same in plotly and pgfplots. For instance, if nothing is specified, plotly will always use a dot marker, while pgfplot will change for each trace.
* The order of displaying the traces may be unconsistent between plotly and pgfplots. For instance, for [this example](https://plotly.com/python/histograms/#several-histograms-for-the-different-values-of-one-column), the two traces are inverted.
* The angle of rotation is different between Plotly and Ti*k*Z, but the function Plotly ↦ Ti*k*Z is not know at this current point.
* When tricky names are used in symbolic expression (such as names with a space within), the space is removed by tisk plotly (*e.g.* the text `United Kingdom` in Plotly will be exported as `UnitedKindgon` in Ti*k*Z), fill free to update the exported file to render the figure you wish!