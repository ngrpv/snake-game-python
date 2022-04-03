from common.game_map import GameMap, MapCellType


class MapEmpty(GameMap):
    """Empty game map"""

    def _get(self, x: int, y: int) -> MapCellType:
        return MapCellType.Empty
