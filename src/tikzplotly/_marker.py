from warnings import warn

marker_symbol_dict = {
    "circle": "*",
    "circle-open": "o",
    "square": "square*",
    "square-open": "square",
    "diamond": "diamond*",
    "diamond-open": "diamond",

    "cross": "+",
    "cross-open": "+",
    "x": "x",
    "x-open": "x",

    "triangle-up": "triangle*",
    "triangle-up-open": "triangle",
    "triangle-down": "triangle*",       # TODO
    "triangle-down-open": "triangle",   # TODO
    "triangle-left": "triangle*",       # TODO
    "triangle-left-open": "triangle",   # TODO
    "triangle-right": "triangle*",      # TODO
    "triangle-right-open": "triangle",  # TODO
    "triangle-ne": "triangle",          # TODO
    "triangle-ne-open": "triangle",     # TODO
    "triangle-se": "triangle",          # TODO
    "triangle-se-open": "triangle",     # TODO
    "triangle-sw": "triangle",          # TODO
    "triangle-sw-open": "triangle",     # TODO
    "triangle-nw": "triangle",          # TODO
    "triangle-nw-open": "triangle",     # TODO

    "pentagon": "pentagon*",
    "pentagon-open": "pentagon",
    # "hexagon": "hexagon*",        # not supported
    # "hexagon-open": "hexagon",
    # "hexagon2": "hexagon*",
    # "hexagon2-open": "hexagon",
    # "octagon": "octagon*",
    # "octagon-open": "octagon",

    "star": "star",
    "star-open": "star",
    "hexagram": "10-pointed star",         # not supported
    "hexagram-open": "10-pointed star",    # not supported

    "star-triangle-up": "star",
    "star-triangle-up-open": "star",    # TODO: use rotate option
    "star-triangle-down": "star",
    "star-triangle-down-open": "star",  # TODO: use rotate option
    "star-square": "square*",           # not supported
    "star-square-open": "square",       # not supported
    "star-diamond": "diamond*",         # not supported
    "star-diamond-open": "diamond",     # not supported

    "diamond-tall": "diamond*",
    "diamond-tall-open": "diamond",
    "diamond-wide": "diamond*",          # TODO: use rotate option
    "diamond-wide-open": "diamond",      # TODO: use rotate option

    # "hourglass": "hourglass*",        # not supported
    # "hourglass-open": "hourglass",    # not supported
    # "bowtie": "bowtie*",              # not supported
    # "bowtie-open": "bowtie",          # not supported

    "circle-cross": "oplus*",
    "circle-cross-open": "oplus",
    "circle-x": "otimes*",
    "circle-x-open": "otimes",
    "square-cross": "square*",        # not supported
    "square-cross-open": "square",    # not supported
    "square-x": "square*",            # not supported
    "square-x-open": "square",        # not supported
    "diamond-cross": "diamond*",      # not supported
    "diamond-cross-open": "diamond",  # not supported
    "diamond-x": "diamond*",          # not supported
    "diamond-x-open": "diamond",      # not supported

    "cross-thin": "+",
    "x-thin": "x",
    "asterisk": "asterisk",
    # "hash": "hash",
    # "hash-open": "hash",

    "y-up": "Mercedes star flipped",
    "y-down": "Mercedes star flipped",
    "y-left": "Mercedes star",      # TODO: use rotate option
    "y-right": "Mercedes star",     # TODO: use rotate option

    "line-ew": "-",
    "line-ns": "|",
    "line-ne": "|",     # TODO: use rotate option
    "line-nw": "|",     # TODO: use rotate option

    "arrow-up": "triangle*",            # not supported
    "arrow-up-open": "triangle",        #
    "arrow-down": "triangle*",          #
    "arrow-down-open": "triangle",      #
    "arrow-left": "triangle*",          #
    "arrow-left-open": "triangle",      #
    "arrow-right": "triangle*",         #
    "arrow-right-open": "triangle",     #
    "arrow-bar-up": "triangle*",        #
    "arrow-bar-up-open": "triangle",    #
    "arrow-bar-down": "triangle*",      #
    "arrow-bar-down-open": "triangle",  #
    "arrow-bar-left": "triangle*",      #
    "arrow-bar-left-open": "triangle",  #
    "arrow-bar-right": "triangle*",     #
    "arrow-bar-right-open": "triangle", #
    "arrow": "triangle*",               #
    "arrow-open": "triangle",           #
    "arrow-wide": "triangle*",          #
    "arrow-wide-open": "triangle",      #

}

def marker_symbol_to_tex(symbol):
    if "-dot" in symbol:
        warn("Dotted markers are not supported (yet), the symbol without dot will be used instead.")
    return marker_symbol_dict.get(symbol.replace("-dot", ""), "*")
