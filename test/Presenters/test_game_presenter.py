import unittest
from unittest.mock import MagicMock, patch

from src.Presenters.GamePresenter import GamePresenter


class TestGamePresenter(unittest.TestCase):
    def setUp(self):
        self.mock_stdscr = MagicMock()
        self.mock_game_model = MagicMock()
        self.mock_settings_model = MagicMock()
        self.mock_record_model = MagicMock()

        self.mock_game_model.exercise_time_seconds = 5
        self.mock_game_model.is_completed = False
        self.mock_game_model.current_position = 0
        self.mock_game_model.correct_keystrokes = 0
        self.mock_game_model.text = "test text"

        # Имитация поведения process_keystroke
        def mock_process_keystroke(key_char: str) -> bool:
            if self.mock_game_model.current_position >= len(
                    self.mock_game_model.text):
                self.mock_game_model.is_completed = True
                return False

            is_correct = key_char == self.mock_game_model.text[
                self.mock_game_model.current_position]
            if is_correct:
                self.mock_game_model.correct_keystrokes += 1

            self.mock_game_model.current_position += 1

            if self.mock_game_model.current_position >= len(
                    self.mock_game_model.text):
                self.mock_game_model.is_completed = True

            return is_correct

        # Используем MagicMock для process_keystroke
        self.mock_game_model.process_keystroke = MagicMock(
            side_effect=mock_process_keystroke)

        self.presenter = GamePresenter(
            stdscr=self.mock_stdscr,
            game_model=self.mock_game_model,
            settings_model=self.mock_settings_model,
            record_model=self.mock_record_model
        )

        self.presenter.exercise_view = MagicMock()

    @patch('time.time')
    def test_run_exercise_basic_flow(self, mock_time):
        test_text = "test text"
        self.mock_game_model.text = test_text

        # Симулируем ввод символов
        input_chars = [ord(c) for c in test_text] + [-1]
        self.mock_stdscr.getch.side_effect = input_chars

        # Эмулируем время
        mock_time.side_effect = list(range(20))

        # Выполнение
        self.presenter._run_exercise()

        # Проверки вызовов
        self.presenter.exercise_view.draw.assert_called_once_with(
            self.mock_stdscr)
        self.presenter.exercise_view.show_exercise.assert_called_once_with(
            self.mock_stdscr)
        self.mock_stdscr.nodelay.assert_called_once_with(True)


if __name__ == '__main__':
    unittest.main()
