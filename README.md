![logo-tikzplotly](https://raw.githubusercontent.com/thomas-saigre/tikzplotly/main/doc/img/logo.svg "Tikzplotly")

[![PyPi Version](https://img.shields.io/pypi/v/tikzplotly.svg?style=flat-square)](https://pypi.org/project/tikzplotly)

[![Issue](https://img.shields.io/github/issues-raw/thomas-saigre/tikzplotly?style=flat-square)](https://github.com/thomas-saigre/tikzplotly/issues)

# Tikzplotly

Convert [plotly](https://plotly.com/python/) figures to tikz code for inclusion into [PGFPlots](https://www.ctan.org/pkg/pgfplots) ([PGF/TikZ](https://www.ctan.org/pkg/pgf)) figures.

This results in a ti*k*z code, that can be easily included into your LaTeX document.
This also allow to easily edit the content of the figure.

## Example

The following Python code

```python
import plotly.express as px
import tikzplotly

df = px.data.gapminder().query("country=='Canada'")
fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
tikzplotly.save("example.tex", fig)
```

will result in the following ti*k*z code

```latex
% This file was created with tikzplotly version 0.0.1.
\begin{tikzpicture}

\definecolor{636efa}{HTML}{636efa}

\begin{axis}[
title=Life expectancy in Canada,
xlabel=year,
ylabel=lifeExp,
]
\addplot+ [mark=none, solid, color=636efa, forget plot] table {%
1952 68.75
1957 69.96
1962 71.3
1967 72.13
1972 72.88
1977 74.21
1982 75.76
1987 76.86
1992 77.95
1997 78.61
2002 79.77
2007 80.653
};
\end{axis}
\end{tikzpicture}
```

## Installation

Tikzplotly is available from the [Python Package Index](https://pypi.org/project/tikzplotly/), so it can be installed with `pip` :

```bash
pip install tikzplotly
```



## Note

* This module is in development and new features are added bit by bit, when needed. If you have a feature request, please open an issue with the plotly figure you want to convert and the desired output.
You can also submit a pull request with the desired feature !
* Some feature can result in different output between the plotly figure and the tikz figure, for instance the size of markers.


## References

* [plotly](https://plotly.com/python/)
* [PGFPlots](https://www.ctan.org/pkg/pgfplots) (with [manual](https://ctan.mines-albi.fr/graphics/pgf/contrib/pgfplots/doc/pgfplots.pdf))
* [PGF/TikZ](https://www.ctan.org/pkg/pgf)
* [tikzplotlib](https://github.com/nschloe/tikzplotlib) : a similar project for matplotlib figures from which this one is inspired.


## License

This project is licensed under the MIT [License](LICENSE).