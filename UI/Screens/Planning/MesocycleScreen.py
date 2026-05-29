import flet as ft

from AppState import AppState
from UI.Screens.BaseView import BaseView

from UI.Components.TemplateContainer import TemplateContainer
from Classes.TrainingProcess import TrainingProcess


class MesocycleScreen(BaseView):
    def __init__(
        self, 
        id_mesocycle: int, 
        page: ft.Page, 
        navigate_callback, 
        app_state: AppState, 
        previous_screen_name: str | None = "mesocycle_menu"
    ):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        self.app_state.resize_subscribe(self._on_resize_)

        self._on_data_changed = lambda: self._init_data_(self.id)
        self.app_state.data_changed_subscribe(self._on_data_changed)


        self.id     = id_mesocycle

        self.labels = self.translator.mesocycle_screen_labels

        self.training_process = TrainingProcess(self.app_state)



        # Кнопка добавления нового шаблона тренировки
        self.add_microcycle_button = ft.Container(
            margin=10,
            gradient=self.colors.Gradients.BUTTON_SUCCESS,
            shape=ft.BoxShape.CIRCLE,
            content=ft.IconButton(
                icon=ft.Icons.ADD_ROUNDED,
                icon_size=25,
                icon_color=ft.Colors.ON_TERTIARY,

                on_click=self._add_microcycle_button_on_click_,
                on_hover=self._add_microcycle_button_on_hover_
            ),
            alignment=ft.Alignment.CENTER
        )



        self.microcycles = []
        self.microcycles_row = ft.Row(
            spacing=0,

            controls=[*self.microcycles, self.add_microcycle_button],

            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )

        self.microcycles_container = ft.Container(
            expand=True,
            content=self.microcycles_row,

            border_radius=10,

            alignment=ft.Alignment.CENTER_LEFT
        )


        # Меню действий с мезоциклом
        self.actions_menu = ft.Row(
            expand=True,
            margin=ft.Margin.symmetric(vertical=5, horizontal=10),
            controls=
            [
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            visible=False
        )

        self.main_container.padding = 0
        self.main_container.content = ft.Column(
            spacing=0,
            controls=
            [
                self.microcycles_container,
                self.actions_menu
            ],

            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self._init_data_(self.id)
        self._on_resize_(None)


    
    def _init_data_(self, id_mesocycle: int, previous_screen_name: str | None = "mesocycle_menu"):
        if previous_screen_name is not None:
            self.previous_screen_name = previous_screen_name
            
        # Переопределение данных элементов страницы
        if id_mesocycle != self.id:
            try:
                self.app_state._data_changed_listeners.remove(self._on_data_changed)
            except ValueError:
                pass

            self.id = id_mesocycle
            self._on_data_changed = lambda: self._init_data_(self.id)
            self.app_state.data_changed_subscribe(self._on_data_changed)

        self.microcycles = []
        
        for microcycle in self.database.get_microcycles(self.id):
            id_microcycle = int(microcycle[0])
            self.microcycles.append(
                self._create_microcycle_container_(id_microcycle)
            )
        
        self.microcycles_row.controls = [*self.microcycles, self.add_microcycle_button]
        try:
            self.microcycles_row.update()
        except RuntimeError:
            pass



    def _on_resize_(self, e):
        self.__on_page_resize__(e)

        container_width   = 550 if (self.page_width is None) else (self.page_width - 40)
        container_height  = 800 if (self.page_height is None) else (self.page_height - 150)

        self.microcycles_container.width  = container_width
        self.microcycles_container.height = container_height

        for microcycle in self.microcycles_row.controls:
            if isinstance(microcycle, TemplateContainer):
                microcycle.height = self.microcycles_container.height

        try:
            self.microcycles_container.update()
            self.microcycles_row.update()
        except RuntimeError:
            pass


    
    def _create_microcycle_container_(self, id_microcycle: int):
        # Создание чекбокса
        def on_checkbox_change(e):
            self.database.update_microcycle(id_microcycle, e.data)
            
        is_unloading = bool(self.database.get_microcycles(self.id, id_microcycle)[0][1])
        self.is_unloading_checkbox = ft.Checkbox(
            data={"id_microcycle": id_microcycle}, 
            value=is_unloading,
            active_color=self.colors.LIGHT_SECONDARY_CONTAINER if self.colors.theme == 'light' else self.colors.DARK_SECONDARY_CONTAINER,
            label=self.labels["is_unloading_checkbox"],
            label_position=ft.LabelPosition.RIGHT,
            label_style=ft.TextStyle(
                size=14,
                color=ft.Colors.ON_SURFACE
            ),
            on_change=on_checkbox_change
        )

        # Создание контейнера
        microcycle = TemplateContainer(self)

        microcycle.data     = id_microcycle
        microcycle.height   = self.microcycles_container.height
        microcycle.bgcolor  = ft.Colors.SURFACE_CONTAINER_LOW
        microcycle.border   = ft.Border().all(
            width=1,
            color=ft.Colors.SECONDARY
        )
        microcycle.templates.spacing = 10
        microcycle.templates.controls.append(self.is_unloading_checkbox)


        workouts    = self.database.get_workouts_by_microcycle(id_microcycle)
        workouts_list = []

        for workout in workouts:
            id_workout = int(workout[0])
            workout_card = self.training_process._create_workout_card_(
                screen=                     self, 
                id_workout=                 id_workout, 
                planned_info=               False,
                on_card_click=              lambda id=self.id: self.open_workout_screen(id),
                delete_from_list_function=  lambda e: self.remove_workout(e)
            )
            
            if len(workouts_list) == 0:
                workout_card.margin = ft.Margin.only(left=5, top=10, right=5, bottom=0)
            elif len(workouts_list) == (len(workouts) - 1):
                workout_card.margin = ft.Margin.only(left=5, top=0, right=5, bottom=10)

            workouts_list.append(workout_card)

        microcycle.templates.controls = [*microcycle.templates.controls, *workouts_list]
        return microcycle

    

    def open_workout_screen(self, id_workout: int):
        self.navigate(
            screen_name=            "planning_workout_screen",
            is_temporary_screen=    True,
            id_workout=             id_workout, 
            is_planning_screen=     True,
            page=                   self.page, 
            navigate_callback=      self.navigate, 
            app_state=              self.app_state, 
            previous_screen_name=   "mesocycle_screen"
        )

    
    def remove_workout(self, e):
        for microcycle in self.microcycles_row.controls:
            if isinstance(microcycle, TemplateContainer):
                try:
                    microcycle.templates.controls.remove(e)
                    self.database.delete_workout(e.id)

                    if len(microcycle.templates.controls) == 1:
                        self.microcycles.remove(microcycle)
                        self.microcycles_row.controls.remove(microcycle)
                        self.database.delete_microcycle(microcycle.data)

                    self.microcycles_row.update()
                    self.app_state.data_changed_notify()
                    return
                except ValueError:
                    continue




    def _add_microcycle_button_on_click_(self):
        """
        Добавляет новый микроцикл с запланированными тренировками в конец списка
        """
        def add_microcycle(id: int):
            self.training_process.create_microcycle_from_template(id, self.id)
            self.app_state.data_changed_notify()

            self.navigate(
                screen_name=            "mesocycle_screen",
                is_universal_screen=    True,
                id_mesocycle=           self.id
            )


        self.navigate(
            screen_name=            "choosable_microcycle_template_menu",
            is_temporary_screen=    True,
            page=                   self.page, 
            navigate_callback=      self.navigate, 
            app_state=              self.app_state,
            selection_function=     lambda id=self.id: add_microcycle(id),
            previous_screen_name=   "mesocycle_screen"
        )



    def _add_microcycle_button_on_hover_(self, e):
        self.add_microcycle_button.gradient = self.colors.Gradients.BUTTON_SUCCESS_HOVER if e.data == True else self.colors.Gradients.BUTTON_SUCCESS
        self.add_microcycle_button.update()