from pathlib import Path


def scripts_dir() -> Path:
    return Path(__file__).resolve().parents[2]


def templates_dir() -> Path:
    return scripts_dir().parent / "templates"

