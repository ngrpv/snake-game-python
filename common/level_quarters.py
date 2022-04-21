from common.level_empty import EmptyLevel
from common.game_map import GameMap
from common.enums import MapCellType


class QuartersLevel(EmptyLevel):
    """Level with; map which divided into 4 regions, reachable by edges trespassing only"""
    def _create_map(self, width: int, height: int) -> GameMap:
        return QuartersMap(width, height)


class QuartersMap(GameMap):
    """Game map which divided into 4 regions, reachable by edges trespassing only"""

    def _generate_map(self) -> None:
        self._half_width = self.width // 2
        self._half_height = self.height // 2

    def _get(self, x: int, y: int) -> MapCellType:
        if x == self._half_width or y == self._half_height:
            return MapCellType.Obstacle

        return MapCellType.Empty
