import unittest
from unittest.mock import MagicMock, patch

from src.Models.SettingsModel import SettingsModel
from src.Presenters.ListPresenter import ListPresenter


class TestListPresenter(unittest.TestCase):
    def setUp(self):
        self.mock_settings_model = MagicMock(SettingsModel)
        self.presenter = ListPresenter(settings_model=self.mock_settings_model)

    @patch('curses.init_pair')
    @patch('curses.COLOR_GREEN')
    @patch('curses.COLOR_BLACK')
    def test_show_language_selection(self,
                                     mock_color_black,
                                     mock_color_green,
                                     mock_init_pair):
        self.presenter.show_language_selection()

        self.assertEqual(self.presenter.current_view.items, [("English", 2),
                                                             ("Russian", 1),
                                                             ("Chinese", 1)])
        self.assertEqual(self.presenter.current_view.header,
                         "Выберите язык, на котором хотите писать")
        self.assertEqual(self.presenter.current_view_type, "language")

    @patch('curses.init_pair')
    @patch('curses.COLOR_GREEN')
    @patch('curses.COLOR_BLACK')
    def test_show_difficulty_selection(self,
                                       mock_color_black,
                                       mock_color_green,
                                       mock_init_pair):
        self.presenter.show_difficulty_selection()

        self.assertEqual(self.presenter.current_view.items,
                         [("simple", 2),
                          ("middle", 1),
                          ("hard", 1)])
        self.assertEqual(self.presenter.current_view.header,
                         "Выберите сложность")
        self.assertEqual(self.presenter.current_view_type, "difficulty")

    @patch('curses.init_pair')
    @patch('curses.COLOR_GREEN')
    @patch('curses.COLOR_BLACK')
    def test_show_level_selection(self,
                                  mock_color_black,
                                  mock_color_green, mock_init_pair):
        self.presenter.show_level_selection()

        self.assertEqual(self.presenter.current_view.items, [("Level 0", 2),
                                                             ("Level 1", 1),
                                                             ("Level 2", 1),
                                                             ("Level 3", 1),
                                                             ("Level 4", 1),
                                                             ("Big Text", 1)])
        self.assertEqual(self.presenter.current_view.header,
                         "Выберите уровень")
        self.assertEqual(self.presenter.current_view_type, "level")


if __name__ == '__main__':
    unittest.main()
