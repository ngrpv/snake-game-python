import pytest
import unittest

from common.game import Game
from common.snake import Snake
from common.point import Point
from common.level_empty import MapEmpty
from common.enums import Direction, MapCellType, PortalDestination
from common.level import GameLevel
from common.game_map import Portal, GameMap


class TestGame(unittest.TestCase):
    def setUp(self):
        self.snake = Snake(Point(6, 0), Point(0, 0))
        self.levels = [TestEmptyLevel(10, 10, 10)]

    def test_game_score_is_zero_after_init(self):
        game = Game(self.levels)
        assert game.score == 0

    def test_game_change_state_if_move(self):
        game = Game(self.levels)
        assert game.get(7, 0) == MapCellType.Empty
        game.move(Direction.Right)
        assert game.get(7, 0) == MapCellType.Snake

    def test_game_is_over_if_snake_collides(self):
        game = Game(self.levels)
        game.move(Direction.Down)
        game.move(Direction.Left)
        assert not game.is_game_over
        game.move(Direction.Up)
        assert game.is_game_over

    def test_game_score_increment_if_snake_eats(self):
        game = Game(self.levels)
        game._food_point = Point(7, 0)
        assert game.score == 0
        game.move(Direction.Right)
        assert game.score == 1

    def test_snake_grows(self):
        game = Game(self.levels)
        game._food_point = Point(7, 0)
        assert game.get(6, 0) == MapCellType.Snake
        game.move(Direction.Right)
        assert game.get(7, 0) == MapCellType.Snake
        assert game.get(0, 0) == MapCellType.Snake

    def test_game_raises_if_move_on_opposite(self):
        game = Game(self.levels)
        game.move(Direction.Down)
        with pytest.raises(AttributeError):
            game.move(Direction.Up)

    def test_snake_should_move_prev_direction(self):
        game = Game(self.levels)
        assert game.get(6, 2) == MapCellType.Empty
        game.move(Direction.Down)
        game.move()
        assert game.get(6, 2) == MapCellType.Snake

    def test_game_teleport_snake_if_it_in_portal(self):
        game = Game([TestPortalsLevel(10, 10, 10)])
        game.move(Direction.Down)
        assert game.get(3, 3) == MapCellType.Snake
        game.move(Direction.Down)
        assert game.get(3, 4) == MapCellType.Empty
        assert game.get(5, 5) == MapCellType.Snake

    def test_game_teleport_snake_to_random_point(self):
        game = Game([TestPortalsLevel(10, 10, 10)])
        game.move(Direction.Right)
        assert game.get(4, 2) == MapCellType.Snake
        game.move(Direction.Right)
        assert game.get(4, 3) == MapCellType.Empty

    def test_game_teleport_snake_to_next_level(self):
        game = Game([TestPortalsLevel(10, 10, 0), TestEmptyLevel(10, 10, 10)])
        game.move(Direction.Left)
        game.move(Direction.Left)
        assert game.level_number == 2


class TestEmptyLevel(GameLevel):
    def _create_snake(self, width: int, height: int) -> Snake:
        return Snake(Point(6, 0), Point(0, 0))

    def _create_map(self, width: int, height: int) -> GameMap:
        return MapEmpty(width, height)

    def _get_start_direction(self) -> Direction:
        return Direction.Right


class TestPortalsLevel(GameLevel):
    def _create_snake(self, width: int, height: int) -> Snake:
        return Snake(Point(3, 2), Point(3, 0))

    def _create_map(self, width: int, height: int) -> GameMap:
        return TestMap(width, height)

    def _get_start_direction(self) -> Direction:
        return Direction.Down


class TestMap(GameMap):
    def _get(self, x: int, y: int) -> MapCellType:
        return MapCellType.Empty

    def _generate_portals(self) -> tuple[Portal]:
        portal = Portal(Point(3, 3),
                        destination_type=PortalDestination.StaticPoint,
                        destination=Point(5, 5))
        random_portal = Portal(Point(4, 2), PortalDestination.RandomPoint)
        next_level_portal = Portal(Point(2, 2), PortalDestination.NextLevel)

        return tuple([portal, random_portal, next_level_portal])
