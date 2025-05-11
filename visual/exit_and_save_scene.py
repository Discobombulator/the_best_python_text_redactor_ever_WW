from control.controller import no_save_check
from logic.hotkeys_maneger import HotkeysManager
from logic.read_texts import read_cnf


def exit_no_save(std):
    std.clear()

    lines = read_cnf("exit_no_save_text")

    for i in range(len(lines)):
        std.addstr(i, 0, lines[i])

    res = no_save_check(std)
    if res == "exit":
        return "exit_no_save"
    elif res == "no_exit":
        return


def make_file_name_scene(std):
    std.clear()

    lines = read_cnf("make_file_name_text")

    # Получаем актуальное название горячей клавиши для подтверждения
    hotkeys_manager = HotkeysManager()

    # Обновляем строку с клавишей подтверждения
    updated_lines = []
    for line in lines:
        if "CTRL+S - Подтвердить" in line:
            updated_lines.append(
                f"{hotkeys_manager.get_key_desc('confirm')} - Подтвердить новое имя файла")
        else:
            updated_lines.append(line)

    for i in range(len(updated_lines)):
        std.addstr(i, 0, updated_lines[i])
