# config_loader.py

import json
import os


def load_config(path: str = "config.json") -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)

    return config


# Create a global config object that other modules can import
CONFIG = load_config()
