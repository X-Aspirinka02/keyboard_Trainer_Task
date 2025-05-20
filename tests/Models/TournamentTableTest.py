import unittest

from src.Models.SettingsModel import SettingsModel
from src.Models.tournament.TournamentTable import TournamentTable


class TournamentTableTest(unittest.TestCase):
    def setUp(self):
        self.test_gamers = ["player1", "player2", "player3", "player4"]
        self.test_settings_model = SettingsModel()

    def test_set_first_tour(self):
        test_tournament_table = TournamentTable(self.test_gamers,
                                                self.test_settings_model,
                                                False)
        # Проверяем, что в уздах то, что нужно
        player1 = test_tournament_table.table.get("player1")
        self.assertEqual(player1.tour, 2)
        self.assertEqual(player1.opponent, "player2")

        player2 = test_tournament_table.table.get("player2")
        self.assertEqual(player2.tour, 2)
        self.assertEqual(player2.opponent, "player1")

        player3 = test_tournament_table.table.get("player3")
        self.assertEqual(player3.tour, 2)
        self.assertEqual(player3.opponent, "player4")

        player4 = test_tournament_table.table.get("player4")
        self.assertEqual(player4.tour, 2)
        self.assertEqual(player4.opponent, "player3")
        # Проверяем что в таблице всё правильно
        self.assertEqual(test_tournament_table.table,
                         {"player1": player1, "player2": player2,
                          "player3": player3, "player4": player4})
