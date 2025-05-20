import json
import os
from src.Models.SettingsModel import Language, Difficulty


class TournamentStatsModel:
    """
    Модель для хранения и управления историей результатов упражнений.
    """

    def __init__(self):
        self.tournament_file = "tournament.json"
        self.stats = self._load_stats()

    def _load_stats(self):
        """
        Загружает историю результатов из файла.

        Returns:
            dict: Словарь с историей результатов
        """
        if os.path.exists(self.tournament_file):
            try:
                with open(self.tournament_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"stats": []}
        return {"stats": []}

    def save_stat(self, language: Language, difficulty: Difficulty,
                  name: bytes, correct_keystrokes: int, uniformity_score: int):
        """
        Сохранение победителей.
        """

        record = {
            "language": language.name,
            "difficulty": difficulty.name,
            "correct_keystrokes": correct_keystrokes,
            "uniformity_score": uniformity_score,
            "name": name
        }

        self.stats["stats"].append(record)
        self._save_to_file()

    def _save_to_file(self):
        """
        Сохраняет историю результатов в файл.
        """
        with open(self.tournament_file, "w", encoding="utf-8") as f:
            json.dump(self.stats, f, indent=4, ensure_ascii=False)

    def get_last_records(self, count=5):
        """
        Взять последние count рекордов турнира.
        :param count: Количество записей.
        :return: Count записей
        """

        return self.stats['stats'][-count:]
