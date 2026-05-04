import flet as ft

from AppState import AppState
from UI.Screens.BaseView import BaseView




class ActiveUserStatusesScreen(BaseView):
    def __init__(self, page: ft.Page, navigate_callback, app_state: AppState, previous_screen_name: str | None = None):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        # Назначение статусов, которые будут участвовать в сортировке пользователей в меню на главном экране
