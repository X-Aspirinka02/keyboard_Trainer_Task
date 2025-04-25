from abc import abstractmethod, ABC
import curses

class IView(ABC):
    """Абстрактный класс для выводимых в терминал сущностей"""
    @abstractmethod
    def draw(self, window: curses.window):
        pass
