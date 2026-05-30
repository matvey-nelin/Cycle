from types import MethodType

import flet as ft
import os
import sys

from Database.Database import Database
from Languages.Translator import Translator
from Settings import Settings

from UI.ColorThemes.AppColors import AppColors
from UI.ColorThemes import SupportedColorThemes

import utils


class AppState:
    def __init__(self, page: ft.Page) -> None:        
        self.page = page

        self.app_dir = os.path.dirname(sys.executable)

        self.db_path        = utils.get_data_directory() / "CycleDatabase.db"
        self.settings_path  = utils.get_data_directory() / "settings.json"
        self.lang_pack_path = lambda language: utils.get_data_directory() / rf"language_packs/{language}.json"
        self.backups_dir_name = "CycleBackups"
        
        self.settings   = Settings()
        self.database   = Database()
        self.translator = Translator(self.settings.language) 
        
        theme_mode = self.settings.theme_mode
        # Фактическая тема для инициализации цветов (dark/light)
        if self.settings.theme_mode == "system":
            theme_mode = self.page.platform_brightness.value if self.page.platform_brightness is not None else "light"
        self.colors     = AppColors(theme_mode, self.settings.color_theme)
    

        self._listeners = []
        self._resize_listeners = []
        self._data_changed_listeners = []
        self._language_changed_listeners = []

        self.is_mobile = None

        self.hot_restart_methods = []
        

    def change_orientation(self, page: ft.Page):
        self.height = page.height
        self.width  = page.width

        update_page = False
        new_orientation = True if ((self.width is None) or (self.width < 600)) else False

        # Первая запись флага is_mobile
        if self.is_mobile is None:
            self.is_mobile  = new_orientation

        elif self.is_mobile != new_orientation:
            self.is_mobile = new_orientation
            update_page = True

        return update_page



    # SetupWizard вызовы. ПЕРЕДЕЛАТЬ ПОТОМ. РЕАЛИЗАЦИЯ ЕСТЬ НИЖЕ
    def set_language(self, new_lang: str):
        if new_lang != self.settings.language:
            self.settings.language = new_lang
            self.settings.unloading()

            self.translator = Translator(self.settings.language)

            self.notify()
    

    def set_theme(self, new_theme: str):
        if new_theme != self.settings.theme_mode:
            self.settings.theme_mode = new_theme
            self.settings.unloading()

            self.notify()



    def subscribe(self, callback):
        self._listeners.append(callback)

    def notify(self):
        for update_listener in self._listeners:
            update_listener()




    def resize_subscribe(self, callback):
        self._resize_listeners.append(callback)

    def resize_notify(self, e):
        for resize_listener in self._resize_listeners:
            try:
                resize_listener(e)
            except Exception as _ex:
                pass


    
    def data_changed_subscribe(self, callback):
        self._data_changed_listeners.append(callback) 

    def data_changed_notify(self):
        for data_changed_listener in self._data_changed_listeners:
            try:
                self.page.run_task(data_changed_listener)
            except:
                pass


    
    def language_changed_subscribe(self, callback):
        self._language_changed_listeners.append(callback)

    def language_changed_notify(self):
        for update_listener in self._language_changed_listeners:
            update_listener()


    def append_hot_restart_methods(self, callback):
        self.hot_restart_methods.append(callback)

    async def hot_restart_app(self):
        self.database   = Database()
        self.settings   = Settings()
        self.translator = Translator(self.settings.language)
        
        theme_mode = self.settings.theme_mode
        # Фактическая тема для инициализации цветов (dark/light)
        if self.settings.theme_mode == "system":
            theme_mode = self.page.platform_brightness.value if self.page.platform_brightness is not None else "light"
        self.colors     = AppColors(theme_mode, self.settings.color_theme)


        # Назначение цветовой темы приложения при горячей перезагрузке
        current_text_theme = self.page.theme.text_theme if self.page.theme is not None else None

        self.page.theme = ft.Theme(color_scheme=self.colors.light_color_scheme, text_theme=current_text_theme)
        self.page.dark_theme = ft.Theme(color_scheme=self.colors.dark_color_scheme, text_theme=current_text_theme)


        for restart_method in self.hot_restart_methods:
            if isinstance(restart_method, MethodType):
                restart_method()



    def change_user(self, id_user: int):
        self.settings.change_current_user(id_user)
        self.data_changed_notify()

    
    def change_current_language(self, language_code: str):
        self.settings.change_language(language_code)
        self.translator = Translator(language_code)

        self.language_changed_notify()
        self.page.run_task(self.hot_restart_app)

    
    def change_theme_mode(self, e):
        # Подгонка e под str
        theme_mode = e
        if isinstance(e, ft.ThemeMode):
            theme_mode = e.value
        self.settings.change_theme_mode(theme_mode)
        
        # Фактическая тема для инициализации цветов (dark/light)
        if theme_mode == "system":
            theme_mode = self.page.platform_brightness.value if self.page.platform_brightness is not None else "light"

        self.page.run_task(self.hot_restart_app)


    def change_color_theme(self, color_theme: str):
        if color_theme not in list(SupportedColorThemes.COLOR_THEMES.keys()):
            raise ValueError("Insupported color theme")
        
        self.settings.change_color_theme(color_theme)
        self.page.run_task(self.hot_restart_app)



    def change_trainer_mode(self, trainer_mode: bool):
        self.settings.change_trainer_mode(trainer_mode)
        self.page.run_task(self.hot_restart_app)