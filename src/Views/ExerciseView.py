from src.Views.IView import IView
import curses
from src.Views.TextOutput import draw_text_with_wrap
from wcwidth import wcwidth
from typing import Optional


class ExerciseView(IView):
    """
    Представление для упражнения.
    """

    def __init__(self, exercise_text: str, best_record: Optional[dict] = None):
        self.exercise_text = exercise_text
        self.best_record = best_record
        self.index_column = 0
        self._initialize_colors()

    def _initialize_colors(self) -> None:
        """Устанавливает цвета для упражнения."""
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        # правильное нажатие
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
        # неправильное нажатие
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        # инфа о рекордах

    def draw(self, window: curses.window) -> None:
        """
        Отрисовывает начальный экран

        Args:
            window: окно из библиотеки curses, где отрисовывать.
        """
        window.clear()

        self.index_column = draw_text_with_wrap(window,
                                                self.exercise_text, 1, 0)

        window.addstr(self.index_column + 1, 0,
                      "Нажмите любую клавишу, чтобы начать...")

        # Показываем лучший результат, если есть
        if self.best_record:
            window.addstr(self.index_column + 3, 0,
                          "Your best result:",
                          curses.color_pair(3))
            window.addstr(self.index_column + 4, 0,
                          f"WPM: {self.best_record['wpm']:.1f}" +
                          f" | Accuracy: {self.best_record['accuracy']:.1f}%",
                          curses.color_pair(3))
            window.addstr(self.index_column + 5,
                          0, f"Date: {self.best_record['timestamp']}",
                          curses.color_pair(3))

        window.refresh()

    def show_exercise(self, window: curses.window) -> None:
        """
        Отображает текст упражнения в его начале.
        Args:
            window: окно из библиотеки curses, где отрисовывать
        """
        window.clear()
        draw_text_with_wrap(window, self.exercise_text, 1, 0)
        window.move(self.index_column + 1, 0)
        window.refresh()

    def update_display(self, window: curses.window, is_correct: bool,
                       current_position: int, correct_keystrokes: int) -> None:
        """
        Обновить экран (окно) после нажатия.

        Args:
            window: окно из библиотеки curses, где отрисовывать
            is_correct: было ли нажатие корректным
            current_position: нынешняя позиция в тексте
            correct_keystrokes: количество правильных нажатий
        """

        window.erase()
        window.move(0, 0)

        passed_text = self.exercise_text[:current_position - 1]
        current_char = self.exercise_text[current_position - 1]
        remaining_text = self.exercise_text[current_position:]
        y, x = 1, 0

        color_pair = 2 if is_correct else 1
        feedback = "CORRECT" if is_correct else "INCORRECT"
        window.addstr(self.index_column + 2,
                      0, feedback, curses.color_pair(color_pair))

        max_y, max_x = window.getmaxyx()

        for char in passed_text:
            if char == '\n' or x + wcwidth(char) >= max_x:
                y += 1
                x = 0
                if char == '\n':
                    continue

            window.addch(y, x, char)
            window.refresh()
            x += 1

        if current_char:
            if current_char == '\n' or x + wcwidth(current_char) >= max_x:
                y += 1
                x = 0
                if current_char != '\n':
                    window.addch(y, x,
                                 current_char, curses.color_pair(color_pair))
                    x += 1
            else:
                window.addch(y, x, current_char, curses.color_pair(color_pair))
                x += 1

        window.move(y, x)
        for i in range(y, self.index_column + 4):
            window.clrtoeol()

        for char in remaining_text:
            if char == '\n' or x + wcwidth(char) >= max_x:
                y += 1
                x = 0
                window.move(y, 0)
            if char != '\n':
                window.addch(y, x, char)
                x += 1

        window.addstr(self.index_column + 4, 0,
                      f"Correct keystrokes: {correct_keystrokes}")

        window.refresh()

    def show_results_screen(self, window: curses.window, chars_typed: int,
                            total_chars: int, correct_keystrokes: int,
                            wpm: float = 0, accuracy: float = 0,
                            is_best_record: bool = False) -> None:
        """
        Show the final results screen.
        Args:
            window: окно из библиотеки curses, где отрисовывать
            chars_typed: количество введенных
            total_chars: общеее количество символов в упражнении
            correct_keystrokes: количество корректных нажатий
            wpm: скорость набора (слов в минуту)
            accuracy: точность набора в процентах
            is_best_record: является ли этот результат лучшим
        """
        window.clear()
        window.nodelay(False)
        window.addstr(0, 0, "Exercise finished")
        window.addstr(1, 0, f"Correct keystrokes: {correct_keystrokes}")

        if chars_typed < total_chars:
            window.addstr(2, 0, "Characters typed:" +
                          f" {chars_typed}/{total_chars}")
        else:
            window.addstr(2, 0, "Exercise completed!")

        # Показываем результаты
        window.addstr(3, 0, f"Speed: {wpm:.1f}" +
                      f" WPM | Accuracy: {accuracy:.1f}%")

        if is_best_record:
            window.addstr(4, 0, "NEW BEST RECORD!",
                          curses.color_pair(2) | curses.A_BOLD)

        window.addstr(6, 0, "Press any key to continue")
        window.refresh()
