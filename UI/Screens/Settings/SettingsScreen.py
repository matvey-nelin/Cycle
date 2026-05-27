import flet as ft

import utils

from Languages import SupportedLanguages 

from AppState import AppState
from UI.Screens.BaseView import BaseView

from UI.Components.NavigationOption import NavigationOption



class SettingsScreen(BaseView):
    def __init__(self, page: ft.Page, navigate_callback, app_state: AppState, previous_screen_name: str | None = None):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        self.app_state.data_changed_subscribe(self._init_data_)
        self.labels = self.translator.settings_screen_labels

        self._init_components_()
        self._init_data_()


    def _init_components_(self):
        self.divider = ft.Container(
            content=ft.Divider(),
            padding=5
        )

        self.app_info_block = ft.Row(
            expand=True,
            margin=ft.Margin.symmetric(vertical=50, horizontal=25),
            controls=
            [
                ft.Column(
                    spacing=0,
                    controls=
                    [
                        ft.Image(
                            margin=ft.Margin.only(bottom=10), 
                            src=str(utils.resource_path(r"assets/icons/android-chrome-192x192_without_background.png")),
                            error_content=ft.Icon(
                                icon=ft.Icons.CHANGE_CIRCLE_OUTLINED,
                                size=75,
                                color=self.colors.LIGHT_PRIMARY if self.colors.theme == 'light' else self.colors.DARK_PRIMARY
                            )
                        ),
                        ft.Text(
                            value="Cycle",
                            size=16,
                            color=ft.Colors.ON_SURFACE
                        ),
                        ft.Text(
                            value="by Matvey Nelin",
                            size=12,
                            color=ft.Colors.ON_SURFACE
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )


        # Выбор языка
        self.language_dropdown = ft.Dropdown(
            expand=True,
            height=75,

            options=[],
            helper_text=self.labels["language"],
            text_style=ft.TextStyle(
                size=16, 
                color=ft.Colors.ON_SURFACE
            ),

            value=self.settings.language,
            on_select=self.language_dropdown_on_select,
            align=ft.Alignment.CENTER
        )

        language_options = []
        for key, value in list(SupportedLanguages.LANGUAGES.items()):
            language_options.append(
                ft.DropdownOption(
                    key=key, 
                    text=value
                )
            )
        self.language_dropdown.options = language_options

        # Выбор темы приложения (светлая, темная, системная)
        self.theme_mode_icon = {
            "system": ft.Icons.SETTINGS_DISPLAY_ROUNDED,
            "dark"  : ft.Icons.DARK_MODE_ROUNDED,
            "light" : ft.Icons.WB_SUNNY_ROUNDED
        }
        self.theme_app_button = ft.IconButton(
            icon=self.theme_mode_icon[self.settings.theme_mode],
            icon_size=30,
            on_click=self.theme_app_on_click,
            alignment=ft.Alignment.CENTER
        )

        self.language_and_theme_mode_row = ft.Row(
            expand=True,
            margin=ft.Margin.symmetric(vertical=5, horizontal=15),
            controls=
            [
                self.language_dropdown,
                ft.Container(
                    height=75,
                    content=self.theme_app_button,
                    alignment=ft.Alignment.TOP_CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )


        # Выбор режима тренера (идентичный NavigationOption дизайн)
        self.trainer_mode_switch = ft.Container(
            padding=15,
            content=ft.Row(
                controls=
                [
                    ft.Text(
                        expand=True,
                        value=self.labels["trainer_mode_switch"],
                        size=16,
                        color=ft.Colors.ON_SURFACE,
                        no_wrap=False,
                        max_lines=3,
                    ),
                    ft.Switch(
                        value=self.settings.trainer_mode,
                        active_color=self.colors.LIGHT_PRIMARY if self.colors.theme == "light" else self.colors.DARK_PRIMARY,
                        on_change=self.trainer_mode_switch_on_change
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),

            border=ft.Border().all(
                width=2, 
                color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE
            ),
            border_radius=12,

            alignment=ft.Alignment.CENTER
        )



        # Определяю контейнер со всем содержимым с шириной не более 600px
        self.main_container.width   = 600 # ограничение максимальной ширины
        # self.main_container.padding = ft.Padding.symmetric(horizontal=50)
        self.main_container.content = ft.Column(
            margin=ft.Margin.only(top=15, left=50, right=50),

            controls=
            [
                self.app_info_block,

                self.language_and_theme_mode_row,
                self.trainer_mode_switch,

                self.divider,

                # NavigationOption(self.app_state.colors, self.labels["active_user_statuses"], "active_user_statuses_screen", self.navigate),
                NavigationOption(self.app_state.colors, self.labels["app_color_themes"], "app_color_themes_screen", self.navigate),

                # self.divider,

                # NavigationOption(self.app_state.colors, self.labels["mesocycle_menu"], "mesocycle_menu", self.navigate),
                # NavigationOption(self.app_state.colors, self.labels["macrocycle_menu"], "macrocycle_menu", self.navigate)
            ],
            scroll=ft.ScrollMode.AUTO
        )


        



    def _init_data_(self):
        pass



    def theme_app_on_click(self):
        if  self.page.theme_mode in [ft.ThemeMode.LIGHT.value, ft.ThemeMode.LIGHT]:  # Переключение темы на темную
            self.page.theme_mode = ft.ThemeMode.DARK
            self.app_state.change_theme_mode(ft.ThemeMode.DARK)
            self.colors = self.app_state.colors

        elif self.page.theme_mode in [ft.ThemeMode.DARK.value, ft.ThemeMode.DARK]: # Переключение темы на системную
            self.page.theme_mode = ft.ThemeMode.SYSTEM
            self.app_state.change_theme_mode(ft.ThemeMode.SYSTEM)
            self.colors = self.app_state.colors
        
        elif self.page.theme_mode in [ft.ThemeMode.SYSTEM.value, ft.ThemeMode.SYSTEM]: # Переключение темы на светлую
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.app_state.change_theme_mode(ft.ThemeMode.LIGHT)     
            self.colors = self.app_state.colors

        self._init_components_()

        self.page.update()
    


    def language_dropdown_on_select(self, e):
        self.app_state.change_current_language(e.control.value)



    def trainer_mode_switch_on_change(self, e):
        self.app_state.change_trainer_mode(e.data)