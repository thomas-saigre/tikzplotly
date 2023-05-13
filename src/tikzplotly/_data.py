from warnings import warn

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
            - 'month' : data is a month
    """
    if isinstance(data, str):
        if len(data.split('-')) == 3:
            warn("Assuming this a a data, add \"\\usetikzlibrary{pgfplots.dateplot}\" to your tex preamble.")
            return 'date'
        elif data.lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',' september', 'october', 'november', 'december']:
            warn(f"Assuming data {data} is a month. This feature is experimental.")
            return 'month'
        else:
            warn(f"Data type of {data} is not supported yet.")
            return None
    else:
        return None