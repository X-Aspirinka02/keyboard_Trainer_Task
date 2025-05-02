from Views.IView import IView
import curses
from wcwidth import wcwidth
from typing import Optional

class ExerciseView(IView):
    """
    Представление для упражнения.
    """
    def __init__(self, exercise_text: str, best_record: Optional[dict] = None):
        self.exercise_text = exercise_text
        self.best_record = best_record
        self._initialize_colors()
        
    def _initialize_colors(self) -> None:
        """Устанавливает цвета для упражнения."""
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)   # правильное нажатие
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN) # неправильное нажатие
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # инфа о рекордах
        
    def draw(self, window: curses.window) -> None:
        """
        Отрисовывает начальный экран
        
        Args:
            window: окно из библиотеки curses, где отрисовывать.
        """
        max_y, max_x = window.getmaxyx()
        window.clear()
        window.addstr(0, 0, self.exercise_text[:max_x])
        window.addstr(1, 0, "Press any key to start...")
        
        # Показываем лучший результат, если есть
        if self.best_record:
            window.addstr(3, 0, "Your best result:", curses.color_pair(3))
            window.addstr(4, 0, f"WPM: {self.best_record['wpm']:.1f} | Accuracy: {self.best_record['accuracy']:.1f}%", 
                        curses.color_pair(3))
            window.addstr(5, 0, f"Date: {self.best_record['timestamp']}", curses.color_pair(3))
        
        window.refresh()
        
    def show_exercise(self, window: curses.window) -> None:
        """
        Отображает текст упражнения в его начале.
        
        Args:
            window: окно из библиотеки curses, где отрисовывать
        """
        window.clear()
        max_y, max_x = window.getmaxyx()
        window.addstr(0, 0, self.exercise_text[:max_x])
        window.move(6, 0)
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

        color_pair = 2 if is_correct else 1
        feedback = "CORRECT" if is_correct else "INCORRECT"

        # Clear feedback line
        window.move(3, 0)
        window.clrtoeol()
        window.addstr(3, 0, feedback, curses.color_pair(color_pair))


        window.move(0, 0)
        window.clrtoeol()
        if current_position > 0:

            passed_text = self.exercise_text[:current_position-1]
            passed_count = 0
            for passed_char in passed_text:
                window.addstr(0, passed_count, passed_char)
                passed_count += wcwidth(passed_char)



            passed_width = 0
            for c in passed_text:
                passed_width+=wcwidth(c)

        else:

            passed_width = 0

        if current_position - 1 < len(self.exercise_text):

            current_char = self.exercise_text[current_position-1]
            window.addstr(0, passed_width, current_char, curses.color_pair(color_pair))


            remaining_text = self.exercise_text[current_position:]
            window.addstr(0, passed_width + wcwidth(current_char), remaining_text)

        window.addstr(5, 0, f"Correct keystrokes: {correct_keystrokes}")
        window.move(6, 0)
        window.refresh()
        
    def show_completion_screen(self, window: curses.window, correct_keystrokes: int) -> None:
        """
        Отображает сообщение о завершении упражнения
        
        Args:
            window: окно из библиотеки curses, где отрисовывать
            correct_keystrokes: количество правильных нажатий
        """
        window.clear()
        window.addstr(0, 0, "Exercise completed!")
        window.addstr(1, 0, f"Correct keystrokes: {correct_keystrokes}")
        window.addstr(2, 0, "Press any key to continue")
        window.nodelay(False)
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
            is_best_record: является ли этот результат лучшим для данных параметров
        """
        window.clear()
        window.nodelay(False)
        window.addstr(0, 0, "Exercise finished")
        window.addstr(1, 0, f"Correct keystrokes: {correct_keystrokes}")
        
        if chars_typed < total_chars:
            window.addstr(2, 0, f"Characters typed: {chars_typed}/{total_chars}")
        else:
            window.addstr(2, 0, "Exercise completed!")
            
        # Показываем результаты
        window.addstr(3, 0, f"Speed: {wpm:.1f} WPM | Accuracy: {accuracy:.1f}%")

        if is_best_record:
            window.addstr(4, 0, "NEW BEST RECORD!", curses.color_pair(2) | curses.A_BOLD)
            
        window.addstr(6, 0, "Press any key to continue")
        window.refresh()