from control.controller import main_controller
from logic.read_texts import read_cnf
from visual.exit_and_save_scene import exit_no_save


def main_scene(std, text_type):
    lines = read_cnf("main_scene")

    while True:
        std.clear()

        for i in range(len(lines)):
            std.addstr(i, 0, lines[i])

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
            if text_type == "olf_f":
                """TODO:
                 сохранение файла по старому названию
                (только для открытых файлов)"""
        elif end_type == "exit_save":
            """TODO:
             сохранение файла с новым названием и потом выход"""
