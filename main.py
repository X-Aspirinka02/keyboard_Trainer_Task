import curses
from src.Presenters.RootPresenter import RootPresenter
import locale


def main(stdscr: curses.window):
    stdscr.encoding = 'utf-8'
    locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
    root_presenter = RootPresenter(stdscr)
    root_presenter.run()


curses.wrapper(main)
