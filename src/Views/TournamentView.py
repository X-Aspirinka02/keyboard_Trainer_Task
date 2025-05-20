import curses

from src.Views.IView import IView


class TournamentView(IView):

    def __init__(self):
        self.init_colors()

    def init_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

    def show_init_gamer(self, window: curses.window, gamer_count: int):
        curses.echo()
        gamers = []
        for gamer in range(0, gamer_count):
            window.clear()
            window.addstr(0, 0,
                          f"Введите имя игрока {gamer}", curses.color_pair(1))
            window.move(2, 0)
            game_name = window.getstr()
            gamers.append(game_name)
        return gamers

    def draw(self, window: curses.window):
        """
        Отрисовывает начальный экран с инициализацией турнира
        :param window: окно приложения
        """""

        curses.echo()
        exit_tour = False
        incorrect_input = False
        gamers_count = 0
        while not exit_tour:

            window.clear()
            window.addstr(0, 0, "Начните турнир!", curses.color_pair(3))
            window.addstr(1, 0,
                          "Введите количество игроков, " +
                          "которые будут участвовать в турнире.",
                          curses.color_pair(3))
            window.addstr(3, 0, "Выход: Q")
            window.addstr(4, 0, "Конец ввода: ENTER")
            if incorrect_input:
                window.addstr(5, 0,
                              "Некорректный ввод, введите еще раз.",
                              curses.color_pair(4))
            window.move(2, 0)

            key = window.getstr()

            if key == b'q' or key == b'Q':
                exit_tour = True

            try:
                gamers_count += int(key)
                incorrect_input = gamers_count % 2 != 0
                if incorrect_input:
                    gamers_count = 0
                    continue
                # exit_tour = True
                return gamers_count
            except ValueError:
                incorrect_input = True
                gamers_count = 0
                continue

        window.refresh()

    def show_vs(self, window: curses.window, gamer1: bytes, gamer2: bytes):
        window.clear()
        window.addstr(0, 0, f"{gamer1.decode("utf-8")}" +
                      f" vs {gamer2.decode("utf-8")}", curses.color_pair(4))
        window.refresh()

    def show_start(self, window: curses.window):
        window.clear()
        window.addstr(0, 0, "НАЧИНАЕМ ТУРНИР!", curses.color_pair(3))
        window.addstr(1, 0,
                      "Нажмите любую клавишу, чтобы начать . . .",
                      curses.color_pair(1))
        window.refresh()
        window.getch()

    def show_winer(self, stdscr: curses.window, winner: bytes):
        stdscr.clear()
        stdscr.addstr(0, 0, f"Победитель: {winner}", curses.color_pair(2))
        stdscr.addstr(1, 0, "Поздравляем!", curses.color_pair(2))
        stdscr.refresh()
        stdscr.getch()

    def is_big_text(self, stdscr: curses.window):
        stdscr.clear()
        stdscr.addstr(0, 0, "Хотите сыграть на большом тексте?")
        stdscr.addstr(1, 0, "1 - да")
        stdscr.addstr(2, 0, "2 - нет")
        stdscr.move(3, 0)
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord("1"):
            return True
        else:
            return False
