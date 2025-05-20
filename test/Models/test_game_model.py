import unittest
from src.Models.GameModel import GameModel


class TestGameModel(unittest.TestCase):

    def setUp(self):
        self.test_game_model = GameModel()
        self.test_text = "Test text"

    def test_set_text_and_process_keystroke(self):
        # Проверяем установку текста
        self.test_game_model.set_exercise_text(self.test_text)
        self.assertEqual(self.test_text, self.test_game_model.text)
        # Проверяем правильное нажатие
        right_ans = self.test_game_model.process_keystroke(self.test_text[0])
        self.assertEqual(True, right_ans)
        # Проверяем неправильное нажатие
        wrong_ans = self.test_game_model.process_keystroke("-")
        self.assertEqual(False, wrong_ans)
