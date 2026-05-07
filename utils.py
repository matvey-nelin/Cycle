import sys
import os
import re


def resource_path(relative_path: str) -> str:
    """Получает абсолютный путь к ресурсу (работает и в dev, и в .exe)"""
    if getattr(sys, 'frozen', False):
        # При запуске из .exe PyInstaller создаёт _MEIPASS во временной папке
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        # При запуске из исходников берём папку со скриптом
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


def detect_language_native(text: str) -> str:
    """
    Определяет язык (RU или EN) без сторонних библиотек.
    Использует твою логику фильтрации.
    """
    # 1. Твоя очистка текста (оставляем только a-z и а-я)
    cleaned = re.sub(r'[^a-zа-я]', '', text.lower())
    
    # Если текст пустой после очистки
    if not cleaned:
        return 'en' # По умолчанию

    # 2. Логика: так как мы оставили только a-z и а-я,
    # достаточно проверить, есть ли в тексте хоть одна русская буква.
    # Если есть -> это русский, если нет -> это английский.
    if re.search(r'[а-я]', cleaned):
        return 'ru'
    
    return 'en'