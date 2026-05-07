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
            {"icon": ft.Icons.FITNESS_CENTER_ROUNDED,       "selected_icon": ft.Icons.FITNESS_CENTER_ROUNDED,   "idx": 0},
            {"icon": ft.Icons.CALENDAR_MONTH_OUTLINED,      "selected_icon": ft.Icons.CALENDAR_MONTH,           "idx": 1},
            {"icon": ft.Icons.MY_LIBRARY_BOOKS_OUTLINED,    "selected_icon": ft.Icons.MY_LIBRARY_BOOKS_ROUNDED, "idx": 2},
            {"icon": ft.Icons.SETTINGS_OUTLINED,            "selected_icon": ft.Icons.SETTINGS,                 "idx": 3}
        ]

        self.destinations = []


    def change_screen(self, screen: BaseView):
        self.content_container.content = screen.content
        self.content_container.update()



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