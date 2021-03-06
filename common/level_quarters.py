from common.level_empty import EmptyLevel
from common.game_map import GameMap, Portal
from common.enums import MapCellType, PortalDestination
from common.point import Point
from common.snake import Snake


class QuartersLevel(EmptyLevel):
    """Level with; map which divided into 4 regions, reachable by edges trespassing only"""

    def _create_map(self, width: int, height: int) -> GameMap:
        return QuartersMap(width, height)

    def _create_snake(self, width: int, height: int) -> Snake:
        x = width // 4
        y = 3 * height // 4
        head = Point(x, y)
        tail = head + Point(2, 0)
        return Snake(head, tail)


class QuartersMap(GameMap):
    """Game map which divided into 4 regions, reachable by edges trespassing only"""

    def _generate_portals(self) -> tuple:
        static_portal = Portal(Point(1, 1), PortalDestination.StaticPoint, Point(self.width - 2, self.height - 2))
        random_portal = Portal(Point(self.width//2 + 1, self.height//2 - 1), PortalDestination.RandomPoint)
        return static_portal, random_portal

    def _generate_map(self) -> None:
        self._half_width = self.width // 2
        self._half_height = self.height // 2

    def _get(self, x: int, y: int) -> MapCellType:
        if x == self._half_width or y == self._half_height:
            return MapCellType.Obstacle

        return MapCellType.Empty
