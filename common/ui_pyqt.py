import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from common.enums import Direction, MapCellType
from common.game import Game


class PyQtGui:
    ONE_TICK_MS = 350
    FIELD_PIXELS = {
        MapCellType.Empty: QColor(0, 0, 0),
        MapCellType.Snake: QColor(0, 250, 0),
        MapCellType.Food: QColor(250, 0, 0),
        MapCellType.Obstacle: QColor(0, 0, 250)
    }
    CELL_SIZE = 20

    def __init__(self, game: Game):
        self.game = game
        app = QApplication([])
        screen = app.primaryScreen()
        size = screen.size()
        width, height = game.map_dimensions.x, game.map_dimensions.y
        PyQtGui.CELL_SIZE = int(min(size.width() // width,
                                size.height() // height) * 0.90)
        window = Window(game, width * PyQtGui.CELL_SIZE,
                        height * PyQtGui.CELL_SIZE)
        sys.exit(app.exec_())


class Window(QMainWindow):
    def __init__(self, game: Game, width, height):
        super(Window, self).__init__()
        self.show()
        self.setWindowTitle("Snake game")
        self.setGeometry(20, 40, width, height)
        self.qp = QPainter(self)
        self.model = game
        self.dimensions = game.map_dimensions
        self.width = self.dimensions.x
        self.height = self.dimensions.y
        self.prev_direction = None
        self.current_direction = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(PyQtGui.ONE_TICK_MS)
        self.separators_painter = QPainter(self)
        self.separators_painter.setPen(
            QPen(Qt.black, PyQtGui.CELL_SIZE * 0.5, Qt.SolidLine))


        self.layout = QVBoxLayout()
        self.label = QLabel("Score")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def start(self):
        while True:
            self.tick()

    def keyPressEvent(self, event):
        self.tick(event.key())

    def tick(self, key=None):
        direction = None
        if key == Qt.Key_Up:
            direction = Direction.Up
        elif key == Qt.Key_Left:
            direction = Direction.Left
        elif key == Qt.Key_Down:
            direction = Direction.Down
        elif key == Qt.Key_Right:
            direction = Direction.Right
        if direction is None:
            direction = self.prev_direction
        if not direction or not self.model.is_direction_valid(direction):
            return
        self.prev_direction = direction
        self.model.move(direction)
        self.timer.start()
        self.update()

    def paint_field(self):
        for x in range(self.width):
            for y in range(self.height):
                self.paint_cell(x, y,
                                PyQtGui.FIELD_PIXELS.get(self.model.get(x, y)))

    def paintEvent(self, a0: QPaintEvent) -> None:
        if not self.model.is_game_over:
            self.paint_field()

    def paint_cell(self, x: int, y: int, color: QColor) -> None:
        self.qp.begin(self)
        self.qp.fillRect(x * PyQtGui.CELL_SIZE, y * PyQtGui.CELL_SIZE,
                         PyQtGui.CELL_SIZE, PyQtGui.CELL_SIZE, color)
        self.qp.end()
        self.separators_painter.begin(self)
        self.separators_painter.setPen(
            QPen(Qt.black, PyQtGui.CELL_SIZE * 0.15, Qt.SolidLine))
        self.separators_painter.drawRect(x * PyQtGui.CELL_SIZE,
                                         y * PyQtGui.CELL_SIZE,
                                         PyQtGui.CELL_SIZE, PyQtGui.CELL_SIZE)
        self.separators_painter.end()

