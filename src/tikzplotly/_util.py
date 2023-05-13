def data_to_string(x_data, y_data):
    """Convert data to a string.

    Parameters
    ----------
    x_data : array-like
        x data
    y_data : array-like
        y data

    Returns
    -------
    str
        data string
    """
    data_str = ""
    for x, y in zip(x_data, y_data):
        data_str += f"{x} {y}\n"
    return data_str.replace("None", "nan")