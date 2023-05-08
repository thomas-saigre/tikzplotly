from warnings import warn

def data_type(data):
    if isinstance(data, str):
        if len(data.split('-')) == 3:
            warn("Add \"\\usetikzlibrary{pgfplots.dateplot}\" to your tex preamble.")
            return 'date'
        else:
            warn(f"Data type of {data} is not supported yet.")
            return None
    else:
        return None