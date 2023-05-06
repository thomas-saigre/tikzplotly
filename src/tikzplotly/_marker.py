
marker_symbol_dict = {
    "circle": "*",
    "square": "square*",
    "diamond": "diamond*",
    "cross": "+",
    "x": "x",
    "triangle-up": "triangle",
    "triangle-down": "triangle",
    "triangle-left": "triangle",
    "triangle-right": "triangle",
    "triangle-ne": "triangle",
    "triangle-se": "triangle",
    "triangle-sw": "triangle",
    "triangle-nw": "triangle",

    "circle-open": "o",

}

def marker_symbol_to_tex(symbol):
    return marker_symbol_dict.get(symbol, "*")