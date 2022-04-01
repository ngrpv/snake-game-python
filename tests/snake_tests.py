import pytest
from prompt_toolkit.data_structures import Point

from common.snake import Snake


def test_move_right():
    snake = Snake(Point(3, 0), Point(0, 0))
    snake.move_right()
    assert snake.get_points() == [Point(4, 0), Point(3, 0), Point(2, 0),
                                  Point(1, 0)]


def test_move_down():
    snake = Snake(Point(3, 0), Point(0, 0))
    snake.move_down()
    assert snake.get_points() == [Point(3, 1), Point(3, 0), Point(2, 0),
                                  Point(1, 0)]
