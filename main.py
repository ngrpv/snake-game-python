from common.game import Game
from common.level_empty import EmptyLevel
from common.level_with_borders import WithBordersLevel
from common.ui_curses import UICurses
from common.level_quarters import QuartersLevel

if __name__ == "__main__":
    screen_width, screen_height = UICurses.get_screen_size_wh()
    width = screen_width
    height = screen_height - 1

    levels = [
        QuartersLevel(width, height, 10),
        EmptyLevel(width, height, 2),
        WithBordersLevel(width, height, 3)
              ]

    model = Game(levels)
    UICurses(model)
