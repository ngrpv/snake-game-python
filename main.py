from common.game import Game
from common.level_empty import EmptyLevel
from common.level_with_borders import WithBordersLevel
from common.ui_curses import UICurses
from common.level_quarters import QuartersLevel
from common.ui_pyqt import PyQtGui

if __name__ == "__main__":
    width = 100
    height = 100

    levels = [
        QuartersLevel(width, height, 10),
        EmptyLevel(width, height, 2),
        WithBordersLevel(width, height, 3)
    ]

    model = Game(levels)
    PyQtGui(model)
