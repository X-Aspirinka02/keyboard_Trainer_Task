from src.Models.RecordModel import RecordModel
import curses
from src.Views.RecordsView import RecordsView
from src.Models.GameModel import GameModel
from src.Models.SettingsModel import SettingsModel


class RecordPresenter:
    """
    Презентер для рекордов. Отвечает за управление отображениями рекордов.
    """

    def __init__(self, stdscr: curses.window, game_model: GameModel,
                 settings_model: SettingsModel, record_model: RecordModel):
        self.record_model = record_model
        self.stdscr = stdscr
        self.game_model = game_model
        self.settings_model = settings_model
        self.current_result = {}

    def save_exercise_rec(self, current_result: dict):
        """
        Сохраняет результат упражнения в историю.
        """

        chars_typed = self.game_model.current_position
        total_chars = len(self.game_model.text)
        correct_keystrokes = current_result['correct_keystrokes']

        # Расчет метрик
        accuracy = current_result['accuracy']
        wpm = current_result['wpm']

        # Проверка, является ли это лучшим результатом
        previous_best = self.record_model.get_best_record(
            language=self.settings_model.current_language,
            difficulty=self.settings_model.current_difficulty,
            level=self.settings_model.current_level
        )

        is_best_record = False
        if previous_best is None or wpm > previous_best['wpm']:
            is_best_record = True

        # Сохраняем данные для отображения в результатах
        self.current_result = {
            'wpm': wpm,
            'accuracy': accuracy,
            'is_best_record': is_best_record
        }
        self.save_record(chars_typed, total_chars,
                         correct_keystrokes, current_result['elapsed_time'])
        return is_best_record

    def save_record(self, chars_typed, total_chars,
                    correct_keystrokes, elapsed_time):
        # Сохраняем результат
        self.record_model.save_record(
            language=self.settings_model.current_language,
            difficulty=self.settings_model.current_difficulty,
            level=self.settings_model.current_level,
            chars_typed=chars_typed,
            total_chars=total_chars,
            correct_keystrokes=correct_keystrokes,
            time_elapsed=elapsed_time
        )

    def show_records_history(self):
        """
        Отображает историю результатов упражнений с возможностью прокрутки.
        """

        # Увеличиваем количество записей для отображения
        records = self.record_model.get_last_records(30)
        records_view = RecordsView(records)

        self.stdscr.clear()
        records_view.draw(self.stdscr)
        self.stdscr.nodelay(False)

        # Обрабатываем ввод пользователя для прокрутки истории
        should_exit = False
        while not should_exit:
            max_y, max_x = self.stdscr.getmaxyx()
            max_visible_records = records_view.get_max_visible_records(max_y)

            key = self.stdscr.getch()

            if key == ord('q') or key == ord('Q') or key == 27:  # q, Q или ESC
                should_exit = True
            elif key == curses.KEY_UP:
                if records_view.scroll_up():
                    records_view.draw(self.stdscr)
            elif key == curses.KEY_DOWN:
                if records_view.scroll_down(max_visible_records):
                    records_view.draw(self.stdscr)
