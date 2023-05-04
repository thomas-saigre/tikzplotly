
marker_symbol_dict = {
    "circle": "o",
    "square": "square",
    "diamond": "diamond",
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

}

def marker_symbol_to_tex(symbol):
    return marker_symbol_dict.get(symbol, "*")