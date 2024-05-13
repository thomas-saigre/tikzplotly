# Adapted from https://github.com/nschloe/tikzplotlib/blob/450712b4014799ec5f151f234df84335c90f4b9d/tests/helpers.py

import tikzplotly


# https://stackoverflow.com/a/845432/353337
def _unidiff_output(expected, actual):
    import difflib

    expected = expected.splitlines(1)
    actual = actual.splitlines(1)
    diff = difflib.unified_diff(expected, actual)
    return "".join(diff)

def assert_equality(fig, target_file, **kwargs):
    tikz_code = tikzplotly.get_tikz_code(fig, include_disclamer=False, **kwargs)


    with open(this_dir / target_file, encoding="utf-8") as f:
        reference = f.read()
    assert reference == tikz_code, target_file + "\n" + _unidiff_output(reference, tikz_code)
