import flet as ft

from AppState import AppState
from UI.Screens.BaseView import BaseView

from UI.Components.NavigationOption import NavigationOption



class ReferenceInformationScreen(BaseView):
    def __init__(self, page: ft.Page, navigate_callback, app_state: AppState, previous_screen_name: str | None = None):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)
        
        self.app_state.language_changed_subscribe(self._init_components_)
        self._init_components_()
        
    
    def _init_components_(self):
        self.labels = self.translator.reference_information_screen_labels

        self.divider = ft.Container(
            content=ft.Divider(),
            padding=5
        )

        self.content = ft.Column(
            margin=ft.Margin.only(top=15),
            controls=
            [
                NavigationOption(self.app_state.colors, self.labels["user_information"], "user_information_screen", self.navigate),

                self.divider,

                NavigationOption(self.app_state.colors, self.labels["workout_statuses"], "workout_statuses_screen", self.navigate),
                NavigationOption(self.app_state.colors, self.labels["workout_types"], "workout_types_screen", self.navigate),
                NavigationOption(self.app_state.colors, self.labels["hypertrophy_types"], "hypertrophy_types_screen", self.navigate),

                self.divider,

                NavigationOption(self.app_state.colors, self.labels["exercises"], "exercises_screen", self.navigate),
                NavigationOption(self.app_state.colors, self.labels["agonists"], "agonists_screen", self.navigate)
            ],
            scroll=ft.ScrollMode.AUTO
        )