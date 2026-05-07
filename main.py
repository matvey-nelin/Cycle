# Библиотеки фактического импорта
import flet as ft
import os
import json


from AppState import AppState
from UI.CycleApp import CycleApp

from Languages import SupportedLanguages

import utils


def get_app_data_dir() -> str:
    """Возвращает безопасную директорию для данных приложения (Android/Windows/Linux)"""
    # В сборке Flet файлы Python лежат в .../files/flet/app/
    # Это приватная папка приложения, куда разрешена запись на всех платформах
    return os.path.dirname(os.path.abspath(__file__))

def check_and_create_service_files():
    base_dir = get_app_data_dir()
    settings_path = os.path.join(base_dir, "settings.json")
    lang_packs_dir = os.path.join(base_dir, "language_packs")

    try:
        # 1. Инициализация настроек
        if not os.path.exists(settings_path):
            # ⚠️ Пути к ассетам всегда пишем с прямыми слэшами /
            default_path = utils.resource_path("assets/settings/default_settings.json")
            with open(default_path, "r", encoding="UTF-8") as f:
                settings_data = json.load(f)

            with open(settings_path, "w", encoding="UTF-8") as f:
                json.dump(settings_data, f, ensure_ascii=False, indent=4)

        # 2. Инициализация языковых пакетов
        # exist_ok=True предотвратит ошибку, если папка уже создана
        os.makedirs(lang_packs_dir, exist_ok=True)

        for lang_code in SupportedLanguages.LANGUAGES.keys():
            lang_pack_path = os.path.join(lang_packs_dir, f"{lang_code}.json")

            if not os.path.exists(lang_pack_path):
                default_pack_path = utils.resource_path(f"assets/LanguagePacks/Default Language Packs/{lang_code}.json")
                with open(default_pack_path, "r", encoding="UTF-8") as f:
                    pack_data = json.load(f)

                with open(lang_pack_path, "w", encoding="UTF-8") as f:
                    json.dump(pack_data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        # 🔴 КРИТИЧНО: не даём приложению упасть молча при инициализации
        print(f"[INIT ERROR] {e}")
        # Если нужно отладить, раскомментируй временный вывод на экран:
        # import flet as ft
        # ft.app(target=lambda page: page.add(ft.Text(f"Ошибка запуска: {e}", color="red", size=16)))



def main(page: ft.Page):
    check_and_create_service_files()

    app_state = AppState(page)
    CycleApp(page, app_state)


ft.run(
    main=main,
    assets_dir="assets",
    name="Cycle"
)
