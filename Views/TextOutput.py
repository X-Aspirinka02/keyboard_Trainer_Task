import curses


def draw_text_with_wrap(window: curses.window, text: str, start_y: int = 0, start_x: int = 0,
                        max_lines: int = None, color_pair: int = 0) -> int:
    """
    Выводит текст с переносами слов и возвращает конечную позицию Y

    Args:
        window: Окно curses
        text: Текст для вывода
        start_y: Начальная позиция Y
        start_x: Начальная позиция X
        max_lines: Максимальное число строк для вывода (None - без ограничений)
        color_pair: Цветовая пара curses

    Returns:
        Последняя использованная позиция Y
    """
    if text == "":
        return start_y
    max_y, max_x = window.getmaxyx()
    current_y = start_y
    words = text.split(' ')
    is_first = True
    line_buffer = ""

    for word in words:
        # Обработка переносов строк в исходном тексте
        if '\n' in word:
            parts = word.split('\n')
            for i, part in enumerate(parts):
                if i > 0:
                    if current_y < max_y - 1 and (max_lines is None or current_y - start_y < max_lines):
                        try:
                            if is_first:
                                window.addstr(current_y, start_x, line_buffer.strip(), color_pair)
                                is_first = False
                            else:
                                window.addstr(current_y, 0, line_buffer.strip(), color_pair)
                        except curses.error:
                            pass
                        line_buffer = ""
                        current_y += 1
                    else:
                        return current_y
                line_buffer += part + " "
            continue

        # Проверяем, помещается ли слово в текущую строку
        if len(line_buffer) + len(word) + 1 <= max_x - start_x - 1:
            line_buffer += word + " "
        else:
            if current_y < max_y - 1 and (max_lines is None or current_y - start_y < max_lines):
                try:
                    window.addstr(current_y, 0, line_buffer.strip(), color_pair)
                except curses.error:
                    pass
                line_buffer = word + " "
                current_y += 1
            else:
                return current_y

    # Выводим оставшийся текст
    if line_buffer and current_y < max_y - 1 and (max_lines is None or current_y - start_y < max_lines):
        try:
            if is_first:
                window.addstr(current_y, start_x, line_buffer.strip(), color_pair)
                is_first = False
            else:
                window.addstr(current_y, 0, line_buffer.strip(), color_pair)
        except curses.error:
            pass
        current_y += 1

    return current_y