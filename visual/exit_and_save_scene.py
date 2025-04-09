from control.controller import no_save_check


def exit_no_save(std):
    std.clear()

    std.addstr(1, 0, "Вы уверены что хотите выйти без сохранения?")
    std.addstr(2, 0, "_________________________________________")
    std.addstr(3, 0, "1 - Да")
    std.addstr(4, 0, "2 - Нет")
    std.addstr(6, 0, "                                         ")
    std.addstr(7, 0, "Ваш ответ:")

    res = no_save_check(std)
    if res == "exit":
        return "exit_no_save"
    elif res == "no_exit":
        return