from control.controller import start_controller
from visual.main_scene import main_scene


def start_scene(std):
    std.clear()

    std.addstr(4, 0, "Добро пожаловать в лучший в мире текстовый редактор")
    std.addstr(5, 0, "_________________________________________")
    std.addstr(6, 0, "                                         ")
    std.addstr(7, 0, "Выберите, что вы хотите сделать")
    std.addstr(8, 0, "1 - Создать новый файл")
    std.addstr(9, 0, "2 - Открыть существующий")
    std.addstr(10, 0, "q - Выйти")
    std.addstr(11, 0, " ")
    std.addstr(12, 0, "Я хочу: ")

    std.refresh()
    type_text = start_controller(std)

    if type_text == "exit":
        return "exit"
    elif type_text == "new_f":
        return main_scene(std, type_text)
    elif type_text == "olf_f":
        return main_scene(std, type_text)

