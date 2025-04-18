from control.controller import start_controller
from logic.read_texts import read_cnf
from visual.main_scene import main_scene

from control.controller import start_controller
from logic.read_texts import read_cnf
from visual.main_scene import main_scene
import curses


def start_scene(std):
    """Отображает стартовое меню и обрабатывает выбор пользователя"""
    try:
        # Получаем строки для отображения
        lines = read_cnf("start_scene")

        # Очищаем экран
        std.clear()
        std.refresh()

        # Включаем поддержку цветов (если нужно)
        curses.start_color()
        curses.use_default_colors()

        # Отображаем меню
        for i, line in enumerate(lines):
            try:
                # Используем addstr с целочисленными координатами
                std.addstr(i + 4, 0, line)
            except curses.error:
                # Пропускаем ошибки вывода за границы экрана
                pass

        std.refresh()

        # Обрабатываем выбор пользователя
        choice = start_controller(std)

        if choice == "exit":
            return "exit"
        return main_scene(std, choice)

    except Exception as e:
        # В случае ошибки выводим её и завершаем программу
        std.addstr(0, 0, f"Error: {str(e)}")
        std.refresh()
        std.getch()
        return "exit"