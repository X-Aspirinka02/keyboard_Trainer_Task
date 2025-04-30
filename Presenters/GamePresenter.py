import curses
import time
from Models.SettingsModel import SettingsModel
from Models.ExerciseModel import ExerciseModel
from Models.GameModel import GameModel
from Models.RecordModel import RecordModel
from Presenters.ListPresenter import ListPresenter
from Presenters.RecordPresenter import RecordPresenter
from Views.ExerciseView import ExerciseView

class GamePresenter:
    """
    Презентер для игры, координирующий взаимодействие между моделями и представлениями.
    Отвечает за обработку пользовательского ввода и обновление отображения.
    """
    def __init__(self, stdscr: curses.window, game_model:GameModel,
                 settings_model: SettingsModel, record_model: RecordModel):
        """
        Инициализация презентера игры.
        
        Args:
            stdscr: Окно curses для отображения интерфейса
        """
        # для каждого разбить
        self.settings_model = settings_model
        self.exercise_model = None
        self.game_model = game_model
        self.record_model = record_model
        self.exercise_view = None

        self.stdscr = stdscr
        self.current_view = None
        self.current_view_type = None


    def start_game(self, list_presenter: ListPresenter, record_presenter: RecordPresenter):
        """
        Запускает игру с выбранными параметрами.
        """
        #game
        self._initialize_exercise()
        self._run_exercise(record_presenter)
        list_presenter.show_language_selection()

    def _initialize_exercise(self):
        """
        Инициализирует упражнение на основе выбранных настроек.
        """
        #game
        self.exercise_model = ExerciseModel(
            difficulty=self.settings_model.current_difficulty,
            level=self.settings_model.current_level,
            language=self.settings_model.current_language
        )

        exercise_text = self.exercise_model.get_exercise_text()
        self.game_model.set_level(exercise_text)
        
        # Получаем лучший результат для текущего упражнения
        best_record = self.record_model.get_best_record(
            language=self.settings_model.current_language,
            difficulty=self.settings_model.current_difficulty,
            level=self.settings_model.current_level
        )
        
        self.exercise_view = ExerciseView(exercise_text, best_record)

    def _run_exercise(self,  record_presenter: RecordPresenter):
        """
        Запускает упражнение по набору текста.
        Управляет циклом упражнения, обрабатывает ввод пользователя
        и обновляет отображение.
        """
        #game
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
                self._show_exercise_completion()
                break
                
            is_correct = self.game_model.process_keystroke(chr(key))
            
            self.exercise_view.update_display(
                self.stdscr,
                is_correct,
                self.game_model.current_position,
                self.game_model.correct_keystrokes
            )
        
        elapsed_time = time.time() - start_time
        record_presenter.save_exercise_record(elapsed_time)
        self._show_exercise_results()

    def _show_exercise_completion(self):
        """
        Отображает экран завершения упражнения.
        """
        #game
        self.exercise_view.show_completion_screen(
            self.stdscr, 
            self.game_model.correct_keystrokes
        )
        self.stdscr.getch()

    def _show_exercise_results(self):
        """
        Отображает экран с результатами упражнения.
        """
        #game
        wpm = self.current_result['wpm'] if hasattr(self, 'current_result') else 0
        accuracy = self.current_result['accuracy'] if hasattr(self, 'current_result') else 0
        is_best_record = self.current_result['is_best_record'] if hasattr(self, 'current_result') else False
        
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



