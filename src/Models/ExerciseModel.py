from src.Models.SettingsModel import Difficulty, Level, Language


class ExerciseModel:
    """Класс для работы с упражнениями для тренировки"""

    def __init__(self, difficulty: Difficulty,
                 level: Level, language: Language):
        self.difficulty = difficulty
        self.level = level
        self.language = language
        self.base_extension = ".txt"
        self.exercises_path = "exercises/"

    def get_exercise_text(self) -> str:
        """Возвращает текст упражнения для тренажёра"""
        try:
            exercise_path = self._get_file_path()
            with open(exercise_path, "r", encoding="utf-8") as exercise_file:
                return exercise_file.read()
        except FileNotFoundError:
            return (f"Exercise not found for {self.language.name}" +
                    f", difficulty {self.difficulty.name}," +
                    f" level {self.level.name}")

    def _get_file_path(self) -> str:
        """Возвращает путь к файлу с заданием,
         основываясь на заданных сложности, уровне и языке"""
        return (f"{self.exercises_path}{self.language.name}" +
                f"_{self.difficulty.name}_" +
                f"{self.level.name}{self.base_extension}")
