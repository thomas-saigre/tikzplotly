import re

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