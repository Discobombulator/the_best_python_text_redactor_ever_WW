import curses

from logic.read_texts import read_cnf
from visual.settings_scene import settings_scene
from logic.settings_manager import settings_manager


def main_settings_scene(std: curses.window):
    """Главное меню настроек с выбором категорий настроек"""
    curses.curs_set(0)  # Скрываем курсор
    std.keypad(True)
    std.clear()

    # Заголовок и инструкции
    header = read_cnf("main_settings_menu_text")

    # Создаем список категорий настроек
    menu_items = [
        ("hotkeys", "Горячие клавиши"),
        ("appearance", "Внешний вид"),
        ("behavior", "Поведение редактора"),
        ("exit", "Выход")
    ]

    current_idx = 0
    update_display = True

    while True:
        if update_display:
            std.clear()
            max_y, max_x = std.getmaxyx()

            # Отображаем заголовок
            for i, line in enumerate(header):
                if i < max_y:
                    std.addstr(i, 0, line[:max_x - 1])

            # Отображаем пункты меню
            for i, (action, name) in enumerate(menu_items):
                if i + len(header) < max_y:
                    if i == current_idx:
                        # Выделение выбранного пункта
                        try:
                            std.attron(curses.A_REVERSE)
                            std.addstr(i + len(header), 0, name.ljust(max_x - 1))
                            std.attroff(curses.A_REVERSE)
                        except:
                            # В случае ошибки пробуем без выделения
                            std.addstr(i + len(header), 0, f"> {name}".ljust(max_x - 1))
                    else:
                        std.addstr(i + len(header), 0, f"  {name}".ljust(max_x - 1))

            update_display = False
            std.refresh()

        # Обработка ввода
        key = std.getch()

        if key == curses.KEY_UP:
            current_idx = max(0, current_idx - 1)
            update_display = True
        elif key == curses.KEY_DOWN:
            current_idx = min(len(menu_items) - 1, current_idx + 1)
            update_display = True
        elif key in (curses.KEY_ENTER, 10, 13):  # Enter
            action, _ = menu_items[current_idx]

            if action == "exit":
                break
            elif action == "hotkeys":
                # Переходим в меню настройки горячих клавиш
                settings_scene(std)
                update_display = True
            elif action == "appearance":
                # Заглушка для будущего меню настройки внешнего вида
                show_not_implemented(std)
                update_display = True
            elif action == "behavior":
                # Заглушка для будущего меню настройки поведения
                show_not_implemented(std)
                update_display = True
        elif key == 27:  # ESC
            break

    # Восстанавливаем настройки экрана
    curses.curs_set(1)  # Показываем курсор
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