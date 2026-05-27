import flet as ft

from AppState import AppState
from UI.Screens.BaseView import BaseView

from UI.Components.RecordsList import RecordsList



class UsersScreen(BaseView):
    def __init__(self, page: ft.Page, navigate_callback, app_state: AppState, previous_screen_name: str | None = None):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)
        
        self.labels = self.translator.users_screen_labels

        self.add_record_button = ft.IconButton(
            icon=ft.Icons.ADD_ROUNDED,
            on_click=self.open_record_screen
        )

        self.appbar = ft.Container(
            margin=ft.Margin.symmetric(horizontal=5),
            content=ft.Row(
                controls=
                [
                    self.open_previous_screen_button,
                    self.add_record_button

                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )


                
        self.app_state.data_changed_subscribe(self._init_data_)
        self.app_state.language_changed_subscribe(self._init_data_)
        self._init_data_()

        self.content = ft.Column(
            spacing=0,
            controls=[
                self.appbar,
                self.main_container
            ], 
            expand=True, 
            scroll=None,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )


    def _init_data_(self):
        records_list = RecordsList(self.page, self.app_state, "users", self.navigate)

        self.main_container.alignment = ft.Alignment.TOP_CENTER
        self.main_container.content = records_list 
        
        if records_list.controls == []:
            self.main_container.content = ft.Text(
                value=self.labels["no_data"],
                size=16,
                color=ft.Colors.ON_SURFACE
            )
            self.main_container.alignment = ft.Alignment.CENTER

        try:
            self.main_container.update()
        except:
            pass


    def open_record_screen(self):
        self.navigate(
            screen_name=            "user_management_screen",
			is_temporary_screen=	True,
            page= 				    self.page, 
            app_state=		        self.app_state,
            navigate_callback= 	    self.navigate,
            previous_screen_name=   "users_screen",
            id=                     0
        )