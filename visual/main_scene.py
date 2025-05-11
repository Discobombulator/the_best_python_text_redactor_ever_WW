from logic.chech_esc_buttons import is_program_end
from logic.hotkeys_maneger import HotkeysManager
from logic.read_texts import read_cnf


def main_scene(std, text_type):
    lines = read_cnf("main_scene")

    # Получаем актуальные названия горячих клавиш
    hotkeys_manager = HotkeysManager()

    # Обновляем визуальное отображение горячих клавиш с учетом настроек
    updated_lines = []
    for line in lines:
        if "CTRL+S - Сохранить" in line:
            updated_lines.append(
                f"{hotkeys_manager.get_key_desc('save')} - Сохранить(только для открытых файлов)")
        elif "CTRL+P - Сохранить как" in line:
            updated_lines.append(
                f"{hotkeys_manager.get_key_desc('save_how')} - Сохранить как")
        elif "CTRL+R - Выйти с сохранением" in line:
            updated_lines.append(
                f"{hotkeys_manager.get_key_desc('exit_save')} - Выйти с сохранением")
        elif "CTRL+Q - Выйти без сохранения" in line:
            updated_lines.append(
                f"{hotkeys_manager.get_key_desc('exit_no_save')} - Выйти без сохранения")
        else:
            updated_lines.append(line)

    text = ""
    name = ""
    if text_type == "olf_f":
        """TODO:
                  тут надо выбрать файл, прочитать его и в name
                   поместить название файла без .txt
              """
        name = "test"
        text = ["test_text"]

    while True:
        std.clear()

        for i in range(len(updated_lines)):
            std.addstr(i, 0, updated_lines[i])

        """TODO:
                  Выводится текст если открыт старый или просто можно писать
                   если ничего нету
              """

        res = is_program_end(std, text_type, text, name)
        if res == "exit":
            return "exit"