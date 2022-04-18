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
        MapCellType.Empty: QColor(0,0,0),
        MapCellType.Snake: QColor(0, 250, 0),
        MapCellType.Food: QColor(250, 0, 0),
        MapCellType.Obstacle: QColor(0, 0, 250)
    }
    cell_size = 20

    def __init__(self, game: Game, start_direction: Direction):
        self.game = game
        self.current_direction = start_direction
        app = QApplication([])
        window = Window(game)
        sys.exit(app.exec_())


class Window(QMainWindow):
    def __init__(self, game: Game):
        super(Window, self).__init__()
        self.show()
        self.setWindowTitle("Snake game")
        self.setGeometry(200, 100, 600, 400)
        self.qp = QPainter(self)
        self.model = game
        self.dimensions = game.map_dimensions
        self.width = self.dimensions.x
        self.height = self.dimensions.y

    def keyPressEvent(self, event):
        try:
            key = event.key()
            if key == Qt.Key_Up:
                self.model.move(Direction.Up)
            elif key == Qt.Key_Left:
                self.model.move(Direction.Left)
            elif key == Qt.Key_Down:
                self.model.move(Direction.Down)
            elif key == Qt.Key_Right:
                self.model.move(Direction.Right)
            self.update()
        except Exception:
            pass



    def paintField(self):
        for x in range(self.width):
            for y in range(self.height):
                self.paintCell(x, y, PyQtGui.FIELD_PIXELS.get(self.model.get(x, y)))

    def paintEvent(self, a0: QPaintEvent) -> None:
        if not self.model.is_over:
            self.paintField()

    def paintCell(self, x: int, y: int, color: QColor) -> None:
        self.qp.begin(self)
        self.qp.fillRect(x * PyQtGui.cell_size, y * PyQtGui.cell_size,
                         PyQtGui.cell_size, PyQtGui.cell_size, color)

        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))

        painter.drawRect(x * PyQtGui.cell_size, y * PyQtGui.cell_size,
                         PyQtGui.cell_size, PyQtGui.cell_size)
        painter.end()
        self.qp.end()
