"""The four axes and the single operation that opens them.

A pipeline is not a line. It is a tesseract opened along four orthogonal axes by
one repeated operation, the sweep: push a structure along a new orthogonal axis and
take the whole trail as the next structure.

    point --order--> line --breadth--> plane --depth--> solid --time--> tesseract
"""

from enum import Enum


class Axis(str, Enum):
    """One direction a structure can be swept along.

    LEAF is not a sweep. It marks a node that is handled directly, in one pass.
    """

    ORDER = "order"      # 1D, line:      serial dependency
    BREADTH = "breadth"  # 2D, plane:     parallel independence
    DEPTH = "depth"      # 3D, solid:     recursive nesting (seed, not leaf)
    TIME = "time"        # 4D, tesseract: iterative self-evolution (rounds)
    LEAF = "leaf"        # 0D, point:     work done directly


GEOMETRY = {
    Axis.ORDER: "line",
    Axis.BREADTH: "plane",
    Axis.DEPTH: "solid",
    Axis.TIME: "tesseract",
    Axis.LEAF: "point",
}

MECHANISM = {
    Axis.ORDER: "serial dependency",
    Axis.BREADTH: "parallel independence",
    Axis.DEPTH: "recursive nesting",
    Axis.TIME: "iterative self-evolution",
    Axis.LEAF: "work done directly",
}

# The four sweepable axes, in dimensional order. LEAF is excluded on purpose.
FOUR_AXES = (Axis.ORDER, Axis.BREADTH, Axis.DEPTH, Axis.TIME)
