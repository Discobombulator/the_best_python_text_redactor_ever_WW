from control.controller import main_controller
from visual.exit_and_save_scene import exit_no_save


def main_scene(std, type_text):
    while True:
        std.clear()

        std.addstr(1, 0, "Что вым доступно:")
        std.addstr(2, 0, "_________________________________________")
        std.addstr(3, 0, "                                         ")
        std.addstr(4, 0, "CTRL+S - Сохранить(только для открытых файлов)")
        std.addstr(5, 0, "CTRL+P - Сохранить как")
        std.addstr(6, 0, "CTRL+R - Выйти с сохранением")
        std.addstr(7, 0, "CTRL+Q - Выйти без сохранения")
        std.addstr(8, 0, "")

        std.addstr(9, 0, "Ваш текст:")

        """TODO:
                  Выводится текст если открыт старый или просто можно писать
                   если ничего нету
              """

        end_type = main_controller(std)

        if end_type == "exit_no_save":
            if exit_no_save(std) == "exit_no_save":
                return "exit"
        elif end_type == "save_how":
            """TODO:
             сохранение файла с новым названием и продолжение работы
            без выхода"""
        elif end_type == "save":
            if type_text == "olf_f":
                """TODO:
                 сохранение файла по старому названию
                (только для открытых файлов)"""
        elif end_type == "exit_save":
            """TODO:
             сохранение файла с новым названием и потом выход"""
