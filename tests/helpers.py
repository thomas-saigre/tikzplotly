# Adapted from https://github.com/nschloe/tikzplotlib/blob/450712b4014799ec5f151f234df84335c90f4b9d/tests/helpers.py

import tikzplotly
import re
from math import isclose


# https://stackoverflow.com/a/845432/353337
def _unidiff_output(expected, actual):
    import difflib

    expected = expected.splitlines(1)
    actual = actual.splitlines(1)
    diff = difflib.unified_diff(expected, actual)
    return "".join(diff)

def extract_floats_from_string(s):
    """Extract all floating-point numbers from a string."""
    float_pattern = re.compile(r"[-+]?\d*\.\d+|\d+")
    floats = [float(num) for num in float_pattern.findall(s)]
    return floats

def assert_equality(fig, target_file, tolerance=1e-9, **kwargs):
    tikz_code = tikzplotly.get_tikz_code(fig, include_disclamer=False, **kwargs)

    with open(target_file, encoding="utf-8") as f:
        reference = f.read()

    reference_floats = extract_floats_from_string(reference)
    tikz_floats = extract_floats_from_string(tikz_code)

    if len(reference_floats) != len(tikz_floats):
        assert False, "Number of floats in the reference and tikz code differ.\n" + _unidiff_output(reference, tikz_code)

    for ref, tikz in zip(reference_floats, tikz_floats):
        if not isclose(ref, tikz, rel_tol=tolerance, abs_tol=tolerance):
            assert False, f"Values differ: {ref} vs {tikz}\n" + _unidiff_output(reference, tikz_code)

    # If all floating-point comparisons pass, ensure the structures are the same.
    reference_non_floats = re.sub(r"[-+]?\d*\.\d+|\d+", "FLOAT", reference)
    tikz_non_floats = re.sub(r"[-+]?\d*\.\d+|\d+", "FLOAT", tikz_code)

    assert reference_non_floats == tikz_non_floats, target_file + "\n" + _unidiff_output(reference, tikz_code)

