import flet as ft

from Languages.Translator import Translator
from UI.Screens.BaseView import BaseView


class BaseLayout():
    def __init__(self, page: ft.Page, translator: Translator, navigate_callback) -> None:
        self.translator = translator
        self.navigate   = navigate_callback

        self.page = page

        self.layout_container   = ft.Container( # Контейнер всего экрана
            expand=True
        ) 
        self.content_container  = ft.Container( # Контейнер содержимого окна
            expand=True,
            margin=ft.Margin.symmetric(vertical=15, horizontal=15)
        ) 

        self.destination_labels  = list(self.translator.navigation_menu_labels.keys())
        self.config_destinations = \
        [
            {"icon": ft.Icon(ft.Icons.FITNESS_CENTER_ROUNDED, size=25),           "selected_icon": ft.Icon(ft.Icons.FITNESS_CENTER_ROUNDED, size=25),   "idx": 0},
            {"icon": ft.Icon(ft.Icons.CALENDAR_MONTH_OUTLINED, size=25),          "selected_icon": ft.Icon(ft.Icons.CALENDAR_MONTH, size=25),           "idx": 1},
            {"icon": ft.Icon(ft.Icons.INSERT_CHART_OUTLINED_ROUNDED, size=25),    "selected_icon": ft.Icon(ft.Icons.INSERT_CHART_ROUNDED, size=25),     "idx": 2},
            {"icon": ft.Icon(ft.Icons.MY_LIBRARY_BOOKS_OUTLINED, size=25),        "selected_icon": ft.Icon(ft.Icons.MY_LIBRARY_BOOKS_ROUNDED, size=25), "idx": 3},
            {"icon": ft.Icon(ft.Icons.SETTINGS_OUTLINED, size=25),                "selected_icon": ft.Icon(ft.Icons.SETTINGS, size=25),                 "idx": 4}
        ]

        self.destinations = []


    def change_screen(self, screen: BaseView):
        self.content_container.content = screen.content



    def handle_navigation(self, e):
        self.navigate(self.destination_labels[e.control.selected_index])
    


    def __on_state_changes__(self, navigation_menu: ft.NavigationRail):
        icons_labels = {}
        for index, value in enumerate(self.destination_labels):
            icons_labels[index] = value

        for i in range(len(navigation_menu.destinations)):
            bar_destination = self.translator.navigation_menu_labels[icons_labels[i]]

            navigation_menu.destinations[i].label    = bar_destination["label"]
            navigation_menu.destinations[i].tooltip  = bar_destination["tooltip"]

        navigation_menu.update()