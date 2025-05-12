import curses

from visual.exit_and_save_scene import exit_no_save
from logic.saving_file_functions import save_text, save_text_no_name


def is_program_end(std: curses.window, text_type: str, text: list[str],
                   name: str, command_type=None):
    """
    Обработка команд завершения программы или сохранения с использованием настраиваемых горячих клавиш

    Args:
        std: Окно curses
        text_type: Тип текста ('new_f' или 'olf_f')
        text: Содержимое текста
        name: Имя файла
        command_type: Тип команды (может быть передан напрямую)

    Returns:
        "exit" если программа должна завершиться, None иначе
    """
    # Отключаем таймаут на время проверки выхода
    std.timeout(-1)
    std.nodelay(False)

    # Если команда уже определена (передана извне),
    # то используем её, иначе определяем через контроллер
    end_type = command_type

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