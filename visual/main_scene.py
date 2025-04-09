from control.controller import main_controller
from logic.read_texts import read_cnf
from visual.exit_and_save_scene import exit_no_save


def main_scene(std, type_text):
    lines = read_cnf("main_scene")

    while True:
        std.clear()

        for i in range(len(lines)):
            std.addstr(i, 0, lines[i])

        """TODO:
                  Выводится текст если открыт старый или просто можно писать
                   если ничего нету
              """

        type_text = main_controller(std)
        if type_text == "exit_no_save":
            if exit_no_save(std) == "exit_no_save":
                return "exit"
        elif type_text == "save_how":
            """TODO:
             сохранение файла с новым названием и продолжение работы
            без выхода"""
        elif type_text == "save":
            if type_text == "olf_f":
                """TODO:
                 сохранение файла по старому названию
                (только для открытых файлов)"""
        elif type_text == "exit_save":
            """TODO:
             сохранение файла с новым названием и потом выход"""
