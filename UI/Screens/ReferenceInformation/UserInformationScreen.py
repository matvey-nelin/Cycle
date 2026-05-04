import flet as ft

from AppState import AppState
from UI.Screens.BaseView import BaseView

from UI.Components.NavigationOption import NavigationOption



class UserInformationScreen(BaseView):
    def __init__(self, page: ft.Page, navigate_callback, app_state: AppState, previous_screen_name: str | None = None):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)
        
        self.app_state.language_changed_subscribe(self._init_components_)
        self._init_components_()
        
    
    def _init_components_(self):
        self.labels = self.translator.user_information_screen_labels

        self.divider = ft.Container(
            content=ft.Divider(),
            padding=5
        )

        self.main_container.alignment = ft.Alignment.TOP_CENTER
        self.main_container.content = ft.Column(
            controls=
            [
                NavigationOption(self.app_state.colors, self.labels["users"], "users_screen", self.navigate),
                NavigationOption(self.app_state.colors, self.labels["user_statuses"], "user_statuses_screen", self.navigate),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )
