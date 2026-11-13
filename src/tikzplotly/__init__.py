"""
tikzplotly package initialization.

This module imports and exposes the package version, as well as the main
functions for generating and saving TikZ code from plotly figures.

Exports:
    get_tikz_code (Callable): Function to generate TikZ code from a plotly figure.
    save (Callable): Function to save TikZ code to a file.
    show (Callable): Function to show a figure in the browser, with a button exporting it to TikZ.

Importing the package also registers the ``"tikzplotly"`` Plotly renderer, so that
``fig.show(renderer="tikzplotly")`` adds the same button.
"""
from .__about__ import __version__, __author__, __license__, __description__
from ._save import get_tikz_code, save
from ._browser import show, TikzBrowserRenderer, register_renderer as _register_renderer

_register_renderer()

__all__ = ["__version__", "__author__", "__license__", "__description__", "get_tikz_code", "save",
           "show", "TikzBrowserRenderer"]
