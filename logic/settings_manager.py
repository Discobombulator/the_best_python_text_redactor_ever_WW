import json
import os


class SettingsManager:
    """Менеджер настроек приложения, включая настройки горячих клавиш"""

    def __init__(self, config_file="settings.json"):
        self.config_file = config_file
        self.default_settings = {
            "hotkeys": {
                "save": 19,  # Ctrl+S
                "save_as": 16,  # Ctrl+P
                "exit_save": 18,  # Ctrl+R
                "exit_no_save": 17,  # Ctrl+Q
                "settings": 15  # Ctrl+O
            }
        }
        self.settings = self.load_settings()

    def load_settings(self):
        """Загрузка настроек из файла или создание файла с настройками по умолчанию"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                # Если файл поврежден или не найден, создаем новый с настройками по умолчанию
                return self.reset_to_defaults()
        else:
            return self.reset_to_defaults()

    def reset_to_defaults(self):
        """Сброс настроек на значения по умолчанию"""
        self.settings = self.default_settings.copy()
        self.save_settings()
        return self.settings

    def save_settings(self):
        """Сохранение настроек в файл"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=2, ensure_ascii=False)

    def get_hotkey(self, action):
        """Получение кода клавиши для указанного действия"""
        return self.settings["hotkeys"].get(action, self.default_settings[
            "hotkeys"].get(action))

    def set_hotkey(self, action, key_code):
        """Установка кода клавиши для указанного действия"""
        if action in self.settings["hotkeys"]:
            self.settings["hotkeys"][action] = key_code
            self.save_settings()
            return True
        return False

    def get_all_hotkeys(self):
        """Получение всех горячих клавиш"""
        return self.settings["hotkeys"].copy()

    @staticmethod
    def key_code_to_str(key_code):
        """Преобразование кода клавиши в читаемый вид"""
        if 1 <= key_code <= 26:  # Ctrl+A to Ctrl+Z
            return f"Ctrl+{chr(key_code + 64)}"
        return f"Key {key_code}"

    @staticmethod
    def get_key_name(key_code):
        """Получение названия клавиши по её коду"""
        if 1 <= key_code <= 26:  # Ctrl+A to Ctrl+Z
            return f"Ctrl+{chr(key_code + 64)}"
        return f"Unknown ({key_code})"


# Глобальный экземпляр настроек
settings_manager = SettingsManager()