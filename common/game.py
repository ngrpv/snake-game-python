from random import randint

from common.enums import Direction, MapCellType
from common.level import GameLevel
from common.point import Point


class Game:
    def __init__(self, levels: list[GameLevel]):
        self._levels = levels
        self._level = None
        self._level_number = 0
        self._is_game_clear = False
        self._food_point = None
        self._previous_direction = None
        self._score = 0
        self._score_on_level = 0

        self._is_game_over = not self._next_level()

    def _next_level(self) -> bool:
        self._score_on_level = 0

        if len(self._levels) == 0:
            self._is_game_clear = True
            return False
        level = self._levels.pop(0)
        self._level_number += 1

        self._level = level
        self._snake = level.snake
        self._previous_direction = level.start_direction
        self._map = level.map

        self._snake.set_coordinate_limits(
            self._map.width,
            self._map.height)
        self._next_food()
        return True

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

    @property
    def level_number(self) -> int:
        return self._level_number

    @property
    def is_game_clear(self) -> bool:
        return self._is_game_clear

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
        return not self._previous_direction or self._previous_direction.value != -direction.value

    def move(self, direction: Direction = None) -> None:
        """Move snake in specified direction"""
        if not direction:
            direction = self._previous_direction

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
            self._score_on_level += 1
            if self._score_on_level == self._level.clear_score:
                self._is_game_over = not self._next_level()
                if self._is_game_over:
                    return
            self._next_food()
