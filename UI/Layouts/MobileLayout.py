import flet as ft

from Languages.Translator import Translator
from UI.Layouts.BaseLayout import BaseLayout
from AppState import AppState


class MobileLayout(BaseLayout):
    def __init__(self, page: ft.Page, app_state: AppState, translator: Translator, navigate_callback) -> None:
        super().__init__(page, translator, navigate_callback)

        self.app_state 	= app_state
        
        self.database 	= self.app_state.database
        self.settings	= self.app_state.settings
        self.translator = self.app_state.translator
        self.colors     = self.app_state.colors

        self.navigation_destintinations = {
            0: "dashboard_screen",
            1: "planning_screen",
            2: "statistics_screen",
            3: "reference_information_screen",
            4: "settings_screen"
        }


        # Определение навигационного меню внизу страницы для телефона
        for config in self.config_destinations:
            self.destinations.append(
                ft.IconButton(
                    icon=config["icon"],
                    selected_icon=config["selected_icon"],
                    selected_icon_color=ft.Colors.TERTIARY_CONTAINER,
                    selected=(config["idx"] == 0),
                    data=config["idx"],
                    on_click=self._bottom_bar_click_ 
                )
            )
        
        self.bottom_appbar = ft.BottomAppBar(
            height=75,
            content=ft.Row(
                controls=self.destinations,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            bgcolor=None
        )

        self.layout_container.content = ft.Column(
            expand=True,
            spacing=0,
            margin=ft.Margin.symmetric(vertical=15),
            controls=
            [
                self.content_container
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        )


    def _bottom_bar_click_(self, e):
        for menu_option in self.destinations:
            if isinstance(menu_option, ft.IconButton):
                if (menu_option.data == e.control.data):
                    menu_option.selected    = True
                else:
                    menu_option.selected    = False

        self.bottom_appbar.update()
        self.navigate(self.navigation_destintinations[e.control.data])