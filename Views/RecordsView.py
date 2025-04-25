import curses
from Views.IView import IView

class RecordsView(IView):
    """
    Представление для отображения истории результатов упражнений.
    """
    def __init__(self, records):
        """
        Инициализирует представление истории результатов.
        
        Args:
            records: Список записей истории для отображения
        """
        self.records = records
        self.scroll_position = 0
        self._initialize_colors()
        
    def _initialize_colors(self):
        """Настраивает цветовые пары для отображения."""
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Обычный текст
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Выделение для хороших результатов
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Выделение для средних результатов
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)    # Выделение для плохих результатов
        
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

        headers = ["Дата", "Язык", "Сложность", "Уровень", "WPM", "Точность", "Завершено"]
        header_widths = [19, 10, 10, 10, 8, 10, 10]
        
        y_pos = 2
        x_pos = 0
        
        for i, header in enumerate(headers):
            window.addstr(y_pos, x_pos, header, curses.A_BOLD)
            x_pos += header_widths[i]
        
        y_pos += 1
        window.addstr(y_pos, 0, "-" * (max_x - 1))
        y_pos += 1

        if not self.records:
            window.addstr(y_pos, 0, "Нет записей истории")
        else:
            max_visible_records = max_y - y_pos - 3


            display_records = list(reversed(self.records))
            visible_records = display_records[self.scroll_position:self.scroll_position + max_visible_records]
            
            for record in visible_records:
                x_pos = 0

                window.addstr(y_pos, x_pos, record["timestamp"], curses.color_pair(1))
                x_pos += header_widths[0]

                window.addstr(y_pos, x_pos, record["language"], curses.color_pair(1))
                x_pos += header_widths[1]

                window.addstr(y_pos, x_pos, record["difficulty"], curses.color_pair(1))
                x_pos += header_widths[2]

                window.addstr(y_pos, x_pos, record["level"], curses.color_pair(1))
                x_pos += header_widths[3]


                wpm = record["wpm"]
                wpm_color = 2 if wpm > 30 else 3 if wpm > 20 else 4
                window.addstr(y_pos, x_pos, f"{wpm:.1f}", curses.color_pair(wpm_color))
                x_pos += header_widths[4]

                accuracy = record["accuracy"]
                acc_color = 2 if accuracy > 90 else 3 if accuracy > 70 else 4
                window.addstr(y_pos, x_pos, f"{accuracy:.1f}%", curses.color_pair(acc_color))
                x_pos += header_widths[5]

                completed = "Да" if record["completed"] else "Нет"
                comp_color = 2 if record["completed"] else 4
                window.addstr(y_pos, x_pos, completed, curses.color_pair(comp_color))
                
                y_pos += 1
                
            total_pages = (len(display_records) + max_visible_records - 1) // max_visible_records
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
        total_records = len(self.records)
        
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