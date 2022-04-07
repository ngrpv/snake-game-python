from common.enums import Direction
from common.game import Game
from common.map_empty import MapEmpty
from common.Point import Point
from common.snake import Snake
from common.ui_curses import UICurses

if __name__ == "__main__":
    game_map = MapEmpty(84, 20)
    snake = Snake(Point(8, 8), Point(10, 8))
    model = Game(snake, game_map)
    model.get(0, 0)
    UICurses(model, Direction.Left)
