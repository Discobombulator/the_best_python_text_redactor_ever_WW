import curses

from visual.exit_and_save_scene import make_file_name_scene


def save_text(lines: list[str], name: str):
    with open(name + ".txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def save_text_no_name(std: curses.window, lines: list[str]):
    with open(make_file_name(std) + ".txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def make_file_name(std: curses.window):
    make_file_name_scene(std)
    name = []
    curses.noecho()
    std.keypad(True)

    while True:
        std.move(3, 12)
        std.clrtoeol()
        std.addstr(3, 12, "".join(name))
        std.refresh()

        key = std.getch()

        if key in (curses.KEY_BACKSPACE, 127, 8):
            if name:
                name.pop()
        elif key == curses.KEY_ENTER or key == 10:
            break
        elif key == curses.ascii.ctrl(83) or key == curses.ascii.ctrl(115):
            break
        elif 32 <= key <= 126:
            name.append(chr(key))

    return "".join(name).strip()
