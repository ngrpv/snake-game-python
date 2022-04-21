from common.level_empty import EmptyLevel
from common.game_map import GameMap
from common.enums import MapCellType


class WithBordersLevel(EmptyLevel):
    """Level with classic snake map (with borders at the edges)"""
    def _create_map(self, width: int, height: int) -> GameMap:
        return MapWithBorders(width, height)


class MapWithBorders(GameMap):
    """Game map with borders at the edges (classic snake)"""

    def _get(self, x: int, y: int) -> MapCellType:
        if x == 0 or y == 0 \
                or x == self.width - 1 or y == self.height - 1:
            return MapCellType.Obstacle

        return MapCellType.Empty
