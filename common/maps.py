from common.game_map import GameMap, MapCellType
from common.point import Point


class Level1(GameMap):
    """Empty game map"""
    obstacles = [Point(1, 1), Point(0, 0), Point(1, 0)]

    def _get(self, x: int, y: int) -> MapCellType:
        if Point(x, y) in Level1.obstacles:
            return MapCellType.Obstacle
        return MapCellType.Empty
