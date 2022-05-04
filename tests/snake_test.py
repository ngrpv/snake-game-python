import pytest
from common.point import Point
from common.enums import Direction
from common.snake import Snake


class TestSnake:
    def test_snake_should_raise_if_init_snake_is_not_straight(self):
        with pytest.raises(AttributeError):
            Snake(Point(1, 1), Point(0, 0))

    @staticmethod
    def move_test(directions: list[Direction], snake_on_start: Snake,
                  snake_on_end: Snake):
        for d in directions:
            snake_on_start.move(d)
        assert snake_on_end.__eq__(snake_on_start)

    def test_move_right(self):
        snake = Snake(Point(3, 0), Point(0, 0))
        expected = Snake(Point(4, 0), Point(1, 0))
        TestSnake.move_test([Direction.Right], snake, expected)

    def test_move_right_2(self):
        snake = Snake(Point(0, 3), Point(0, 0))
        expected = Snake(Point(0, 3), Point(0, 0))
        expected.points = [Point(1, 3), Point(0, 3), Point(0, 2), Point(0, 1)]
        TestSnake.move_test([Direction.Right], snake, expected)

    def test_move_down(self):
        snake = Snake(Point(3, 0), Point(0, 0))
        expected = Snake(Point(3, 0), Point(0, 0))
        expected.points = [Point(3, 1), Point(3, 0), Point(2, 0), Point(1, 0)]
        TestSnake.move_test([Direction.Down], snake, expected)

    def test_move_complex(self):
        snake = Snake(Point(3, 0), Point(0, 0))
        expected = Snake(Point(3, 0), Point(0, 0))
        expected.points = [Point(5, 1), Point(5, 0), Point(4, 0), Point(4, 1)]
        directions = [Direction.Down, Direction.Right, Direction.Up,
                      Direction.Right, Direction.Down]
        TestSnake.move_test(directions, snake, expected)

    @staticmethod
    def grow_test(start_snake: Snake, result_snake: Snake,
                  movings: list[Direction]):
        for m in movings:
            start_snake.move(m)
        start_snake.grow()
        assert start_snake.__eq__(result_snake)

    def test_grow_on_moving_right(self):
        snake = Snake(Point(3, 0), Point(0, 0))
        expected = Snake(Point(4, 0), Point(0, 0))
        TestSnake.grow_test(snake, expected, [Direction.Right])

    def test_grow_on_moving_up(self):
        snake = Snake(Point(3, 1), Point(0, 1))
        expected = Snake(Point(3, 1), Point(0, 1))
        expected.points = [
            Point(3, 0), Point(3, 1), Point(2, 1), Point(1, 1), Point(0, 1)
        ]
        TestSnake.grow_test(snake, expected, [Direction.Up])

    def test_grow_on_zig_zag(self):
        snake = Snake(Point(2, 0), Point(0, 0))
        expected = Snake(Point(3, 1), Point(0, 1))
        expected.points = [
            Point(3, 2), Point(3, 1), Point(2, 1), Point(2, 0)
        ]
        directions = [Direction.Down, Direction.Right, Direction.Down]
        TestSnake.grow_test(snake, expected, directions)

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

    def test_raises_if_start_coordinate_is_negative(self):
        with pytest.raises(AttributeError):
            Snake(Point(0, -1), Point(1, 1))

    def test_game_snake_coordinate_is_not_out_of_bounds_if_set_limits(self):
        snake = Snake(Point(4, 0), Point(2, 0))
        snake.set_coordinate_limits(5, 1)
        snake.move(Direction.Right)
        assert snake.head == Point(0, 0)

    def test_snake_teleports_to_target(self):
        snake = Snake(Point(3, 0), Point(0, 0))
        snake.teleport(Point(2, 2))
        assert snake.get_points() == [
            Point(2, 2), Point(3, 0), Point(2, 0), Point(1, 0)
        ]
