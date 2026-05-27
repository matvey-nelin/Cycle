import flet as ft

from AppState import AppState
from UI.Screens.BaseView import BaseView

from UI.Components.InvalidDataAlertDialog import InvalidDataAlertDialog



class UserManagementScreen(BaseView):
    def __init__(
        self, 
        page: ft.Page, 
        navigate_callback, 
        app_state: AppState, 
        previous_screen_name: str | None,
        id: int
    ):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        self.id             = id
        self.id_user_status = None
        self.username       = ""
        self.phone          = ""
        
        self.all_statuses = [ 
            ft.DropdownOption(
                key=status[0],
                text=self.translator.user_statuses[status[1]]
            )

            for status in self.database.get_user_statuses()               
        ]

        self.labels = self.translator.user_management_screen_labels


        # Поле имени пользователя
        def on_username_field_change(e):
            self.username = str(e.data)
        
        self.username_field = ft.Container(    
            content= ft.TextField(
                expand=True,
                margin=ft.Margin.only(bottom=0, left=25, right=25, top=0),

                text_align=ft.TextAlign.CENTER, 
                helper=self.labels["username_field_helper_text"],
                
                value=self.username, 
                text_style=ft.TextStyle(
                    size=14,
                    color=ft.Colors.ON_SURFACE
                ),
                border=ft.InputBorder.UNDERLINE,
                border_color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE,
                focused_border_color=self.colors.LIGHT_PRIMARY if self.colors.theme == "light" else self.colors.DARK_PRIMARY,

                max_lines=5,
                max_length=100,
                keyboard_type=ft.KeyboardType.TEXT,

                on_change=on_username_field_change
            )
        )

        # Поле телефона пользователя
        def on_phone_field_change(e):
            self.phone = str(e.data)

        self.phone_field = ft.Container(    
            content= ft.TextField(
                expand=True,
                margin=ft.Margin.only(bottom=0, left=25, right=25, top=0),

                text_align=ft.TextAlign.CENTER,
                helper=self.labels["phone_field_helper_text"],
                
                value=self.phone,  
                text_style=ft.TextStyle(
                    size=14,
                    color=ft.Colors.ON_SURFACE
                ),
                
                border=ft.InputBorder.UNDERLINE,
                border_color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE,
                focused_border_color=self.colors.LIGHT_PRIMARY if self.colors.theme == "light" else self.colors.DARK_PRIMARY,

                max_lines=3,
                max_length=50,
                keyboard_type=ft.KeyboardType.PHONE,

                on_change=on_phone_field_change
            )
        )

        def on_status_dropdown_change(e):
            self.id_user_status = int(e.data)

        self.status_dropdown = ft.Dropdown(
            expand=False,
            content_padding=ft.Padding.only(left=10, top=0, right=10, bottom=15),

            value=self.id_user_status,
            options=self.all_statuses,

            helper_text=self.labels["status_dropdown_helper_text"],

            text_align=ft.TextAlign.CENTER,
            text_size=14,
            border=ft.InputBorder.OUTLINE,
            color=ft.Colors.ON_SURFACE,

            on_select=on_status_dropdown_change
        )
        

        self.save_button = ft.Container(
            height=40,
            width=300,

            gradient=self.colors.Gradients.BUTTON_SUCCESS,
            content=ft.Text(
                value=self.labels["save_button"],
                color=self.colors.LIGHT_ON_PRIMARY if self.colors.theme == "light" else self.colors.DARK_ON_PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),

            border=ft.Border().all(
                width=1,
                color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE
            ),
            border_radius=15,

            alignment=ft.Alignment.CENTER,

            on_click=self._save_button_on_click_,
            on_hover=self._save_button_on_hover_
        )

        self.main_container.content = ft.Column(
            expand=True,
            controls=
            [ 
                ft.Column(
                    expand=True,
                    spacing=0,
                    controls=
                    [
                        self.username_field,
                        self.phone_field,
                        self.status_dropdown
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                self.save_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self._init_data_()



    def _init_data_(self):
        if self.id == 0:
            return

        record = self.database.get_users(self.id)[0]

        self.id_user_status = record[1]
        self.username       = record[2]
        self.phone          = record[3]

        if isinstance(self.username_field.content, ft.TextField):
            self.username_field.content.value = self.username

        if isinstance(self.phone_field.content, ft.TextField):
            self.phone_field.content.value = self.phone

        self.status_dropdown.value = self.id_user_status
        

        

    def _save_button_on_hover_(self, e):
        self.save_button.gradient = self.colors.Gradients.BUTTON_SUCCESS_HOVER if e.data == True else self.colors.Gradients.BUTTON_SUCCESS
        self.save_button.update()


    def _save_button_on_click_(self):
        if (self.id_user_status is None) or (self.username.strip() == ""):
            self.page.show_dialog(InvalidDataAlertDialog(self.app_state))
            return

        if self.id == 0:
            request = f"""
                INSERT INTO 
                    users (id_user_status, username, phone)
                VALUES  
                    ({self.id_user_status}, '{self.username}', '{self.phone.strip()}')
            """

            self.database.__execute_request__(request)

            # Новый id последней созданной записи
            self.id = self.database.get_users()[-1][0]

        else:
            request = f"""
                UPDATE 
                    users
                SET
                    id_user_status = {self.id_user_status},
                    username = '{self.username}',
                    phone  = '{self.phone.strip()}'
                WHERE 
                    id_user = {self.id}
            """

            self.database.__execute_request__(request)

        # Статус "Активен"
        if (self.id_user_status != 1) and (self.id == self.settings.current_user):
            self.app_state.change_user(self.database.get_users(id_user_status=1)[0][0])
            

        self.app_state.data_changed_notify()
        self.return_previous_screen()