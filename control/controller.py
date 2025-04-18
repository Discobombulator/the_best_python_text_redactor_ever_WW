import curses
import curses.ascii


def start_controller(std):
    """
    Ждём ввода 1, 2 или q/й/ESC для выбора действия в меню.
    Возвращает 'new_f', 'olf_f' или 'exit'.
    """
    # Переключаем клавиатуру в режим чтения специальных клавиш
    std.keypad(True)
    curses.curs_set(0)

    while True:
        key = std.getch()
        # Для отладки можно раскомментировать следующие строки:
        # std.addstr(0, 0, f"Key: {key:3d}   ")
        # std.refresh()

        if key == ord('1'):
            return "new_f"
        elif key == ord('2'):
            return "olf_f"
        elif key in (ord('q'), ord('й'), 27):  # 27 = ESC
            return "exit"
        # иначе игнорируем и ждём следующего нажатия


def main_controller(std):
    key = std.getch()
    if key == 19:  # Ctrl+S
        return "save"
    elif key == 16:  # Ctrl+P
        return "save_how"
    elif key == 18:  # Ctrl+R
        return "exit_save"
    elif key == 17:  # Ctrl+Q
        return "exit_no_save"
    return None


def no_save_check(std):
    std.keypad(True)
    while True:
        key = std.getch()
        if key == ord('1'):
            return "exit"
        elif key == ord('2'):
            return "no_exit"


def new_name_check(std):
    key = std.getch()
    if key in (curses.ascii.ctrl(83), curses.ascii.ctrl(115)):
        return "confirm"


# controller.py (дополнение)
def logic_controller(std, text, cursor_y, cursor_x):
    key = std.getch()

    max_y, max_x = std.getmaxyx()
    max_text_width = max_x - 1

    # Перемещение курсора
    if key == curses.KEY_UP:
        cursor_y = max(0, cursor_y - 1)
        cursor_x = min(len(text[cursor_y]), cursor_x)
    elif key == curses.KEY_DOWN:
        cursor_y = min(len(text) - 1, cursor_y + 1)
        cursor_x = min(len(text[cursor_y]), cursor_x)
    elif key == curses.KEY_LEFT:
        cursor_x = max(0, cursor_x - 1)
    elif key == curses.KEY_RIGHT:
        cursor_x = min(len(text[cursor_y]), cursor_x + 1)

    # Обработка Enter (новая строка)
    elif key == curses.KEY_ENTER or key == 10 or key == 13:
        new_line = text[cursor_y][cursor_x:]
        text[cursor_y] = text[cursor_y][:cursor_x]
        text.insert(cursor_y + 1, new_line)
        cursor_y += 1
        cursor_x = 0

    # Backspace
    elif key == curses.KEY_BACKSPACE or key == 127:
        if cursor_x > 0:
            text[cursor_y] = text[cursor_y][:cursor_x - 1] + text[cursor_y][cursor_x:]
            cursor_x -= 1
        elif cursor_y > 0:
            prev_line_len = len(text[cursor_y - 1])
            text[cursor_y - 1] += text[cursor_y]
            del text[cursor_y]
            cursor_y -= 1
            cursor_x = prev_line_len

    # Ввод обычных символов (включая кириллицу)
    elif 32 <= key <= 0xFFFF:  # Широкий диапазон для Unicode
        try:
            char = chr(key)
            text[cursor_y] = text[cursor_y][:cursor_x] + char + text[cursor_y][cursor_x:]
            cursor_x += 1
        except:
            pass

    # Ограничение позиции курсора
    cursor_x = max(0, min(cursor_x, len(text[cursor_y])))

    return text, cursor_y, cursor_x
