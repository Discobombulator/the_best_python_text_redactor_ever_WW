import curses

from logic.read_texts import read_cnf
from logic.text_collor_changer import text_color_manager
from visual.settings_scene import settings_scene
from logic.settings_manager import settings_manager


def main_settings_scene(std: curses.window, current_file: str = ""):
    curses.curs_set(0)
    std.keypad(True)

    # Заголовок и инструкции
    header = read_cnf("main_settings_menu_text")
    menu_items = [
        ("hotkeys", "Горячие клавиши"),
        ("text_color", "Цвет текста"),
        ("exit", "Выход")
    ]

    current_idx = 0
    update = True

    while True:
        if update:
            std.clear()
            max_y, max_x = std.getmaxyx()

            # Отображаем заголовок
            for i, line in enumerate(header):
                if i < max_y:
                    std.addstr(i, 0, line[:max_x - 1])

            # Отображаем пункты меню
            for i, (action, name) in enumerate(menu_items):
                y = i + len(header)
                if y < max_y:
                    if i == current_idx:
                        std.attron(curses.A_REVERSE)
                    std.addstr(y, 0, f"  {name}".ljust(max_x - 1))
                    if i == current_idx:
                        std.attroff(curses.A_REVERSE)

            update = False
            std.refresh()

        key = std.getch()

        if key == curses.KEY_UP:
            current_idx = max(0, current_idx - 1)
            update = True
        elif key == curses.KEY_DOWN:
            current_idx = min(len(menu_items) - 1, current_idx + 1)
            update = True
        elif key in (curses.KEY_ENTER, 10, 13):
            action = menu_items[current_idx][0]

            if action == "exit":
                break
            elif action == "hotkeys":
                settings_scene(std)
                update = True
            elif action == "text_color":
                # Даже если current_file пустой, мы вызываем функцию для настройки цвета
                file_to_use = current_file if current_file else "new_file.txt"
                text_color_scene(std, file_to_use)
                # Применяем обновленный цвет сразу после выбора
                try:
                    # Обновляем цветовую пару
                    curses.init_pair(1, text_color_manager.get_color(),
                                     curses.COLOR_BLACK)
                except:
                    pass
                update = True
        elif key == 27:  # ESC
            break

    curses.curs_set(1)
    std.clear()
    std.refresh()


def text_color_scene(std: curses.window, txt_file: str):
    """Сцена выбора цвета текста"""
    curses.curs_set(0)
    std.keypad(True)

    colors = {
        0: ("Черный", curses.COLOR_BLACK),
        1: ("Красный", curses.COLOR_RED),
        2: ("Зеленый", curses.COLOR_GREEN),
        3: ("Желтый", curses.COLOR_YELLOW),
        4: ("Синий", curses.COLOR_BLUE),
        5: ("Пурпурный", curses.COLOR_MAGENTA),
        6: ("Голубой", curses.COLOR_CYAN),
        7: ("Белый", curses.COLOR_WHITE)
    }

    # Получаем текущий цвет или используем белый по умолчанию
    current_idx = 0
    for idx, (_, color_val) in colors.items():
        if color_val == text_color_manager.get_color():
            current_idx = idx
            break

    update = True

    while True:
        if update:
            std.clear()
            h, w = std.getmaxyx()

            title = "ВЫБОР ЦВЕТА ТЕКСТА"
            std.addstr(1, (w - len(title)) // 2, title)
            std.addstr(3, 2, "Выберите цвет и нажмите Enter:")

            # Отображаем цвета с образцами
            for i, (name, color_val) in colors.items():
                y = 5 + i
                if y < h - 2:
                    # Инициализируем пару цветов для примера
                    try:
                        color_pair_idx = i + 10  # Используем индексы с 10, чтобы избежать конфликтов
                        curses.init_pair(color_pair_idx, color_val,
                                         curses.COLOR_BLACK)
                    except:
                        pass

                    if i == current_idx:
                        std.attron(curses.A_REVERSE)

                    # Отображаем название цвета
                    std.addstr(y, 4, f"{i + 1}. {name}")

                    # Отображаем образец текста в этом цвете
                    try:
                        std.addstr(y, 20, " Образец текста ",
                                   curses.color_pair(color_pair_idx))
                    except:
                        pass

                    if i == current_idx:
                        std.attroff(curses.A_REVERSE)

            std.addstr(h - 2, 2, "Enter - сохранить, ESC - отмена")
            update = False
            std.refresh()

        key = std.getch()

        if key == curses.KEY_UP:
            current_idx = max(0, current_idx - 1)
            update = True
        elif key == curses.KEY_DOWN:
            current_idx = min(len(colors) - 1, current_idx + 1)
            update = True
        elif key in (curses.KEY_ENTER, 10, 13):
            # Сохраняем выбранный цвет
            selected_color = colors[current_idx][1]
            text_color_manager.set_color(selected_color)
            text_color_manager.save_color(txt_file)

            # Важно: убедимся, что цвет действительно изменился
            if text_color_manager.get_color() != selected_color:
                # Принудительно устанавливаем цвет, если что-то пошло не так
                text_color_manager.color = selected_color

            break
        elif key == 27:  # ESC
            break

    curses.curs_set(1)
    std.clear()
    std.refresh()


def show_not_implemented(std: curses.window):
    """Показывает сообщение о том, что функция еще не реализована"""
    h, w = std.getmaxyx()
    message = "Эта функция находится в разработке. Нажмите любую клавишу..."
    std.clear()
    std.addstr(h // 2, (w - len(message)) // 2, message)
    std.refresh()
    std.getch()