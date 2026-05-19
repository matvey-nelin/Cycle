import flet as ft

from AppState import AppState


class ManagerDialog(ft.AlertDialog):
    def __init__(self, app_state: AppState, id: int, title: str | ft.Text, essence: str, delete_function) -> None:
        super().__init__()

        self.app_state = app_state

        self.delete_function = delete_function

        self.settings   = self.app_state.settings
        self.database   = self.app_state.database
        self.translator = self.app_state.translator
        self.colors     = self.app_state.colors

        self.labels = self.translator.manager_dialog_labels

        self.id = id

        self.title = ft.Text(
                value=title,
                size=18,
                color=ft.Colors.ON_SURFACE
            ) if isinstance(title, str) \
            else title
        self.title.text_align = ft.TextAlign.CENTER

        self.essence = essence

        self.expand = False
        self.alignment = ft.Alignment.CENTER

        
        if self.essence not in [*list(app_state.translator.data_labels.keys()), "users"]:
            return
    
        
        self.delete_button = ft.IconButton(
            icon=ft.Icons.DELETE_ROUNDED,
            icon_size=20,
            icon_color=ft.Colors.ON_SURFACE,

            align=ft.Alignment.CENTER,
            on_click=self.on_delete_button_click
        )

        self.actions_menu = ft.Row(
            expand=False,
            controls=
            [
                self.delete_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.actions = [self.delete_button]



    def on_delete_button_click(self):
        self.delete_function()

        self.title = ft.Row(
            expand=False,
            controls=
            [
                ft.Text(
                    self.labels["delete_succes"],
                    size=14,
                    align=ft.Alignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.actions = []

        