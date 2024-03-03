![logo-tikzplotly](https://raw.githubusercontent.com/thomas-saigre/tikzplotly/main/doc/img/logo.svg "Tikzplotly")

[![PyPi Version](https://img.shields.io/pypi/v/tikzplotly.svg?style=flat-square)](https://pypi.org/project/tikzplotly)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/tikzplotly.svg?style=flat-square)](https://pypi.org/pypi/tikzplotly/)

[![Issue](https://img.shields.io/github/issues-raw/thomas-saigre/tikzplotly?style=flat-square)](https://github.com/thomas-saigre/tikzplotly/issues)

# Tikzplotly

Convert [plotly](https://plotly.com/python/) figures to tikz code for inclusion into [PGFPlots](https://www.ctan.org/pkg/pgfplots) ([PGF/TikZ](https://www.ctan.org/pkg/pgf)) figures.

This results in a ti*k*z code, that can be easily included into your LaTeX document.
This also allows to easily edit the content of the figure.

## Example

The following Python code

```python
import plotly.express as px
import tikzplotly

df = px.data.gapminder().query("continent == 'Oceania'")
fig = px.line(df, x='year', y='lifeExp', color='country', markers=True)
tikzplotly.save("example.tex", fig)
```

will result in the following ti*k*z code

```latex
\pgfplotstableread{data0 Australia New_Zealand
1952 69.12 69.39
1957 70.33 70.26
1962 70.93 71.24
1967 71.1 71.52
1972 71.93 71.89
1977 73.49 72.22
1982 74.74 73.84
1987 76.32 74.32
1992 77.56 76.33
1997 78.83 77.55
2002 80.37 79.11
2007 81.235 80.204
}\dataZ

\begin{tikzpicture}

\definecolor{636efa}{HTML}{636efa}
\definecolor{EF553B}{HTML}{EF553B}

\begin{axis}[
xlabel=year,
ylabel=lifeExp,
]
\addplot+ [mark=*, solid, color=636efa, mark options={solid, draw=636efa}] table[y=Australia] {\dataZ};
\addlegendentry{Australia}
\addplot+ [mark=*, solid, color=EF553B, mark options={solid, draw=EF553B}] table[y=New_Zealand] {\dataZ};
\addlegendentry{New Zealand}
\end{axis}
\end{tikzpicture}
```

## Installation

Tikzplotly is available from the [Python Package Index](https://pypi.org/project/tikzplotly/), so it can be installed with `pip` :

```bash
pip install tikzplotly
```

## Usage

1. Generate the figure with Plotly,
2. Invoke `tikzplotly` to convert the figure to ti*k*z code :
```py
import tikzplotly

tikzplotly.save("figure.tex", fig)
```
3. Add the content of the generated file `figure.tex` to your LaTeX document :
```latex
\input{figure.tex}
```
To correctly compile the document, you will need to add the following packages to your preamble :
```latex
\usepackage{pgfplots}
\pgfplotsset{compat=newest}
```


## Note

* This module is in development and new features are added bit by bit, when needed. If you have a feature request, please open an issue with the plotly figure you want to convert and the desired output.
You can also submit a pull request with the desired feature !
* Some feature can result in different output between the plotly figure and the tikz figure, for instance the size of markers.
* More details in [doc/NB.md](doc/NB.md).


## References

* [plotly](https://plotly.com/python/)
* [PGFPlots](https://www.ctan.org/pkg/pgfplots) (with [manual](https://ctan.mines-albi.fr/graphics/pgf/contrib/pgfplots/doc/pgfplots.pdf))
* [PGF/TikZ](https://www.ctan.org/pkg/pgf)
* [tikzplotlib](https://github.com/nschloe/tikzplotlib) : a similar project for matplotlib figures from which this one is inspired.


## License

This project is licensed under the MIT [License](LICENSE).