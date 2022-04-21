from common.enums import MapCellType


class GameMap:
    """Game map abstract class"""
    def __init__(self, width: int, height: int):
        if width < 0 or height < 0:
            raise ValueError("Map width or height cannot be negative!")

        self._width = width
        self._height = height
        self._generate_map()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def get(self, x: int, y: int) -> MapCellType:
        """Retrieve cell type at (x, y)"""
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            raise IndexError(
                f"Coordinates index out of map size range: ({x}, {y})")
        return self._get(x, y)

    def _generate_map(self) -> None:
        """Map generation method, which should be
        implemented in particular implementation"""
        pass

    def _get(self, x: int, y: int) -> MapCellType:
        "Map getter"
        pass
