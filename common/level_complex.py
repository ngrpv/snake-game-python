from common.enums import Direction
from common.game_map import GameMap, Portal, MapCellType
from common.level import GameLevel
from common.point import Point
from common.snake import Snake
from common.enums import PortalDestination


class ComplexLevel(GameLevel):
    def _create_snake(self, width: int, height: int) -> Snake:
        head_position = Point(width - 1, 2)
        tail_position = Point(width - 1, 0)
        return Snake(head_position, tail_position)

    def _create_map(self, width: int, height: int) -> GameMap:
        return ComplexMap(width, height)

    def _get_start_direction(self) -> Direction:
        return Direction.Down


class ComplexMap(GameMap):
    """Empty game map"""

    def __init__(self, width, height):
        super().__init__(width, height)
        self.obstacles = []
        self.add_line(Point(width * 2 // 3, 0),
                      Point(width * 2 // 3, height * 2 // 3))
        self.add_line(Point(width, height * 2 // 3),
                      Point(width // 3, height * 2 // 3))
        self.add_line(Point(width // 3, height // 2),
                      Point(width // 3, height))
        self.add_line(Point(0, height * 2 // 3),
                      Point(0, height))
        self.add_line(Point(0, height // 3),
                      Point(width // 3, height // 3))
        self.add_line(Point(width // 3, 0),
                      Point(width // 3, height // 3 + 1))

    def _get(self, x: int, y: int) -> MapCellType:
        if Point(x, y) in self.obstacles:
            return MapCellType.Obstacle
        return MapCellType.Empty

    def _generate_portals(self) -> tuple[Portal]:
        p = Portal(Point(4, 4), PortalDestination.StaticPoint, Point(self.width // 2, self.height // 2))
        return p,

    def add_line(self, a: Point, b: Point):
        dx = b.x - a.x
        dy = b.y - a.y
        if dx == 0 and dy != 0:
            for i in range(dy):
                self.obstacles.append(Point(a.x, a.y + i))
        else:
            for i in range(min(a.x, b.x), max(a.x, b.x)):
                self.obstacles.append(Point(i, a.y))
