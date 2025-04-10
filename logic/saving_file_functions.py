from control.controller import new_name_check
from visual.exit_and_save_scene import make_file_name_scene


def save_text(lines, name):
    with open(name + ".txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def make_file_name(std):
    make_file_name_scene(std)

    while True:
        """TODO:
            Здесь создается новое имя файла при помощи андрюхиного метода
        """

        name = "test"
        if new_name_check(std) == "confirm":
            return name


def save_text_no_name(std, lines):
    with open(make_file_name(std) + ".txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
