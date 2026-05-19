import flet as ft

from Languages.Translator import Translator
from UI.Layouts.BaseLayout import BaseLayout
from AppState import AppState


class DesktopLayout(BaseLayout):
    def __init__(self, page: ft.Page, app_state: AppState, translator: Translator, navigate_callback) -> None:
        super().__init__(page, translator, navigate_callback)

        self.app_state 	= app_state
        
        self.database 	= self.app_state.database
        self.settings	= self.app_state.settings
        self.translator = self.app_state.translator
        self.colors     = self.app_state.colors


        for config in self.config_destinations:
            self.destinations.append(
                ft.NavigationRailDestination(
                    padding=0,
                    icon=config["icon"],
                    selected_icon=config["selected_icon"],
                    label=ft.Text(self.translator.navigation_menu_labels[self.destination_labels[config["idx"]]]["label"]), 
                    tooltip=self.translator.navigation_menu_labels[self.destination_labels[config["idx"]]]["tooltip"]
                )
            )

        self.navigation_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            destinations=self.destinations,
            on_change=self.handle_navigation, 
            expand=False,
            height=float("inf"),
            indicator_color=self.colors.LIGHT_TERTIARY_CONTAINER if self.colors.theme == 'light' else self.colors.DARK_TERTIARY_CONTAINER,
            bgcolor=ft.Colors.SURFACE_BRIGHT
        )

        self.layout_container.content = ft.Row(
            margin=0,
            expand=True,
            spacing=0,
            controls=
            [
                self.navigation_rail,
                ft.VerticalDivider(2, color=ft.Colors.OUTLINE),
                self.content_container
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH
        )


    def _on_state_changes(self):
        self.__on_state_changes__(self.navigation_rail)
        