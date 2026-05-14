import json

from Languages import SupportedLanguages

import utils



class Settings:
    def __init__(self) -> None:
        self.settings_path = utils.get_data_directory() / "settings.json"

        # Запись файла настроек в первый запуск программы
        if not self.settings_path.exists():
            self._settings_dict = {
                "first_launch"  : True,
                "language"      : "en",

                "trainer_mode"  : False,

                "theme_mode"    : "system",
                "color_theme"   : "Aurora Borealis",
                
                "current_user"      : 0,
                "current_workout"   : 0,
                "unchangeable_records" : {
                    "user_statuses"     : [_ for _ in range(1, 6)],   # Первые 5 инициируемых при создании БД записей
                    "workout_statuses"  : [_ for _ in range(1, 8)],   # Первые 7 инициируемых при создании БД записей
                    "workout_types"     : [_ for _ in range(1, 19)],  # Первые 18 инициируемых при создании БД записей
                    "hypertrophy_types" : [_ for _ in range(1, 5)],   # Первые 4 инициируемых при создании БД записей
                    "exercises"         : [], # [_ for _ in range(1, 31)],  # Первые 30 инициируемых при создании БД записей
                    "agonists"          : [] # [_ for _ in range(1, 51)]   # Первые 50 инициируемых при создании БД записей
                }
            }
            with open(self.settings_path, "w", encoding="UTF-8") as file:
                json.dump(self._settings_dict, file, ensure_ascii=False, indent=4)

        try:
            # Назначение параметров настроек 
            # (для проверки правильности написания: в файле должно быть 5 имен каждой настройки (через поиск))
            
            with open(self.settings_path, "r", encoding="UTF-8") as file:
                self._settings_dict = dict(json.load(file))


            self.first_launch   = bool(self._settings_dict["first_launch"])
            self.language       = str(self._settings_dict["language"])

            self.trainer_mode   = bool(self._settings_dict["trainer_mode"])

            self.theme_mode     = str(self._settings_dict["theme_mode"])
            self.color_theme    = str(self._settings_dict["color_theme"])

            self.current_user       = int(self._settings_dict["current_user"])
            self.current_workout    = int(self._settings_dict["current_workout"])


            # Неизменяемые записи
            self.unchangeable_records = dict(self._settings_dict["unchangeable_records"])

            self.unchangeable_user_statuses     = list(self.unchangeable_records["user_statuses"])
            self.unchangeable_workout_statuses  = list(self.unchangeable_records["workout_statuses"])
            self.unchangeable_workout_types     = list(self.unchangeable_records["workout_types"])
            self.unchangeable_hypertrophy_types = list(self.unchangeable_records["hypertrophy_types"])
            self.unchangeable_exercises         = list(self.unchangeable_records["exercises"])
            self.unchangeable_agonists          = list(self.unchangeable_records["agonists"])



        except Exception as _ex:
            print(_ex)



    def unloading(self):
        try:
            # Смена стандартных настроек на текущие, если файл настроек существует
            self._settings_dict = {
                "first_launch"  : self.first_launch,
                "language"      : self.language,

                "trainer_mode"  : self.trainer_mode,
                "theme_mode"    : self.theme_mode,
                "color_theme"   : self.color_theme,
                
                "current_user"      : self.current_user,
                "current_workout"   : self.current_workout,

                "unchangeable_records" : {
                    "user_statuses"     : self.unchangeable_user_statuses,      # Первые 5 инициируемых при создании БД записей
                    "workout_statuses"  : self.unchangeable_workout_statuses,   # Первые 7 инициируемых при создании БД записей
                    "workout_types"     : self.unchangeable_workout_types,      # Первые 18 инициируемых при создании БД записей
                    "hypertrophy_types" : self.unchangeable_hypertrophy_types,  # Первые 4 инициируемых при создании БД записей
                    "exercises"         : self.unchangeable_exercises,          # Первые 30 инициируемых при создании БД записей
                    "agonists"          : self.unchangeable_agonists            # Первые 50 инициируемых при создании БД записей
                }
            }

            with open(self.settings_path, "w", encoding="UTF-8") as file:
                json.dump(self._settings_dict, file, ensure_ascii=False, indent=4)

        except Exception as _ex:
            print(_ex)



    def change_current_user(self, id_user: int):
        self.current_user = id_user
        self.unloading()

    
    def change_language(self, language_code: str):
        if language_code not in list(SupportedLanguages.LANGUAGES.keys()):
            raise ValueError("Insupported language code")

        self.language = language_code
        self.unloading()


    def change_theme_mode(self, theme_mode: str):
        if theme_mode not in ['light', 'dark', 'system']:
            raise ValueError("Incorrect value of app theme")
        
        self.theme_mode = theme_mode
        self.unloading()

    
    def change_color_theme(self, color_theme: str):        
        self.color_theme = color_theme
        self.unloading()


    def change_trainer_mode(self, trainer_mode: bool):
        self.trainer_mode = trainer_mode
        self.unloading()
    



    def start_workout(self, id_workout: int):
        self.current_workout = id_workout
        self.unloading()

    def end_workout(self):
        self.current_workout = 0
        self.unloading()


    def determine_unchangeable_records(self, exercises: bool, agonists: bool):
        """
        Determine which records will be unchangeable.
        Parameters:
            exercises:  [bool]. Insert first 30 exercises records
            agonists:   [bool]. Insert first 50 agonists records
        """

        self.unchangeable_exercises = [_ for _ in range(1, 31)]     if exercises    else []
        self.unchangeable_agonists  = [_ for _ in range(1, 51)]     if agonists     else []

        self.unloading()