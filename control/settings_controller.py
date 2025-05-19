import curses


def settings_controller(std: curses.window, key: int):
    """
    Проверяет, была ли нажата клавиша настроек.
    Теперь принимает key как аргумент, а не читает его сама.
    """
    if key == 15:  # Ctrl+O
        return "settings"
    return None