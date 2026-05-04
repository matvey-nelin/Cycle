import flet as ft

from AppState import AppState
from UI.Screens.BaseView import BaseView

from UI.Components.InvalidDataAlertDialog import InvalidDataAlertDialog



class UniversalRecordManagementScreen(BaseView):
    def __init__(
        self, 
        page: ft.Page, 
        navigate_callback, 
        app_state: AppState, 
        previous_screen_name: str | None,
        entity: str,
        id: int,
        field_max_length: int
    ):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)
        
        self.entity = entity
        self.id     = id
        self.title  = ""

        self.labels = self.translator.universal_record_management_screen_labels


        self.entities = {
            "user_statuses" : {
                "table" : "user_status",
                "labels": "user_statuses",
                "data"  : lambda id: self.database.get_user_statuses(id),
                "all_data"  : lambda: self.database.get_user_statuses()
            },
            "workout_statuses" : {
                "table" : "workout_status",
                "labels": "workout_statuses",
                "data"  : lambda id: self.database.get_workout_statuses(id),
                "all_data"  : lambda: self.database.get_workout_statuses()
            },
            "workout_types" : {
                "table" : "workout_type",
                "labels": "workout_types",
                "data"  : lambda id: self.database.get_workout_types(id),
                "all_data"  : lambda: self.database.get_workout_types()
            },
            "hypertrophy_types" : {
                "table" : "hypertrophy_type",
                "labels": "hypertrophy_types",
                "data"  : lambda id: self.database.get_hypertrophy_types(id),
                "all_data"  : lambda: self.database.get_hypertrophy_types()
            }
        }

        if self.entity not in list(self.entities.keys()):
            raise ValueError("Incorrect value of 'entity'")
        
        
        self.entity_labels = self.entities[self.entity]["labels"]
        

        # Поля имени записи
        def on_title_field_change(e):
            self.title = str(e.data)

        self.title_field = ft.Container(    
            content= ft.TextField(
                expand=True,
                margin=ft.Margin.only(bottom=0, left=25, right=25, top=0),

                text_align=ft.TextAlign.CENTER,
                helper=self.labels["title_helper_text"],
                
                value=self.title,  
                text_style=ft.TextStyle(
                    size=14,
                    color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                ),
                border=ft.InputBorder.UNDERLINE,
                border_color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE,
                focused_border_color=self.colors.LIGHT_PRIMARY if self.colors.theme == "light" else self.colors.DARK_PRIMARY,

                max_lines=3,
                max_length=field_max_length,
                keyboard_type=ft.KeyboardType.TEXT,

                on_change=on_title_field_change
            )
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
                self.title_field,
                self.save_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )


        self._init_data_()



    def _init_data_(self):
        if self.id == 0:
            return


        record = self.entities[self.entity]["data"](self.id)[0]
        self.slug = record[1]
        self.title = self.translator.data_labels[self.entity_labels][self.slug]

        if isinstance(self.title_field.content, ft.TextField):
            self.title_field.content.value = self.title


        

    def _save_button_on_hover_(self, e):
        self.save_button.gradient = self.colors.Gradients.BUTTON_SUCCESS_HOVER if e.data == True else self.colors.Gradients.BUTTON_SUCCESS
        self.save_button.update()


    def _save_button_on_click_(self):
        if self.title.strip() == "":
            self.page.show_dialog(InvalidDataAlertDialog(self.app_state))
            return

        if self.id == 0:
            new_slug = self.translator.get_slug(self.title, self.entity_labels)
            self.translator.add_slug(self.title, new_slug, self.entity_labels)

            request = f"""
                INSERT INTO 
                    {self.entities[self.entity]["table"]} (title, slug)
                VALUES  
                    ('{self.title}', '{new_slug}')
            """

            self.database.__execute_request__(request)

            # Новый id последней созданной записи
            self.id = self.entities[self.entity]["all_data"]()[-1][0]

        else:
            new_slug = self.translator.get_slug(self.title, self.entity_labels, self.slug)
            self.translator.add_slug(self.title, new_slug, self.entity_labels, self.slug)

            request = f"""
                UPDATE 
                    {self.entities[self.entity]["table"]}
                SET  
                    title = '{self.title}',
                    slug  = '{new_slug}'
                WHERE 
                    slug = '{self.slug}'
            """

            self.database.__execute_request__(request)

            # Новый slug записи
            self.slug = new_slug


        self.app_state.data_changed_notify()
        self.return_previous_screen()