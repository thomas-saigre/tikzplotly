"""
tikzplotly package initialization.

This module imports and exposes the package version, as well as the main
functions for generating and saving TikZ code from plotly figures.

Exports:
    get_tikz_code (Callable): Function to generate TikZ code from a plotly figure.
    save (Callable): Function to save TikZ code to a file.
"""
from .__about__ import __version__, __author__, __license__, __description__
from ._save import get_tikz_code, save

__all__ = ["__version__", "__author__", "__license__", "__description__", "get_tikz_code", "save"]
