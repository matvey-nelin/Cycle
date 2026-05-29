import flet as ft

from AppState import AppState
from UI.Screens.BaseView import BaseView

from UI.Components.InvalidDataAlertDialog import InvalidDataAlertDialog



class ExerciseManagementScreen(BaseView):
    def __init__(
        self, 
        page: ft.Page, 
        navigate_callback, 
        app_state: AppState, 
        previous_screen_name: str | None,
        id: int
    ):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        self.id                 = id
        self.title              = ""
        self.slug               = ""
        self.chosen_id_agonists     = []
        self.chosen_title_agonists  = []

        
        self._init_data_()

        
        def on_agonists_expansion_tile_change(e):
            if e.control.value:
                self.chosen_id_agonists.append(e.control.data["id"])
                self.chosen_title_agonists.append(e.control.label)
            else:
                self.chosen_id_agonists.remove(e.control.data["id"])
                self.chosen_title_agonists.remove(e.control.label)

            self.agonists_expansion_tile.title = ", ".join(self.chosen_title_agonists)

        
        self.all_agonists: list[ft.Control] = [ 
            ft.Checkbox(
                data={"id": agonist[0]},
                label=self.translator.agonists.get(agonist[1], agonist[1]),
                label_style=ft.TextStyle(
                    size=14,
                    color=ft.Colors.ON_SURFACE
                ),
                
                value=(agonist[0] in self.chosen_id_agonists),
                
                active_color=self.colors.LIGHT_SECONDARY_CONTAINER if self.colors.theme == "light" else self.colors.DARK_SECONDARY_CONTAINER,
                check_color=self.colors.LIGHT_ON_SECONDARY_CONTAINER if self.colors.theme == "light" else self.colors.DARK_ON_SECONDARY_CONTAINER,

                on_change=on_agonists_expansion_tile_change
            )

            for agonist in self.database.get_agonists()               
        ]

        self.labels = self.translator.exercise_management_screen_labels 


        # Поле имени пользователя
        def on_title_field_change(e):
            self.title = str(e.data)
        
        self.title_field = ft.Container(    
            content= ft.TextField(
                expand=True,
                margin=ft.Margin.only(bottom=0, left=25, right=25, top=0),

                disabled=bool(self.id in self.settings.unchangeable_exercises),

                text_align=ft.TextAlign.CENTER,
                helper=self.labels["title_helper_text"],
                
                value=self.title,  
                text_style=ft.TextStyle(
                    size=16,
                    color=ft.Colors.ON_SURFACE
                ),
                border=ft.InputBorder.UNDERLINE,
                border_color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE,
                focused_border_color=self.colors.LIGHT_PRIMARY if self.colors.theme == "light" else self.colors.DARK_PRIMARY,

                max_lines=5,
                max_length=100,
                keyboard_type=ft.KeyboardType.TEXT,

                on_change=on_title_field_change
            )
        )



        self.agonists_expansion_tile = ft.ExpansionTile(
            margin=ft.Margin.only(left=25, right=25),

            title=ft.Text(
                value=", ".join(self.chosen_title_agonists),
                size=14
            ),
            subtitle=ft.Text(
                value=self.labels["agonists_helper_text"],
                size=12
            ),
            controls=
            [
                ft.Column(
                    height=400,
                    controls=self.all_agonists,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO
                )
            ],
             
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
                    margin=ft.Margin.only(top=25),
                    spacing=10,
                    controls=
                    [
                        self.title_field,
                        self.agonists_expansion_tile
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                self.save_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )




    def _init_data_(self):
        if self.id == 0:
            return

        record = self.database.get_exercises(id_exercise=self.id)[0]

        self.slug        = record[1]
        self.title       = self.translator.exercises.get(self.slug, self.slug)


        for agonist in self.database.get_agonists(self.id):
            self.chosen_id_agonists.append(agonist[0])
            self.chosen_title_agonists.append(self.translator.agonists.get(agonist[1], agonist[1]))
        
        

        

    def _save_button_on_hover_(self, e):
        self.save_button.gradient = self.colors.Gradients.BUTTON_SUCCESS_HOVER if e.data == True else self.colors.Gradients.BUTTON_SUCCESS
        self.save_button.update()


    def _save_button_on_click_(self):
        if self.title.strip() == "":
            self.page.show_dialog(InvalidDataAlertDialog(self.app_state))
            return

        if self.id == 0:
            new_slug = self.translator.get_slug(self.title, "exercises")
            self.translator.add_slug(self.title, new_slug, "exercises")

            request = f"""
                INSERT INTO 
                    exercises (title, slug)
                VALUES  
                    ('{self.title.strip()}', '{new_slug}')
            """

            self.database.__execute_request__(request)

            # Новый id последней созданной записи
            self.id = self.database.get_exercises()[-1][0]

        else:
            if self.id not in self.settings.unchangeable_exercises:
                new_slug = self.translator.get_slug(self.title, "exercises", self.slug)
                self.translator.add_slug(self.title, new_slug, "exercises", self.slug)

                request = f"""
                    UPDATE 
                        exercises
                    SET
                        title = '{self.title.strip()}',
                        slug = '{new_slug}'
                    WHERE 
                        id_exercise = {self.id}
                """

                self.database.__execute_request__(request)

        self.slug = new_slug if (self.id not in self.settings.unchangeable_exercises) else self.slug


        self.database.delete_agonist_exercises(self.id)

        new_agonist_exercises = [(id_agonist, self.id) for id_agonist in self.chosen_id_agonists]
        request = """
            INSERT INTO 
                agonist_exercises(id_agonist, id_exercise)
            VALUES
                (?, ?)
        """
        self.database.__insert_request__(request, new_agonist_exercises)

        self.app_state.data_changed_notify()
        self.return_previous_screen()