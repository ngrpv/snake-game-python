import curses
import traceback

from time import sleep
from common.enums import Direction, MapCellType
from common.game import Game


class UICurses:
    ONE_TICK_SEC = 0.05
    AUTOMOVE_TICKS = 5
    FIELD_PIXELS = {
        MapCellType.Empty: " ",
        MapCellType.Snake: "o",
        MapCellType.Food: "@",
        MapCellType.Obstacle: "#"
    }

    @staticmethod
    def get_screen_size_wh() -> (int, int):
        try:
            stdscr = curses.initscr()
            result = stdscr.getmaxyx()
        finally:
            curses.endwin()

        return result[1], result[0]

    def __init__(self, game: Game):
        self._model = game
        self._stdscr = curses.initscr()
        self._stdscr.keypad(True)
        self._stdscr.nodelay(True)
        self._map_buffer = dict()

        game_is_running = True
        try:
            update_count = 0
            direction = None
            while game_is_running and not self._model.is_game_over:
                inp = self._stdscr.getch()
                key_code = inp
                while inp != curses.ERR:
                    key_code = inp
                    inp = self._stdscr.getch()
                if key_code == ord("q"):
                    game_is_running = False
                if key_code == curses.KEY_DOWN:
                    direction = Direction.Down
                    update_count = 0
                if key_code == curses.KEY_UP:
                    direction = Direction.Up
                    update_count = 0
                if key_code == curses.KEY_LEFT:
                    direction = Direction.Left
                    update_count = 0
                if key_code == curses.KEY_RIGHT:
                    direction = Direction.Right
                    update_count = 0

                if direction and not self._model.is_direction_valid(direction):
                    direction = None

                if update_count == 0:
                    self._model.move(direction)
                    self._draw_frame()

                update_count += 1
                update_count %= self.AUTOMOVE_TICKS

                sleep(self.ONE_TICK_SEC)

            game_over_text = "You win!!1" if self._model.is_game_clear else "Game over"
            self._stdscr.addstr(
                self._model.map_dimensions.y // 2,
                (self._model.map_dimensions.x - 9) // 2,
                game_over_text)
            self._stdscr.refresh()
            sleep(2)
        except Exception:
            self.__del__()
            traceback.print_exc()

    def __del__(self):
        curses.nocbreak()
        self._stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def _draw_frame(self):
        screen = self._stdscr
        model = self._model
        map_dimensions = model.map_dimensions

        for j in range(map_dimensions.y):
            for i in range(map_dimensions.x):
                cell_type = model.get(i, j)
                coordinates = (i, j)
                if (coordinates not in self._map_buffer
                        or self._map_buffer[coordinates] != cell_type):
                    screen.addstr(j, i, self.FIELD_PIXELS[cell_type])
                self._map_buffer[coordinates] = cell_type

        status_line = f"Level: {model.level_number} | Score: {model.score}"
        screen.addstr(map_dimensions.y, 2,
                      status_line)

        screen.refresh()
