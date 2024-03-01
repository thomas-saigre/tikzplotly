from warnings import warn

marker_symbol_dict = {
    "circle": ("*", None),
    "circle-open": ("o", None),
    "square": ("square*", None),
    "square-open": ("square", None),
    "diamond": ("diamond*", None),
    "diamond-open": ("diamond", None),

    "cross": ("+", None),
    "cross-open": ("+", None),
    "x": ("x", None),
    "x-open": ("x", None),

    "triangle-up": ("triangle*", None),
    "triangle-up-open": ("triangle", None),
    "triangle-down": ("triangle*", ("rotate", 180)),
    "triangle-down-open": ("triangle", ("rotate", 180)),
    "triangle-left": ("triangle*", ("rotate", 90)),
    "triangle-left-open": ("triangle", ("rotate", 90)),
    "triangle-right": ("triangle*", ("rotate", -90)),
    "triangle-right-open": ("triangle", ("rotate", -90)),
    "triangle-ne": ("triangle*", ("rotate", -45)),
    "triangle-ne-open": ("triangle", ("rotate", -45)),
    "triangle-se": ("triangle*", ("rotate", -135)),
    "triangle-se-open": ("triangle", ("rotate", -135)),
    "triangle-sw": ("triangle*", ("rotate", 135)),
    "triangle-sw-open": ("triangle", ("rotate", 135)),
    "triangle-nw": ("triangle*", ("rotate", 45)),
    "triangle-nw-open": ("triangle", ("rotate", 45)),

    "pentagon": ("pentagon*", None),
    "pentagon-open": ("pentagon", None),
    # "hexagon": ("hexagon*"",None),        # not supported
    # "hexagon-open": ("hexagon", None),
    # "hexagon2": ("hexagon*", ("rotate", 90)),
    # "hexagon2-open": ("hexagon", ("rotate", 90)),
    # "octagon": ("octagon*", None),
    # "octagon-open": ("octagon", None),

    "star": ("star", None),
    "star-open": ("star", None),
    "hexagram": ("10-pointed star", None),         # not supported
    "hexagram-open": ("10-pointed star", None),    # not supported

    "star-triangle-up": ("triangle*", None),        # not supported
    "star-triangle-up-open": ("triangle", None),    #
    "star-triangle-down": ("triangle*", ("rotate", 180)),       # not supported, but rotation of the previous
    "star-triangle-down-open": ("triangle", ("rotate", 180)),   #
    "star-square": ("square*", None),           # not supported
    "star-square-open": ("square", None),       # not supported
    "star-diamond": ("diamond*", None),         # not supported
    "star-diamond-open": ("diamond", None),     # not supported

    "diamond-tall": ("diamond*", None),
    "diamond-tall-open": ("diamond", None),
    "diamond-wide": ("diamond*", ("rotate", 90)),
    "diamond-wide-open": ("diamond", ("rotate", 90)),

    # "hourglass": ("hourglass*", None);        # not supported
    # "hourglass-open": ("hourglass", None);    #
    # "bowtie": ("bowtie*", ("rotate", 90));              # not supported but rotation of the previous
    # "bowtie-open": ("bowtie", ("rotate", 90));          #

    "circle-cross": ("oplus*", None),
    "circle-cross-open": ("oplus", None),
    "circle-x": ("otimes*", None),
    "circle-x-open": ("otimes", None),
    "square-cross": ("square*", None),        # not supported
    "square-cross-open": ("square", None),    #
    "square-x": ("square*", None),            #
    "square-x-open": ("square", None),        #
    "diamond-cross": ("diamond*", None),      #
    "diamond-cross-open": ("diamond", None),  #
    "diamond-x": ("diamond*", None),          #
    "diamond-x-open": ("diamond", None),      #

    "cross-thin": ("+", None),
    "x-thin": ("x", None),
    "asterisk": ("asterisk", None),
    # "hash": ("hash", None),           # not supported
    # "hash-open": ("hash", None),

    "y-up": ("Mercedes star flipped", None),
    "y-down": ("Mercedes star", None),
    "y-left": ("Mercedes star", ("rotate", 90)),
    "y-right": ("Mercedes star", ("rotate", -90)),

    "line-ew": ("-", None),
    "line-ns": ("|", None),
    "line-ne": ("|", ("rotate", -45)),
    "line-nw": ("|", ("rotate", 45)),

    "arrow-up": ("triangle*", None),            # not supported
    "arrow-up-open": ("triangle", None),        #
    "arrow-down": ("triangle*", ("rotate", 180)),          # not supported, but rotation of the previous
    "arrow-down-open": ("triangle", ("rotate", 180)),      #
    "arrow-left": ("triangle*", ("rotate", 90)),           #
    "arrow-left-open": ("triangle", ("rotate", 90)),       #
    "arrow-right": ("triangle*", ("rotate", -90)),         #
    "arrow-right-open": ("triangle", ("rotate", -90)),     #
    "arrow-bar-up": ("triangle*", None),                   #
    "arrow-bar-up-open": ("triangle", None),               #
    "arrow-bar-down": ("triangle*", ("rotate", 180)),      #
    "arrow-bar-down-open": ("triangle", ("rotate", 180)),  #
    "arrow-bar-left": ("triangle*", ("rotate", -90)),      #
    "arrow-bar-left-open": ("triangle", ("rotate", -90)),  #
    "arrow-bar-right": ("triangle*", ("rotate", 90)),      #
    "arrow-bar-right-open": ("triangle", ("rotate", 90)),  #
    "arrow": ("triangle*", ("xscale", 0.5)),               # not supported
    "arrow-open": ("triangle", ("xscale", 0.5)),           #
    "arrow-wide": ("triangle*", ("xscale", 1.5)),          #
    "arrow-wide-open": ("triangle", ("xscale", 1.5)),      #

}

def marker_symbol_to_tex(symbol):
    if "-dot" in symbol:
        warn("Dotted markers are not supported (yet), the symbol without dot will be used instead.")
    return marker_symbol_dict.get(symbol.replace("-dot", ""), ("*", None))
