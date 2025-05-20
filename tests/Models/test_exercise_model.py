import unittest

from src.Models.ExerciseModel import ExerciseModel
from src.Models.SettingsModel import Difficulty, Level, Language


class TestExerciseModel(unittest.TestCase):
    def setUp(self):
        """Настройка тестового окружения"""
        self.exercise = ExerciseModel(
            difficulty=Difficulty(0),
            level=Level(0),
            language=Language(0)
        )

    def test_get_file_path(self):
        """Тестирование формирования пути к файлу"""
        expected_path = "exercises/English_simple_l1.txt"
        self.assertEqual(self.exercise._get_file_path(), expected_path)


if __name__ == '__main__':
    unittest.main()
