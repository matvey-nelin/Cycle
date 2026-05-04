import flet as ft

from AppState import AppState
from UI.Screens.BaseView import BaseView

from UI.Components.NavigationOption import NavigationOption



class PlanningScreen(BaseView):
    def __init__(self, page: ft.Page, navigate_callback, app_state: AppState, previous_screen_name: str | None = None):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        self.labels = self.translator.planning_screen_labels

        self.divider = ft.Container(
            content=ft.Divider(),
            padding=5
        )

        self.content = ft.Column(
            margin=ft.Margin.only(top=15),
            controls=
            [
                NavigationOption(self.app_state.colors, self.labels["workout_template_menu"], "workout_template_menu", self.navigate),
                NavigationOption(self.app_state.colors, self.labels["microcycle_template_menu"], "microcycle_template_menu", self.navigate),

                self.divider,

                NavigationOption(self.app_state.colors, self.labels["mesocycle_menu"], "mesocycle_menu", self.navigate),
                NavigationOption(self.app_state.colors, self.labels["macrocycle_menu"], "macrocycle_menu", self.navigate)
            ],
            scroll=ft.ScrollMode.AUTO
        )