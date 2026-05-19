import flet as ft

from AppState import AppState
from UI.Screens.BaseView import BaseView

from UI.Components.SetsList import SetsList
from UI.Components.InvalidDataAlertDialog import InvalidDataAlertDialog


class WorkoutTemplateScreen(BaseView):
    def __init__(
        self, 
        id_workout_template: int, 
        page: ft.Page, 
        navigate_callback, 
        app_state: AppState, 
        previous_screen_name: str = "workout_template_menu"
    ):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        self.id = id_workout_template
        self.labels = self.translator.workout_template_screen_labels

        self.title = ""
        self.chosen_workout_type_title     = ""
        self.chosen_hypertrophy_type_title = ""

        self.id_workout_type = 1

        if self.id != 0:
            result = self.database.get_workout_template_info(self.id)
            if isinstance(result, Exception):
                raise result
            
            self.slug = str(result[0][0])
            self.title = self.translator.workout_templates[str(result[0][0])]
            self.chosen_workout_type_title = self.translator.workout_types[str(result[0][1])]
            self.chosen_hypertrophy_type_title = self.translator.hypertrophy_types[str(result[0][2])]


        # Поля имени шаблона
        def on_title_field_change(e):
            self.title = str(e.data)

        self.title_field = ft.Container(    
            content=ft.TextField(
                expand=True,
                margin=ft.Margin.only(bottom=0, left=10, right=10, top=0),
                
                value=self.title, 
                text_style=ft.TextStyle(
                    size=16,
                    color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
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

        
        # Данные тренировки (тип тренировки и гипетрофии)
        self.__init_workout_dropdown__()
        self.__init_hypertrophy_dropdown__()

        self.info_template = ft.Row(
            expand=True,
            spacing=5,
            height=30, 
            margin=ft.Margin.only(left=10, right=10, bottom=5),
            controls=
            [
                self.dropdown_workout_types,
                self.dropdown_hypertrophy_types
            ],

            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )



        self.sets_container = SetsList(
            screen=self, 
            is_template=True, 
            is_planned=True, 
            id=self.id
        )
             


        self.save_button = ft.Container(
            height=40,
            width=300,

            gradient=self.colors.Gradients.BUTTON_PRIMARY,
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

        self.actions_template = ft.Row(
            expand=True,
            controls=
            [
                self.save_button
            ],
            
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.actions_menu = ft.Column(
            expand=1,
            margin=ft.Margin.only(left=0, top=10, right=0, bottom=5),

            controls=[self.actions_template],

            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )


        self.main_container.content = ft.Column(
            expand=True,
            spacing=0,
            controls=
            [
                self.title_field,
                self.info_template,
                self.sets_container,
                self.actions_menu
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
            



    def _save_button_on_hover_(self, e):
        self.save_button.gradient = self.colors.Gradients.BUTTON_HOVER if e.data == True else self.colors.Gradients.BUTTON_PRIMARY
        self.save_button.update()


    def _save_button_on_click_(self):
        if not self.title.strip():
            self.page.show_dialog(InvalidDataAlertDialog(self.app_state, self.labels["save_error"]))
            return
        
        if self.id != 0:
            slug = self.translator.get_slug(self.title, "workout_templates", self.slug)
            save_template_info = f"""
                UPDATE 
                    workout_templates
                SET 
                    id_workout_type = {self.id_workout_type},
                    id_hypertrophy_type = {self.id_hypertrophy_type},
                    title = '{self.title}',
                    slug  = '{slug}'
                WHERE 
                    id_workout_template = {self.id}
            """
            self.translator.add_slug(self.title, slug, "workout_templates", self.slug)
        else:
            slug = self.translator.get_slug(self.title, "workout_templates", "")
            save_template_info = f"""
                INSERT INTO 
                    workout_templates (id_workout_type, id_hypertrophy_type, title, slug)
                VALUES 
                    ({self.id_workout_type}, {self.id_hypertrophy_type}, '{self.title}', '{slug}')
            """
            self.translator.add_slug(self.title, slug, "workout_templates", "")


        
        self.slug = slug
        self.database.__execute_request__(save_template_info)

        if self.id == 0:
            self.id = self.database.get_workout_templates()[-1][0] # Последний добавленый шаблон
        
        # Сбор и компановка данных перед их заменой
        try:
            inserting_exercise_list = []            
            for exercise_set in self.sets_container.sets:
                if (exercise_set.exercise_dropdown.value == "") or (exercise_set.count_text_field.value in [0, None]):
                    continue

                inserting_string = (self.id, int(exercise_set.exercise_dropdown.value))
                for i in range(int(exercise_set.count_text_field.value)):
                    inserting_exercise_list.append(inserting_string)

        except ValueError:
            raise ValueError(self.labels["save_error"])
        
        
        self.database.delete_workout_template(self.id, False)


        insert_request = """
            INSERT INTO workout_template_composition(id_workout_template, id_exercise)
            VALUES (?, ?)
        """
        self.database.__insert_request__(insert_request, inserting_exercise_list)

       
        self.sets_container = SetsList(
            screen=self, 
            is_template=True, 
            is_planned=True, 
            id=self.id
        )
        self.main_container.content = ft.Column(
            expand=True,
            spacing=0,
            controls= 
            [
                self.title_field,
                self.info_template,
                self.sets_container,
                self.actions_menu
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.main_container.update()
        self.app_state.data_changed_notify()

        self.return_previous_screen()


    

    def __init_workout_dropdown__(self):
        def on_workout_dropdown_select(e):
            self.sets_container.__init_sets_dropdown_menu__(e)
            self.id_workout_type = self.sets_container.id_workout_type
        
        # Тип тренировки в шаблоне
        result = self.database.get_workout_types()
        if isinstance(result, Exception):
            raise result
        
        self.workout_types = []
        for workout_type in result:
            id_workout_type     = workout_type[0]
            title_workout_type  = self.translator.workout_types[workout_type[1]]

            # Сбор первого id типа тренировки
            if self.id == 0 and self.workout_types == []:
                self.id_workout_type = id_workout_type

            self.workout_types.append(
                ft.DropdownOption(
                    key=id_workout_type,
                    text=title_workout_type
                )
            )

            if title_workout_type == self.chosen_workout_type_title:
                self.id_workout_type = workout_type[0]

            
        self.dropdown_workout_types = ft.Dropdown(
            expand=1,
            content_padding=ft.Padding.only(left=10, top=0, right=10, bottom=15),

            value=str(self.id_workout_type),
            options=self.workout_types,

            text_align=ft.TextAlign.START,
            text_size=12,
            border=ft.InputBorder.OUTLINE,
            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND,

            on_select=on_workout_dropdown_select
        )


    def __init_hypertrophy_dropdown__(self):
        def on_hypertrophy_dropdown_select(e):
            self.id_hypertrophy_type = int(e.data)

        # Тип гипертрофии в шаблоне
        result = self.database.get_hypertrophy_types()
        if isinstance(result, Exception):
            raise result
        
        self.hypertrophy_types = []
        for hypertrophy_type in result:
            id_hypertrophy_type = hypertrophy_type[0]
            title_hypertrophy_type = self.translator.hypertrophy_types[hypertrophy_type[1]]

            # Сбор первого id типа гипертрофии
            if self.id == 0 and self.hypertrophy_types == []:
                self.id_hypertrophy_type = id_hypertrophy_type

            self.hypertrophy_types.append(
                ft.DropdownOption(
                    key=id_hypertrophy_type,
                    text=title_hypertrophy_type
                )
            )

            if title_hypertrophy_type == self.chosen_hypertrophy_type_title:
                self.id_hypertrophy_type = hypertrophy_type[0]
                
            
            
        self.dropdown_hypertrophy_types = ft.Dropdown(
            expand=1,
            content_padding=ft.Padding.only(left=10, top=0, right=10, bottom=15),

            value=str(self.id_hypertrophy_type),
            options=self.hypertrophy_types,

            text_align=ft.TextAlign.START,
            text_size=12,
            border=ft.InputBorder.OUTLINE,
            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND,

            on_select=on_hypertrophy_dropdown_select
        )