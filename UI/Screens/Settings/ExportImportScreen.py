import datetime
import shutil
import sqlite3
from pathlib import Path
import gc

import flet as ft
import os

from AppState import AppState
from UI.Screens.BaseView import BaseView
from Classes.BackupMaster import BackupMaster

from UI.Components.BackupOption import BackupOption




class ExportImportScreen(BaseView):
    def __init__(self, page: ft.Page, navigate_callback, app_state: AppState, previous_screen_name: str | None = None):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        self.labels = self.translator.export_import_screen

        self.app_state.resize_subscribe(self._on_resize_)


        self.file_picker    = ft.FilePicker()
        self.backup_master  = BackupMaster(self.app_state)


        self.current_mode = "db"

        self.database_backups_dir   = self.settings.db_backups_dir if self.settings.db_backups_dir != "" else "No data"
        self.databases_count        = 0
        self.total_databases_size   = 0
        self.last_db_time           = ""
        self.first_db_time          = ""
        self._update_db_file_info_()


        self.archive_backups_dir    = self.settings.archive_backups_dir if self.settings.archive_backups_dir != "" else "No data"
        self.archives_count         = 0
        self.total_archives_size    = 0
        self.last_archive_time      = ""
        self.first_archive_time     = ""
        self._update_archive_info_()




        self.database_toogle_button = ft.Segment(
            value="db",
            label=ft.Container(
                content=ft.Text(
                    self.labels["toggle_database_button_title"],
                    text_align=ft.TextAlign.CENTER
                ),

                alignment=ft.Alignment.CENTER
            )
        )        
        
        self.archive_toogle_button = ft.Segment(
            value="archive",
            label=ft.Container(
                content=ft.Text(
                    self.labels["toogle_archive_button_title"],
                    text_align=ft.TextAlign.CENTER
                ),

                alignment=ft.Alignment.CENTER
            )
        )


        self.toogle_button = ft.SegmentedButton(
            expand=True,
            margin=ft.Margin.symmetric(horizontal=25),
            width=200,

            segments=
            [
                self.database_toogle_button,
                self.archive_toogle_button
            ],

            selected=[self.current_mode],
            show_selected_icon=False,     
            
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                color=ft.Colors.ON_PRIMARY_CONTAINER,
                elevation=0,
            ),
            

            on_change=self._on_toogle_button_change_
        )

        if isinstance(self.appbar.content, ft.Row):
            self.appbar.content.controls = [
                self.open_previous_screen_button,
                self.toogle_button,
                ft.Container(
                    width=self.open_previous_screen_button.width
                ) # Заглушка для выравнивания
            ]
            self.appbar.content.alignment = ft.MainAxisAlignment.SPACE_BETWEEN




        self.current_db_information_block = ft.Container(
            expand=6, 

            margin=ft.Margin.only(top=25, bottom=0, right=25, left=25),
            padding=ft.Padding.symmetric(vertical=15, horizontal=15), 

            width=500,
            height=350,

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
                                        expand=2, 

                                        value=f"{self.labels["path_to_databases"]}",
                                        size=12,

                                        no_wrap=False,
                                        max_lines=2,

                                        color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                                    ),

                                    ft.Text(
                                        expand=2, 

                                        value=f"{self.database_backups_dir}",
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
                                        expand=2,
                                        value=f"{self.labels["databases_count"]}",
                                        size=12,
                                        color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                                    ),

                                    ft.Text(    
                                        expand=2,
                                        value=f"{self.databases_count}",
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
                                        expand=2,
                                        value=f"{self.labels["total_databases_size"]}",
                                        size=12,
                                        color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                                    ),

                                    ft.Text(    
                                        expand=2,
                                        value=f"{self.total_databases_size}",
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
                                        expand=2,
                                        value=f"{self.labels["last_database_time"]}",
                                        size=12,
                                        color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                                    ),

                                    ft.Text(
                                        expand=2,
                                        value=f"{self.last_db_time}",
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
                                        expand=2,
                                        value=f"{self.labels["first_database_time"]}",
                                        size=12,
                                        color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                                    ),

                                    ft.Text(
                                        expand=2,
                                        value=f"{self.first_db_time}",
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
                color=ft.Colors.with_opacity(0.5, ft.Colors.SHADOW),
                offset=ft.Offset(0, 4)
            ),

            alignment=ft.Alignment.CENTER
        )


        
        self.current_archive_information_block = ft.Container(
            expand=6, 

            margin=ft.Margin.only(top=25, bottom=0, right=25, left=25),
            padding=ft.Padding.symmetric(vertical=15, horizontal=15),

            width=500,
            height=350,

            content=ft.Row(
                expand=True,
                controls=
                [
                    ft.Icon(
                        icon=ft.Icons.FOLDER_ZIP_ROUNDED,
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
                                        expand=2, 

                                        value=f"{self.labels["path_to_archives"]}",
                                        size=12,

                                        no_wrap=False,
                                        max_lines=2,

                                        color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                                    ),

                                    ft.Text(
                                        expand=2, 

                                        value=f"{self.archive_backups_dir}",
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
                                        expand=2,
                                        value=f"{self.labels["archives_count"]}",
                                        size=12,
                                        color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                                    ),

                                    ft.Text(    
                                        expand=2,
                                        value=f"{self.archives_count}",
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
                                        expand=2,
                                        value=f"{self.labels["total_archives_size"]}",
                                        size=12,
                                        color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                                    ),

                                    ft.Text(
                                        expand=2,
                                        value=f"{self.total_archives_size}",
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
                                        expand=2,
                                        value=f"{self.labels["last_archive_time"]}",
                                        size=12,
                                        color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                                    ),

                                    ft.Text(
                                        expand=2,
                                        value=f"{self.last_archive_time}",
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
                                        expand=2,
                                        value=f"{self.labels["first_archive_time"]}",
                                        size=12,
                                        color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)
                                    ),

                                    ft.Text(
                                        expand=2,
                                        value=f"{self.first_archive_time}",
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
                color=ft.Colors.with_opacity(0.5, ft.Colors.SHADOW),
                offset=ft.Offset(0, 4)
            ),

            alignment=ft.Alignment.CENTER
        )




        self.import_button = ft.Container(
            expand=1,

            content=ft.Row(
                expand=True,
                controls=
                [
                    ft.Icon(
                        icon=ft.Icons.FILE_DOWNLOAD_OUTLINED,
                        color=ft.Colors.ON_PRIMARY_CONTAINER
                    ),
                    
                    ft.Text(
                        value=f"{self.labels["import_button"]}",
                        size=12,
                        color=ft.Colors.ON_PRIMARY_CONTAINER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),

            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=10,

            alignment=ft.Alignment.CENTER,

            on_click=lambda: self.page.run_task(self._handle_import_),
            on_hover=self._on_import_button_hover_,

            animate=ft.Animation(
                duration=300,
                curve=ft.AnimationCurve.FAST_OUT_SLOWIN
            )
        )


        self.export_button = ft.Container(
            expand=1,

            content=ft.Row(
                expand=True,
                controls=
                [
                    ft.Icon(
                        icon=ft.Icons.FILE_UPLOAD_OUTLINED,
                        color=ft.Colors.ON_SECONDARY_CONTAINER
                    ),
                    
                    ft.Text(
                        value=f"{self.labels["export_button"]}",
                        size=12,
                        color=ft.Colors.ON_SECONDARY_CONTAINER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),

            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            border_radius=10,

            alignment=ft.Alignment.CENTER,
            
            on_click=lambda: self.page.run_task(self._handle_export_),
            on_hover=self._on_export_button_hover_,

            animate=ft.Animation(
                duration=300,
                curve=ft.AnimationCurve.FAST_OUT_SLOWIN
            )
        )


        self.data_actions = ft.Container(
            expand=1,
            margin=ft.Margin.symmetric(horizontal=0, vertical=10),

            content=None
        )



        self.backup_option_list = ft.ListView(
            expand=True,
            margin=ft.Margin.symmetric(horizontal=25),
            width=500,
            
            spacing=10,

            controls=[],

            scroll=ft.ScrollMode.AUTO
        )

        self._init_backup_option_list_controls_()



        self.main_container.content = ft.Column(
            expand=True,

            controls=
            [
                self.current_db_information_block,
                self.data_actions,
                self.backup_option_list
            ],

            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            scroll=ft.ScrollMode.AUTO
        )

        
        self._on_resize_(None)





    def _init_backup_option_list_controls_(self):
        try:
            options = []

            if self.current_mode == "db":
                backup_options = self.backup_master.get_backup_files(self.settings.db_backups_dir, "db")

            elif self.current_mode == "archive":
                backup_options = self.backup_master.get_backup_files(self.settings.archive_backups_dir, "zip")
            
            for backup_path in backup_options:
                options.append(
                    BackupOption(
                        app_state=  self.app_state,
                        path=       backup_path
                    )
                )

            if not options:
                options.append(
                    ft.Text(
                        margin=ft.Margin.all(50),

                        value=self.labels["no_backups"],
                        size=14,
                        weight=ft.FontWeight.BOLD,

                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER
                    )
                )

            self.backup_option_list.controls = options

        except Exception as _ex:
            self._show_snackbar_(f"{self.labels["error_load_backups"]}\nError: {_ex}", is_error=True)


    def _show_snackbar_(self, message: str, is_error: bool = False):
        self.page.show_dialog(
            ft.SnackBar(
                expand=True,
                close_icon_color=ft.Colors.PRIMARY,

                content=ft.Container(
                    expand=True,
                    margin=ft.Margin.symmetric(vertical=15, horizontal=25),
                    # height=50,

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



    def _on_toogle_button_change_(self, e):
        self.current_mode = e.data[0]

        self._init_backup_option_list_controls_()

        
        self.main_container.content = ft.Column(
            expand=True,

            controls=
            [
                self.current_db_information_block if self.current_mode == "db" else self.current_archive_information_block,
                self.data_actions,
                self.backup_option_list
            ],

            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            scroll=ft.ScrollMode.AUTO
        )

        self.page.update()





    def _update_db_file_info_(self):
        try:
            database_backups = self.backup_master.get_backup_files(self.settings.db_backups_dir, "db")

            self.databases_count        = len(database_backups)
            self.total_databases_size   = sum([database.stat().st_size for database in database_backups])


            if self.total_databases_size < 1024:
                self.total_databases_size = f"{self.total_databases_size} B"
            elif self.total_databases_size < (1024 ** 2):
                self.total_databases_size = f"{self.total_databases_size / 1024:.2f} KB"
            else:
                self.total_databases_size = f"{self.total_databases_size / (1024 ** 2):.2f} MB"


            
            if database_backups != []:
                self.last_db_time   = datetime.datetime.fromtimestamp(database_backups[0].stat().st_mtime).strftime("%d.%m.%Y, %H:%M:%S")
                self.first_db_time  = datetime.datetime.fromtimestamp(database_backups[-1].stat().st_mtime).strftime("%d.%m.%Y, %H:%M:%S")


        except Exception as _ex:
            self.databases_count        = "-"
            self.total_databases_size   = "-"   
            self.last_db_time           = "No data"
            self.first_db_time          = "No data"



    def _update_archive_info_(self):
        try:
            archives_backups = self.backup_master.get_backup_files(self.settings.archive_backups_dir, "zip")

            self.archives_count       = len(archives_backups)
            self.total_archives_size  = sum([archive.stat().st_size for archive in archives_backups])

            if self.total_archives_size < 1024:
                self.total_archives_size = f"{self.total_archives_size} B"
            elif self.total_archives_size < (1024 ** 2):
                self.total_archives_size = f"{self.total_archives_size / 1024:.2f} KB"
            else:
                self.total_archives_size = f"{self.total_archives_size / (1024 ** 2):.2f} MB"


            if archives_backups != []:
                self.last_archive_time  = datetime.datetime.fromtimestamp(archives_backups[0].stat().st_mtime).strftime("%d.%m.%Y, %H:%M:%S")
                self.first_archive_time = datetime.datetime.fromtimestamp(archives_backups[-1].stat().st_mtime).strftime("%d.%m.%Y, %H:%M:%S")

        except Exception as _ex:
            self.archives_count         = 0
            self.total_archives_size    = 0
            self.last_archive_time      = "No data"
            self.first_archive_time     = "No data"





    async def _handle_export_(self):
        try:
            if self.current_mode == "db":
                result = await self.backup_master.export_database(
                    file_picker=self.file_picker, 
                    dialog_title=self.labels["export_dialog_title"]
                )

            elif self.current_mode == "archive":
                result = await self.backup_master.export_archive(
                    file_picker=self.file_picker, 
                    dialog_title=self.labels["export_dialog_title"]
                )

            if result:
                self._show_snackbar_(self.labels["export_succes"])

        except Exception as _ex:
            self._show_snackbar_(f"{self.labels["export_error"]}\nError: {_ex}", is_error=True)
            



    async def _handle_import_(self):
        try:
            if self.current_mode == "db":
                result = await self.backup_master.import_database(
                    file_picker=self.file_picker,
                    dialog_title=self.labels["import_dialog_title"]
                )

            elif self.current_mode == "archive":
                result = await self.backup_master.import_archive(
                    file_picker=self.file_picker,
                    dialog_title=self.labels["import_dialog_title"]
                )
            
            if result:
                self._show_snackbar_(self.labels["import_succes"])
                
        except Exception as _ex:
            self._show_snackbar_(f"{self.labels["import_error"]}\nError: {_ex}", is_error=True)
        



    def _on_resize_(self, e):
        if self.app_state.is_mobile:
            self.data_actions.content = ft.Column(
                expand=True,

                height=90,
                width=500,

                margin=ft.Margin.symmetric(horizontal=25),

                controls=
                [
                    self.import_button,
                    self.export_button
                ],

                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        else:
            self.data_actions.content = ft.Row(
                expand=True,

                height=40,
                width=500,

                margin=ft.Margin.symmetric(horizontal=25),

                controls=
                [
                    self.import_button,
                    self.export_button
                ],

                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        
        try:
            self.data_actions.update()
            self.page.update()
        except RuntimeError as ex:
            pass



    def _on_export_button_hover_(self, e):
        self.export_button.bgcolor = ft.Colors.PRIMARY if e.data else ft.Colors.PRIMARY_CONTAINER
        self.export_button.update()


    def _on_import_button_hover_(self, e):
        self.import_button.bgcolor = ft.Colors.SECONDARY if e.data else ft.Colors.SECONDARY_CONTAINER
        self.import_button.update()