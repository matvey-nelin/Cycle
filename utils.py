import sys
import os
import re

from pathlib import Path

def resource_path(relative_path: str) -> Path:
    """
    Возвращает абсолютный путь к упакованному ресурсу.
    Предназначен ТОЛЬКО для ЧТЕНИЯ (ассеты, дефолтные конфиги).
    Работает в: dev-режиме Flet, сборке PyInstaller (Windows), Flet Android.
    """
    base = Path(__file__).resolve().parent

    # Ветка PyInstaller: при заморозке sys.frozen == True
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            base = Path(meipass)

    return base / relative_path


def get_data_directory() -> Path:
    APP_NAME = "Cycle"
    """Возвращает безопасную директорию для данных приложения."""    
    # 🛠 РЕЖИМ РАЗРАБОТКИ: если задана переменная окружения
    if os.environ.get("CYCLE_DEV") == "1":
        dev_dir = Path(__file__).resolve().parent / "app_data"
        dev_dir.mkdir(parents=True, exist_ok=True)
        return dev_dir

    # 🌍 РЕЖИМ ПРОДАКШЕНА: стандартные пути ОС
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        result_path = base / APP_NAME

    elif sys.platform == "darwin":
        result_path = Path.home() / "Library" / "Application Support" / APP_NAME

    elif os.environ.get("ANDROID_DATA"):
        result_path = Path(__file__).resolve().parent
        
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        result_path = base / APP_NAME
    
    result_path.mkdir(parents=True, exist_ok=True)
    return result_path


def detect_language_native(text: str) -> str:
    """
    Определяет язык (RU или EN) без сторонних библиотек.
    Использует твою логику фильтрации.
    """
    cleaned = re.sub(r'[^a-zа-я]', '', text.lower())
    
    if not cleaned:
        return 'en'

    if re.search(r'[а-я]', cleaned):
        return 'ru'
    
    return 'en'