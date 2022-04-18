import pytest
from common.point import Point
from common.enums import Direction
from common.snake import Snake


class TestSnake:
    def test_snake_should_raise_if_init_snake_is_not_straight(self):
        with pytest.raises(AttributeError):
            Snake(Point(1, 1), Point(0, 0))

    def test_move_right(self):
        snake = Snake(Point(3, 0), Point(0, 0))
        snake.move(Direction.Right)
        assert snake.get_points() == [Point(4, 0), Point(3, 0), Point(2, 0),
                                      Point(1, 0)]

    def test_move_right_2(self):
        snake = Snake(Point(0, 3), Point(0, 0))
        snake.move(Direction.Right)
        assert snake.get_points() == [Point(1, 3), Point(0, 3),
                                      Point(0, 2),
                                      Point(0, 1)]

    def test_move_down(self):
        snake = Snake(Point(3, 0), Point(0, 0))
        snake.move(Direction.Down)
        assert snake.get_points() == [Point(3, 1), Point(3, 0), Point(2, 0),
                                      Point(1, 0)]

    def test_move_complex(self):
        snake = Snake(Point(3, 0), Point(0, 0))
        snake.move(Direction.Down)
        snake.move(Direction.Right)
        snake.move(Direction.Up)
        snake.move(Direction.Right)
        snake.move(Direction.Down)
        assert snake.get_points() == [Point(5, 1), Point(5, 0), Point(4, 0),
                                      Point(4, 1)]

    def test_grow_on_moving_right(self):
        snake = Snake(Point(3, 0), Point(0, 0))
        snake.move(Direction.Right)
        snake.grow()
        assert snake.get_points() == [Point(4, 0), Point(3, 0), Point(2, 0),
                                      Point(1, 0), Point(0, 0)]

    def test_grow_on_moving_up(self):
        snake = Snake(Point(3, 1), Point(0, 1))
        snake.move(Direction.Up)
        snake.grow()
        assert snake.get_points() == [Point(3, 0), Point(3, 1), Point(2, 1),
                                      Point(1, 1), Point(0, 1)]

    def test_grow_on_zig_zag(self):
        snake = Snake(Point(2, 0), Point(0, 0))
        snake.move(Direction.Down)
        snake.move(Direction.Right)
        snake.move(Direction.Down)
        snake.grow()
        assert len(snake.get_points()) == 4
        assert snake.get_points() == [Point(3, 2), Point(3, 1), Point(2, 1),
                                      Point(2, 0)]

    def test_snake_is_die_if_move_to_cell_with_self(self):
        snake = Snake(Point(4, 0), Point(0, 0))
        snake.move(Direction.Down)
        snake.move(Direction.Left)
        assert snake.can_collide_with_itself(Direction.Up)

    def test_snake_is_not_dead_if_move_to_cell_with_tail(self):
        snake = Snake(Point(3, 0), Point(0, 0))
        snake.move(Direction.Down)
        snake.move(Direction.Left)
        assert not snake.can_collide_with_itself(Direction.Up)

    def test_move_on_opposite_direction_should_raise(self):
        snake = Snake(Point(3, 0), Point(0, 0))
        snake.move(Direction.Right)
        with pytest.raises(AttributeError):
            snake.move(Direction.Left)
