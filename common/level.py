from common.snake import Snake
from common.game_map import GameMap
from common.enums import Direction


class GameLevel:
    """Game level abstract class"""

    def __init__(self, width: int, height: int, clear_score: int):
        self._snake = self._create_snake(width, height)
        self._map = self._create_map(width, height)
        self._start_direction = self._get_start_direction()
        self._clear_score = clear_score

    def _create_snake(self, width: int, height: int) -> Snake:
        pass

    def _create_map(self, width: int, height: int) -> GameMap:
        pass

    def _get_start_direction(self) -> Direction:
        pass

    @property
    def snake(self) -> Snake:
        return self._snake

    @property
    def map(self) -> GameMap:
        return self._map

    @property
    def start_direction(self) -> Direction:
        return self._start_direction

    @property
    def clear_score(self) -> int:
        return self._clear_score
