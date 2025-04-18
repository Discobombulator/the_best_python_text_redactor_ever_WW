from control.controller import main_controller
from logic.saving_file_functions import save_text, save_text_no_name
from visual.exit_and_save_scene import exit_no_save


def is_program_end(std, text_type, text, name):
    std.refresh()

    # Используем non-blocking ввод
    std.nodelay(False)  # Переключаем в режим ожидания клавиши
    end_type = main_controller(std)
    std.nodelay(True)  # Возвращаем предыдущий режим

    # Выход без сохранения
    if end_type == "exit_no_save":
        if exit_no_save(std) == "exit_no_save":
            return "exit"
    # Сохранение с новым названием
    elif end_type == "save_how":
        save_text_no_name(std, text)
    # Сохранение по старому названию
    elif end_type == "save":
        if text_type == "olf_f":
            save_text(text, name)
    # Сохранение с новым названием и выход
    elif end_type == "exit_save":
        save_text_no_name(std, text)
        return "exit"
    return None
