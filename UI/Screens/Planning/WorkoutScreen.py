import flet as ft
import datetime

from Classes.TrainingMetrics import TrainingMetrics

from AppState import AppState
from UI.Screens.BaseView import BaseView

from UI.Components.SetsList import SetsList
from UI.Components.ExerciseSet import ExerciseSet


class WorkoutScreen(BaseView):
    def __init__(
        self, 
        id_workout: int, 
        page: ft.Page, 
        navigate_callback, 
        app_state: AppState, 
        previous_screen_name: str,
        is_planning_screen: bool
    ):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        self.id = id_workout
        
        self.labels = self.translator.workout_screen_labels
        self.is_planning_screen = is_planning_screen

        self.time_changed           = False
        self.composition_changed    = False

        self.app_state.resize_subscribe(self._on_resize_)

        
        self._init_data_()
        self._init_components_()

        
        


    def _init_data_(self):
        request = f"""
            SELECT  wt.id_workout_template, ws.slug
            FROM    workouts AS wt
            JOIN    workout_status AS ws ON ws.id_workout_status = wt.id_workout_status
            WHERE   id_workout = {self.id}
        """
        workout_info = self.database.__select_request__(request)[0]

        workout_template_info   = self.database.get_workout_template_info(workout_info[0])[0]
        self.workout_template_title  = self.translator.workout_templates.get(workout_template_info[0], workout_template_info[0]) 

        self.workout_type_title     = self.translator.workout_types.get(workout_template_info[1], workout_template_info[1])
        self.hypertrophy_type_title = self.translator.hypertrophy_types.get(workout_template_info[2], workout_template_info[2])

        self.workout_status_id       = self.database.get_workout_statuses(status_slug=workout_info[1])[0][0]
        workout_status_slug     = workout_info[1]
        self.workout_status_title    = self.translator.workout_statuses.get(workout_status_slug, workout_status_slug) 


        time_ranges = self.database.get_all_workout_datetimes(self.id)[0]
        # self.start_time = time_ranges[0] if self.is_planning_screen else time_ranges[2]
        # self.end_time   = time_ranges[1] if self.is_planning_screen else time_ranges[3]
        
        # Беру всегда фактическое время
        self.start_time = time_ranges[2]
        self.end_time   = time_ranges[3]



        if self.start_time == 0 or self.end_time == 0:
            self.start_time = datetime.datetime.now().timestamp()
            self.end_time   = self.start_time + 3600
            

        self.date_time_string   = datetime.datetime.fromtimestamp(float(self.start_time)).strftime("%d.%m.%Y")
        self.start_time_string  = datetime.datetime.fromtimestamp(float(self.start_time)).strftime("%H:%M")
        self.end_time_string    = datetime.datetime.fromtimestamp(float(self.end_time)).strftime("%H:%M")

        self.picked_date        = datetime.datetime.fromtimestamp(self.start_time).date()
        self.picked_start_time  = datetime.datetime.fromtimestamp(self.start_time).time()
        self.picked_end_time    = datetime.datetime.fromtimestamp(self.end_time).time()


        self.status_items = []
        for status in self.database.get_workout_statuses():
            status_id    = status[0]
            status_slug  = status[1]
            status_title = self.translator.workout_statuses.get(status_slug, status_slug)

            self.status_items.append(
                ft.PopupMenuItem(
                    content=status_title,
                    checked=(status_id == self.workout_status_id),
                    data=[status_id, status_slug, status_title],  
                    on_click=self.change_and_save_workout_status
                )
            )


    def _init_date_time_pickers_(self):
        def determine_date(e): 
            self.time_changed = True

            self.picked_date        = datetime.datetime.fromtimestamp(e.data.timestamp()).date()
            self.start_time         = datetime.datetime.combine(self.picked_date, self.picked_start_time).timestamp()
            self.end_time           = self.start_time + 3600

            self.date_time_string   = datetime.datetime.fromtimestamp(float(self.start_time)).strftime("%d.%m.%Y")
            self.start_time_string  = datetime.datetime.fromtimestamp(float(self.start_time)).strftime("%H:%M")
            self.end_time_string    = datetime.datetime.fromtimestamp(float(self.end_time)).strftime("%H:%M")

            self.date_picker.value          = self.picked_date
            self.date_picker_button.content = self.date_time_string
            self.date_picker_button.update()


        def determine_start_time(e):
            self.time_changed = True

            self.picked_start_time  = e.data
            self.start_time         = datetime.datetime.combine(self.picked_date, self.picked_start_time).timestamp()
            self.end_time           = self.start_time + 3600

            self.start_time_string  = datetime.datetime.fromtimestamp(float(self.start_time)).strftime("%H:%M")
            self.end_time_string    = datetime.datetime.fromtimestamp(float(self.end_time)).strftime("%H:%M")

            self.start_time_picker.value          = self.picked_start_time
            self.start_time_picker_button.content = self.start_time_string
            self.start_time_picker_button.update()
            
            determine_end_time(ft.Event('change', control=self.end_time_picker, data=datetime.datetime.fromtimestamp(self.end_time).time()))


        def determine_end_time(e):
            self.time_changed = True

            self.picked_end_time    = e.data
            self.end_time           = datetime.datetime.combine(self.picked_date, self.picked_end_time).timestamp()
            self.end_time_string    = datetime.datetime.fromtimestamp(float(self.end_time)).strftime("%H:%M")

            self.end_time_picker.value          = self.picked_end_time
            self.end_time_picker_button.content = self.end_time_string
            self.end_time_picker_button.update()



        self.date_picker = ft.DatePicker(
            value=self.picked_date,
            locale=ft.Locale(language_code=self.settings.language),

            switch_to_input_icon=ft.Icons.EDIT_ROUNDED,
            switch_to_calendar_icon=ft.Icons.EDIT_CALENDAR_ROUNDED,

            on_change=determine_date if self.is_planning_screen else None
        )

        self.start_time_picker = ft.TimePicker(
            value=self.picked_start_time,
            locale=ft.Locale(language_code=self.settings.language),

            switch_to_input_icon=ft.Icons.EDIT_ROUNDED,
            switch_to_timer_icon=ft.Icons.ACCESS_TIME_ROUNDED,

            on_change=determine_start_time if self.is_planning_screen else None
        )
        
        self.end_time_picker = ft.TimePicker(
            value=self.picked_end_time,
            locale=ft.Locale(language_code=self.settings.language),

            switch_to_input_icon=ft.Icons.EDIT_ROUNDED,
            switch_to_timer_icon=ft.Icons.ACCESS_TIME_ROUNDED,

            on_change=determine_end_time if self.is_planning_screen else None
        )


        
        def open_picker_dialog(dialog: ft.DialogControl):
            try:
                self.page.show_dialog(dialog)
            except RuntimeError:
                pass

        self.date_picker_button = ft.OutlinedButton(
            expand=1,
            content=datetime.datetime.fromtimestamp(float(self.start_time)).strftime("%d.%m.%Y"),
            on_click=lambda: open_picker_dialog(self.date_picker),
        )

        self.start_time_picker_button = ft.OutlinedButton(
            expand=1,
            content=self.start_time_string,
            on_click=lambda: open_picker_dialog(self.start_time_picker),
        )

        self.end_time_picker_button = ft.OutlinedButton(
            expand=1,
            content=self.end_time_string,
            on_click=lambda: open_picker_dialog(self.end_time_picker),
        )


        self.date_picker_row = ft.Row(
            expand=1,
            controls=[self.date_picker_button]
        )
        self.time_pickers_row = ft.Row(
            expand=1,
            controls=[self.start_time_picker_button, self.end_time_picker_button]
        )
        self.time_pickers_column = ft.Column(
            expand=1,
            controls=
            [
                ft.Row(
                    expand=1,
                    controls=[self.start_time_picker_button]
                ),
                ft.Row(
                    expand=1,
                    controls=[self.end_time_picker_button]
                )
            ] 
            if self.app_state.is_mobile
            else 
            [
                ft.Row(
                    expand=1,
                    controls=
                    [
                        self.start_time_picker_button,
                        self.end_time_picker_button
                    ]
                )
            ]
            
        )

        if self.is_planning_screen:
            list_time_pickers: list[ft.Control] = [self.date_picker_row, self.time_pickers_row] if self.settings.trainer_mode \
                                            else  [self.date_picker_row]
        else:
            self.start_time_picker_button.on_click  = None
            self.end_time_picker_button.on_click    = None

            list_time_pickers: list[ft.Control] = [self.time_pickers_column] 
        
        
        self.time_pickers = ft.Column(
            expand=2,
            spacing=3,
            controls=list_time_pickers,

            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )


    def _init_components_(self):
        self._init_date_time_pickers_()

        self.top_info_block = ft.Container(
            expand=True,
            content=ft.Row(
                expand=True,
                tight=False,
                margin=ft.Margin.only(top=10, left=10, right=10),
                controls=
                [
                    ft.Row(
                        expand=1,
                        spacing=5,
                        controls=
                        [
                            ft.Text(
                                expand=1, 
                                value=self.workout_template_title,
                                size=14,
                                color=ft.Colors.ON_SURFACE
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.START
                    ),
                    self.time_pickers
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )


        
        self.sets_list = SetsList(
            screen=         self, 
            is_template=    False, 
            is_planned=     self.is_planning_screen,
            id=             self.id
        )


        # Меню действий с тренировкой
        self.save_button = ft.Container(
            expand=2,
            height=40,
            width=300,

            gradient=self.colors.Gradients.BUTTON_PRIMARY,
            content=ft.Text(
                value=self.labels["save_button"],
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.ON_PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),

            border_radius=15,

            alignment=ft.Alignment.CENTER,

            on_click=self._save_button_on_click_,
            on_hover=self._save_button_on_hover_
        )


        self.start_workout_button = ft.Container(
            expand=2,
            height=40,
            width=300,

            gradient=self.colors.Gradients.BUTTON_SUCCESS,
            content=ft.Text(
                value=self.labels["start_workout"],
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.ON_PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),
            border_radius=15,

            alignment=ft.Alignment.CENTER,

            on_click=self._start_workout_button_on_click_
        )

        self.end_workout_button = ft.Container(
            expand=2,
            height=40,
            width=300,

            gradient=self.colors.Gradients.BUTTON_DANGER,
            content=ft.Text(
                value=self.labels["end_workout"],
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.ON_ERROR,
                text_align=ft.TextAlign.CENTER
            ),

            border_radius=15,

            alignment=ft.Alignment.CENTER,

            on_click=self._end_workout_button_on_click_
        )


        self.workout_status_button = ft.PopupMenuButton(
            expand=1,
            items=self.status_items,
            menu_position=ft.PopupMenuPosition.OVER
        )

        if self.is_planning_screen:
            self.actions_menu_controls: list[ft.Control] = [
                ft.Container(expand=1),
                self.save_button,
                self.workout_status_button
            ]
        else:
            if self.settings.current_workout == 0:
                self.actions_menu_controls: list[ft.Control] = [
                    ft.Container(expand=1),
                    self.start_workout_button,
                    self.workout_status_button
                ]
            elif (self.settings.current_workout != 0) and (self.id == self.settings.current_workout):
                self.actions_menu_controls: list[ft.Control] = [
                    ft.Container(expand=1),
                    self.end_workout_button,
                    ft.Container(expand=1),
                ]
            elif (self.settings.current_workout != 0) and (self.id != self.settings.current_workout):
                self.actions_menu_controls: list[ft.Control] = [
                    self.workout_status_button
                ]



        self.actions_menu = ft.Row(
            expand=True,
            margin=ft.Margin.symmetric(vertical=5, horizontal=10),
            controls=self.actions_menu_controls,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )



        self.main_container.content = ft.Column(
            expand=True,
            controls=
            [
                self.top_info_block,
                self.sets_list,
                self.actions_menu
            ],

            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        self._on_resize_(None)



    def _save_button_on_click_(self):
        if self.is_planning_screen:
            self.database.update_workout_status(self.id, self.workout_status_id)

            if self.time_changed:
                self.database.update_workout_datetime(self.id, "planned_workout_start_datetime", int(self.start_time))
                self.database.update_workout_datetime(self.id, "planned_workout_end_datetime",   int(self.end_time))
                self.database.update_workout_datetime(self.id, "actual_workout_start_datetime", int(self.start_time))
                self.database.update_workout_datetime(self.id, "actual_workout_end_datetime",   int(self.end_time))


            if self.composition_changed:
                self.database.delete_workout_composition(self.id)

                for set in self.sets_list.sets:
                    if isinstance(set, ExerciseSet):
                        self.database.create_workout_composition(
                            id_workout=     self.id, 
                            id_exercise=    int(set.chosen_dropdown_exercise), 
                            reps=           int(set.reps_text_field.value)                              if set.reps_text_field.value   != "NULL" else None,
                            weight=         float(str(set.weight_text_field.value).replace(",", "."))   if set.weight_text_field.value != "NULL" else None
                        )

            self.app_state.data_changed_notify()
            self.return_previous_screen()


    def _save_button_on_hover_(self, e):
        self.save_button.gradient = self.colors.Gradients.BUTTON_HOVER if e.data == True else self.colors.Gradients.BUTTON_PRIMARY
        self.save_button.update()




    def _start_workout_button_on_click_(self):
        self.settings.start_workout(self.id)

        new_start_time  = int(datetime.datetime.now().timestamp())
        new_end_time    = int(new_start_time + (self.end_time - self.start_time))

        self.database.update_workout_datetime(self.id, "actual_workout_start_datetime", new_start_time)
        self.database.update_workout_datetime(self.id, "actual_workout_end_datetime",   new_end_time)

        id_workout_status_in_progress = self.database.get_workout_statuses(status_slug='in_progress')[0][0]
        self.database.update_workout_status(id_workout=self.id, id_status=id_workout_status_in_progress)

        self.app_state.data_changed_notify()

        self.navigate(
            screen_name=            "planning_workout_screen",
            is_temporary_screen=    True,
            id_workout=             self.id, 
            is_planning_screen=     False,
            page=                   self.page, 
            navigate_callback=      self.navigate, 
            app_state=              self.app_state, 
            previous_screen_name=   "dashboard_screen"
        )



    def _end_workout_button_on_click_(self):
        self.settings.end_workout()
        self.database.update_workout_datetime(self.id, "actual_workout_end_datetime", int(datetime.datetime.now().timestamp()))

        training_metrics = TrainingMetrics()
        workout_volumes = training_metrics.get_workout_volume(id_workout=self.id)

        if workout_volumes["workout_planned_volume"] == workout_volumes["workout_actual_volume"]:
            id_workout_status = self.database.get_workout_statuses(status_slug='completed')[0][0]
        elif workout_volumes["workout_planned_volume"] < workout_volumes["workout_actual_volume"]:
            id_workout_status = self.database.get_workout_statuses(status_slug='overcompleted')[0][0]
        elif workout_volumes["workout_planned_volume"] > workout_volumes["workout_actual_volume"]:
            id_workout_status = self.database.get_workout_statuses(status_slug='partially_completed')[0][0]

        self.database.update_workout_status(id_workout=self.id, id_status=id_workout_status)


        self.app_state.data_changed_notify()

        self.return_previous_screen()



    def _on_resize_(self, e):
        if self.app_state.is_mobile:
            self.workout_status_button.content = ft.Container(
                content=ft.Row(
                    controls=  
                    [
                        ft.Icon(
                            icon=ft.Icons.FILTER_LIST_ROUNDED, 
                            size=20,
                            color=ft.Colors.SECONDARY
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                border=ft.Border.all(1, ft.Colors.OUTLINE),
                border_radius=20
            )

            self.time_pickers_column.controls = [
                ft.Row(
                    expand=1,
                    controls=[self.start_time_picker_button]
                ),
                ft.Row(
                    expand=1,
                    controls=[self.end_time_picker_button]
                )
            ] 

        else:
            self.workout_status_button.content = ft.Container(
                content=ft.Row(
                    controls=  
                    [
                        ft.Icon(
                            icon=ft.Icons.FILTER_LIST_ROUNDED, 
                            size=20,
                            color=ft.Colors.SECONDARY
                        ),
                        ft.Text(
                                self.workout_status_title,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.SURFACE_TINT
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                border=ft.Border.all(1, ft.Colors.OUTLINE),
                border_radius=20
            ) 
            
            self.time_pickers_column.controls = [
                ft.Row(
                    expand=1,
                    controls=
                    [
                        self.start_time_picker_button,
                        self.end_time_picker_button
                    ]
                )
            ]

        try:
            self.workout_status_button.update()
            self.time_pickers_column.update()
        except:
            pass


    
    def change_and_save_workout_status(self, e):
        self.workout_status_id    = e.control.data[0]
        self.workout_status_title = e.control.data[2]

        for status_item in self.workout_status_button.items:
            status_item.checked = (status_item.data[0] == self.workout_status_id)

        # Сохраняю в БД изменения сразу
        if not self.is_planning_screen:
            self.database.update_workout_status(self.id, self.workout_status_id)

        self.app_state.data_changed_notify()

        # Вызываю для перерисовки кнопки (текста)
        self._on_resize_(None)