# Some differences between plotly ans pgfplots

We gather here some points that are different between a plotly figure and the corresponding ti*k*z figure generated with `tikzplotly`.

* Size of the objects: in plotly, the size is given in `px` unit, while in ti*k*z it is given in `pt`. A conversion is performed (`1 px = 0.75 pt`), but this still results in objects of different sizes.
* There are somes markers implemented in plotly that are not available in pgfplots (or at least not referenced in the [documentation](https://tikz.dev/pgfplots/reference-markers)). For more details, refer to the example [test_markers](../tests/test_markers.py). By defualt, the marker style `*` will be used.
* By default, the colors or the markers are not the same in plotly and pgfplots. For instance, if nothing is specified, plotly will always use a dot marker, while pgfplot will change for each trace.
* The order of displaying the traces may be unconsistent between plotly and pgfplots. For instance, for [this example](https://plotly.com/python/histograms/#several-histograms-for-the-different-values-of-one-column), the two traces are inverted.
* There may be issues when many histograms are plotted on the same figure...