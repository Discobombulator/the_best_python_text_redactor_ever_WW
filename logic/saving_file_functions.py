import curses

from visual.exit_and_save_scene import make_file_name_scene


def save_text(lines, name):
    with open(name + ".txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def make_file_name(std):
    saved_timeout = std.gettimeout()
    std.timeout(-1)

    make_file_name_scene(std)
    name = []
    curses.echo()

    while True:
        std.addstr(3, 12, "".join(name))
        key = std.getch()
        if key == curses.KEY_BACKSPACE or key == 127:
            if name:
                name.pop()
        elif key == curses.KEY_ENTER or key == 10:
            break
        elif key == curses.ascii.ctrl(83) or key == curses.ascii.ctrl(115):
            break
        elif 32 <= key <= 126:
            name.append(chr(key))
        std.refresh()

    curses.noecho()
    # Восстанавливаем таймаут
    std.timeout(saved_timeout)
    return "".join(name).strip()


def save_text_no_name(std, lines):
    with open(make_file_name(std) + ".txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def make_file_name(std):
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
