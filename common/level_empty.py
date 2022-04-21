from common.level import GameLevel
from common.snake import Snake
from common.game_map import GameMap
from common.enums import Direction
from common.point import Point
from common.map_empty import MapEmpty


class EmptyLevel(GameLevel):
    def _create_snake(self, width: int, height: int) -> Snake:
        head_position = Point(width // 2, height // 2)
        tail_position = head_position + Point(2, 0)
        return Snake(head_position, tail_position)

    def _create_map(self, width: int, height: int) -> GameMap:
        return MapEmpty(width, height)

    def _get_start_direction(self) -> Direction:
        return Direction.Left
