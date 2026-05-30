import datetime
import shutil
import sqlite3
from pathlib import Path
import gc

import flet as ft
import os

from AppState import AppState
from UI.Screens.BaseView import BaseView



class ExportImportScreen(BaseView):
    def __init__(self, page: ft.Page, navigate_callback, app_state: AppState, previous_screen_name: str | None = None):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        self.file_picker = ft.FilePicker()

        self.labels = self.translator.export_import_screen


        self.app_state.resize_subscribe(self._on_resize_)

        self.database_path      = self.database.db_path
        self.database_size      = 0
        self.last_backup_time   = datetime.datetime.fromtimestamp(self.settings.last_backup).strftime("%d.%m.%Y, %H:%M:%S") \
            if self.settings.last_backup != 0 else self.labels["no_backups"]
        self.update_db_file_info()



        self.current_db_information_block = ft.Container(
            margin=ft.Margin.only(top=50, bottom=25, right=25, left=25),
            padding=ft.Padding.symmetric(vertical=15, horizontal=15),

            width=500,
            height=200,

            content=ft.Row(
                expand=True,
                controls=
                [
                    ft.Icon(
                        icon=ft.Icons.STORAGE_ROUNDED,
                        size=50,
                        color=ft.Colors.ON_PRIMARY
                    ),

                    ft.Column(
                        expand=True,
                        controls=
                        [
                            ft.Row(
                                controls=
                                [
                                    ft.Text(
                                        expand=1, 

                                        value=f"{self.labels["path_to_database"]}",
                                        size=12,

                                        no_wrap=False,
                                        max_lines=2,

                                        color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                                    ),

                                    ft.Text(
                                        expand=2, 

                                        value=f"{self.database_path}",
                                        size=12,
                                        
                                        no_wrap=False,
                                        max_lines=5,

                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.with_opacity(1.0, ft.Colors.ON_SURFACE)
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.START
                            ),
                            
                            ft.Row(
                                controls=
                                [
                                    ft.Text(    
                                        expand=1,
                                        value=f"{self.labels["size_database"]}",
                                        size=12,
                                        color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                                    ),

                                    ft.Text(    
                                        expand=2,
                                        value=f"{self.database_size}",
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.with_opacity(1.0, ft.Colors.ON_SURFACE)
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.START
                            ),
                            
                            ft.Row(
                                controls=
                                [
                                    ft.Text(    
                                        expand=1,
                                        value=f"{self.labels["last_backup_time"]}",
                                        size=12,
                                        color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                                    ),

                                    ft.Text(
                                        expand=2,
                                        value=f"{self.last_backup_time}",
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.with_opacity(1.0, ft.Colors.ON_SURFACE)
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.START
                            )
                        ],
                        
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.START
                    )
                ],

                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),

            gradient=self.colors.Gradients.CARD_ACTIVE,
            border_radius=10,

            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12, 
                color=ft.Colors.SHADOW,
                offset=ft.Offset(0, 4)
            ),

            alignment=ft.Alignment.CENTER
        )




        self.import_database_button = ft.ElevatedButton(
            width=200,

            icon=ft.Icons.FILE_DOWNLOAD_OUTLINED,
            icon_color=ft.Colors.ON_PRIMARY_CONTAINER,

            bgcolor=ft.Colors.SECONDARY_CONTAINER,

            content=ft.Text(
                value=f"{self.labels["import_button"]}",
                size=12,
                color=ft.Colors.ON_PRIMARY_CONTAINER
            ),

            on_click=lambda: self.page.run_task(self._handle_import_)
        )


        self.export_database_button = ft.ElevatedButton(
            width=200,

            icon=ft.Icons.FILE_UPLOAD_OUTLINED,
            icon_color=ft.Colors.ON_SECONDARY_CONTAINER,

            bgcolor=ft.Colors.PRIMARY_CONTAINER,

            content=ft.Text(
                value=f"{self.labels["export_button"]}",
                size=12,
                color=ft.Colors.ON_SECONDARY_CONTAINER
            ),

            on_click=lambda: self.page.run_task(self._handle_export_)
        )


        self.database_actions = ft.Container(
            expand=False,
            margin=ft.Margin.symmetric(horizontal=25),

            content=None
        )





        self.main_container.content = ft.Column(
            expand=True,

            controls=
            [
                self.current_db_information_block,
                self.database_actions
            ],

            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            scroll=ft.ScrollMode.AUTO
        )

        
        self._on_resize_(None)


    def update_db_file_info(self):
        try:
            self.last_backup_time = datetime.datetime.fromtimestamp(self.settings.last_backup).strftime("%d.%m.%Y, %H:%M:%S") \
                if self.settings.last_backup != 0 else self.labels["no_backups"]

            size_in_bytes = os.path.getsize(self.database.db_path)

            if size_in_bytes < 1024:
                self.database_size = f"{size_in_bytes} B"
            elif size_in_bytes < (1024 ** 2):
                self.database_size = f"{size_in_bytes / 1024:.2f} KB"
            else:
                self.database_size = f"{size_in_bytes / (1024 ** 2):.2f} MB"

        except Exception as _ex:
            self.database_path = "File read error"
            self.database_size = "-"


    def _show_snackbar_(self, message: str, is_error: bool = False):
        self.page.show_dialog(
            ft.SnackBar(
                expand=True,
                close_icon_color=ft.Colors.PRIMARY,

                content=ft.Container(
                    expand=True,
                    margin=ft.Margin.symmetric(vertical=15, horizontal=25),
                    height=50,

                    content=ft.Text(
                        expand=True,
                        value=message,

                        size=14,
                        weight=ft.FontWeight.NORMAL,
                        max_lines=10,

                        color=ft.Colors.ON_TERTIARY if not is_error else ft.Colors.ON_ERROR,

                        text_align=ft.TextAlign.CENTER
                    ),
                    
                    gradient=self.colors.Gradients.STATUS_SUCCESS if not is_error else self.colors.Gradients.STATUS_ERROR,
                    border_radius=10,

                    alignment=ft.Alignment.CENTER
                ),

                bgcolor=ft.Colors.TRANSPARENT
            )
        )



    async def _handle_export_(self):
        export_time = datetime.datetime.now()
        file_name   = f"CycleDatabase_backup_from_{export_time.strftime('%d_%m_%Y_%H_%M_%S')}.db"
        db_bytes = self.database._perform_export_()

        self.saved_file_path = await self.file_picker.save_file(
            dialog_title=self.labels["export_dialog_title"],
            file_name=file_name,
            initial_directory=self.settings.backups_dir,
            src_bytes=db_bytes
        )

        if not self.saved_file_path:
            return
        

        self.saved_file_path = Path(self.saved_file_path)
        self.destination_dir = self.saved_file_path.parent

        is_desktop = self.page.platform.value in ("windows", "macos", "linux") if self.page.platform is not None else False

        try:
            # Перемещение файла резервной копии в специальную папку
            # выполняется только на платформах где это возможно ("windows", "macos", "linux")
            if is_desktop: 
                if self.destination_dir.name.lower() != self.app_state.backups_dir_name.lower():
                    self.destination_dir = self.destination_dir / self.app_state.backups_dir_name

                self.destination_dir.mkdir(parents=True, exist_ok=True)

                if not self.destination_dir.is_dir():
                    raise NotADirectoryError(f"Expected a folder, but found a file along the way: {self.destination_dir}")

                self.destination_file_path = self.destination_dir / file_name
                shutil.move(str(self.saved_file_path), str(self.destination_file_path))


            # Далее страндартное поведение для всех ОС
            self.settings.update_last_backup_time(export_time.timestamp())
            self.settings.change_backups_dir(self.destination_dir)

            self.page.run_task(self.app_state.hot_restart_app)

            self._show_snackbar_(self.labels["export_succes"])

        except Exception as _ex:
            self._show_snackbar_(f"{self.labels["export_error"]}\nError: {_ex}", is_error=True)



    async def _handle_import_(self):
        self.imported_file_path = await self.file_picker.pick_files(
            dialog_title=self.labels["import_dialog_title"],
            initial_directory=self.settings.backups_dir,
            allowed_extensions=["db", "sqlite"],
            allow_multiple=False
        )
        
        if (not self.imported_file_path) or (self.imported_file_path[0].path is None):
            return
        
        self.imported_file_path = Path(self.imported_file_path[0].path)

        try:
            self._validate_sqlite_file_(self.imported_file_path)
            
            gc.collect()

            shutil.copy2(self.imported_file_path, self.database.db_path)
            self.page.run_task(self.app_state.hot_restart_app)

            self._show_snackbar_(self.labels["import_succes"])


        except Exception as _ex:
            self._show_snackbar_(f"{self.labels["import_error"]}\nError: {_ex}", is_error=True)
            
        


    def _on_resize_(self, e):
        if self.app_state.is_mobile:
            self.database_actions.content = ft.Column(
                expand=True,
                margin=ft.Margin.symmetric(horizontal=25),

                controls=
                [
                    self.import_database_button,
                    self.export_database_button
                ],

                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        else:
            self.database_actions.content = ft.Row(
                expand=True,
                margin=ft.Margin.symmetric(horizontal=25),

                controls=
                [
                    self.import_database_button,
                    self.export_database_button
                ],

                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        
        try:
            self.database_actions.update()
            self.page.update()
        except RuntimeError as ex:
            pass



    def _validate_sqlite_file_(self, path: str | Path):
        try:
            with sqlite3.connect(path, check_same_thread=False, timeout=10) as conn:
                cur = conn.cursor()
                cur.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1;")

        except sqlite3.DatabaseError:
            raise ValueError("The selected file is corrupted or is not a SQLite database.")