import curses

from control.controller import main_controller
from logic.saving_file_functions import save_text, save_text_no_name
from visual.exit_and_save_scene import exit_no_save


def is_program_end(std: curses.window, text_type: str, text: list[str],
                   name: str):
    # Отключаем таймаут на время проверки выхода
    std.timeout(-1)
    std.nodelay(False)

    end_type = main_controller(std)

    # Восстанавливаем настройки
    std.timeout(50)
    std.nodelay(True)

    if end_type == "exit_no_save":
        if exit_no_save(std) == "exit_no_save":
            return "exit"
    elif end_type == "save_how":
        save_text_no_name(std, text)
    elif end_type == "save":
        if text_type == "olf_f":
            save_text(text, name)
    elif end_type == "exit_save":
        save_text_no_name(std, text)
        return "exit"
    return None
