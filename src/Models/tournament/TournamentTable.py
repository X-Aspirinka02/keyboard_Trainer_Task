import math
from src.Models.SettingsModel import SettingsModel


class TableNode:
    """
    Узел для турнирной таблицы.
    """

    def __init__(self, opponent: bytes, tour: int):
        self.place = None
        self.opponent = opponent
        self.exercise_text = None
        self.results = []
        self.tour = tour


class TournamentTable:
    """
    Модель турнирной таблицы.
    """

    def __init__(self, gamers: list, settings: SettingsModel,
                 big_text: bool):
        self.table = self.set_first_tour(gamers, settings, big_text)

    def set_first_tour(self, gamers: list,
                       settings_model: SettingsModel, is_big_text: bool):
        """
        Создание 1 слоя турнирной таблицы
        :param gamers: список имён игроков
        :param settings_model: язык и сложность турнира
        :param is_big_text: флаг уровня большого текста
        :return: первый уровень турнирной таблицы
        """
        table = {}
        for i in range(0, len(gamers), 2):
            gamer1 = gamers[i]
            gamer2 = gamers[i + 1] if i + 1 < len(gamers) else None
            if is_big_text:
                settings_model.set_big_text_level()
            else:
                settings_model.set_random_level()
            table[gamer1] = TableNode(gamer2, int(math.log2(len(gamers))))
            if gamer2:
                table[gamer2] = TableNode(gamer1, int(math.log2(len(gamers))))
        return table
