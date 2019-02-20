from aenum import MultiValueEnum


class Motion(MultiValueEnum):

    North = (-1, 0), 0

    East = (0, 1), 1

    South = (1, 0), 2

    West = (0, -1), 3

    Stay = (0, 0), 4
