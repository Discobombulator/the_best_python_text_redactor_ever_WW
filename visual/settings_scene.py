import curses

from logic.read_texts import read_cnf
from logic.settings_manager import settings_manager


def settings_scene(std: curses.window):
    """Сцена настроек горячих клавиш"""
    curses.curs_set(0)  # Скрываем курсор
    std.keypad(True)
    std.clear()

    # Заголовок и инструкции
    header = [
        "НАСТРОЙКИ ГОРЯЧИХ КЛАВИШ",
        "==========================================",
        "Используйте стрелки вверх/вниз для навигации",
        "Enter - изменить выбранную комбинацию",
        "ESC - вернуться в редактор",
        ""
    ]

    # Получаем текущие горячие клавиши
    hotkeys = settings_manager.get_all_hotkeys()

    # Отображаемые названия действий
    action_names = {
        "save": "Сохранить",
        "save_as": "Сохранить как",
        "exit_save": "Выйти с сохранением",
        "exit_no_save": "Выйти без сохранения",
        "settings": "Открыть настройки"
    }

    # Создаем список пунктов меню
    menu_items = []
    for action, key_code in hotkeys.items():
        key_name = settings_manager.get_key_name(key_code)
        menu_items.append((action, action_names.get(action, action), key_name))

    menu_items.append(("reset", "Сбросить на значения по умолчанию", ""))
    menu_items.append(("exit", "Выход", ""))  # Добавляем пункт "Выход"

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
            for i, (action, name, key) in enumerate(menu_items):
                if i + len(header) < max_y:
                    if i == current_idx:
                        # Выделение выбранного пункта
                        try:
                            std.attron(curses.A_REVERSE)
                            std.addstr(i + len(header), 0,
                                       f"{name}: {key}".ljust(max_x - 1))
                            std.attroff(curses.A_REVERSE)
                        except:
                            # В случае ошибки пробуем без выделения
                            std.addstr(i + len(header), 0,
                                       f"> {name}: {key}".ljust(max_x - 1))
                    else:
                        std.addstr(i + len(header), 0,
                                   f"  {name}: {key}".ljust(max_x - 1))

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
            action, _, _ = menu_items[current_idx]

            if action == "reset":
                # Сброс настроек
                settings_manager.reset_to_defaults()
                hotkeys = settings_manager.get_all_hotkeys()
                # Обновляем отображаемые значения клавиш
                for i in range(len(menu_items) - 2):  # -2 потому что добавили "Выход"
                    action = menu_items[i][0]
                    menu_items[i] = (action, menu_items[i][1],
                                     settings_manager.get_key_name(
                                         hotkeys[action]))
                update_display = True
            elif action == "exit":  # Обработка выхода
                break
            else:
                # Настройка горячей клавиши
                key_value = change_hotkey(std, menu_items[current_idx][1])
                if key_value is not None:
                    settings_manager.set_hotkey(action, key_value)
                    menu_items[current_idx] = (
                    action, menu_items[current_idx][1],
                    settings_manager.get_key_name(key_value))
                    update_display = True
        elif key == 27:  # ESC
            break

    # Восстанавливаем настройки экрана
    curses.curs_set(1)  # Показываем курсор
    std.clear()
    std.refresh()


def change_hotkey(std: curses.window, action_name):
    """Изменение горячей клавиши для указанного действия"""
    std.clear()
    std.addstr(1, 0, f"Настройка горячей клавиши для действия: {action_name}")
    std.addstr(3, 0,
               "Нажмите комбинацию клавиш (поддерживаются Ctrl+A - Ctrl+Z)")
    std.addstr(4, 0, "или ESC для отмены")
    std.refresh()

    while True:
        key = std.getch()

        if key == 27:  # ESC
            return None
        elif 1 <= key <= 26:  # Ctrl+A to Ctrl+Z
            return key
        # Можно добавить поддержку других комбинаций клавиш