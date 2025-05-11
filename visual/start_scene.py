from control.controller import start_controller
from logic.read_texts import read_cnf
from visual.main_scene import main_scene
from visual.hotkeys_scene import hotkeys_scene


def start_scene(std):
    lines = read_cnf("start_scene")
    std.clear()

    # Добавляем новую опцию для настройки горячих клавиш
    updated_lines = lines.copy()
    if "3 - Настроить горячие клавиши" not in updated_lines:
        # Находим индекс строки с "q - Выйти" и вставляем новую опцию перед ней
        for i, line in enumerate(updated_lines):
            if "q - Выйти" in line:
                updated_lines.insert(i, "3 - Настроить горячие клавиши")
                break

    for i in range(len(updated_lines)):
        std.addstr(i + 4, 0, updated_lines[i])

    std.refresh()
    type_text = start_controller(std)

    if type_text == "exit":
        return "exit"
    elif type_text == "new_f":
        return main_scene(std, type_text)
    elif type_text == "olf_f":
        return main_scene(std, type_text)
    elif type_text == "hotkeys":
        hotkeys_scene(std)
        # После настройки горячих клавиш возвращаемся в стартовое меню
        return start_scene(std)
