# visual/main_scene.py
import curses
from logic.read_texts import read_cnf
from control.controller import logic_controller
from logic.chech_esc_buttons import is_program_end


def main_scene(std, text_type):

    curses.curs_set(1)  # Видимый курсор
    std.keypad(True)  # Для обработки спецклавиш
    curses.noecho()  # Выключаем автоматический вывод символов

    lines = read_cnf("main_scene")
    header_h = len(lines)

    # Инициализация текста
    text = [""]
    name = ""

    if text_type == "olf_f":
        prompt_y = header_h + 2
        std.clear()
        std.addstr(prompt_y, 0, "Введите имя файла для открытия (без .txt): ")
        curses.echo()  # Временно включаем echo для ввода имени файла
        name = std.getstr(prompt_y, 30, 60).decode('utf-8').strip()
        curses.noecho()
        try:
            with open(f"{name}.txt", "r", encoding="utf-8") as f:
                text = f.read().splitlines()
        except FileNotFoundError:
            std.addstr(prompt_y + 2, 0, "Файл не найден! Нажмите любую клавишу...")
            std.getch()
            return "exit"

    # Первоначальная отрисовка
    std.clear()
    max_y, max_x = std.getmaxyx()
    for i, line in enumerate(lines):
        if i < max_y:
            std.addstr(i, 0, line[:max_x - 1])

    # Главный цикл редактирования
    cursor_y, cursor_x = 0, 0
    while True:
        # Отрисовка текста
        for idx, line in enumerate(text):
            y = header_h + idx
            if y < max_y:
                std.addstr(y, 0, line[:max_x - 1])

        # Позиционирование курсора
        std.move(header_h + cursor_y, cursor_x)
        std.refresh()

        # Обработка ввода
        old_text = [line for line in text]
        text, cursor_y, cursor_x = logic_controller(std, text, cursor_y, cursor_x)

        # Проверка на выход
        res = is_program_end(std, text_type, text, name)
        if res == "exit":
            return "exit"

        # Очистка старых строк при изменении текста
        if text != old_text:
            std.clear()
            for i, line in enumerate(lines):
                if i < max_y:
                    std.addstr(i, 0, line[:max_x - 1])
