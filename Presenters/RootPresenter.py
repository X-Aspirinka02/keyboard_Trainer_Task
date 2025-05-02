import curses

from Models.GameModel import GameModel
from Models.RecordModel import RecordModel
from Models.SettingsModel import SettingsModel
from Models.TournamentModel import TournamentModel
from Presenters.ListPresenter import ListPresenter
from Presenters.RecordPresenter import RecordPresenter
from Presenters.GamePresenter import GamePresenter
from Presenters.TournamentPresenter import TournamentPresenter
from Views.ListView import ListView


class RootPresenter:
    """
    Управляющая структура над всеми презентерами. Координирующая взаимодействие между моделями и представлениями.
    Отвечает за обработку пользовательского ввода и обновление отображения.
    """

    def __init__(self, stdscr: curses.window):
        """
        Инициализирует структуру.
        """

        self.stdscr = stdscr

        self.settings_model = SettingsModel()
        self.game_model = GameModel()
        self.record_model = RecordModel()
        self.tournament_model = TournamentModel()

        self.game_presenter = GamePresenter(stdscr, self.game_model,
                                            self.settings_model, self.record_model)
        self.list_presenter = ListPresenter(self.settings_model)
        self.tournament_presenter = TournamentPresenter(stdscr, self.tournament_model)
        self.record_presenter = RecordPresenter(stdscr, self.game_model,
                                                self.settings_model, self.record_model)

        self._setup_terminal()
        self.list_presenter.show_language_selection()

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

        if self.list_presenter.current_view is not None:
            self.handle_input(key)

    def handle_input(self, key: int):
        """
        Обрабатывает пользовательский ввод.

        Args:
            key: Код нажатой клавиши
        """

        if isinstance(self.list_presenter.current_view, ListView):
            self.handle_list_view_input(key)
            if key == ord('h'):  # Добавляем возможность просмотра истории результатов
                self.record_presenter.show_records_history()
            elif key == ord('t'):  # Добавляем возможность начать турнир
                self.tournament_presenter.show_tournament_begin()
                # Полностью перерисовываем экран
                self.stdscr.clear()
                if self.list_presenter.current_view is not None:
                    self.list_presenter.current_view.draw(self.stdscr)
                self.stdscr.refresh()

    def handle_list_view_input(self, key: int):
        """
        Обрабатывает ввод для представления списка.

        Args:
            key: Код нажатой клавиши
        """

        if key == curses.KEY_DOWN:
            self.settings_model.select_next_item()
            self.list_presenter.current_view.update_selected_item(self.settings_model.current_selected_item)
        elif key == curses.KEY_UP:
            self.settings_model.select_prev_item()
            self.list_presenter.current_view.update_selected_item(self.settings_model.current_selected_item)
        elif key in [curses.KEY_ENTER, 10, 13]:
            self.handle_selection()

    def handle_selection(self):
        """
        Обрабатывает выбор пользователя в текущем представлении.
        """

        match self.list_presenter.current_view_type:
            case "language":
                self.settings_model.set_language()
                self.list_presenter.show_difficulty_selection()
            case "difficulty":
                self.list_presenter.settings_model.set_difficulty()
                self.list_presenter.show_level_selection()
            case "level":
                self.settings_model.set_level()
                self.game_presenter.start_game(self.list_presenter, self.record_presenter)

    def _draw(self):
        """
        Отрисовывает текущее представление.
        """

        self.stdscr.clear()
        if self.list_presenter.current_view is not None:
            self.list_presenter.current_view.draw(self.stdscr)
        self.stdscr.refresh()

    def stop(self):
        """
        Возвращает терминал в стандартное состояние.
        """

        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
