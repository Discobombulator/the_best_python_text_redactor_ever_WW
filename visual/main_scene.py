import curses
from logic.read_texts import read_cnf
from control.controller import logic_controller
from control.settings_controller import settings_controller
from logic.chech_esc_buttons import is_program_end
from visual.settings_scene import settings_scene
from visual.main_settings_scene import main_settings_scene
from logic.settings_manager import settings_manager


def get_status_bar_text(name, cursor_y, cursor_x, hotkey_settings):
    """Генерирует текст статусной строки с текущими горячими клавишами"""
    hotkey_save = settings_manager.get_key_name(
        settings_manager.get_hotkey("save"))
    hotkey_save_as = settings_manager.get_key_name(
        settings_manager.get_hotkey("save_as"))
    hotkey_exit_save = settings_manager.get_key_name(
        settings_manager.get_hotkey("exit_save"))
    hotkey_exit_no_save = settings_manager.get_key_name(
        settings_manager.get_hotkey("exit_no_save"))
    hotkey_settings_name = settings_manager.get_key_name(hotkey_settings)

    return (f"{hotkey_save} - Сохранить | "
            f"{hotkey_save_as} - Сохранить как | "
            f"{hotkey_exit_save} - Выйти с сохранением | "
            f"{hotkey_exit_no_save} - Выйти без сохранения | "
            f"{hotkey_settings_name} - Настройки | "
            f"{name + '.txt' if name else 'Новый файл'} | "
            f"Стр:{cursor_y + 1} Кол:{cursor_x + 1}")


def main_scene(std: curses.window, text_type: str):
    curses.curs_set(1)
    std.keypad(True)
    curses.noecho()
    curses.cbreak()

    lines = read_cnf("main_scene")
    header_h = len(lines)
    text = [""]
    name = ""
    cursor_y, cursor_x = 0, 0
    scroll_y = 0
    modified = False

    try:
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    except:
        pass

    if text_type == "olf_f":
        prompt_y = header_h + 2
        std.clear()
        std.addstr(prompt_y, 0, "Введите имя файла для открытия (без .txt): ")
        curses.echo()
        name = std.getstr(prompt_y, 43, 60).decode('utf-8').strip()
        curses.noecho()
        try:
            with open(f"{name}.txt", "r", encoding="utf-8") as f:
                text = f.read().splitlines()
                if not text:
                    text = [""]
        except FileNotFoundError:
            std.addstr(prompt_y + 2, 0, "Файл не найден! Нажмите любую клавишу...")
            std.getch()
            return "exit"

    std.timeout(10)
    std.nodelay(True)

    hotkey_save = settings_manager.get_hotkey("save")
    hotkey_save_as = settings_manager.get_hotkey("save_as")
    hotkey_exit_save = settings_manager.get_hotkey("exit_save")
    hotkey_exit_no_save = settings_manager.get_hotkey("exit_no_save")
    hotkey_settings = settings_manager.get_hotkey("settings")

    while True:
        max_y, max_x = std.getmaxyx()
        text_area_height = max_y - header_h - 1

        if cursor_y < scroll_y:
            scroll_y = cursor_y
        elif cursor_y >= scroll_y + text_area_height:
            scroll_y = cursor_y - text_area_height + 1

        std.clear()

        for i, line in enumerate(lines):
            if i < max_y:
                std.addstr(i, 0, line[:max_x - 1])

        line_num_width = len(str(len(text) + scroll_y)) + 2

        for i in range(min(text_area_height, len(text) - scroll_y)):
            line_idx = scroll_y + i
            if line_idx < len(text):
                line_num = f"{line_idx + 1:>{len(str(len(text)))}}"
                try:
                    std.addstr(i + header_h, 0, line_num, curses.color_pair(2))
                except:
                    std.addstr(i + header_h, 0, line_num)

                line = text[line_idx]
                display_line = line[:max_x - line_num_width - 1]
                std.addstr(i + header_h, line_num_width, display_line)

        # Используем функцию get_status_bar_text для генерации статусной строки
        status_bar = get_status_bar_text(name, cursor_y, cursor_x, hotkey_settings)
        try:
            std.addstr(max_y - 1, 0, status_bar.ljust(max_x - 1), curses.color_pair(1))
        except:
            try:
                std.addstr(max_y - 1, 0, status_bar.ljust(max_x - 1))
            except:
                pass

        cursor_screen_y = cursor_y - scroll_y + header_h
        if 0 <= cursor_screen_y < max_y - 1:
            try:
                std.move(cursor_screen_y, cursor_x + line_num_width)
            except curses.error:
                pass

        std.refresh()

        key = std.getch()

        if key == -1:
            continue

        if key == hotkey_settings:
            # Вместо вызова settings_scene теперь вызываем main_settings_scene
            main_settings_scene(std)
            # Обновляем горячие клавиши после выхода из настроек
            hotkey_save = settings_manager.get_hotkey("save")
            hotkey_save_as = settings_manager.get_hotkey("save_as")
            hotkey_exit_save = settings_manager.get_hotkey("exit_save")
            hotkey_exit_no_save = settings_manager.get_hotkey("exit_no_save")
            hotkey_settings = settings_manager.get_hotkey("settings")
            continue

        if key in (hotkey_save, hotkey_save_as, hotkey_exit_save, hotkey_exit_no_save):
            command_type = None
            if key == hotkey_save:
                command_type = "save"
            elif key == hotkey_save_as:
                command_type = "save_how"
            elif key == hotkey_exit_save:
                command_type = "exit_save"
            elif key == hotkey_exit_no_save:
                command_type = "exit_no_save"

            if command_type:
                res = is_program_end(std, text_type, text, name, command_type)
                if res == "exit":
                    return res
            continue

        if key == curses.KEY_PPAGE:
            cursor_y = max(0, cursor_y - text_area_height)
            cursor_x = min(len(text[cursor_y]), cursor_x)
            continue
        elif key == curses.KEY_NPAGE:
            cursor_y = min(len(text) - 1, cursor_y + text_area_height)
            cursor_x = min(len(text[cursor_y]), cursor_x)
            continue
        elif key == curses.KEY_HOME:
            cursor_x = 0
            continue
        elif key == curses.KEY_END:
            cursor_x = len(text[cursor_y])
            continue

        old_text = text.copy()
        text, cursor_y, cursor_x = logic_controller(std, text, cursor_y, cursor_x, key)
        if text != old_text:
            modified = True