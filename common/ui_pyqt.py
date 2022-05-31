import sys

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QPainter, QPen, QFont, QPaintEvent
from PyQt5.QtWidgets import QApplication, QMainWindow

from common.enums import Direction, MapCellType
from common.game import Game


class PyQtGui:
    ONE_TICK_MS = 350
    FIELD_PIXELS = {
        MapCellType.Empty: QColor(0, 0, 0),
        MapCellType.Snake: QColor(0, 170, 0),
        MapCellType.Food: QColor(190, 0, 0),
        MapCellType.Obstacle: QColor(0, 0, 190),
        MapCellType.PortalOut: QColor(255, 154, 0),
        MapCellType.PortalIn: QColor(0, 162, 255)
    }
    GAME_OVER_COLOR = QColor(255, 255, 255)
    SCORE_COLOR = QColor(255, 255, 255)
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
        self.game_width = self.dimensions.x
        self.game_height = self.dimensions.y
        self.width = width
        self.height = height
        self.prev_direction = None
        self.current_direction = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(PyQtGui.ONE_TICK_MS)
        self.separators_painter = QPainter(self)
        self.separators_painter.setPen(
            QPen(Qt.black, PyQtGui.CELL_SIZE * 0.5, Qt.SolidLine))

    def keyPressEvent(self, event):
        self.tick(event.key())

    def tick(self, key=None):
        if key == Qt.Key_Up:
            direction = Direction.Up
        elif key == Qt.Key_Left:
            direction = Direction.Left
        elif key == Qt.Key_Down:
            direction = Direction.Down
        elif key == Qt.Key_Right:
            direction = Direction.Right
        else:
            direction = self.prev_direction

        if not direction or not self.model.is_direction_valid(direction):
            return

        self.prev_direction = direction
        self.model.move(direction)
        if self.model.is_game_over:
            self.timer.stop()
        else:
            self.timer.start()

        self.update()

    def paint_field(self):
        for x in range(self.game_width):
            for y in range(self.game_height):
                self.paint_cell(x, y,
                                PyQtGui.FIELD_PIXELS.get(self.model.get(x, y)))

        self.print_score_level()
        if self.model.is_game_over:
            self.print_game_over()

    def print_game_over(self):
        painter = QPainter(self)
        painter.begin(self)
        painter.setPen(PyQtGui.GAME_OVER_COLOR)
        painter.setFont(QFont("Arial", 50))
        game_over_text = "You win!!!" if self.model.is_game_clear else f"Game over"
        painter.drawText(0, 0, self.width, self.height,
                         Qt.AlignCenter, game_over_text)
        painter.end()

    def print_score_level(self):
        painter = QPainter(self)
        painter.begin(self)
        painter.setPen(PyQtGui.SCORE_COLOR)
        painter.setFont(QFont("Arial", 16))
        painter.drawText(0, 0, self.width, self.height,
                         Qt.AlignLeft, f"Score: {self.model.score}")
        painter.drawText(0, 0, self.width, self.height,
                         Qt.AlignRight, f"Level: {self.model.level_number} ")

        painter.end()

    def paintEvent(self, a0: QPaintEvent) -> None:
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
                                         PyQtGui.CELL_SIZE,
                                         PyQtGui.CELL_SIZE)
        self.separators_painter.end()
