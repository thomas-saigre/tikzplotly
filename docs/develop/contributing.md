# Contributing

If there is a Plotly figure that you would like to convert to ti*k*z and is not [supported yet](../plot/supported.md) of if the generated LaTeX code is not correct, please open an issue.


[:octicons-issue-opened-16: Open Issue](https://github.com/thomas-saigre/tikzplotly/issues/new/choose){.md-button}

You can also submit a pull request with the desired feature or the correction of the issue.


## Development

The actual code maybe quite messy (is with your contribution you manage to improve it, I thank you in advance !).
The source code of the package are present in the directory `src/tikzplotly`, in which each file is dedicated to a specific feature of the library.

Some external packages are necessary to make tikzplotly work, that are specified in the `requirements.txt` file.
You can create a virtual environment and install the dependencies with the following commands:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add some tests

There are two types of tests:

- The tests that are run locally to make the development easier and see if the code is working as expected. More details are provided on [this page](tests.md#local-tests).
- Tests with a reference TeX code that will be run on the CI to check if the code is working well. More details are provided on [this page](tests.md#tests-for-the-ci).


## Run the tests and look at code coverage

To run the tests, you need to install the development dependencies with the following command :

```bash
tox -- --cov tikzplotly --cov-report html --cov-report term
```

The code coverage is available in the directory `htmlcov`.

!!! Tip "Note about coverage"
    The coverage CI is quite strict, so you need to cover all the modification to pass it.
    I found that tedious at first, but actually making it pass make me realize that there were some bogs in the code!

??? Info "Pytest"
    Some warnings are ignored by `pytest`, as they are intended for the user in some specific cases, that are not relevant in general test cases.
    This corresponds to:
    - the warning raised when [heat maps](../plot/supported/#heat-maps) PNG file is not resized (cf [issue comment](https://github.com/thomas-saigre/tikzplotly/issues/6#issuecomment-2106180586)),
    - warning for features that are not yet implemented (such as text templates, or `barpolar` plots).


## Documentation

Feel free to add some comments on this page, especially if there are some notable differences between plotly and pgfplots (see [this page](../plot/NB.md)).
These pages are written in Markdown and are present in the directory `docs`.
The site is build using [Mkdocs-materials](https://squidfunk.github.io/mkdocs-material/).
