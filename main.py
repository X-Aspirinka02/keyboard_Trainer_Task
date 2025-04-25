import curses
from Presenters.GamePresenter import GamePresenter
import locale



def main(stdscr: curses.window):
    stdscr.encoding = 'utf-8'
    locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
    game_presenter = GamePresenter(stdscr)
    game_presenter.run()

curses.wrapper(main)