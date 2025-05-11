import curses
from control.hotkeys_controller import hotkeys_controller
from logic.hotkeys_maneger import HotkeysManager


def hotkeys_scene(std):
    hotkeys_manager = HotkeysManager()

    # Выключаем отображение курсора
    curses.curs_set(0)

    # Константы для управления интерфейсом
    TITLE_LINE = 1
    START_LINE = 4
    INSTRUCTIONS_LINE = 15
    CURRENT_KEY_LINE = 18

    # Текущий выбранный элемент
    current_selection = 0

    # Находимся ли в режиме редактирования клавиши
    edit_mode = False

    # Получаем список всех горячих клавиш
    hotkeys_list = hotkeys_manager.get_all_hotkeys()

    while True:
        std.clear()

        # Отображаем заголовок
        std.addstr(TITLE_LINE, 0, "Настройка горячих клавиш")
        std.addstr(TITLE_LINE + 1, 0, "_" * 50)

        # Отображаем инструкции
        std.addstr(INSTRUCTIONS_LINE, 0, "Управление:")
        std.addstr(INSTRUCTIONS_LINE + 1, 0, "↑/↓ - Перемещение")
        std.addstr(INSTRUCTIONS_LINE + 2, 0, "Enter - Редактировать клавишу")
        std.addstr(INSTRUCTIONS_LINE + 3, 0, "S - Сохранить настройки")
        std.addstr(INSTRUCTIONS_LINE + 4, 0, "Esc - Отмена/Выход")

        # Отображаем список горячих клавиш
        for i, (action, desc, key) in enumerate(hotkeys_list):
            line = START_LINE + i

            # Выделяем текущий выбранный элемент
            if i == current_selection:
                std.attron(curses.A_REVERSE)

            std.addstr(line, 2, f"{desc}: CTRL+{key}")

            if i == current_selection:
                std.attroff(curses.A_REVERSE)

        # Если находимся в режиме редактирования, показываем инструкцию
        if edit_mode:
            std.addstr(CURRENT_KEY_LINE, 0,
                       "Нажмите клавишу для назначения (A-Z):")
            std.addstr(CURRENT_KEY_LINE + 1, 0, "Esc - Отмена")

        std.refresh()

        # Обрабатываем ввод пользователя
        if edit_mode:
            # В режиме редактирования ожидаем новую клавишу
            key = std.getch()

            # Escape для отмены редактирования
            if key == 27:  # ASCII код для Escape
                edit_mode = False
                continue

            # Проверяем, что введена буква
            key_char = chr(key).lower() if 'a' <= chr(
                key).lower() <= 'z' else None

            if key_char:
                # Обновляем горячую клавишу
                action = hotkeys_list[current_selection][0]
                if hotkeys_manager.update_hotkey(action, key_char):
                    # Обновляем список для отображения
                    hotkeys_list = hotkeys_manager.get_all_hotkeys()
                edit_mode = False
        else:
            # В режиме навигации обрабатываем управление
            cmd = hotkeys_controller(std)

            if cmd == "exit":
                # Восстанавливаем видимость курсора перед выходом
                curses.curs_set(1)
                return None
            elif cmd == "up" and current_selection > 0:
                current_selection -= 1
            elif cmd == "down" and current_selection < len(hotkeys_list) - 1:
                current_selection += 1
            elif cmd == "edit":
                edit_mode = True
            elif cmd == "save":
                hotkeys_manager.save_hotkeys()
                # Восстанавливаем видимость курсора перед выходом
                curses.curs_set(1)
                return None
