import json


def read_cnf(name):
    with open("configs.json", "r", encoding="utf-8") as f:
        lines = json.load(f)
    return lines[name]
