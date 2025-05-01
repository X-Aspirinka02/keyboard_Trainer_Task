from Models.SettingsModel import Language, Difficulty, Level, SettingsModel
from Views.ListView import ListView


class ListPresenter:
    """
    Презентер отображения списка. Отвечает за управление отображениями всех списков настроек.
    """

    def __init__(self, settings_model: SettingsModel):
        self.settings_model = settings_model
        self.current_view = None
        self.current_view_type = None

    def _create_selection_view(self, items, header, view_type):
        """
        Создает представление для выбора из списка.

        Args:
            items: Список элементов для выбора
            header: Заголовок представления
            view_type: Тип представления (язык, сложность, уровень)
        """

        self.current_view = ListView(items, header, view_type)
        self.current_view_type = view_type
        self.settings_model.current_selected_item = 0
        self.settings_model.items_count = len(items)

        self.current_view.update_selected_item(0)

    def show_language_selection(self):
        """
        Отображает экран выбора языка.
        """

        languages = [(f"{lang.name}", 1) for lang in Language]
        self._create_selection_view(languages, "Выберите язык, на котором хотите писать", "language")

    def show_difficulty_selection(self):
        """
        Отображает экран выбора сложности.
        """

        difficulties = [(f"{diff.name}", 1) for diff in Difficulty]
        self._create_selection_view(difficulties, "Выберите сложность", "difficulty")

    def show_level_selection(self):
        """
        Отображает экран выбора уровня.
        """

        levels = [(f"Level {level.value}", 1) for level in Level]
        self._create_selection_view(levels, "Выберите уровень", "level")
