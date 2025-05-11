def hotkeys_controller(std):
    key = std.getch()

    # Управление перемещением
    if key == 258:  # Стрелка вниз
        return "down"
    elif key == 259:  # Стрелка вверх
        return "up"
    elif key == 10:  # Enter (редактировать выбранную клавишу)
        return "edit"
    elif key in [27, ord('q')]:  # Escape или 'q' (выход)
        return "exit"
    elif key in [ord('s'), ord('S')]:  # 's' или 'S' (сохранить)
        return "save"
