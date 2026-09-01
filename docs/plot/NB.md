# Some differences between Plotly ans pgfplots

We gather here some points that are different between a Plotly figure and the corresponding Ti*k*Z figure generated with `tikzplotly`.

* Size of the objects: in Plotly, the size is given in `px` unit, while in Ti*k*Z it is given in `pt`. A conversion is performed (`1 px = 0.75 pt`), but this still results in objects of different sizes.
* By default, the colors or the markers are not the same in Plotly and pgfplots. For instance, if nothing is specified, Plotly will always use a dot marker, while pgfplots will change for each trace.
* The order of displaying the traces may be inconsistent between Plotly and pgfplots. For instance, for [this example](https://Plotly.com/python/histograms/#several-histograms-for-the-different-values-of-one-column), the two traces are inverted.
* The angle of rotation is different between Plotly and Ti*k*Z, but the function Plotly ↦ Ti*k*Z is not known at this current point.
* When tricky names are used in symbolic expression (such as names with a space within), the space is removed by tikzplotly (*e.g.* the text `United Kingdom` in Plotly will be exported as `UnitedKindgon` in Ti*k*Z), fill free to update the exported file to render the figure you wish!
