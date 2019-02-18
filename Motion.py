from enum import Enum


class Motion(Enum):

    UP = (-1, 0)

    RIGHT = [0, 1]

    DOWN = [1, 0]

    LEFT = [0, 1]

    STAY = [0, 0]
