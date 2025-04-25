import curses
import time
from Models.SettingsModel import Language, Difficulty, Level, SettingsModel
from Models.ExerciseModel import ExerciseModel
from Models.GameModel import GameModel
from Models.RecordModel import RecordModel
from Views.ListView import ListView
from Views.ExerciseView import ExerciseView
from Views.RecordsView import RecordsView

class GamePresenter:
    """
    Презентер для игры, координирующий взаимодействие между моделями и представлениями.
    Отвечает за обработку пользовательского ввода и обновление отображения.
    TODO: Разбить на несколько презентеров надо наверное
    """
    def __init__(self, stdscr: curses.window):
        """
        Инициализация презентера игры.
        
        Args:
            stdscr: Окно curses для отображения интерфейса
        """
        self.settings_model = SettingsModel()
        self.exercise_model = None
        self.game_model = GameModel()
        self.record_model = RecordModel()
        self.exercise_view = None

        self.stdscr = stdscr
        self.current_view = None
        self.current_view_type = None

        self._setup_terminal()
        self.show_language_selection()

    def _setup_terminal(self):
        """
        Настраивает параметры терминала для работы приложения.
        """
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Для выделения выбранного элемента

        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

    def run(self):
        """
        Основной цикл работы презентера и программы.
        Обрабатывает пользовательский ввод и обновляет отображение.
        """
        curses.noecho()
        curses.cbreak()
        self.stdscr.clear()

        try:
            while True:
                self._update()
                self._draw()
        except Exception as e:
            self._show_error(str(e))
        finally:
            self.stop()

    def _show_error(self, error_message: str):
        """
        Отображает сообщение об ошибке.
        
        Args:
            error_message: Сообщение об ошибке
        """
        self.stdscr.addstr(0, 0, f"Ошибка: {error_message}")
        self.stdscr.refresh()
        self.stdscr.getch()

    def _update(self):
        """
        Обновляет состояние презентера и модели на основе пользовательского ввода.
        """
        key = self.stdscr.getch()
        
        if self.current_view is not None:
            self.handle_input(key)

    def handle_input(self, key: int):
        """
        Обрабатывает пользовательский ввод.
        
        Args:
            key: Код нажатой клавиши
        """
        if isinstance(self.current_view, ListView):
            self._handle_list_view_input(key)

    def _handle_list_view_input(self, key: int):
        """
        Обрабатывает ввод для представления списка.
        
        Args:
            key: Код нажатой клавиши
        """
        if key == curses.KEY_DOWN:
            self.settings_model.select_next_item()
            self.current_view.update_selected_item(self.settings_model.current_selected_item)
        elif key == curses.KEY_UP:
            self.settings_model.select_prev_item()
            self.current_view.update_selected_item(self.settings_model.current_selected_item)
        elif key in [curses.KEY_ENTER, 10, 13]:
            self.handle_selection()
        elif key == ord('h'):  # Добавляем возможность просмотра истории результатов
            self.show_records_history()

    def handle_selection(self):
        """
        Обрабатывает выбор пользователя в текущем представлении.
        """
        match self.current_view_type:
            case "language":
                self.settings_model.set_language()
                self.show_difficulty_selection()
            case "difficulty":
                self.settings_model.set_difficulty()
                self.show_level_selection()
            case "level":
                self.settings_model.set_level()
                self.start_game()

    def _create_selection_view(self, items, header, view_type):
        """
        Создает представление для выбора из списка.
        
        Args:
            items: Список элементов для выбора
            header: Заголовок представления
            view_type: Тип представления (язык, сложность, уровень)
        """
        self.current_view = ListView(items, header, view_type)
        self.current_view_type = view_type
        self.settings_model.current_selected_item = 0
        self.settings_model.items_count = len(items)

        self.current_view.update_selected_item(0)

    def show_language_selection(self):
        """
        Отображает экран выбора языка.
        """
        languages = [(f"{lang.name}", 1) for lang in Language]
        self._create_selection_view(languages, "Выберите язык, на котором хотите писать", "language")
    
    def show_difficulty_selection(self):
        """
        Отображает экран выбора сложности.
        """
        difficulties = [(f"{diff.name}", 1) for diff in Difficulty]
        self._create_selection_view(difficulties, "Выберите сложность", "difficulty")
    
    def show_level_selection(self):
        """
        Отображает экран выбора уровня.
        """
        levels = [(f"Level {level.value}", 1) for level in Level]
        self._create_selection_view(levels, "Выберите уровень", "level")
    
    def start_game(self):
        """
        Запускает игру с выбранными параметрами.
        """
        self._initialize_exercise()
        self._run_exercise()
        self.show_language_selection()

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
        best_record = self.record_model.get_best_record(
            language=self.settings_model.current_language,
            difficulty=self.settings_model.current_difficulty,
            level=self.settings_model.current_level
        )
        
        self.exercise_view = ExerciseView(exercise_text, best_record)

    def _run_exercise(self):
        """
        Запускает упражнение по набору текста.
        Управляет циклом упражнения, обрабатывает ввод пользователя
        и обновляет отображение.
        """
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
        self._save_exercise_record(elapsed_time)
        self._show_exercise_results()

    def _show_exercise_completion(self):
        """
        Отображает экран завершения упражнения.
        """
        self.exercise_view.show_completion_screen(
            self.stdscr, 
            self.game_model.correct_keystrokes
        )
        self.stdscr.getch()

    def _show_exercise_results(self):
        """
        Отображает экран с результатами упражнения.
        """
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

    def _save_exercise_record(self, elapsed_time: float):
        """
        Сохраняет результат упражнения в историю.
        
        Args:
            elapsed_time: Время выполнения упражнения
        """
        chars_typed = self.game_model.current_position
        total_chars = len(self.game_model.text)
        correct_keystrokes = self.game_model.correct_keystrokes
        
        # Расчет метрик
        accuracy = (correct_keystrokes / chars_typed) * 100 if chars_typed > 0 else 0
        wpm = (chars_typed / 5) / (elapsed_time / 60) if elapsed_time > 0 else 0
        
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
        
        # Полностью перерисовываем экран
        self.stdscr.clear()
        if self.current_view is not None:
            self.current_view.draw(self.stdscr)
        self.stdscr.refresh()

    def _draw(self):
        """
        Отрисовывает текущее представление.
        """
        self.stdscr.clear()
        if self.current_view is not None:
            self.current_view.draw(self.stdscr)
        self.stdscr.refresh()

    def stop(self):
        """
        Возвращает терминал в стандартное состояние.
        """
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()