from control.controller import start_controller
from logic.read_texts import read_cnf
from visual.main_scene import main_scene

from control.controller import start_controller
from logic.read_texts import read_cnf
from visual.main_scene import main_scene
import curses


def start_scene(std):
    lines = read_cnf("start_scene")
    std.clear()

    for i in range(len(lines)):
        std.addstr(i+4, 0, lines[i])

    std.refresh()
    type_text = start_controller(std)

    if type_text == "exit":
        return "exit"
    elif type_text == "new_f":
        return main_scene(std, type_text)
    elif type_text == "olf_f":
        return main_scene(std, type_text)