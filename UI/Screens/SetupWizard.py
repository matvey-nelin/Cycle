import flet as ft

from Languages import SupportedLanguages

from AppState import AppState
from Languages.Translator import Translator

from UI.Components.InvalidDataAlertDialog import InvalidDataAlertDialog

# Отдельный от приложения класс. Он не наследуется и работает самостоятельно. Вызывается только в первый запуск приложения
class SetupWizard:
    def __init__(self, page: ft.Page, navigate_callback, app_state: AppState) -> None:
        self.app_state  = app_state

        self.settings   = self.app_state.settings        
        self.database   = self.app_state.database
        self.translator = self.app_state.translator
        self.colors     = self.app_state.colors


        self.page = page
        self.page.bottom_appbar = None
        self.navigate = navigate_callback



        self.initial_data = {
            "language"          : self.settings.language,
            "user_name"         : "",
            "trainer_mode"      : self.settings.trainer_mode,
            "insert_agonists"   : True,
            "insert_exercises"  : True
        }

        self.screens = {
            0: self.language_screen,
            1: self.user_screen,
            2: self.initial_data_screen,
            3: self.finish_screen
        }

        self.current_step = 0

        
        self.__init_languages__()
        self.update_screen()


    def __init_languages__(self, e = None):
        # Смена языка при вызове функции через выбор из dropdown
        if e is not None:
            self.initial_data["language"] = e.control.value
            self.settings.language        = e.control.value
        
        # Ининицализация языковых настроек
        self.translator = Translator(self.settings.language)
        self.labels     = self.translator.setup_wizard_labels

        # Смена лейбла в dropdown
        if e is not None:
            self.language_dropdown.label = self.labels["language_screen"]["choose_language"]
            self.page.update()


    def __init_components__(self):
        """Метод для опеределения общих элементов экранов"""
        
        # Главный контейнер экранов
        self.main_container = ft.Container(
            expand=True,
            padding=50
        )

        # Создание общего прогресс-бара (в виде заполненных и полых точек)
        self.progress_bar_points = ft.Row(
            spacing=45,
            controls=[],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        for i in range(0, len(self.screens)):
            if i <= self.current_step:
                self.progress_bar_points.controls.insert(
                    i, ft.Icon(icon=ft.Icons.CIRCLE_ROUNDED, color=ft.Colors.GREY_600, size=15)
                )
            else:
                self.progress_bar_points.controls.insert(
                    i, ft.Icon(icon=ft.Icons.CIRCLE_OUTLINED, color=ft.Colors.GREY_600, size=15)
                )
        
        
        # Определение панели навигации
        self.step_buttons = ft.Row(
            expand=1,
            controls=
            [
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_ROUNDED,
                    icon_color=ft.Colors.GREY_800 if self.current_step == 0 else ft.Colors.PINK_700,
                    icon_size=30,
                    on_click=self.previous_screen,
                    disabled=(True if self.current_step == 0 else False)
                ),

                ft.IconButton(
                    icon=ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
                    icon_color=ft.Colors.GREEN_700,
                    icon_size=30,
                    on_click=self.next_screen
                )                
            ],
            align=ft.Alignment.BOTTOM_CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.END        
        )

        # Определение кнопки завершения настройки
        self.finish_button = ft.Row(
            expand=1,
            controls=
            [
                ft.Button(
                    content=self.labels["finish_screen"]["button_label"],
                    color=ft.Colors.TEAL_ACCENT_200,
                    bgcolor=ft.Colors.BLACK_87,
                    on_click=self.__save_initial_data__
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )


        
    def update_screen(self):
        self.page.clean()
        self.__init_components__()

        self.main_container.content = ft.Column(
            expand=True,
            controls=
            [
                self.progress_bar_points,
                self.screens[self.current_step](),
                self.step_buttons if (self.current_step != (len(self.screens) - 1 )) else self.finish_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER     
        )

        self.page.add(self.main_container)
        self.page.update()



    def language_screen(self):
        def change_app_theme(e):
            if  self.page.theme_mode in [ft.ThemeMode.LIGHT.value, ft.ThemeMode.LIGHT]:  # Переключение темы на темную
                self.page.theme_mode        = ft.ThemeMode.DARK
                self.theme_app_button.icon  = ft.Icons.DARK_MODE_ROUNDED
                self.settings.theme_mode    = ft.ThemeMode.DARK.value

            elif self.page.theme_mode in [ft.ThemeMode.DARK.value, ft.ThemeMode.DARK]: # Переключение темы на системную
                self.page.theme_mode        = ft.ThemeMode.SYSTEM
                self.theme_app_button.icon  = ft.Icons.SETTINGS_DISPLAY_ROUNDED
                self.settings.theme_mode    = ft.ThemeMode.SYSTEM.value
            
            elif self.page.theme_mode in [ft.ThemeMode.SYSTEM.value, ft.ThemeMode.SYSTEM]: # Переключение темы на светлую
                self.page.theme_mode        = ft.ThemeMode.LIGHT
                self.theme_app_button.icon  = ft.Icons.WB_SUNNY_ROUNDED
                self.settings.theme_mode    = ft.ThemeMode.LIGHT.value

            self.page.update()
            

        language_options = []
        for key, value in list(SupportedLanguages.LANGUAGES.items()):
            language_options.append(ft.DropdownOption(key, value))

        self.language_dropdown = ft.Dropdown(
            label=self.labels["language_screen"]["choose_language"],
            options=language_options,
            value=self.settings.language,
            text_style=(ft.TextStyle(
                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
            )),
            on_select=self.__init_languages__,
            align=ft.Alignment.CENTER
        )

        self.theme_app_button = ft.IconButton(
            icon=ft.Icons.SETTINGS_DISPLAY_ROUNDED,
            icon_size=25,
            on_click=change_app_theme
        )

        self.screen_content = ft.Row(
            expand=6,
            spacing=25,
            controls=
            [
                self.language_dropdown,
                self.theme_app_button
            ],
            align=ft.Alignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        return self.screen_content


    def user_screen(self):
        text_field_label = self.labels["user_screen"]["insert_username"]
        switch_label     = self.translator.settings_labels["trainer_mode"]

        def change_text(e):
            self.initial_data["user_name"]      = e.data

        def change_trainer_mode(e):
            self.initial_data["trainer_mode"]   = e.data

        self.screen_content = ft.Row(
            expand=6,
            controls=
            [
                ft.Column(
                    expand=True,
                    spacing=25,
                    controls=
                    [
                        ft.TextField(
                            value=self.initial_data["user_name"],
                            label=text_field_label,
                            text_style=(ft.TextStyle(
                                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
                            )),
                            on_change=change_text
                        ),
                        ft.Switch(
                            value=self.initial_data["trainer_mode"],
                            label=switch_label,
                            label_position=ft.LabelPosition.LEFT,
                            label_text_style=(ft.TextStyle(
                                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
                            )),
                            on_change=change_trainer_mode,
                            active_color=self.colors.LIGHT_PRIMARY if self.colors.theme == "light" else self.colors.DARK_PRIMARY,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        return self.screen_content


    def initial_data_screen(self):
        def switch_insertion(e):
            if e.control.label == self.labels["initial_data_screen"]["insert_agonists"]:
                self.initial_data["insert_agonists"] = e.data

            if e.control.label == self.labels["initial_data_screen"]["insert_exercises"]:
                self.initial_data["insert_exercises"] = e.data


        self.screen_content = ft.Row(
            expand=6,
            controls=
            [
                ft.Column(
                    expand=True,
                    spacing=25,
                    controls=
                    [
                        ft.Text(
                            value=self.labels["initial_data_screen"]["main_label"],
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND,
                            size=24
                        ),

                        ft.Switch(
                            value=self.initial_data["insert_agonists"],
                            label=self.labels["initial_data_screen"]["insert_agonists"],
                            label_position=ft.LabelPosition.LEFT,
                            label_text_style=(ft.TextStyle(
                                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
                            )),
                            on_change=switch_insertion,
                            data=self.initial_data["insert_agonists"],
                            active_color=self.colors.LIGHT_PRIMARY if self.colors.theme == "light" else self.colors.DARK_PRIMARY,
                        ),

                        ft.Switch(
                            value=self.initial_data["insert_exercises"],
                            label=self.labels["initial_data_screen"]["insert_exercises"],
                            label_position=ft.LabelPosition.LEFT,
                            label_text_style=(ft.TextStyle(
                                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
                            )),
                            on_change=switch_insertion,
                            data=self.initial_data["insert_exercises"],
                            active_color=self.colors.LIGHT_PRIMARY if self.colors.theme == "light" else self.colors.DARK_PRIMARY,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        return self.screen_content


    def finish_screen(self):
        self.screen_content = ft.Row(
            expand=6,
            controls=
            [
                ft.Column(
                    expand=True,
                    spacing=25,
                    controls=
                    [
                        ft.Text(
                            value=self.labels["finish_screen"]["main_label"],
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND,
                            size=24
                        ),
                        ft.Text(
                            value=self.labels["finish_screen"]["secondary_label"],
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND,
                            size=18
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        
        return self.screen_content



    def next_screen(self):
        if (self.current_step == 1) and (self.initial_data["user_name"].strip() == ""):
            self.page.show_dialog(InvalidDataAlertDialog(self.app_state))
            return

        self.current_step   += 1
        self.update_screen()
        

    def previous_screen(self):
        self.current_step   -= 1
        self.update_screen()



    def __save_initial_data__(self):
        # Сохранение настроек        
        self.settings.first_launch = False
        self.settings.language = self.initial_data["language"]
        self.settings.trainer_mode = self.initial_data["trainer_mode"]
        self.settings.unloading()

        # Вставка данных в БД
        self.database.insert_user(self.initial_data["user_name"])
        self.settings.change_current_user(id_user=1)

        self.database.__insertion_secondary_data__(
            insert_agonists=self.initial_data["insert_agonists"],
            insert_exercises=self.initial_data["insert_exercises"]
        )
        self.settings.determine_unchangeable_records(
            agonists=self.initial_data["insert_agonists"],
            exercises=self.initial_data["insert_exercises"]
        )

        self.app_state.data_changed_notify()

        self.navigate("dashboard_screen")
        self.app_state.change_current_language(self.settings.language)
