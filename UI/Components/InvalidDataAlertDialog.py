import flet as ft

from AppState import AppState


class InvalidDataAlertDialog(ft.AlertDialog):
    def __init__(self, app_state: AppState, title: str | None = None) -> None:
        super().__init__()

        self.app_state = app_state


        self.settings   = self.app_state.settings
        self.database   = self.app_state.database
        self.translator = self.app_state.translator
        self.colors     = self.app_state.colors

        self.labels = self.translator.invalid_data_alert_dialog_labels

        self.expand = False
        self.title_text_style = ft.TextStyle(
            size=16,
            color=self.colors.LIGHT_ON_ERROR_CONTAINER if self.colors.theme == "light" else self.colors.DARK_ON_ERROR_CONTAINER
        )
        self.bgcolor = self.colors.LIGHT_ERROR_CONTAINER if self.colors.theme == "light" else self.colors.DARK_ERROR_CONTAINER

        self.title  = title if title is not None else self.labels["check_data"]