"""
Contain the code to handle data in TikZ plots.
"""
import hashlib
import numpy as np
from ._utils import replace_all_digits, sanitize_text
from ._data import treat_data, post_treat_data

def hexid_to_alpha(num):
    """
    Converts a hexadecimal string or integer to an alphabetic representation using the letters A-P.
    Each hexadecimal digit (0-15) is mapped to a corresponding uppercase letter (A-P).

    Parameters
    ----------
    num : int or str
        The hexadecimal number to convert. Can be an integer or a string containing hexadecimal digits.

    Returns
    -------
        Alphabetic representation of the hexadecimal input, where each digit is replaced by a letter from A to P.

    Examples
    --------
    >>> hexid_to_alpha(255)
    'PP'
    >>> hexid_to_alpha('1a3')
    'ABD'
    """
    hexstr = str(num)
    table = "ABCDEFGHIJKLMNOP"
    return ''.join(table[int(c, 16)] for c in hexstr if c in "0123456789abcdef")

def index_to_letters(idx):
    """Convert an integer to a string like Excel columns: A, B, ..., Z, AA, AB, ..."""
    letters = ""
    while True:
        idx, rem = divmod(idx, 26)
        letters = chr(65 + rem) + letters  # 65 = ord('A')
        if idx == 0:
            break
        idx -= 1
    return letters

class Data:
    """Class to handle data in TikZ plots.
    """

    def __init__(self, name, x):
        """Initialize a Data object.

        Parameters
        ----------
        name
            name of the data
        x
            x_values of the data
        """
        self.name = name
        self.macro_name = "\\" + replace_all_digits(name)
        self.x = x
        self.y_label = []
        self.y_data = []

    def add_y_data(self, y, y_label=None):
        """Add y data to the Data object.
        Parameters
        ----------
        y
            y values of the data
        y_label, optional
            name of the y data, by default None
        Returns
        -------
            name of the y data in LaTeX
        """
        if y_label is not None and len(y_label) > 0:
            self.y_label.append(y_label)
        else:
            self.y_label.append(f"y{len(self.y_label)}")
        self.y_data.append(y)
        return self.y_label[-1]

class Data3D:
    """Handle 3D data in Tikz plots
    """
    def __init__(self, x, y, z, name):
        """Initialize the Data3D object

        Parameters
        ----------
        x
            x_values of the data
        y
            y_values of the data
        z
            z_values of the data
        name
            name of the data
        """
        self.x = np.array(x)
        self.y = np.array(y)
        self.z = np.array(z)
        if name:
            self.name = sanitize_text(name, keep_space=0)
        else:
            hash_digest = self.get_hash()
            self.name = f"data{hexid_to_alpha(hash_digest)}"
        self.z_name = "z"

    def get_hash(self, tolerance=1e-6):
        """
        Generates the unique hash corresponding to the data, up to tolerance
        """
        def normalize_float(value):
            return np.round(value / tolerance) * tolerance
        x_norm = normalize_float(self.x)
        y_norm = normalize_float(self.y)
        z_norm = normalize_float(self.z)
        hash_input = f"{x_norm}{y_norm}{z_norm}"
        return hashlib.md5(hash_input.encode()).hexdigest()


class DataContainer:
    """Container for data used in TikZ plots.
    """

    def __init__(self):
        self.data = []

    def add_data(self, x, y, name=None, y_label=None):
        """Add data to the container.

        Parameters
        ----------
        x
            x values of the data
        y
            y values of the data
        y_label, optional
            name of the y data, by default None
        name, optional
            name of the data, by default None

        Returns
        -------
            tuple (macro_name, y_label), where macro_name is the name of the data in LaTeX and y_label the name of the y data in LaTeX
        """
        for data in self.data:
            if len(data.x) != len(x):
                continue
            are_equals = data.x == x
            if isinstance(are_equals, bool):
                if are_equals:
                    y_label_val = data.add_y_data(y, y_label or name)
                    return data.macro_name, treat_data(y_label_val)
            elif hasattr(are_equals, "all") and are_equals.all():
                y_label_val = data.add_y_data(y, y_label or name)
                return data.macro_name, treat_data(y_label_val)
        data_to_add = Data(f"data{index_to_letters(len(self.data))}", x)
        y_label_val = data_to_add.add_y_data(y, y_label or name)
        self.data.append(data_to_add)
        return data_to_add.macro_name, treat_data(y_label_val)

    def add_data3d(self, x, y, z, name=None):
        """Add data to the container.

        Parameters
        ----------
        x
            x values of the data
        y
            y values of the data
        z
            z values of the data
        name, optional
            name of the data, by default None

        Returns
        -------
            tuple (macro_name, z_name), where macro_name is the name of the data in LaTeX and z_name the name of the z data in LaTeX
        """
        for data in self.data:
            if hasattr(data, "x") and hasattr(data, "y") and hasattr(data, "z"):
                if np.array_equal(data.x, x) and np.array_equal(data.y, y) and np.array_equal(data.z, z):
                    return data.name, data.z_name
        data_obj = Data3D(x, y, z, name)
        self.data.append(data_obj)
        return data_obj.name, data_obj.z_name

    def export_data(self):
        """Generate LaTeX code to export the data from DataContainer.

        Returns
        -------
            string of LaTeX code
        """
        export_string = ""

        for data in self.data:
            # 3D
            if hasattr(data, "z"):
                export_string += "\\pgfplotstableread{\n"
                export_string += "x y z\n"
                for x, y, z in zip(data.x, data.y, data.z):
                    export_string += f"{treat_data(x)} {treat_data(y)} {treat_data(z)}\n"
                export_string += f"}}{{\\{data.name}}}\n"

            # 2D
            else:
                export_string += "\\pgfplotstableread{\n"
                header = "x"
                if hasattr(data, "y_label") and data.y_label:
                    for label in data.y_label:
                        header += f" {treat_data(label)}"
                else:
                    header += " y"
                export_string += header + "\n"
                for i, x in enumerate(data.x):
                    row = [treat_data(x)]
                    for y_col in data.y_data:
                        row.append(treat_data(y_col[i]))
                    export_string += " ".join(row) + "\n"
                export_string += f"}}\\{data.name}\n"

        return post_treat_data(export_string)
