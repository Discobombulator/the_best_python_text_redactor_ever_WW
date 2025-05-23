import curses

from control.controller import no_save_check
from logic.read_texts import read_cnf


def exit_no_save(std: curses.window):
    std.clear()

    lines = read_cnf("exit_no_save_text")

    for i in range(len(lines)):
        std.addstr(i, 0, lines[i])

    res = no_save_check(std)
    if res == "exit":
        return "exit_no_save"
    elif res == "no_exit":
        return


def make_file_name_scene(std: curses.window):
    std.clear()

    lines = read_cnf("make_file_name_text")

    for i in range(len(lines)):
        std.addstr(i, 0, lines[i])
