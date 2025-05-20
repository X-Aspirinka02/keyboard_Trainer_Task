import unittest
from unittest.mock import MagicMock, patch
import curses

from src.Presenters.RecordPresenter import RecordPresenter
from src.Presenters.RootPresenter import RootPresenter
from src.Views.ListView import ListView


class TestRootPresenter(unittest.TestCase):

    @patch('src.Models.SettingsModel.SettingsModel')
    @patch('src.Models.GameModel.GameModel')
    @patch('src.Models.RecordModel.RecordModel')
    @patch('src.Presenters.ListPresenter.ListPresenter')
    @patch('src.Presenters.RecordPresenter.RecordPresenter')
    @patch('src.Presenters.GamePresenter.GamePresenter')
    @patch('src.Presenters.TournamentPresenter.TournamentPresenter')
    @patch('curses.initscr')
    @patch('curses.start_color')
    @patch('curses.init_pair')
    @patch('curses.noecho')
    @patch('curses.echo')
    @patch('curses.cbreak')
    @patch('curses.nocbreak')
    @patch('curses.endwin')
    def setUp(self, MockGetch, MockEndwin, MockNocbreak,
              MockCbreak, MockEcho, MockNoecho,
              MockInitPair, MockStartColor,
              MockInitscr,
              MockTournamentPresenter, MockGamePresenter,
              MockRecordPresenter, MockListPresenter, MockRecordModel,
              MockGameModel):
        self.stdscr = MagicMock(curses.window)
        MockInitscr.return_value = self.stdscr
        self.presenter = RootPresenter(self.stdscr)

    @patch('curses.start_color')
    @patch('curses.init_pair')
    @patch.object(RecordPresenter, "show_records_history",
                  return_value="Patched Method")
    def test_handle_input(self, MockInitPair, MockStartColor, MockRecord):
        self.presenter.list_presenter.current_view = ListView((
            [("English", 2), ("Russian", 1), ("Chinese", 1)]),
            "Выберите язык, на котором хотите писать",
            "language")
        self.presenter.record_presenter.show_records_history = MockRecord
        self.presenter.list_presenter.current_view.draw = MagicMock()
        self.presenter.handle_input(ord('h'))

        self.presenter.record_presenter.show_records_history.assert_called()

    def test_show_error(self):
        error_message = "Test error"
        self.presenter._show_error(error_message)

        self.stdscr.addstr.assert_called_once_with(
            0, 0, f"Ошибка: {error_message}")
        self.stdscr.refresh.assert_called()


if __name__ == '__main__':
    unittest.main()
