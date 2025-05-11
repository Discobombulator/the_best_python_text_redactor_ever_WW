import curses.ascii

from logic.hotkeys_maneger import HotkeysManager

# Загружаем менеджер горячих клавиш
hotkeys_manager = HotkeysManager()


def start_controller(std):
    key = std.getch()
    if key in [ord('1'), ord('!')]:
        return "new_f"
    elif key in [ord('2'), ord('@')]:
        return "olf_f"
    elif key in [ord('3'), ord('#')]:
        return "hotkeys"
    elif key in [ord('q'), ord('й')]:
        return "exit"


def main_controller(std):
    key = std.getch()

    # Используем менеджер горячих клавиш для проверки комбинаций
    save_key = hotkeys_manager.get_key_code("save")
    save_how_key = hotkeys_manager.get_key_code("save_how")
    exit_save_key = hotkeys_manager.get_key_code("exit_save")
    exit_no_save_key = hotkeys_manager.get_key_code("exit_no_save")

    if key == save_key:
        return "save"
    elif key == save_how_key:
        return "save_how"
    elif key == exit_save_key:
        return "exit_save"
    elif key == exit_no_save_key:
        return "exit_no_save"


def no_save_check(std):
    key = std.getch()
    if key in [ord('1'), ord('!')]:
        return "exit"
    elif key in [ord('2'), ord('@')]:
        return "no_exit"


def new_name_check(std):
    key = std.getch()

    # Используем менеджер горячих клавиш для подтверждения
    confirm_key = hotkeys_manager.get_key_code("confirm")

    if key == confirm_key:
        return "confirm"
