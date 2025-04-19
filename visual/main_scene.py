# visual/main_scene.py
import curses
from logic.read_texts import read_cnf
from control.controller import logic_controller
from logic.chech_esc_buttons import is_program_end


def main_scene(std, text_type):
    # Инициализация curses
    curses.curs_set(1)
    std.keypad(True)
    curses.noecho()
    curses.cbreak()

    lines = read_cnf("main_scene")
    header_h = len(lines)
    text = [""]
    name = ""

    if text_type == "olf_f":
        prompt_y = header_h + 2
        std.clear()
        std.addstr(prompt_y, 0, "Введите имя файла для открытия (без .txt): ")
        curses.echo()  # Временно включаем echo для ввода имени файла
        name = std.getstr(prompt_y, 43, 60).decode('utf-8').strip()
        curses.noecho()
        try:
            with open(f"{name}.txt", "r", encoding="utf-8") as f:
                text = f.read().splitlines()
                if not text:
                    text = [""]
        except FileNotFoundError:
            std.addstr(prompt_y + 2, 0,
                       "Файл не найден! Нажмите любую клавишу...")
            std.getch()
            return "exit"

    cursor_y, cursor_x = 0, 0
    while True:
        # Отрисовка
        std.clear()
        for i, line in enumerate(lines):
            if i < curses.LINES:
                std.addstr(i, 0, line)

        for idx, line in enumerate(text):
            y = header_h + idx
            if y < curses.LINES:
                std.addstr(y, 0, line[:curses.COLS - 1])

        std.move(header_h + cursor_y, cursor_x)
        std.refresh()

        # Обработка ввода
        try:
            key = std.getch()
            if key == -1:  # Таймаут
                continue

            # Сначала проверяем системные команды (сохранение/выход)
            if key in (17, 18, 19, 16):  # Ctrl+Q, Ctrl+R, Ctrl+S, Ctrl+P
                # Временно отключаем таймаут для обработки команд
                std.timeout(-1)
                res = is_program_end(std, text_type, text, name)
                std.timeout(50)  # Возвращаем таймаут
                if res == "exit":
                    return res
                continue

            # Обработка обычных клавиш
            text, cursor_y, cursor_x = logic_controller(std, text, cursor_y,
                                                        cursor_x, key)

        except curses.error:
            pass