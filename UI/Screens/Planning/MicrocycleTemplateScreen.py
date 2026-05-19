import flet as ft

from AppState import AppState
from UI.Components.TemplateCard import TemplateCard
from UI.Screens.BaseView import BaseView

from UI.Components.TemplateContainer import TemplateContainer
from UI.Components.InvalidDataAlertDialog import InvalidDataAlertDialog


class MicrocycleTemplateScreen(BaseView):
    def __init__(self, id_microcycle_template: int, page: ft.Page, navigate_callback, app_state: AppState):
        super().__init__(page, navigate_callback, app_state, "microcycle_template_menu")


        self.id     = id_microcycle_template
        self.title = ""

        self.labels = self.translator.microcycle_template_screen_labels

        self.update_function = self._fill_workout_template_cards_list_


        # Поля имени шаблона
        def on_title_field_change(e):
            self.title = str(e.data)

        self.title_field = ft.TextField(
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

        self.title_field_container = ft.Container(    
            content=self.title_field
        )


        # Контейнер шаблонов
        self.template_container = TemplateContainer(self)


        # Кнопка добавления нового шаблона тренировки
        self.add_workout_template_button = ft.Container(
            margin=10,
            gradient=self.colors.Gradients.BUTTON_SUCCESS,
            shape=ft.BoxShape.CIRCLE,
            content=ft.IconButton(
                icon=ft.Icons.ADD_ROUNDED,
                icon_size=25,
                icon_color=self.colors.LIGHT_ON_TERTIARY if self.colors.theme == "light" else self.colors.DARK_ON_TERTIARY,

                on_click=self._add_workout_template_button_on_click_,
                on_hover=self._add_workout_template_button_on_hover_
            ),
            alignment=ft.Alignment.CENTER
        )

        self.template_container.templates.controls = [self.add_workout_template_button]


        # Меню действий с шаблоном микроцикла
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

        self.actions_menu = ft.Row(
            expand=True,
            margin=ft.Margin.symmetric(vertical=5, horizontal=10),
            controls=
            [
                self.save_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )


        # Определение списка шаблонов
        self._init_data_(self.id)
        

        self.main_container.content = ft.Column(
            expand=True,
            spacing=0,
            controls=
            [
                self.title_field,
                self.template_container,
                self.actions_menu
            ]
        )
        


    

    def _init_data_(self, id_microcycle_template: int):
        # Переопределение данных элементов страницы
        if id_microcycle_template == 0:
            self.id = 0
            self.title = ""
            self.title_field.value = self.title
            
            self.workout_templates_list_info = []
            self._fill_workout_template_cards_list_()
            return
        
        # Подписка на обновление, с поддержанием единственной актуальной функции в списке
        if id_microcycle_template != self.id:
            try:
                self.app_state._data_changed_listeners.remove(self.update_function)
            except ValueError:
                pass

            self.id = id_microcycle_template
            self.update_function = self._fill_workout_template_cards_list_
            self.app_state.data_changed_subscribe(self.update_function)   
        
        
        # Получение данных о шаблоне микроцикла
        self.workout_templates_list_info = []

        self.result = self.database.get_microcycle_template_info(self.id)

        self.slug = str(self.result[0][1])
        self.title = self.translator.microcycle_templates[self.slug]
        self.title_field.value = self.title


        # Определение списка данных шаблонов тренировок
        for workout_template_info in self.result:
            workout_template_info = workout_template_info[2:]
            
            workout_template_id    = int(workout_template_info[0])
            workout_template_title = self.translator.workout_templates[workout_template_info[1]]

            self.workout_templates_list_info.append([workout_template_id, workout_template_title])

        self._fill_workout_template_cards_list_()


    
    def _fill_workout_template_cards_list_(self):
        new_controls = []

        # Определение списка карточек шаблонов тренировок
        for template_id, template_title in self.workout_templates_list_info:
            # Определение списка упражнений шаблона
            new_controls.append(self._create_template_card_(template_id, template_title))
        new_controls.append(self.add_workout_template_button)

        self.template_container.templates.controls = new_controls
        try:
            self.template_container.templates.update()
        except RuntimeError:
            pass



    def _add_workout_template_button_on_click_(self):
        """
        Добавляет новую карточку шаблона тренировки в конец списка
        """
        def add_workout_template(id: int):
            result  = self.database.get_workout_template_info(id)
            title   = self.translator.workout_templates[result[0][0]]

            self.workout_templates_list_info.append([id, title])
            self._fill_workout_template_cards_list_()

            self.navigate("microcycle_template_screen")
            self.template_container.templates.update()

        
        self.navigate(
            screen_name=            "choosable_workout_template_menu",
            is_temporary_screen=    True,
            page=                   self.page, 
            navigate_callback=      self.navigate, 
            app_state=              self.app_state,
            selection_function=     lambda id: add_workout_template(id)
        )


    def _add_workout_template_button_on_hover_(self, e):
        self.add_workout_template_button.gradient = self.colors.Gradients.BUTTON_SUCCESS_HOVER if e.data == True else self.colors.Gradients.BUTTON_SUCCESS
        self.add_workout_template_button.update()



    def _save_button_on_hover_(self, e):
        self.save_button.gradient = self.colors.Gradients.BUTTON_HOVER if e.data == True else self.colors.Gradients.BUTTON_PRIMARY
        self.save_button.update()


    def _save_button_on_click_(self):
        if not self.title.strip():
            self.page.show_dialog(InvalidDataAlertDialog(self.app_state, self.labels["save_error"]))
            return
            
        if self.id != 0:
            old_slug = self.slug
            slug = self.translator.get_slug(self.title, "microcycle_templates", old_slug)
            self.translator.add_slug(self.title, slug, "microcycle_templates", old_slug)

            save_template_info = f"""
                UPDATE 
                    microcycle_templates
                SET
                    title   = '{self.title}',
                    slug    = '{slug}'
                WHERE 
                    id_microcycle_template = {self.id}
            """
        else:
            old_slug = ""
            slug = self.translator.get_slug(self.title, "microcycle_templates", old_slug)
            self.translator.add_slug(self.title, slug, "microcycle_templates", old_slug)

            save_template_info = f"""
                INSERT INTO 
                    microcycle_templates (title, slug)
                VALUES
                    ('{self.title}', '{slug}')
            """

        self.database.__execute_request__(save_template_info)
        self.slug = slug

        if self.id == 0:
            self.id = self.database.get_microcycle_templates()[-1][0] # Последний добавленый шаблон
        
        # Сбор и компановка данных перед их заменой
        inserting_templates_list = []
        for workout_template_id, _  in self.workout_templates_list_info:
            inserting_templates_list.append([self.id, workout_template_id])
        
        self.database.delete_microcycle_template(self.id, False)


        insert_request = """
            INSERT INTO microcycle_template_composition(id_microcycle_template, id_workout_template)
            VALUES (?, ?)
        """
        self.database.__insert_request__(insert_request, inserting_templates_list)

        self.app_state.data_changed_notify()

        self.return_previous_screen() 



    def open_template_screen(self, id: int):
        self.navigate(
            screen_name=            "workout_template_screen",
            is_temporary_screen=    True,
            id_workout_template=    id, 
            page=                   self.page, 
            navigate_callback=      self.navigate, 
            app_state=              self.app_state,
            previous_screen_name=   "microcycle_template_screen"
        )

    

    def remove_workout_template(self, e):
        index_template_to_remove = self.template_container.templates.controls.index(e)

        self.template_container.templates.controls.pop(index_template_to_remove)
        self.workout_templates_list_info.pop(index_template_to_remove)

        self.template_container.templates.update()

        # Определение списка данных шаблонов тренировок
        temp_workout_card_list = []
        for id, title in self.workout_templates_list_info:
            temp_workout_card_list.append([id, title])

        self.workout_templates_list_info = temp_workout_card_list



    def _create_template_data_(self, template_data: list[list[str | int]]):
        template_information = []

        template_data.insert(0, [self.labels["set_name"], self.labels["set_count"]])

        for index, exercise_string in enumerate(template_data):
            exercise_title = f"{index}: {exercise_string[0]}" if index > 0 else f"{exercise_string[0]}"
            exercise_count = str(exercise_string[1])

            row_info: list[ft.Control] = [ # Указание pylance, что список корректный
                ft.Text(
                    value=exercise_title,
                    size=12,
                    max_lines=3,
                    color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                ),

                ft.Text(
                    value=exercise_count,
                    size=12,
                    max_lines=1,
                    color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                )
            ]


            template_information.append(
                ft.Row(
                    expand=True,
                    margin=ft.Margin.symmetric(vertical=5),
                    controls=row_info,

                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        return template_information

    
    def _create_template_card_(self, workout_template_id: int, workout_template_title: str) -> TemplateCard:
        exercises = self.database.get_workout_template_exercises(workout_template_id)
        template_card_data = [workout_template_title]

        if exercises != []:
            excercises_list = []
            temp_title   = self.translator.exercises[exercises[0][1]]
            temp_count  = 1

            for exercise in exercises[1:]:
                exercise = self.translator.exercises[exercise[1]]
                
                if (exercise != temp_title):
                    excercises_list.append((temp_title, temp_count))
                    temp_title   = exercise
                    temp_count  = 0
                
                temp_count += 1

            excercises_list.append((temp_title, temp_count))
            template_card_data = [*template_card_data, *self._create_template_data_(excercises_list)]

        return TemplateCard(
            self,
            id=workout_template_id,
            data=template_card_data,
            width=200,
            height=300,
            on_card_click=lambda id: self.open_template_screen(id),
            delete_from_list_function=lambda e: self.remove_workout_template(e),
        )