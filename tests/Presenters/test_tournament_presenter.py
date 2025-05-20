import unittest
from unittest.mock import MagicMock, patch
from src.Models.SettingsModel import SettingsModel
from src.Presenters.GamePresenter import GamePresenter
from src.Presenters.TournamentPresenter import TournamentPresenter
from src.Presenters.TournamentStatPresenter import TournamentStatPresenter


class TestTournamentPresenter(unittest.TestCase):

    @patch('src.Models.GameModel.GameModel')
    @patch('src.Presenters.GamePresenter.GamePresenter')
    @patch('src.Views.TournamentView.TournamentView')
    @patch('src.Presenters.TournamentStatPresenter.TournamentStatPresenter')
    @patch('curses.start_color')
    @patch('curses.init_pair')
    def setUp(self, MockTournamentStat, MockTournamentView,
              MockGamePresenter, MockGameModel, mock_start_color,
              mock_init_pair):
        self.stdscr = MagicMock()
        self.settings_model = SettingsModel()
        self.presenter = TournamentPresenter(self.stdscr)

        # Настройка замокированных объектов
        self.presenter.game_model = MockGameModel.return_value
        self.presenter.tournament_view = MockTournamentView.return_value
        self.presenter.stat_presenter = MockTournamentStat.return_value
        self.presenter.stat_presenter.save_winner = MagicMock()

        # Настройка поведения замокированных методов
        self.presenter.tournament_view.draw.return_value = 4
        self.presenter.tournament_view.show_init_gamer.return_value = [
            b'Player1', b'Player2', b'Player3', b'Player4']
        self.presenter.tournament_view.is_big_text.return_value = False
        self.presenter.game_model.start_game.return_value = {
            'correct_keystrokes': 10,
            'uniformity_score': 5
        }

    @patch("curses.initscr")
    @patch("curses.flushinp")
    @patch.object(GamePresenter, 'start_game',
                  return_value={"correct_keystrokes": 20,
                                "uniformity_score": 5})
    @patch.object(TournamentStatPresenter, "save_winner")
    @patch("time.sleep")
    def test_tournament(self, mock_initscr, mock_flushinp, mock_start_game,
                        mock_stat, mock_sleep):
        self.presenter.tournament(self.settings_model)

        # Проверка, что методы были вызваны
        self.presenter.tournament_view.draw.assert_called_once()
        self.presenter.tournament_view.show_init_gamer.assert_called_once()
        self.presenter.tournament_view.show_start.assert_called_once()
        self.presenter.stat_presenter.save_winner.assert_called_once()




if __name__ == '__main__':
    unittest.main()
