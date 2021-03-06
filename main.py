from common.game import Game
from common.level_empty import EmptyLevel
from common.level_quarters import QuartersLevel
from common.level_with_borders import WithBordersLevel
from common.level_complex import ComplexLevel
from common.ui_pyqt import PyQtGui

if __name__ == "__main__":
    width = 40
    height = 30

    levels = [
        QuartersLevel(width, height, 8),
        ComplexLevel(width, height, 10),
        EmptyLevel(width, height, 2),
        WithBordersLevel(width, height, 4),
    ]

    model = Game(levels)
    PyQtGui(model)
