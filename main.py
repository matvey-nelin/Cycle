# Библиотеки фактического импорта
import flet as ft
import os
import sys
import json


from AppState import AppState
from UI.CycleApp import CycleApp

from Languages import SupportedLanguages

import utils



def check_and_create_service_files():
    # Создание файла настроек
    settings_path = os.path.join(os.path.dirname(sys.executable), "settings.json")

    if not os.path.exists(settings_path):
        with open(utils.resource_path(r"assets\settings\default_settings.json"), "r", encoding="UTF-8") as file:
            settings_dict = dict(json.load(file))

        with open(settings_path, "w", encoding="UTF-8") as file:
            json.dump(settings_dict, file, ensure_ascii=False, indent=4)


    # Создание языковых пакетов
    if not os.path.exists(os.path.join(os.path.dirname(sys.executable), "language_packs")):
        os.mkdir(os.path.join(os.path.dirname(sys.executable), "language_packs"))

    for language in list(SupportedLanguages.LANGUAGES.keys()):
        language_pack_path = os.path.join(os.path.dirname(sys.executable), fr"language_packs\{language}.json")

        if not os.path.exists(language_pack_path):
            with open(utils.resource_path(fr"assets\LanguagePacks\Default Language Packs\{language}.json"), "r", encoding="UTF-8") as pack:
                language_pack = dict(json.load(pack))

            with open(language_pack_path, "w", encoding="UTF-8") as pack:
                json.dump(language_pack, pack, ensure_ascii=False, indent=4)




def main(page: ft.Page):
    check_and_create_service_files()

    app_state = AppState(page)
    CycleApp(page, app_state)


ft.run(
    main=main,
    assets_dir="assets"
)
