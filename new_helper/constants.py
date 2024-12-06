ADJACENT_4 = ((-1, 0), (1, 0), (0, -1), (0, 1))
ADJACENT_5 = ((-1, 0), (1, 0), (0, 0), (0, -1), (0, 1))
ADJACENT_8 = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
ADJACENT_9 = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1))

DIRECTIONS: dict[str, tuple[int, int]] = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
    "n": (0, -1),
    "s": (0, 1),
    "e": (1, 0),
    "w": (-1, 0),
    "NE": (1, 1),
    "NW": (-1, 1),
    "SE": (1, -1),
    "SW": (-1, -1),
    "ne": (1, 1),
    "Nnw": (-1, 1),
    "se": (1, -1),
    "sw": (-1, -1),
    "U": (0, -1),
    "D": (0, 1),
    "R": (1, 0),
    "L": (-1, 0),
    "u": (0, -1),
    "d": (0, 1),
    "r": (1, 0),
    "l": (-1, 0),
    "up": (0, -1),
    "down": (0, 1),
    "right": (1, 0),
    "left": (-1, 0),
    "Up": (0, -1),
    "Down": (0, 1),
    "Right": (1, 0),
    "Left": (-1, 0),
    "UP": (0, -1),
    "DOWN": (0, 1),
    "RIGHT": (1, 0),
    "LEFT": (-1, 0),
}

DIRS = DIRECTIONS
