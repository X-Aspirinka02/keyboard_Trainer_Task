import curses
from Views.IView import IView


class TournamentStatsView(IView):
    """
    Представление для отображения истории результатов упражнений.
    """

    def __init__(self, stats):
        """
        Инициализирует представление истории результатов.

        Args:
            records: Список записей истории для отображения
        """
        self.stats = stats
        self.scroll_position = 0
        self._initialize_colors()

    def _initialize_colors(self):
        """Настраивает цветовые пары для отображения."""
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Обычный текст
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Выделение для хороших результатов
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Выделение для средних результатов
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)  # Выделение для плохих результатов

    def draw(self, window: curses.window):
        """
        Отрисовывает экран с историей результатов.

        Args:
            window: Окно curses для отрисовки
        """
        window.clear()
        max_y, max_x = window.getmaxyx()

        window.addstr(0, 0, "История результатов", curses.A_BOLD)
        window.addstr(1, 0, "=" * (max_x - 1))

        headers = ["Язык", "Сложность", "Имя", "Равномерность", "Правильные нажатия"]
        header_widths = [19, 10, 10, 18, 10]

        y_pos = 2
        x_pos = 0

        for i, header in enumerate(headers):
            window.addstr(y_pos, x_pos, header, curses.A_BOLD)
            x_pos += header_widths[i]

        y_pos += 1
        window.addstr(y_pos, 0, "-" * (max_x - 1))
        y_pos += 1

        if not self.stats:
            window.addstr(y_pos, 0, "Нет записей истории")
        else:
            max_visible_records = max_y - y_pos - 3

            display_stats = list(reversed(self.stats))
            visible_records = display_stats[self.scroll_position:self.scroll_position + max_visible_records]

            for record in visible_records:
                x_pos = 0

                window.addstr(y_pos, x_pos, record["language"], curses.color_pair(1))
                x_pos += header_widths[0]

                window.addstr(y_pos, x_pos, record["difficulty"], curses.color_pair(1))
                x_pos += header_widths[1]

                window.addstr(y_pos, x_pos, record["name"], curses.color_pair(1))
                x_pos += header_widths[2]


                window.addstr(y_pos, x_pos, f"{record["uniformity_score"]}%", curses.color_pair(2))
                x_pos += header_widths[4]

                window.addstr(y_pos, x_pos, f"{record["correct_keystrokes"]}", curses.color_pair(2))



                y_pos += 1

            total_pages = (len(display_stats) + max_visible_records - 1) // max_visible_records
            current_page = self.scroll_position // max_visible_records + 1

            if total_pages > 1:
                window.addstr(max_y - 3, 0, f"Страница {current_page}/{total_pages}")

        window.addstr(max_y - 2, 0, "=" * (max_x - 1))
        window.addstr(max_y - 1, 0, "↑/↓: прокрутка  |  Q: выход", curses.A_BOLD)

        window.refresh()

    def scroll_up(self):
        """
        Прокручивает список записей вверх.

        Returns:
            bool: True, если прокрутка выполнена
        """
        if self.scroll_position > 0:
            self.scroll_position -= 1
            return True
        return False

    def scroll_down(self, max_visible_records):
        """
        Прокручивает список записей вниз.

        Args:
            max_visible_records: Максимальное количество видимых записей

        Returns:
            bool: True, если прокрутка выполнена
        """
        # Получаем общее количество записей (с учетом реверса списка)
        total_records = len(self.stats)

        if self.scroll_position < total_records - max_visible_records:
            self.scroll_position += 1
            return True
        return False

    def get_max_visible_records(self, window_height):
        """
        Рассчитывает максимальное количество видимых записей.

        Args:
            window_height: Высота окна

        Returns:
            int: Максимальное количество видимых записей
        """
        # 7 = 2 (заголовок) + 1 (шапка таблицы) + 1 (разделитель) + 3 (нижняя информация)
        return window_height - 7