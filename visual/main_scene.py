import curses
from logic.read_texts import read_cnf
from control.controller import logic_controller
from logic.chech_esc_buttons import is_program_end


def main_scene(std: curses.window, text_type: str):
    # Инициализация curses
    curses.curs_set(1)
    std.keypad(True)

    curses.noecho()
    curses.cbreak()

    lines = read_cnf("main_scene")
    header_h = len(lines)
    text = [""]
    name = ""
    cursor_y, cursor_x = 0, 0
    scroll_y = 0  # Позиция прокрутки
    modified = False

    # Инициализация цветов
    try:
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE,
                         curses.COLOR_BLUE)  # Для статусной строки
        curses.init_pair(2, curses.COLOR_CYAN,
                         curses.COLOR_BLACK)  # Для номеров строк
    except:
        pass  # Игнорируем ошибки инициализации цветов

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

    # Настройка таймаута для неблокирующего ввода
    std.timeout(50)
    std.nodelay(True)

    while True:
        # Получение размеров окна
        max_y, max_x = std.getmaxyx()
        text_area_height = max_y - header_h - 1  # -1 для статусной строки

        # Обновление прокрутки
        if cursor_y < scroll_y:
            scroll_y = cursor_y
        elif cursor_y >= scroll_y + text_area_height:
            scroll_y = cursor_y - text_area_height + 1

        # Отрисовка
        std.clear()

        # Отрисовка заголовка
        for i, line in enumerate(lines):
            if i < max_y:
                std.addstr(i, 0, line[:max_x - 1])

        # Вычисление ширины для нумерации строк
        line_num_width = len(str(len(text) + scroll_y)) + 2

        # Отрисовка текста с номерами строк
        for i in range(min(text_area_height, len(text) - scroll_y)):
            line_idx = scroll_y + i
            if line_idx < len(text):
                # Номер строки
                line_num = f"{line_idx + 1:>{len(str(len(text)))}}"
                try:
                    std.addstr(i + header_h, 0, line_num, curses.color_pair(2))
                except:
                    std.addstr(i + header_h, 0, line_num)

                # Текст строки
                line = text[line_idx]
                display_line = line[:max_x - line_num_width - 1]
                std.addstr(i + header_h, line_num_width, display_line)

        # Позиционирование курсора
        cursor_screen_y = cursor_y - scroll_y + header_h
        if 0 <= cursor_screen_y < max_y - 1:
            try:
                std.move(cursor_screen_y, cursor_x + line_num_width)
            except curses.error:
                # Если координаты курсора за пределами экрана
                pass

        std.refresh()

        # Обработка ввода
        try:
            key = std.getch()
            if key == -1:  # Таймаут
                continue

            # Проверяем системные команды (сохранение/выход)
            if key in (17, 18, 19, 16):  # Ctrl+Q, Ctrl+R, Ctrl+S, Ctrl+P
                # Временно отключаем таймаут для обработки команд
                std.timeout(-1)
                res = is_program_end(std, text_type, text, name)
                std.timeout(50)  # Возвращаем таймаут
                if res == "exit":
                    return res
                continue

            # Обработка навигации по страницам (Page Up/Down)
            if key == curses.KEY_PPAGE:  # Page Up
                cursor_y = max(0, cursor_y - text_area_height)
                cursor_x = min(len(text[cursor_y]), cursor_x)
                continue
            elif key == curses.KEY_NPAGE:  # Page Down
                cursor_y = min(len(text) - 1, cursor_y + text_area_height)
                cursor_x = min(len(text[cursor_y]), cursor_x)
                continue
            elif key == curses.KEY_HOME:  # Home
                cursor_x = 0
                continue
            elif key == curses.KEY_END:  # End
                cursor_x = len(text[cursor_y])
                continue

            # Обработка обычных клавиш
            old_text = text.copy()
            text, cursor_y, cursor_x = logic_controller(std, text, cursor_y,
                                                        cursor_x, key)

            # Проверка изменений
            if text != old_text:
                modified = True

        except curses.error:
            pass