import enum
import random


class Difficulty(enum.Enum):
    simple = 0
    middle = 1
    hard = 2


class Language(enum.Enum):
    English = 0
    Russian = 1
    Chinese = 2


class Level(enum.Enum):
    l1 = 0
    l2 = 1
    l3 = 2
    l4 = 3
    l5 = 4
    big_text = 5


WELCOME_HEADER = "Добро пожаловать в клавиатурный тренажер"
LANGUAGE_HEADER = "Выберете язык, на котором вы хотите писать"
DIFFICULTY_HEADER = "Выберете сложность"
LEVEL_HEADER = "Выберете уровень"


class SettingsModel:
    def __init__(self):
        self.current_language = Language.English
        self.current_difficulty = Difficulty.simple
        self.current_level = Level.l1

        self.current_selected_item = 0
        self.items_count = 0

    def set_random_level(self):
        """Устанавливает случайный уровень."""
        level = random.choice([Level.l1, Level.l5])
        self.current_level = level

    def set_big_text_level(self):
        self.current_level = Level.big_text

    def select_next_item(self):
        if self.items_count > 0:
            self.current_selected_item = (self.current_selected_item +
                                          1) % self.items_count

    def select_prev_item(self):
        if self.items_count > 0:
            self.current_selected_item = ((self.current_selected_item - 1)
                                          % self.items_count)

    def set_language(self):
        self.current_language = Language(self.current_selected_item)

    def set_difficulty(self):
        self.current_difficulty = Difficulty(self.current_selected_item)

    def set_level(self):
        self.current_level = Level(self.current_selected_item)
