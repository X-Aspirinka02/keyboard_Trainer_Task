import math
from array import ArrayType
from Models.SettingsModel import SettingsModel, Level


class TableNode:
    def __init__(self, opponent: bytes, tour: int):
        self.place = None
        self.opponent = opponent
        self.exercise_text = None
        self.results = []
        self.tour = tour


class TournamentTable:
    def __init__(self, gamers: ArrayType, settings_model: SettingsModel, is_big_text: bool):
        self.table: dict[bytes, TableNode] = self.set_first_tour(gamers, settings_model, is_big_text)



    def set_first_tour(self, gamers: ArrayType, settings_model: SettingsModel, is_big_text: bool):
        table = {}
        for i in range(0, len(gamers), 2):
            gamer1 = gamers[i]
            gamer2 = gamers[i + 1] if i + 1 < len(gamers) else None  # Если нечётное число игроков
            if is_big_text:
                settings_model.set_big_text_level()
            else:
                settings_model.set_random_level()
            table[gamer1] = TableNode(gamer2, int(math.log2(len(gamers))))
            if gamer2:
                table[gamer2] = TableNode(gamer1, int(math.log2(len(gamers))))
        return table
