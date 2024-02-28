# Some differences between plotly ans pgfplots

We gather here some points that are different between a plotly figure and the corresponding ti*k*z figure generated with `tikzplotly`.

* Size of the objects: in plotly, the size is given in `px` unit, while in ti*k*z it is given in `pt`. A conversion is performed (`1 px = 0.75 pt`), but this still objects of different times.
* There are somes markers implemented in plotly that are not available in pgfplots (or at least not referenced in the [documentation](https://tikz.dev/pgfplots/reference-markers)). For more details, refer to the example [test_markers](../tests/test_markers.py). By defualt, the marker style `*` will be used.