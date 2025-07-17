# Add some tests

## Local tests

These tests are for development purpose, to ensure that the features that are developped are working as expected.
They are present in the directory `src/tests` and can be run with the following command, from the `src` directory.

```bash
python3 -m tests.test_<feature>
```

A file `test_<feature>.py` contains the plotly figures that are used to test the feature `<feature>`.
Each desired plot should be a function that returns the figure and a string that is the expected output:

```python
def fig1():
    fig = px.imshow([[1, 20, 30],
                    [20, 1, 60],
                    [30, 60, 1]])
    return fig, "Heatmaps with Plotly Express"
```

Then set a list `functions` that contains the list of all the plot functions that you want to test:

```python
    functions = [
        ("1", fig1),
        # ("2", fig2),  # you can comment a line to not run the test
        ("3", fig3)
    ]
```

Then the main function will run all the selected tests, and generate a TeX file in a subdirectory `outputs/test_<feature>`, named `main.tex`.
Compile this TeX file with your favorite LaTeX compiler to see the result.


## Tests for the CI

These tests are run on the CI to check that the generated LaTeX code is still the same after the modifications.
They are placed in the directory `tests` at the root of the repository.
When `tox` is run (see [here](contributing.md#run-the-tests-and-look-at-code-coverage)), they are the tests that are run, not the ones on the present section.

Here is an example of a test that is run on the CI:

```python
def plot_1():
    fig = px.imshow([[1, 20, 30],
                    [20, 1, 60],
                    [30, 60, 1]])
    return fig

def test_1():
    assert_equality(plot_1(), os.path.join(this_dir, test_name, test_name + "_1_reference.tex"))
```

The reference TeX code should be inserted in a file `test_<test_name>_<number>_reference.tex` in the directory `tests/<test_name>`.

!!! Note
    The reference code should not contain the header `% This file was created with tikzplotly version 0.1.7.`, as the version number is bound to change.
    This header can be hidden with the option `include_disclamer=False` in the function `tikzplotly.save`.