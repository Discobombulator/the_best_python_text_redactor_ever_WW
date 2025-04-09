import curses.ascii


def start_controller(std):
    key = std.getch()
    if key in [ord('1'), ord('!')]:
        return "new_f"
    elif key in [ord('2'), ord('@')]:
        return "olf_f"
    elif key in [ord('q'), ord('й')]:
        return "exit"


def main_controller(std):
    key = std.getch()
    if key == curses.ascii.ctrl(83) or key == curses.ascii.ctrl(115):
        return "save"
    elif key == curses.ascii.ctrl(80) or key == curses.ascii.ctrl(112):
        return "save_how"
    elif key == curses.ascii.ctrl(82) or key == curses.ascii.ctrl(114):
        return "exit_save"
    elif key == curses.ascii.ctrl(81) or key == curses.ascii.ctrl(113):
        return "exit_no_save"


def no_save_check(std):
    key = std.getch()
    if key in [ord('1'), ord('!')]:
        return "exit"
    elif key in [ord('2'), ord('@')]:
        return "no_exit"


def logic_controller(std):
    """TODO:
        Метод для управления редактирования текста
        1 менять положение курсорв
        2 переписывать буквы
        3...
    """
