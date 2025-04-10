from logic.chech_esc_buttons import is_program_end
from logic.read_texts import read_cnf


def main_scene(std, text_type):
    lines = read_cnf("main_scene")

    text = ""
    name = ""
    if text_type == "olf_f":
        """TODO:
                  тут надо выбрать файл, прочитать его и в name
                   поместить название файла без .txt
              """
        name = "test"
        text = ["test_text"]

    while True:
        std.clear()

        for i in range(len(lines)):
            std.addstr(i, 0, lines[i])

        """TODO:
                  Выводится текст если открыт старый или просто можно писать
                   если ничего нету
              """

        res = is_program_end(std, text_type, text, name)
        if res == "exit":
            return "exit"
