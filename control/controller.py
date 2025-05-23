import curses
import curses.ascii


def start_controller(std: curses.window):
    std.keypad(True)
    curses.curs_set(0)

    while True:
        key = std.getch()

        if key == ord('1'):
            return "new_f"
        elif key == ord('2'):
            return "olf_f"
        elif key in (ord('q'), ord('й'), 27):  # 27 = ESC
            return "exit"
        # иначе игнорируем и ждём следующего нажатия


def main_controller(std: curses.window):
    # Временно отключаем таймаут для проверки специальных клавиш
    std.timeout(-1)
    key = std.getch()
    # Возвращаем таймаут обратно
    std.timeout(50)

    if key == 19:  # Ctrl+S
        return "save"
    elif key == 16:  # Ctrl+P
        return "save_how"
    elif key == 18:  # Ctrl+R
        return "exit_save"
    elif key == 17:  # Ctrl+Q
        return "exit_no_save"
    elif key == 15:  # Ctrl+O
        return "settings"


def no_save_check(std: curses.window):
    std.keypad(True)
    while True:
        key = std.getch()
        if key == ord('1'):
            return "exit"
        elif key == ord('2'):
            return "no_exit"


def new_name_check(std: curses.window):
    key = std.getch()
    if key in (curses.ascii.ctrl(83), curses.ascii.ctrl(115)):
        return "confirm"


def logic_controller(std: curses.window, text: list, cursor_y: int,
                     cursor_x: int, key: int):
    # max_y, max_x = std.getmaxyx()

    if key == curses.KEY_UP:
        cursor_y = max(0, cursor_y - 1)
        cursor_x = min(len(text[cursor_y]), cursor_x)
    elif key == curses.KEY_DOWN:
        cursor_y = min(len(text) - 1, cursor_y + 1)
        cursor_x = min(len(text[cursor_y]), cursor_x)
    elif key == curses.KEY_LEFT:
        if cursor_x > 0:
            cursor_x -= 1
        elif cursor_y > 0:
            cursor_y -= 1
            cursor_x = len(text[cursor_y])
    elif key == curses.KEY_RIGHT:
        if cursor_x < len(text[cursor_y]):
            cursor_x += 1
        elif cursor_y < len(text) - 1:
            cursor_y += 1
            cursor_x = 0

    # Обработка Enter (новая строка)
    elif key in (curses.KEY_ENTER, 10, 13):
        new_line = text[cursor_y][cursor_x:]
        text[cursor_y] = text[cursor_y][:cursor_x]
        text.insert(cursor_y + 1, new_line)
        cursor_y += 1
        cursor_x = 0

    # Backspace
    elif key in (curses.KEY_BACKSPACE, 127, 8):
        if cursor_x > 0:
            text[cursor_y] = text[cursor_y][:cursor_x - 1] + text[cursor_y][
                                                             cursor_x:]
            cursor_x -= 1
        elif cursor_y > 0:
            prev_line_len = len(text[cursor_y - 1])
            text[cursor_y - 1] += text[cursor_y]
            del text[cursor_y]
            cursor_y -= 1
            cursor_x = prev_line_len

    # Delete key
    elif key == curses.KEY_DC:
        if cursor_x < len(text[cursor_y]):
            text[cursor_y] = text[cursor_y][:cursor_x] + text[cursor_y][cursor_x + 1:]
        elif cursor_y < len(text) - 1:
            text[cursor_y] += text[cursor_y + 1]
            del text[cursor_y + 1]

    # Ввод обычных символов
    elif 32 <= key <= 0x10FFFF:  # Широкий диапазон для Unicode
        char = chr(key)
        text[cursor_y] = text[cursor_y][:cursor_x] + char + text[cursor_y][
                                                            cursor_x:]
        cursor_x += 1

    return text, cursor_y, cursor_x