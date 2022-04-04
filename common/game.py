from random import randint

from common.enums import Direction, MapCellType
from common.game_map import GameMap
from common.Point import Point
from common.snake import Snake


class Game:
    def __init__(self, snake: Snake, game_map: GameMap):
        self._snake = snake
        self._map = game_map
        self._is_game_over = False
        self._next_food()
        self._last_direction = None

    def _next_food(self) -> None:
        is_point_generated = False
        while not is_point_generated:
            x = randint(0, self._map.width - 1)
            y = randint(0, self._map.height - 1)
            if self._map.get(x, y) == MapCellType.Empty:
                is_point_generated = True

        self._food_point = Point(x, y)

    @property
    def map_dimensions(self) -> Point:
        return Point(self._map.width, self._map.height)

    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    def get(self, x: int, y: int) -> MapCellType:
        """Get current map representation for view"""

        point = Point(x, y)
        if point == self._food_point:
            return MapCellType.Food
        if point in self._snake.get_points():
            return MapCellType.Snake

        return self._map.get(x, y)

    def move(self, direction: Direction) -> None:
        "Move snake in specified direction"
        if self._is_game_over:
            return

        head_after_move = Point(
            self._snake.head.x + direction.value.x,
            self._snake.head.y + direction.value.y)

        if (self._snake.can_collide_with_itself(direction)
                or self._map.get(
                    head_after_move.x,
                    head_after_move.y) == MapCellType.Obstacle):
            self._is_game_over = True
            return

        self._snake.move(direction)
        head = self._snake.head
        if head == self._food_point:
            self._snake.grow()
