"""
This module contains the code to handle data types in TikZ using Plotly data.
"""
from warnings import warn
from ._utils import sanitize_text

def data_type(data):
    """Return the type of data, for special handling.

    Parameters
    ----------
    data
        string of data

    Returns
    -------
        Type of data, can be :
            - None : no special handling
            - 'date' : data is a date
            - 'string' : a symbolic data
    """
    if isinstance(data, str):
        if len(data.split('-')) == 3:
            warn("Assuming this is a date, add \"\\usetikzlibrary{pgfplots.dateplot}\" to your tex preamble.")
            return 'date'

        if data.lower() in ['january', 'february', 'march', 'april', 'may', 'june',
                            'july', 'august', 'september', 'october', 'november', 'december']:
            warn(f"Assuming data {data} is a month. This feature is experimental.")
            return 'month'
    return None

def treat_data(data_str):
    """Treat data for correct TeX display

    Parameters
    ----------
    data_str
        string of data to be treated

    Returns
    -------
        Sanitized TeX string
    """
    data_str = sanitize_text(str(data_str), keep_space=-1)
    if data_str.find(' ') !=- 1: # Add curly braces if space in string
        if not data_str.startswith("{") and not data_str.startswith("}"):
            data_str = "{" + data_str + "}"
            return data_str
    return data_str

def post_treat_data(data_str):
    """Post-treat the data string to replace all months with their corresponding number.
    Parameters
    ----------
    data_str
        string of data to post-treat
    Returns
    -------
        string of post-treated data
    """
    # data_str = replace_all_months(data_str)
    return data_str.replace("None", "nan")
