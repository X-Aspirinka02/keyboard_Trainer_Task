from Views.IView import IView
import curses


class ListView(IView):
    def __init__(self, items_for_choice: list[tuple[str, int]], header: str, view_type: str = None):
        self.items = items_for_choice
        self.header = header
        self.view_type = view_type

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def draw(self, window: curses.window):
        window.clear()
        window.addstr(0, 0, self.header)

        for i, (text, color_pair) in enumerate(self.items):
            y_coor = i + 1
            is_selected = color_pair == 2

            if is_selected:
                window.addstr(y_coor, 0, text, curses.color_pair(2))
            else:
                window.addstr(y_coor, 0, text, curses.color_pair(1))

        y_pos = len(self.items) + 2
        window.addstr(y_pos, 0, "Use UP/DOWN arrows to navigate, ENTER to select")
        
        if self.view_type == "language":
            window.addstr(y_pos + 1, 0, "Press 'h' to view exercise history", curses.color_pair(3))
            window.addstr(y_pos + 2, 0, "Press 't' to start the tournament", curses.color_pair(3))
            
        window.refresh()

    def update_selected_item(self, selected_index):
        for i in range(len(self.items)):
            item_text = self.items[i][0]
            self.items[i] = (item_text, 1)  # Нет выделения

        if 0 <= selected_index < len(self.items):
            item_text = self.items[selected_index][0]
            self.items[selected_index] = (item_text, 2)  # Выделено