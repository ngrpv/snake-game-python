from common.enums import Direction
from common.game import Game
from common.map_empty import MapEmpty
from common.maps import Level1
from common.Point import Point
from common.snake import Snake
from common.ui_curses import UICurses
from common.ui_pyqt import PyQtGui

if __name__ == "__main__":
    width, height = UICurses.get_screen_size_wh()
    map_lvl1 = Level1(width, height - 1)
    game_map = MapEmpty(width, height - 1)
    snake = Snake(Point(8, 8), Point(10, 8))
    model = Game(snake, map_lvl1)
    model.get(0, 0)
  #  UICurses(model, Direction.Left)
    PyQtGui(model, Direction.Left)
