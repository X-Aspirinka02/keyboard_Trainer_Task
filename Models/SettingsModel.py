import enum
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


WELCOME_HEADER = "Welcome to keyboard trainer"
LANGUAGE_HEADER = "select the language you want to write in"
DIFFICULTY_HEADER = "select difficulty"
LEVEL_HEADER = "select level"

class SettingsModel:
    def __init__(self):
        self.current_language = Language.English
        self.current_difficulty = Difficulty.simple
        self.current_level = Level.l1

        self.current_selected_item = 0
        self.items_count = 0

    def select_next_item(self):
        if self.items_count > 0:
            self.current_selected_item = (self.current_selected_item + 1) % self.items_count

    def select_prev_item(self):
        if self.items_count > 0:
            self.current_selected_item = (self.current_selected_item - 1) % self.items_count

    def set_language(self):
        self.current_language = Language(self.current_selected_item)

    def set_difficulty(self):
        self.current_difficulty = Difficulty(self.current_selected_item)

    def set_level(self):
        self.current_level = Level(self.current_selected_item)