"""
Contain the code to handle data in TikZ plots.
"""
from ._utils import replace_all_digits, sanitize_text
from ._data import post_treat_data

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
            y_label = y_label.replace(" ", "_")
            self.y_label.append(y_label)
        else:
            self.y_label.append(f"y{len(self.y_label)}")
        self.y_data.append(y)
        return self.y_label[-1]

class DataContainer:
    """Container for data used in TikZ plots.
    """

    def __init__(self):
        self.data = []

    def add_data(self, x, y, y_label=None):
        """Add data to the container.

        Parameters
        ----------
        x
            x values of the data
        y
            y values of the data
        y_label, optional
            name of the y data, by default None

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
                    y_label = data.add_y_data(y, y_label)
                    return data.macro_name, y_label
            elif are_equals.all():
                if (data.x == x).all():
                    y_label = data.add_y_data(y, y_label)
                    return data.macro_name, y_label
        data_to_add = Data(f"data{len(self.data)}", x)
        y_label = data_to_add.add_y_data(y, y_label)
        self.data.append(data_to_add)
        return data_to_add.macro_name, sanitize_text(y_label)


    def export_data(self):
        """Generate LaTeX code to export the data from DataContainer.

        Returns
        -------
            string of LaTeX code
        """
        export_string = ""

        for data in self.data:
            export_string += "\\pgfplotstableread{"
            export_string += f"{sanitize_text(data.name)} {' '.join([sanitize_text(label) for label in data.y_label])}\n"
            for i, x_val in enumerate(data.x):
                export_string += f"{x_val} {' '.join([str(y[i]) for y in data.y_data])}\n"

            export_string += "}" + sanitize_text(data.macro_name) + "\n"

        return post_treat_data(export_string)
