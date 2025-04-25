import json
import os
import time
from datetime import datetime
from Models.SettingsModel import Language, Difficulty, Level

class RecordModel:
    """
    Модель для хранения и управления историей результатов упражнений.
    """
    def __init__(self):
        self.records_file = "records.json"
        self.records = self._load_records()
        
    def _load_records(self):
        """
        Загружает историю результатов из файла.
        
        Returns:
            dict: Словарь с историей результатов
        """
        if os.path.exists(self.records_file):
            try:
                with open(self.records_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"records": []}
        return {"records": []}
    
    def save_record(self, language: Language, difficulty: Difficulty, level: Level, 
                   chars_typed: int, total_chars: int, correct_keystrokes: int, time_elapsed: float):
        """
        Сохраняет результат упражнения в историю.
        
        Args:
            language: Язык упражнения
            difficulty: Сложность упражнения
            level: Уровень упражнения
            chars_typed: Количество введенных символов
            total_chars: Общее количество символов в упражнении
            correct_keystrokes: Количество корректных нажатий
            time_elapsed: Время выполнения упражнения в секундах
        """
        accuracy = (correct_keystrokes / chars_typed) * 100 if chars_typed > 0 else 0
        wpm = (chars_typed / 5) / (time_elapsed / 60) if time_elapsed > 0 else 0
        
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "language": language.name,
            "difficulty": difficulty.name,
            "level": f"Level {level.value}",
            "chars_typed": chars_typed,
            "total_chars": total_chars,
            "correct_keystrokes": correct_keystrokes,
            "accuracy": round(accuracy, 2),
            "wpm": round(wpm, 2),
            "time_elapsed": round(time_elapsed, 2),
            "completed": chars_typed >= total_chars
        }
        
        self.records["records"].append(record)
        self._save_to_file()
    
    def _save_to_file(self):
        """
        Сохраняет историю результатов в файл.
        """
        with open(self.records_file, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=4, ensure_ascii=False)
    
    def get_last_records(self, count=5):
        """
        Возвращает последние records из истории.
        
        Args:
            count: Количество записей для возврата
            
        Returns:
            list: Список последних записей
        """
        # Сортируем записи по дате (самые новые в конце)
        sorted_records = sorted(
            self.records["records"], 
            key=lambda r: r["timestamp"]
        )
        
        # Возвращаем последние count записей
        return sorted_records[-count:]
    
    def get_best_record(self, language=None, difficulty=None, level=None):
        """
        Возвращает лучший результат по WPM для указанных параметров.
        
        Args:
            language: Фильтр по языку
            difficulty: Фильтр по сложности
            level: Фильтр по уровню
            
        Returns:
            dict: Лучший результат
        """
        records = self.records["records"]
        
        if language:
            records = [r for r in records if r["language"] == language.name]
        if difficulty:
            records = [r for r in records if r["difficulty"] == difficulty.name]
        if level:
            records = [r for r in records if r["level"] == f"Level {level.value}"]
            
        if not records:
            return None
            
        return max(records, key=lambda x: x["wpm"]) 