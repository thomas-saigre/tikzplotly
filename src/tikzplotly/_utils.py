"""Utility functions for string sanitization, digit and month replacement, LaTeX formatting, and TikZ option formatting.

This module provides helper functions for:
- Replacing digits in strings with corresponding letter codes.
- Replacing month names with their numeric representations.
- Sanitizing text and characters for safe usage in file names or LaTeX.
- Converting pixel units to points.
- Formatting option dictionaries for TikZ.
- Generating tick strings for axis labeling.
"""
import re
import warnings
from math import floor
import numpy as np

rep_digit = {'0': 'Z', '1': 'O', '2': 'T', '3': 'Th', '4': 'F', '5': 'Fi', '6': 'S', '7': 'Se', '8': 'E', '9': 'N'}
rep_digit = dict((re.escape(k), v) for k, v in rep_digit.items())
pattern_digit = re.compile("|".join(rep_digit.keys()))

def replace_all_digits(text):
    """Replace all digits in a string with their corresponding letter.

    Parameters
    ----------
    text
        string to replace digits in

    Returns
    -------
        string with digits replaced by their corresponding letter
    """
    return pattern_digit.sub(lambda m: rep_digit[re.escape(m.group(0))], text)

rep_months = {"January": '1', 'February': '2', 'March': '3', 'April': '4', 'May': '5', 'June': '6',
              'July': '7', 'August': '8', 'September': '9', 'October': '10', 'November': '11', 'December': '12',
              'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
              'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}
rep_months = dict((re.escape(k), v) for k, v in rep_months.items())
pattern_months = re.compile("|".join(rep_months.keys()))

def replace_all_months(text):
    """Replace all months in a string with their corresponding number.

    Parameters
    ----------
    text
        string to replace months in

    Returns
    -------
        string with months replaced by their corresponding number
    """
    return pattern_months.sub(lambda m: rep_months[re.escape(m.group(0))], text)

def sanitize_text(text: str, keep_space: int = 0) -> str:
    """
    Sanitize the input text by removing or replacing unwanted characters.

    Parameters
    ----------
    text : str
        The input text to be sanitized.
    keep_space : int, optional
        If 1, spaces will be preserved in the sanitized text.
        If 0, spaces will be replaced with underscores. Defaults to 0.
        If -1, spaces will be deleted from the text

    Returns
    -------
    str
        The sanitized text.
    """
    return ''.join(sanitize_char(ch, keep_space) for ch in text)

def sanitize_char(ch: str, keep_space: int = 0) -> str:
    """
    Sanitize a character by escaping special characters or converting to hex if non-ASCII/non-printable.

    Parameters
    ----------
    ch : str
        The character to sanitize.
    keep_space : int, optional
        If 1, spaces will be preserved in the sanitized text.
        If 0, spaces will be replaced with underscores. Defaults to 0.
        If -1, spaces will be deleted from the text

    Returns
    -------
    str
        The sanitized character.
    """
    if ch == "@":
        return "at"
    if ch == " ":
        if keep_space == 1:
            return " "
        if keep_space == 0:
            return "_"
        return ""
    if ch in "[]{}= ":
        return f"x{ord(ch):x}"
    # if not ascii, return hex
    if ord(ch) > 127:
        return f"x{ord(ch):x}"
    # if not printable, return hex
    if not ch.isprintable():
        return f"x{ord(ch):x}"
    return ch

def sanitize_tex_text(text: str):
    """
    Sanitize a string for LaTeX, escaping special characters and ensuring proper formatting.

    Parameters
    ----------
    text : str
        The input text to be sanitized.

    Returns
    -------
    str
        The sanitized text, with special characters escaped and formatted for LaTeX.
    """
    sanitized = "".join(map(sanitize_tex_char, text))
    special_chars = "[],"
    if any(c in sanitized for c in special_chars):
        return "{" + sanitized + "}"
    return sanitized

def sanitize_tex_char(ch: str) -> str:
    """
    Sanitize a character for LaTeX.

    Parameters
    ----------
    ch : str
        Character to sanitize.
    Returns
    -------
    str
        Character sanitized for LaTeX.
    """
    if ch in "_{}":
        return f"\\{ch}"
    if ord(ch) > 127 or not ch.isprintable():
        warnings.warn(f"Character {ch} has been replaced by \"x{ord(ch):x}\" in output file")
        return f"x{ord(ch):x}"
    return ch

def px_to_pt(px):
    """Convert size in pixel to a size in point

    Parameters
    ----------
    px
        size in pixel

    Returns
    -------
    float
        size in point
    """
    pt = px * .75
    if floor(pt) == pt:
        return int(pt)
    return pt

def option_dict_to_str(options_dict, sep=" "):
    """Convert a dictionary of options to a string of options for TikZ.

    Parameters
    ----------
    options_dict
        dictionary of options
    sep, optional
        separator between options, by default " "

    Returns
    -------
    string
        string of options for TikZ
    """
    options = ""
    for key, value in options_dict.items():
        if value is None:
            options += f"{key},{sep}"
        else:
            options += f"{key}={value},{sep}"
    if options == "":
        return None
    return options.strip()[:-1]

def get_ticks_str(data, nticks=None):
    """Get the ticks and ticklabels for the axis.

    Parameters
    ----------
    data
        data to be plotted
    nticks
        number of ticks

    Returns
    -------
    tuple
        ticks and ticklabels

    Examples
    --------
    >>> get_ticks_str(["Sun", "Sat", "Thur", "Fri"])
    ({0,1,2,3}, {"Sun", "Sat", "Thur", "Fri"})
    """
    indices = np.arange(len(data))
    if nticks is not None:
        data_ = data[::len(data)//(nticks-1)]
        data = np.append(data_, [data[-1]])
        indices_ = indices[::len(indices)//(nticks-1)]
        indices = np.append(indices_, [indices[-1]])

    ticks = "{"
    ticklabels = "{"
    for i, val in zip(indices, data):
        ticks += str(i) + ","
        ticklabels += str(val) + ","
    ticks = ticks[:-1] + "}"
    ticklabels = ticklabels[:-1] + "}"

    return ticks, ticklabels
