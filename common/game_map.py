from common.enums import MapCellType
from common.point import Point


class Portal:
    def __init__(self, position: Point, destination: Point):
        self._position = position
        self._destination = destination

    @property
    def position(self) -> Point:
        return self._position

    @property
    def destination(self) -> Point:
        return self._destination


class GameMap:
    """Game map abstract class"""

    def __init__(self, width: int, height: int):
        if width < 0 or height < 0:
            raise ValueError("Map width or height cannot be negative!")

        self._width = width
        self._height = height
        self._portals = self._generate_portals()
        self._generate_map()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def portals(self) -> tuple[Portal]:
        return self._portals

    def get(self, x: int, y: int) -> MapCellType:
        """Retrieve cell type at (x, y)"""
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            raise IndexError(
                f"Coordinates index out of map size range: ({x}, {y})")

        point = Point(x, y)

        for portal in self.portals:
            if portal.position == point:
                return MapCellType.PortalIn
            if portal.destination == point:
                return MapCellType.PortalOut


        return self._get(x, y)

    def _generate_map(self) -> None:
        """Map generation method, which should be
        implemented in particular implementation"""
        pass

    def _generate_portals(self) -> tuple[Portal]:
        """Map portals generation method"""
        return ()

    def _get(self, x: int, y: int) -> MapCellType:
        """Map getter"""
        pass
