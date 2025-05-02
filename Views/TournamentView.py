import curses

from Views.IView import IView


class TournamentView(IView):

    def __init__(self):
        pass

    def show_init_gamer(self, window: curses.window, gamer_count: int):
        curses.echo()
        gamers = []
        for gamer in range(0, gamer_count):
            window.clear()
            window.addstr(0, 0, f"Введите имя игрока {gamer}")
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
            window.addstr(0, 0, "Начните турнир!")
            window.addstr(1, 0, "Введите количество игроков, которые будут участвовать в турнире.")
            window.addstr(3, 0, "Выход: Q")
            window.addstr(4, 0, "Конец ввода: ENTER")
            if incorrect_input:
                window.addstr(5, 0, "Некорректный ввод, введите еще раз.")
            window.move(2, 0)

            key = window.getstr()

            if key == b'q' or key == b'Q':
                exit_tour = True

            try:
                gamers_count += int(key)
                exit_tour = True
                return gamers_count
            except ValueError:
                incorrect_input = True
                gamers_count = 0
                continue

        window.refresh()