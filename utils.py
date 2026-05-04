import sys
import os

def resource_path(relative_path: str) -> str:
    """Получает абсолютный путь к ресурсу (работает и в dev, и в .exe)"""
    if getattr(sys, 'frozen', False):
        # При запуске из .exe PyInstaller создаёт _MEIPASS во временной папке
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        # При запуске из исходников берём папку со скриптом
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)