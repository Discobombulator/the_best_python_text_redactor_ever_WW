import json
import os
import curses


class TextColorManager:
    def __init__(self):
        self.default_color = curses.COLOR_WHITE
        self.color = self.default_color

    def get_config_path(self, txt_path: str) -> str:
        """Получаем путь к файлу конфигурации цвета"""
        base, _ = os.path.splitext(txt_path)
        return f"{base}.cnf"

    def load_color(self, txt_path: str) -> None:
        """Загружаем цвет текста из конфига"""
        config_path = self.get_config_path(txt_path)
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    self.color = data.get('text_color', self.default_color)
            except:
                self.color = self.default_color
        else:
            # Установим значение по умолчанию, если файл не существует
            self.color = self.default_color

    def save_color(self, txt_path: str) -> None:
        """Сохраняем цвет текста в конфиг"""
        config_path = self.get_config_path(txt_path)
        with open(config_path, 'w') as f:
            json.dump({'text_color': self.color}, f)
        # Убедимся, что файл был создан
        if not os.path.exists(config_path):
            print(f"Ошибка: не удалось создать файл конфигурации {config_path}")

    def set_color(self, color: int) -> None:
        """Устанавливаем текущий цвет"""
        self.color = color

    def get_color(self) -> int:
        """Получаем текущий цвет"""
        return self.color


# Глобальный экземпляр менеджера цвета
text_color_manager = TextColorManager()