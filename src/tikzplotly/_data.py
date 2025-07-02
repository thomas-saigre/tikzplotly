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
            - 'string' : a symbolic data
    """
    if isinstance(data, str):
        if len(data.split('-')) == 3:
            warn("Assuming this is a date, add \"\\usetikzlibrary{pgfplots.dateplot}\" to your tex preamble.")
            return 'date'
        else:
            warn(f"Data type of {data} is not supported yet.")
            return None
    else:
        return None

def treat_data(data_str): 
    if not isinstance(data_str, str):
        return data_str
    if data_str.find(' ') !=- 1: # Add curly braces if there space in string
        if not data_str.startswith("{") and not data_str.startswith("}"):
            data_str = "{" + data_str + "}"
            return data_str
    return data_str

def post_treat_data(data_str):
    return data_str.replace("None", "nan")
