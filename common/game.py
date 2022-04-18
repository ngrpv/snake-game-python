from random import randint

from common.enums import Direction, MapCellType
from common.game_map import GameMap
from common.point import Point
from common.snake import Snake


class Game:
    def __init__(self, snake: Snake, game_map: GameMap):
        self._snake = snake
        self._map = game_map
        self._is_game_over = False
        self._food_point = None
        self._next_food()
        self._last_direction = None
        self._score = 0
        self._previous_direction = None
        self._snake.set_coordinate_limits(
            self._map.width,
            self._map.height)

    def _next_food(self) -> None:
        is_point_generated = False
        while not is_point_generated:
            x = randint(0, self._map.width - 1)
            y = randint(0, self._map.height - 1)
            if self.get(x, y) == MapCellType.Empty:
                is_point_generated = True

        self._food_point = Point(x, y)

    @property
    def map_dimensions(self) -> Point:
        return Point(self._map.width, self._map.height)

    @property
    def _map_size(self):
        return Point(self._map.width, self._map.height)

    @property
    def score(self):
        return self._score

    @property
    def is_over(self) -> bool:
        return self._is_game_over

    def get(self, x: int, y: int) -> MapCellType:
        """Get current map representation for view"""

        point = Point(x, y)
        if point == self._food_point:
            return MapCellType.Food
        for candidate in self._snake.get_points():
            candidate_truncated = candidate % self._map_size
            if candidate_truncated == point:
                return MapCellType.Snake

        return self._map.get(x, y)

    def is_direction_valid(self, direction: Direction) -> bool:
        """Check, if submitted direction is valid to move"""
        return not self._previous_direction \
            or self._previous_direction.value != -direction.value

    def move(self, direction: Direction) -> None:
        """Move snake in specified direction"""

        if not self.is_direction_valid(direction):
            raise AttributeError("Snake can't move on opposite direction")
        if self._is_game_over:
            return

        self._previous_direction = direction

        head = self._snake.head % self._map_size
        if self._snake.can_collide_with_itself(direction) \
                or self._map.get(head.x, head.y) == MapCellType.Obstacle:
            self._is_game_over = True
            return

        self._snake.move(direction)
        if self._snake.head == self._food_point:
            self._snake.grow()
            self._score += 1
            self._next_food()
