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

rep_mounts = {"January": '1', 'February': '2', 'March': '3', 'April': '4', 'May': '5', 'June': '6', 'July': '7', 'August': '8', 'September': '9', 'October': '10', 'November': '11', 'December': '12',
              'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}
rep_mounts = dict((re.escape(k), v) for k, v in rep_mounts.items())
pattern_mounts = re.compile("|".join(rep_mounts.keys()))

def replace_all_mounts(text):
    """Replace all mounts in a string with their corresponding number.

    Parameters
    ----------
    text
        string to replace mounts in

    Returns
    -------
        string with mounts replaced by their corresponding number
    """
    return pattern_mounts.sub(lambda m: rep_mounts[re.escape(m.group(0))], text)


def sanitize_text(text: str, keep_space=False):
    """
    Sanitize the input text by removing or replacing unwanted characters.

    Parameters
    ----------
    text (str): The input text to be sanitized.
    keep_space (bool, optional): If True, spaces will be preserved in the sanitized text.
                                 If False, spaces will be removed. Defaults to False.

    Returns
    -------
    str: The sanitized text.
    """
    return "".join(sanitize_char(ch, keep_space=keep_space) for ch in text)

def sanitize_char(ch, keep_space=False):
    """
    Sanitize a character by converting it to a hexadecimal representation if it is a special character, non-ASCII, or non-printable.

    Parameters
    ----------
    ch (str): The character to sanitize.
    keep_space (bool, optional): If True, spaces will be kept as is. Defaults to False.

    Returns
    -------
    str: The sanitized character or its hexadecimal representation.
    """
    if keep_space and ch == " ": return " "
    if ch in "[]{}= ": return f"x{ord(ch):x}"
    # if not ascii, return hex
    if ord(ch) > 127: return f"x{ord(ch):x}"
    # if not printable, return hex
    if not ch.isprintable(): return f"x{ord(ch):x}"
    return ch

def sanitize_TeX_text(text: str):
    s = "".join(map(sanitize_TeX_char, text))
    special_chars = "[], "
    if any(c in s for c in special_chars):
        return "{" + s + "}"
    return s

def sanitize_TeX_char(ch):
    if ch in "_{}": return f"\\{ch}"
    # if not ascii, return hex
    if ord(ch) > 127:
        warnings.warn(f"Character {ch} has been replaced by \"x{ord(ch):x}\" in output file")
        return f"x{ord(ch):x}"
    # if not printable, return hex
    if not ch.isprintable():
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
    if floor(pt) == pt: return int(pt)
    else: return pt


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