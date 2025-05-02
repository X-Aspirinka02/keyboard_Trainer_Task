class GameModel:
    """
    Модель клавиатурного тренажера, отслеживающая состояние упражнения и статистику.
    """
    def __init__(self):
        """
        Инициализирует игровую модель.
        """
        self._text = ""
        self._correct_keystrokes = 0
        self._exercise_time_seconds = 60
        self._current_position = 0
        self._is_completed = False

    def process_keystroke(self, key_char: str) -> bool:
        """
        Обрабатывает нажатие клавиши и проверяет корректность.
        
        Args:
            key_char: введенный символ
            
        Returns:
            bool: корректное нажатие или нет
        """
        if self._current_position >= len(self._text):
            self._is_completed = True
            return False

        is_correct = key_char == self._text[self._current_position]
        
        if is_correct:
            self._correct_keystrokes += 1
            
        self._current_position += 1
        
        if self._current_position >= len(self._text):
            self._is_completed = True
            
        return is_correct

    def set_exercise_text(self, text: str) -> None:
        """Устанавливает текст для упражнения."""
        self._text = text
        self._reset()

    def set_level(self, text: str) -> None:
        """
        Устанавливает текст упражнения (для совместимости с существующим кодом).
        
        Args:
            text: Текст для упражнения
        """
        self.set_exercise_text(text)
        
    def set_exercise_time(self, seconds: int) -> None:
        """
        Устанавливает таймер для упражнения.
        :param seconds: Сколько времени будет проходить упражнение
        :return: Сколько времени будет проходить упражнение
        """
        self._exercise_time_seconds = seconds
        
    def _reset(self) -> None:
        """Сбрасывает прогресс упражнения"""
        self._correct_keystrokes = 0
        self._current_position = 0
        self._is_completed = False
        
    @property
    def text(self) -> str:
        """Получить текст упражнения."""
        return self._text
        
    @property
    def current_position(self) -> int:
        """Получить позицию в упражнении"""
        return self._current_position
        
    @property
    def correct_keystrokes(self) -> int:
        """Получить количество корректных нажатий"""
        return self._correct_keystrokes
        
    @property
    def exercise_time_seconds(self) -> int:
        """Получить продолжительность упражнения в секундах"""
        return self._exercise_time_seconds
        
    @property
    def is_completed(self) -> bool:
        """Проверить, завершено ли упражнение"""
        return self._is_completed