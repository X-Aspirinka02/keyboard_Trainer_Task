import curses

from src.Models.tournament.TournamentStatsModel import TournamentStatsModel
from src.Models.GameModel import GameModel
from src.Models.SettingsModel import SettingsModel, Language, Difficulty
from src.Views.TournamentStatsView import TournamentStatsView


class TournamentStatPresenter:
    """
    Презентер для рекордов. Отвечает за управление отображениями рекордов.
    """

    def __init__(self, stdscr: curses.window, game_model: GameModel,
                 settings_model: SettingsModel,
                 stat_model: TournamentStatsModel):
        self.stat_model = stat_model
        self.stdscr = stdscr
        self.game_model = game_model
        self.settings_model = settings_model
        self.current_result = {}

    def save_winner(self, language: Language,
                    difficulty: Difficulty,
                    name: bytes, current_result: dict):
        """
        Сохраняет результат упражнения в историю.

        """
        language = language.name
        difficulty = difficulty.name
        correct_keystrokes = current_result['correct_keystrokes']
        uniformity_score = current_result['uniformity_score']

        # Сохраняем данные для отображения в результатах
        self.current_result = {
            "language": language,
            "difficulty": difficulty,
            'correct_keystrokes': correct_keystrokes,
            'uniformity_score': uniformity_score,
            'name': name
        }
        self.save_stat(correct_keystrokes, uniformity_score, name)

    def save_stat(self, correct_keystrokes, uniformity_score, name: bytes):
        # Сохраняем результат
        self.stat_model.save_stat(
            language=self.settings_model.current_language,
            difficulty=self.settings_model.current_difficulty,
            uniformity_score=uniformity_score,
            name=name,
            correct_keystrokes=correct_keystrokes,

        )
        self.show_records_history()

    def show_records_history(self):
        """
        Отображает историю результатов упражнений с возможностью прокрутки.
        """

        # Увеличиваем количество записей для отображения
        stats = self.stat_model.get_last_records(30)
        stats_view = TournamentStatsView(stats)

        self.stdscr.clear()
        stats_view.draw(self.stdscr)
        self.stdscr.nodelay(False)

        # Обрабатываем ввод пользователя для прокрутки истории
        should_exit = False
        while not should_exit:
            max_y, max_x = self.stdscr.getmaxyx()
            max_visible_records = stats_view.get_max_visible_records(max_y)

            key = self.stdscr.getch()

            if key == ord('q') or key == ord('Q') or key == 27:  # q, Q или ESC
                should_exit = True
            elif key == curses.KEY_UP:
                if stats_view.scroll_up():
                    stats_view.draw(self.stdscr)
            elif key == curses.KEY_DOWN:
                if stats_view.scroll_down(max_visible_records):
                    stats_view.draw(self.stdscr)
