from logic.chech_esc_buttons import is_program_end
from logic.read_texts import read_cnf


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

        res = is_program_end(std,text_type)
        if res =="exit":
            return "exit"
