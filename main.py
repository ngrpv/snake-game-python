from common.game import Game
from common.level_empty import EmptyLevel
from common.level_with_borders import WithBordersLevel
from common.ui_curses import UICurses

if __name__ == "__main__":
    screen_width, screen_height = UICurses.get_screen_size_wh()
    width = screen_width
    height = screen_height - 1

    levels = [
        EmptyLevel(width, height, 2),
        WithBordersLevel(width, height, 3)
              ]

    model = Game(levels)
    UICurses(model)
