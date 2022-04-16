from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from common.game import Game
from common.enums import Direction, MapCellType
import sys


class PyQtGui:
    ONE_TICK_SEC = 0.05
    AUTOMOVE_TICKS = 5
    FIELD_PIXELS = {
        MapCellType.Empty: " ",
        MapCellType.Snake: "o",
        MapCellType.Food: "@",
        MapCellType.Obstacle: "#"
    }
    cell_size = 50

    def __init__(self, game: Game, start_direction: Direction):
        self.game = game
        self.current_direction = start_direction
        app = QApplication([])
        window = Window()
        sys.exit(app.exec_())


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.show()
        self.setWindowTitle("Snake game")
        self.setGeometry(200, 100, 600, 400)
        self.qp = QPainter(self)

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.paintCell(2, 2, QColor(255, 1, 1))

    def paintCell(self, x: int, y: int, color: QColor) -> None:
        self.qp.begin(self)
        self.qp.fillRect(x * PyQtGui.cell_size, y * PyQtGui.cell_size,
                         PyQtGui.cell_size, PyQtGui.cell_size, color)
        self.qp.end()
