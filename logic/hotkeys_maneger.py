import json
import curses.ascii
from pathlib import Path


class HotkeysManager:
    DEFAULT_CONFIG_FILE = "configs.json"
    HOTKEYS_CONFIG_FILE = "hotkeys_config.json"

    # Словарь действий по умолчанию и их описаний
    DEFAULT_ACTIONS = {
        "save": {"desc": "Сохранить", "key": "s"},
        "save_how": {"desc": "Сохранить как", "key": "p"},
        "exit_save": {"desc": "Выйти с сохранением", "key": "r"},
        "exit_no_save": {"desc": "Выйти без сохранения", "key": "q"},
        "confirm": {"desc": "Подтвердить", "key": "s"}
    }

    # Словарь соответствия буквенных кодов и числовых для ctrl+key
    CTRL_KEYS_MAP = {}

    def __init__(self):
        # Инициализация словарей для хранения конфигурации
        self.available_keys = {}
        self.hotkeys = {}
        self.load_available_keys()
        self.load_hotkeys()

        # Заполняем карту клавиш
        for letter in range(97, 123):  # ASCII коды для 'a' до 'z'
            upper_letter = letter - 32
            self.CTRL_KEYS_MAP[chr(letter)] = curses.ascii.ctrl(letter)
            self.CTRL_KEYS_MAP[chr(upper_letter)] = curses.ascii.ctrl(
                upper_letter)

    def load_available_keys(self):
        try:
            with open(self.DEFAULT_CONFIG_FILE, "r", encoding="utf-8") as f:
                configs = json.load(f)
                if "hot_keys" in configs and configs["hot_keys"]:
                    self.available_keys = configs["hot_keys"][0]
        except (FileNotFoundError, json.JSONDecodeError, IndexError) as e:
            print(f"Error loading available keys: {e}")
            # Если не удалось загрузить, используем стандартные Ctrl+A до Ctrl+Z
            for i, letter in enumerate(range(ord('a'), ord('z') + 1)):
                self.available_keys[str(i + 1)] = f"Ctrl+{chr(letter - 32)}"

    def load_hotkeys(self):
        config_path = Path(self.HOTKEYS_CONFIG_FILE)

        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    self.hotkeys = json.load(f)
            except json.JSONDecodeError:
                self._set_default_hotkeys()
        else:
            self._set_default_hotkeys()

    def _set_default_hotkeys(self):
        self.hotkeys = {action: config for action, config in
                        self.DEFAULT_ACTIONS.items()}

    def save_hotkeys(self):
        with open(self.HOTKEYS_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.hotkeys, f, ensure_ascii=False, indent=2)

    def get_key_code(self, action):

        if action not in self.hotkeys:
            return None

        key = self.hotkeys[action].get("key", "").lower()
        if key in self.CTRL_KEYS_MAP:
            return self.CTRL_KEYS_MAP[key]
        return None

    def get_key_desc(self, action):

        if action not in self.hotkeys:
            return f"UNKNOWN"

        key = self.hotkeys[action].get("key", "").upper()
        return f"CTRL+{key}"

    def update_hotkey(self, action, new_key):

        if action not in self.hotkeys:
            return False

        # Проверяем, что клавиша допустима
        new_key = new_key.lower()
        if not ('a' <= new_key <= 'z'):
            return False

        # Обновляем конфигурацию
        self.hotkeys[action]["key"] = new_key
        return True

    def get_all_hotkeys(self):

        result = []
        for action, config in self.hotkeys.items():
            result.append((action, config["desc"], config["key"].upper()))
        return result
