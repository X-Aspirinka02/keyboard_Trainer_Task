import curses
import time
from src.Models.SettingsModel import SettingsModel
from src.Models.ExerciseModel import ExerciseModel
from src.Models.GameModel import GameModel
from src.Models.RecordModel import RecordModel
from src.Views.ExerciseView import ExerciseView


class GamePresenter:
    """
    Презентер для игры, отвечающий за управление прохождением упражнения.
    """

    def __init__(self, stdscr: curses.window, game_model: GameModel,
                 settings_model: SettingsModel,
                 record_model: RecordModel = None):
        """
        Инициализация презентера игры.

        Args:
            stdscr: Окно curses для отображения интерфейса
        """

        self.settings_model = settings_model
        self.exercise_model = None
        self.game_model = game_model
        self.record_model = record_model
        self.exercise_view = None
        self.current_result = {}

        self.stdscr = stdscr

    def start_game(self):
        """
        Запускает игру с выбранными параметрами.
        """

        self._initialize_exercise()
        return self._run_exercise()

    def _initialize_exercise(self):
        """
        Инициализирует упражнение на основе выбранных настроек.
        """

        self.exercise_model = ExerciseModel(
            difficulty=self.settings_model.current_difficulty,
            level=self.settings_model.current_level,
            language=self.settings_model.current_language
        )

        exercise_text = self.exercise_model.get_exercise_text()
        self.game_model.set_level(exercise_text)

        # Получаем лучший результат для текущего упражнения
        if self.record_model is not None:
            best_record = self.record_model.get_best_record(
                language=self.settings_model.current_language,
                difficulty=self.settings_model.current_difficulty,
                level=self.settings_model.current_level
            )

            self.exercise_view = ExerciseView(exercise_text, best_record)
        self.exercise_view = ExerciseView(exercise_text)

    def _run_exercise(self):
        """
        Запускает упражнение по набору текста.
        Управляет циклом упражнения, обрабатывает ввод пользователя
        и обновляет отображение.
        """
        # Добавляем переменные для отслеживания времени нажатий
        last_keystroke_time = None
        keystroke_intervals = []
        avg_deviation = 0

        self.exercise_view.draw(self.stdscr)
        self.stdscr.getch()

        self.stdscr.clear()
        self.exercise_view.show_exercise(self.stdscr)
        self.stdscr.nodelay(True)

        start_time = time.time()

        while time.time() - start_time < self.game_model.exercise_time_seconds:
            key = self.stdscr.getch()

            if key == -1:
                continue

            if key == 27:
                break

            if self.game_model.is_completed:
                # self._show_exercise_completion()
                break

            current_time = time.time()

            # Записываем интервал между нажатиями
            if last_keystroke_time is not None:
                actual_interval = current_time - last_keystroke_time
                keystroke_intervals.append(actual_interval)

            last_keystroke_time = current_time

            is_correct = self.game_model.process_keystroke(chr(key))

            self.exercise_view.update_display(
                self.stdscr,
                is_correct,
                self.game_model.current_position,
                self.game_model.correct_keystrokes
            )

        elapsed_time = time.time() - start_time

        chars_typed = self.game_model.current_position
        correct_keystrokes = self.game_model.correct_keystrokes

        # Расчет метрик
        accuracy = (correct_keystrokes /
                    chars_typed) * 100 if chars_typed > 0 else 0
        wpm = ((chars_typed / 5)
               / (elapsed_time / 60)) if elapsed_time > 0 else 0

        deviation_score = 0
        if len(keystroke_intervals) > 0:
            ideal_interval = (elapsed_time /
                              chars_typed) if chars_typed > 0 else 0

            deviations = [abs(interval -
                              ideal_interval)
                          for interval in keystroke_intervals]

            avg_deviation = (sum(deviations) /
                             len(deviations)) \
                if len(deviations) > 0 else 0

            deviation_score = min(100, int(avg_deviation /
                                           ideal_interval * 100)) \
                if ideal_interval > 0 else 0

        self.current_result = {
            'wpm': wpm,
            'accuracy': accuracy,
            "correct_keystrokes": correct_keystrokes,
            'elapsed_time': elapsed_time,
            'uniformity_score': 100 - deviation_score,
            'avg_deviation': avg_deviation
        }

        return self.current_result

    def _show_exercise_completion(self):
        """
        Отображает экран завершения упражнения.
        """

        self.exercise_view.show_results_screen(
            self.stdscr,
            self.game_model.correct_keystrokes
        )
        self.stdscr.getch()

    def show_exercise_results(self, is_best: bool):
        """
        Отображает экран с результатами упражнения.
        """

        wpm = self.current_result['wpm'] \
            if hasattr(self, 'current_result') else 0
        accuracy = self.current_result['accuracy'] if\
            hasattr(self, 'current_result') else 0
        is_best_record = is_best

        self.exercise_view.show_results_screen(
            self.stdscr,
            self.game_model.current_position,
            len(self.game_model.text),
            self.game_model.correct_keystrokes,
            wpm=wpm,
            accuracy=accuracy,
            is_best_record=is_best_record
        )
        self.stdscr.getch()
