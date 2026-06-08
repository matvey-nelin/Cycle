import flet as ft
import datetime
from pathlib import Path

from AppState import AppState


class BackupOption(ft.Container):
    def __init__(self, app_state: AppState, path: dict) -> None:
        super().__init__()

        self.app_state  = app_state

        self.database   = self.app_state.database
        self.settings   = self.app_state.settings
        self.translator = self.app_state.translator
        self.colors     = self.app_state.colors


        # Обработчики событий
        self.on_hover = self._on_hover_


        # Инициализация данных и элементов бэкапа
        self.path = path


        icon = ft.Icons.FORMAT_LIST_BULLETED_ROUNDED
        if self.path.get("type", "") == ".db":
            icon = ft.Icons.STORAGE_ROUNDED
        elif self.path.get("type", "") == ".zip":
            icon = ft.Icons.FOLDER_ZIP_ROUNDED

        name        = self.path.get("name", "")
        create_time = self.path.get("ctime", "")
        size        = self.path.get("size", "")


        # Настройка отображения контейнера
        self.bgcolor = ft.Colors.SURFACE_CONTAINER_LOW

        self.border = ft.Border().all(
            width=2, 
            color=ft.Colors.OUTLINE
        )
        self.border_radius = 10


        self.alignment = ft.Alignment.CENTER

        
        self.animate = ft.Animation(
            duration=200,
            curve=ft.AnimationCurve.EASE_IN_CIRC
        )
        

        # Назначение данных для опции списка
        self.leading = ft.Icon(
            icon=icon,
            size=25,
            color=ft.Colors.TERTIARY
        )

        self.title = ft.Text(
            value=name,
            size=14,
            weight=ft.FontWeight.NORMAL,
            color=ft.Colors.ON_SURFACE
        )


        self.backup_age  = self.determine_backup_age_date_units(create_time)
        self.backup_size = self.determine_backup_size(size)


        self.subtitle = ft.Row(
            margin=ft.Margin.symmetric(horizontal=5),

            controls=
            [
                ft.Text(
                    value=self.backup_age,
                    size=12,
                    weight=ft.FontWeight.NORMAL,
                    color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                ),
                ft.Text(
                    value=self.backup_size,
                    size=12,
                    weight=ft.FontWeight.NORMAL,
                    color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                )
            ],

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )


        self.content = ft.ListTile(
            leading=self.leading,
            title=self.title,
            subtitle=self.subtitle
        )




    
    def determine_backup_age_date_units(self, create_backup_time: float | int | str):
        if isinstance(create_backup_time, str):
            return create_backup_time
        
        age_seconds = int(datetime.datetime.now().timestamp() - int(create_backup_time))

        if age_seconds   < 60:
            return f"{age_seconds} {self.translator.backup_option_labels["seconds"]}"
        elif age_seconds < (60 * 60):
            return f"{int(age_seconds / 60)} {self.translator.backup_option_labels["minuts"]}"
        elif age_seconds < (24 * 60 * 60):
            return f"{int(age_seconds / (60 * 60))} {self.translator.backup_option_labels["hours"]}"
        else:
            return f"{int(age_seconds / (24 * 60 * 60))} {self.translator.backup_option_labels["days"]}"
        


    def determine_backup_size(self, size_in_bytes: int):
        if isinstance(size_in_bytes, str):
            return size_in_bytes
        
        if size_in_bytes < 1024:
            return f"{size_in_bytes} B"
        elif size_in_bytes < (1024 ** 2):
            return f"{size_in_bytes / 1024:.2f} KB"
        else:
            return f"{size_in_bytes / (1024 ** 2):.2f} MB"
        

    

    def _on_hover_(self, e):
        self.bgcolor = ft.Colors.SECONDARY_CONTAINER if e.data else ft.Colors.SURFACE_CONTAINER_LOW
        self.update()