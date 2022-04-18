import pytest
import unittest

from common.game import Game
from common.snake import Snake
from common.point import Point
from common.map_empty import MapEmpty
from common.enums import Direction, MapCellType


class TestGame(unittest.TestCase):
    def setUp(self):
        self.snake = Snake(Point(6, 0), Point(0, 0))
        self.map = MapEmpty(10, 10)

    def test_game_score_is_zero_after_init(self):
        game = Game(self.snake, self.map)
        assert game.score == 0

    def test_game_change_state_if_move(self):
        game = Game(self.snake, self.map)
        assert game.get(7, 0) == MapCellType.Empty
        game.move(Direction.Right)
        assert game.get(7, 0) == MapCellType.Snake

    def test_game_is_over_if_snake_collides(self):
        game = Game(self.snake, self.map)
        game.move(Direction.Down)
        game.move(Direction.Left)
        assert not game.is_game_over
        game.move(Direction.Up)
        assert game.is_game_over

    def test_game_score_increment_if_snake_eats(self):
        game = Game(self.snake, self.map)
        game._food_point = Point(7, 0)
        assert game.score == 0
        game.move(Direction.Right)
        assert game.score == 1

    def test_snake_grows(self):
        game = Game(self.snake, self.map)
        game._food_point = Point(7, 0)
        assert game.get(6, 0) == MapCellType.Snake
        game.move(Direction.Right)
        assert game.get(7, 0) == MapCellType.Snake
        assert game.get(0, 0) == MapCellType.Snake

    def test_game_raises_if_move_on_opposite(self):
        game = Game(self.snake, self.map)
        game.move(Direction.Down)
        with pytest.raises(AttributeError):
            game.move(Direction.Up)
