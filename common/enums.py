from enum import Enum

from common.point import Point


class Direction(Enum):
    Up = Point(0, -1)
    Down = Point(0, 1)
    Left = Point(-1, 0)
    Right = Point(1, 0)


class MapCellType(Enum):
    Empty = 0
    Obstacle = 1
    Food = 2
    Snake = 3
    PortalIn = 4
    PortalOut = 5
