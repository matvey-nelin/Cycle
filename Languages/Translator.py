import json
import os
import sys

import re
from transliterate import translit

from Languages import SupportedLanguages

import utils



class Translator:
    def __init__(self, language: str) -> None:
        if not isinstance(language, str):
            raise TypeError("Invalid language indicator value")
        
        if language not in list(SupportedLanguages.LANGUAGES.keys()):
            raise ValueError("Unsupported language")
        
        try:
            # Инициализация языковых пакетов
            language_packs_dir = utils.get_data_directory() / "language_packs"
            os.makedirs(language_packs_dir, exist_ok=True)

            for lang_code in SupportedLanguages.LANGUAGES.keys():
                language_pack_path  = language_packs_dir / f"{lang_code}.json"
                default_pack_path   = utils.resource_path(f"assets/language_packs/{lang_code}.json")

                if not language_pack_path.exists():
                    with open(default_pack_path, "r", encoding="UTF-8") as file:
                        pack_data = json.load(file)

                    with open(language_pack_path, "w", encoding="UTF-8") as file:
                        json.dump(pack_data, file, ensure_ascii=False, indent=4)
        
        except Exception as e:
            print(f"[INIT ERROR] {e}")
        


        self.language_pack_path = utils.get_data_directory() / rf"language_packs/{language}.json"
        with open(self.language_pack_path, "r", encoding="UTF-8") as pack:
            self.language_pack = dict(json.load(pack))


        # Назначение надписей данных
        self.data_labels = dict(self.language_pack["data"])

        self.user_statuses 		    = dict(self.data_labels["user_statuses"])
        self.workout_statuses		= dict(self.data_labels["workout_statuses"])
        self.workout_types		    = dict(self.data_labels["workout_types"])
        self.hypertrophy_types	    = dict(self.data_labels["hypertrophy_types"])
        self.agonists			    = dict(self.data_labels["agonists"])
        self.exercises			    = dict(self.data_labels["exercises"])
        self.workout_templates      = dict(self.data_labels["workout_templates"])
        self.microcycle_templates   = dict(self.data_labels["microcycle_templates"])


        # Назначение надписей настроек
        self.settings_labels = dict(self.language_pack["settings"])


        # Назначение надписей классов
        self.classes_labels = dict(self.language_pack["classes"])

        self.training_process_labels = dict(self.classes_labels["training_process"])
        self.app_colors_labels       = dict(self.classes_labels["app_colors"])
        

        # Назначение надписей интерфейса
        self.ui_labels = dict(self.language_pack["ui"])
        self.screens_labels = dict(self.ui_labels["screens"])
        self.components_labels = dict(self.ui_labels["components"])

            # Первые базовые окна
        self.setup_wizard_labels    = dict(self.screens_labels["setup_wizard"])

            # Компоненты
        self.exercise_set_labels    = dict(self.components_labels["exercise_set"])
        self.manager_dialog_labels  = dict(self.components_labels["manager_dialog"])
        self.invalid_data_alert_dialog_labels = dict(self.components_labels["invalid_data_alert_dialog"])
        self.navigation_menu_labels = dict(self.components_labels["navigation_menu"])
        self.records_list_labels    = dict(self.components_labels["records_list"])

            # Главный начальный экран
        self.dashboard_screen_labels = dict(self.screens_labels["dashboard_screen"])


            # Экран планирования
        self.planning_screen_labels         = dict(self.screens_labels["planning_screen"])
        self.workout_template_menu_labels   = dict(self.screens_labels["workout_template_menu"])
        self.workout_template_screen_labels = dict(self.screens_labels["workout_template_screen"])

        self.microcycle_template_menu_labels    = dict(self.screens_labels["microcycle_template_menu"])
        self.microcycle_template_screen_labels  = dict(self.screens_labels["microcycle_template_screen"])

        self.mesocycle_menu_labels          = dict(self.screens_labels["mesocycle_menu"])
        self.mesocycle_screen_labels        = dict(self.screens_labels["mesocycle_screen"])

        self.macrocycle_menu_labels         = dict(self.screens_labels["macrocycle_menu"])
        self.macrocycle_screen_labels       = dict(self.screens_labels["macrocycle_screen"])

        self.workout_screen_labels = dict(self.screens_labels["workout_screen"])


            # Экран статистики
        self.statistics_screen_labels   = dict(self.screens_labels["statistics_screen"])
        

            # Экран справочной информации
        self.reference_information_screen_labels = dict(self.screens_labels["reference_information_screen"])

        self.users_screen_labels               = dict(self.screens_labels["users_screen"])
        self.user_statuses_screen_labels       = dict(self.screens_labels["user_statuses_screen"])
        self.workout_statuses_screen_labels    = dict(self.screens_labels["workout_statuses_screen"])
        self.workout_types_screen_labels       = dict(self.screens_labels["workout_types_screen"])
        self.hypertrophy_types_screen_labels   = dict(self.screens_labels["hypertrophy_types_screen"])
        self.exercises_screen_labels           = dict(self.screens_labels["exercises_screen"])
        self.agonists_screen_labels            = dict(self.screens_labels["agonists_screen"])

        self.user_information_screen_labels             = dict(self.screens_labels["user_information_screen"])
        self.universal_record_management_screen_labels  = dict(self.screens_labels["universal_record_management_screen"])
        self.user_management_screen_labels              = dict(self.screens_labels["user_management_screen"])
        self.exercise_management_screen_labels          = dict(self.screens_labels["exercise_management_screen"])
        self.agonist_management_screen_labels           = dict(self.screens_labels["agonist_management_screen"])


            # Экран настроек
        self.settings_screen_labels     = dict(self.screens_labels["settings_screen"])

        self.app_color_themes_screen    = dict(self.screens_labels["app_color_themes_screen"])


        # Таблицы со слагами
        self.essence_data_labels = {
            "user_statuses"         : self.user_statuses,
            "workout_statuses"      : self.workout_statuses,
            "workout_types"         : self.workout_types,
            "hypertrophy_types"     : self.hypertrophy_types,
            "agonists"              : self.agonists,
            "exercises"             : self.exercises,
            "workout_templates"     : self.workout_templates,
            "microcycle_templates"  : self.microcycle_templates
        }



    def get_slug(self, text: str, essence: str, old_slug: str = "") -> str:
        """
        Add slug key in the language package. Slug will be placed in essence table.
        Slug will be returned.
        """

        if (text is None):
            raise ValueError("Incorrect data for creating slug")
        

        lang_code = utils.detect_language_native(text).lower()

        try:
            if lang_code == 'ru':
                processed_text = translit(text, lang_code, reversed=True)
            else:
                processed_text = text
        except Exception as _ex:
            raise _ex

        slug = processed_text.lower()
        slug = re.sub(r'[^a-zа-я0-9]', '_', slug) # Заменяем всё не буквенное на _
        slug = re.sub(r'_+', '_', slug)         # Убираем дубли __
        slug = slug.strip('_')

        if old_slug == "": 
            counter = 1
            while slug in list(self.language_pack["data"][essence].keys()):
                if counter == 1:
                    slug += "_n"

                slug = slug[:-2] + f"_{counter}"
                counter += 1

        return slug
    
    
    def add_slug(self, text: str, slug: str, entity: str, old_slug: str = ""):
        if entity not in list(self.essence_data_labels.keys()):
            raise ValueError("Incorrect data of essence for creating slug")

        for language in list(SupportedLanguages.LANGUAGES.keys()):
            language_pack_path = utils.get_data_directory() / rf"language_packs/{language}.json"

            with open(language_pack_path, "r", encoding="UTF-8") as pack:
                language_pack = dict(json.load(pack))

                if self.language_pack == language_pack:
                    # Удаляю старые ключи
                    self.language_pack["data"][entity].pop(old_slug, None)
                    self.essence_data_labels[entity].pop(old_slug, None)

                    # Добавляю новые ключи
                    self.language_pack["data"][entity][slug] = text # Можно реализовать перевод в будущем
                    self.essence_data_labels[entity][slug] = text
                
                # Удаляю старый ключ
                language_pack["data"][entity].pop(old_slug, None) 
                # Добавляю новый ключ
                language_pack["data"][entity][slug] = text # Можно реализовать перевод в будущем


            with open(language_pack_path, "w", encoding="UTF-8") as pack:
                json.dump(language_pack, pack, ensure_ascii=False, indent=4)
        
        
    def delete_slug(self, slug: str, essence: str):
        if essence not in list(self.essence_data_labels.keys()):
            raise ValueError("Incorrect data of essence for deleting slug")
        

        for language in list(SupportedLanguages.LANGUAGES.keys()):
            language_pack_path = utils.get_data_directory() / rf"language_packs/{language}.json"

            with open(language_pack_path, "r", encoding="UTF-8") as pack:
                language_pack = dict(json.load(pack))

                if self.language_pack == language_pack:
                    # Удаляю старые ключи
                    self.language_pack["data"][essence].pop(slug, None)
                    self.essence_data_labels[essence].pop(slug, None)
                
                # Удаляю старый ключ
                language_pack["data"][essence].pop(slug, None) 


            with open(language_pack_path, "w", encoding="UTF-8") as pack:
                json.dump(language_pack, pack, ensure_ascii=False, indent=4)


