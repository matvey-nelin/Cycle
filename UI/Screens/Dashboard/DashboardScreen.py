from turtle import color

import flet as ft
import datetime

from numpy import size

from AppState import AppState
from UI.Screens.BaseView import BaseView

from UI.Components.TemplateContainer import TemplateContainer
from Classes.TrainingProcess import TrainingProcess



class DashboardScreen(BaseView):
    def __init__(self, page: ft.Page, navigate_callback, app_state: AppState, previous_screen_name: str | None = None):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        self.training_process = TrainingProcess(self.app_state)
        self.labels = self.translator.dashboard_screen_labels
        self.app_state.data_changed_subscribe(self._init_users_popup_menu_items_)
            

        # Меню выбора пользователя
        self.users_button_menu = ft.PopupMenuButton(
            tooltip=self.labels["user_popup_menu_button_tooltip"],
            icon=ft.Icon(
                icon=ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
                size=35,
                color=self.colors.LIGHT_SECONDARY_CONTAINER if self.colors.theme == 'light' else self.colors.DARK_SECONDARY_CONTAINER,
            ),
            menu_position=ft.PopupMenuPosition.UNDER
        )

        self.users_button_menu_label = ft.Container(
            content=ft.Text(
                value="",
                text_align=ft.TextAlign.CENTER,
                size=14,
                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
            ),
            alignment=ft.Alignment.CENTER
        )

        self.app_bar = ft.Container(
            expand=1,
            content=ft.Row(
                controls=
                [
                    self.users_button_menu_label,
                    self.users_button_menu
                ],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ), 
            alignment=ft.Alignment.CENTER_RIGHT
        )
        

        # Инициализация нужного вида дэшбоарда
        if self.settings.trainer_mode:
            self._init_trainer_dashboard_()
            self.app_state.data_changed_subscribe(self._init_trainer_data_)
        else:
            self._init_sportsmen_dashboard_()
            self.app_state.data_changed_subscribe(self._init_sportsmen_data_)


        self.content = ft.Column(
            expand=True, 
            controls=
            [
                self.app_bar,
                self.main_container
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )


    
    def _init_users_popup_menu_items_(self):
        # Беру только активных пользователей
        self.users_button_menu.items = []
        users = self.database.get_users(id_user_status=1)
        for user in users:
            id_user  = user[0]
            username = user[2]

            if id_user == self.settings.current_user:
                if isinstance(self.users_button_menu_label.content, ft.Text):
                    self.users_button_menu_label.content.value = username

            
            self.users_button_menu.items.append(
                ft.PopupMenuItem(
                    data={"id": id_user}, 

                    content=ft.Container(
                        margin=ft.Margin.symmetric(vertical=2, horizontal=5),
                        padding=ft.Padding.only(left=5),
                        width=250,

                        content=ft.ListTile(
                            title=username,
                            title_alignment=ft.ListTileTitleAlignment.CENTER,
                            title_text_style=ft.TextStyle(
                                size=14,
                                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
                            )
                        ),

                        border=ft.Border.all(
                            width=1,
                            color=self.colors.LIGHT_OUTLINE if self.colors.theme == 'light' else self.colors.DARK_OUTLINE
                        ),
                        border_radius=5,

                        alignment=ft.Alignment.CENTER_RIGHT,
                    ),
                    
                    on_click=self.users_submenu_option_on_click
                ) 
            )
    



    def users_submenu_option_on_click(self, e):
        self.app_state.change_user(e.control.data["id"])

        username = self.database.get_users(id_user=self.settings.current_user)[0][2]
        if isinstance(self.users_button_menu_label.content, ft.Text):
            self.users_button_menu_label.content.value = username




    def _init_trainer_dashboard_(self):
        self.workouts_list = ft.ListView(
            spacing=10,
            controls=[]
        )

        # Создание навигации по временным отрезкам (сейчас только один день)
        day_period = int(24 * 60 * 60)

        self.previous_time_period = ft.IconButton(
            data={"time_period" : -day_period},
            icon=ft.Icons.KEYBOARD_ARROW_LEFT_ROUNDED,
            icon_size=30,
            disabled_color=self.colors.LIGHT_OUTLINE if self.colors.theme == 'light' else self.colors.DARK_OUTLINE,
            on_click=self.change_time_period
        )
        self.next_time_period = ft.IconButton(
            data={"time_period" : day_period},
            icon=ft.Icons.KEYBOARD_ARROW_RIGHT_ROUNDED,
            icon_size=30,
            disabled_color=self.colors.LIGHT_OUTLINE if self.colors.theme == 'light' else self.colors.DARK_OUTLINE,
            on_click=self.change_time_period
        )

        self.time_period_row = ft.Row(
            expand=False,
            controls=
            [
                self.previous_time_period,
                self.next_time_period
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        )


        self.timetable = ft.Container(
            expand=True,
            margin=ft.Margin.symmetric(vertical=25, horizontal=15),
            padding=ft.Padding.symmetric(vertical=10, horizontal=10),
            content=self.workouts_list,
            border = ft.Border().all(
                width=2,
                color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE,
            ),
            alignment=ft.Alignment.CENTER
        )

        self.main_container = ft.Container(
            expand=11,
            content=ft.Column(
                spacing=10,
                controls=
                [   
                    self.time_period_row,
                    self.timetable
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.Alignment.CENTER
        )

        self._init_trainer_data_()


    def _init_trainer_data_(self):
        self._init_users_popup_menu_items_()

        # Тренировки в течении текущего дня
        self.current_date = int(datetime.datetime.now().replace(hour=0, minute=0, second=0).timestamp())
        day_period   = int(24 * 60 * 60)

        self.fill_table_time(date=self.current_date, period=day_period)
    
        time_periods = self.determine_time_period(int(self.current_date), day_period)
        
        self.time_period_row.controls = [
            self.previous_time_period,
            *time_periods,
            self.next_time_period
        ]
        

    
    def fill_table_time(self, date: int, period: int):
        self.workouts_list.controls.clear()
        workouts = self.database.get_workouts_near_to_date(date, abs(period)) 

        if workouts == []:
            self.timetable.content = ft.Text(
                value=self.labels["no_workouts_today"],
                size=16,
                width=None,
                text_align=ft.TextAlign.CENTER,
                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
            )
            return

        for workout in workouts:
            id_workout  = workout[0]
            username    = workout[1]
            workout_status  = self.translator.workout_statuses[workout[2]]
            start_str_time  = datetime.datetime.fromtimestamp(workout[3]).time().strftime("%H:%M")
            end_str_time    = datetime.datetime.fromtimestamp(workout[4]).time().strftime("%H:%M")

            current_workout_bgcolor = self.colors.LIGHT_PRIMARY if self.colors.theme == 'light' else self.colors.DARK_PRIMARY

            self.workouts_list.controls.append(
                ft.Container(
                    data={"id": id_workout},
                    bgcolor=current_workout_bgcolor if self.settings.current_workout == id_workout else None,
                    content=ft.ListTile(
                        expand=True,
                        content_padding=ft.Padding.only(left=15 , right=15),
                        title=ft.Row(
                            # margin=ft.Margin.symmetric(horizontal=25),
                            controls=
                            [
                                ft.Text(
                                    value=username,
                                    size=16,
                                    width=200,
                                    no_wrap=False,
                                    max_lines=3,
                                    color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
                                ),
                                ft.Column(
                                    controls=
                                    [
                                        ft.Text(
                                            value=start_str_time,
                                            size=14,
                                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
                                        ),
                                        ft.Text(
                                            value=end_str_time,
                                            size=14,
                                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        subtitle=ft.Text(
                            value=workout_status,
                            size=12,
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
                        ),
                        hover_color=self.colors.LIGHT_OUTLINE_VARIANT if self.colors.theme == 'light' else self.colors.DARK_OUTLINE_VARIANT
                    ),
                    border=ft.Border.all(
                        width=1,
                        color=self.colors.LIGHT_OUTLINE if self.colors.theme == 'light' else self.colors.DARK_OUTLINE
                    ),
                    border_radius=5,

                    alignment=ft.Alignment.CENTER,

                    on_click=self.open_workout_screen,
                    on_hover=self._on_list_tile_hover if self.settings.current_workout != id_workout else None
                )
            )

        self.timetable.content = self.workouts_list


    def change_time_period(self, e):
        time_period = e.control.data["time_period"]
        self.current_date += time_period

        self.fill_table_time(int(self.current_date), time_period)
        time_periods = self.determine_time_period(int(self.current_date), time_period)
        
        self.time_period_row.controls = [
            self.previous_time_period,
            *time_periods,
            self.next_time_period
        ]

        try:
            self.time_period_row.update()
            self.timetable.update()
        except RuntimeError:
            pass

    
    def determine_time_period(self, date: int, period: int):
        if abs(period) == int(24 * 60 * 60):
            return [
                ft.Text(
                    value=datetime.datetime.fromtimestamp(date).date().strftime("%d.%m.%Y"),
                    size=14,
                    color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
                )
            ]
        else:
            return [
                ft.Text(
                    value=datetime.datetime.fromtimestamp(date).date().strftime("%d.%m.%Y") if period > 0 
                        else datetime.datetime.fromtimestamp(date + period).date().strftime("%d.%m.%Y"),
                    size=14,
                    color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
                ),
                ft.Text(
                    value=" - ",
                    size=14,
                    color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
                ),
                ft.Text(
                    value=datetime.datetime.fromtimestamp(date + period).date().strftime("%d.%m.%Y") if period > 0 
                        else datetime.datetime.fromtimestamp(date).date().strftime("%d.%m.%Y"),
                    size=14,
                    color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
                )
            ]


    def _on_list_tile_hover(self, e):
        list_tile_hover_bgcolor = self.colors.LIGHT_OUTLINE_VARIANT if self.colors.theme == 'light' else self.colors.DARK_OUTLINE_VARIANT
        e.control.bgcolor = list_tile_hover_bgcolor if e.data == True else None



    def open_workout_screen(self, e):
        id_workout = e.control.data["id"]

        self.navigate(
            screen_name=            "planning_workout_screen",
            is_temporary_screen=    True,
            id_workout=             id_workout, 
            is_planning_screen=     False,
            page=                   self.page, 
            navigate_callback=      self.navigate, 
            app_state=              self.app_state, 
            previous_screen_name=   "dashboard_screen"
        )



 







    def _init_sportsmen_dashboard_(self):
        # Создание контейнера тренировок
        self.workouts_list = ft.Column(
            expand=True,
            spacing=10,
            controls=[],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )

        self.microcycle_container = ft.Container(
            expand=True,
            padding=ft.Padding.symmetric(vertical=10, horizontal=20),
            content=self.workouts_list,
            border = ft.Border().all(
                width=2,
                color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE,
            ),
            alignment=ft.Alignment.CENTER
        )

        # Создание навигации по микроциклам
        self.previous_microcycle_button = ft.IconButton(
            data={"step" : -1},
            icon=ft.Icons.KEYBOARD_ARROW_LEFT_ROUNDED,
            icon_size=30,
            disabled_color=self.colors.LIGHT_OUTLINE if self.colors.theme == 'light' else self.colors.DARK_OUTLINE,
            on_click=self.microcycle_navigation
        )
        self.next_microcycle_button = ft.IconButton(
            data={"step" : 1},
            icon=ft.Icons.KEYBOARD_ARROW_RIGHT_ROUNDED,
            icon_size=30,
            disabled_color=self.colors.LIGHT_OUTLINE if self.colors.theme == 'light' else self.colors.DARK_OUTLINE,
            on_click=self.microcycle_navigation
        )

        self.microcycle_time_ranges_row = ft.Row(
            expand=False,
            controls=
            [
                self.previous_microcycle_button,
                self.next_microcycle_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        )

        
        # Наполнение экрана контентом
        self.microcycle_content = ft.Column(
            expand=True,
            margin=ft.Margin.symmetric(vertical=0, horizontal=15),
            spacing=10,
            controls=
            [
                self.microcycle_time_ranges_row,
                self.microcycle_container
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.main_container = ft.Container(
            expand=11,
            content=self.microcycle_content,
            alignment=ft.Alignment.CENTER
        )

        self._init_sportsmen_data_()

    
    def _init_sportsmen_data_(self):
        self._init_users_popup_menu_items_()

        # Определение текущего микро- и мезо- циклов как ближайших к текущему моменту времени
        nearest_mesocycle = self.database.determine_nearest_mesocycle(
            time=int(datetime.datetime.now().timestamp()), id_user=self.settings.current_user
        )
        if nearest_mesocycle == []:
            self.main_container.content = ft.Text(
                value=self.labels["no_planned_mesocycles"],
                text_align=ft.TextAlign.CENTER,
                size=18,
                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
            )
            return
        
        self.id_current_mesocycle = nearest_mesocycle[0][0]


            # Назначение временных отрезков микроциклам
        self.time_ranges_microcycles = self.database.determine_time_ranges_microcycle(id_mesocycle=self.id_current_mesocycle)
        nearest_microcyle = self.database.determine_nearest_microcycle(
            time=int(datetime.datetime.now().timestamp()), id_mesocycle=self.id_current_mesocycle
        )
        if nearest_microcyle == []:
            self.microcycle_container.content = ft.Text(
                value=self.labels["no_planned_workouts"],
                text_align=ft.TextAlign.CENTER,
                size=18,
                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
            )
            return
        
        self.id_current_microcycle = nearest_microcyle[0][0]


        for index, microcycle in enumerate(self.time_ranges_microcycles):
            id_microcycle           = int(microcycle[0])
            start_time_microcycle   = int(microcycle[1])
            end_time_microcycle     = int(microcycle[2])

            if id_microcycle == self.id_current_microcycle:
                self.fill_microcycle_container(id_microcycle=id_microcycle)
                self.fill_microcycle_time_ranges_row(start_time_microcycle, end_time_microcycle)


                self.previous_microcycle_button.disabled = bool(index == 0)
                self.next_microcycle_button.disabled     = bool(index == (len(self.time_ranges_microcycles) - 1))

                break


        # Обновление данных при смене пользователя
        self.microcycle_content.controls = [
            self.microcycle_time_ranges_row,
            self.microcycle_container
        ]
        self.main_container.content = self.microcycle_content

        try:
            self.main_container.update()
            self.content.update()
        except:
            pass



    def fill_microcycle_container(self, id_microcycle: int):
        self.workouts_list.controls.clear()
        workouts = self.database.get_workouts(id_microcycle)

        for workout in workouts:
            id_workout = workout[0]
            workout_card = self.training_process._create_workout_card_(
                screen=self, 
                id_workout=id_workout,
                planned_info=False,
                on_card_click=lambda id: self.on_workout_card_click(id),
                delete_from_list_function=None
            )
            self.workouts_list.controls.append(workout_card)


    def fill_microcycle_time_ranges_row(self, start_time_microcycle: int, end_time_microcycle: int):
        self.microcycle_time_ranges_row.controls.clear()
        
        data_ranges = self.determine_data_ranges(start_time_microcycle, end_time_microcycle)

        self.microcycle_time_ranges_row.controls = [
            self.previous_microcycle_button, 
            *data_ranges,
            self.next_microcycle_button
        ]


    def on_workout_card_click(self, id_workout: int):
        self.navigate(
            screen_name=            "planning_workout_screen",
            is_temporary_screen=    True,
            id_workout=             id_workout, 
            is_planning_screen=     False,
            page=                   self.page, 
            navigate_callback=      self.navigate, 
            app_state=              self.app_state, 
            previous_screen_name=   "dashboard_screen"
        )


        
    def microcycle_navigation(self, e):
        # Навигация по микроциклам текущего мезоцикла
        step = e.control.data["step"]

        for index, microcycle in enumerate(self.time_ranges_microcycles):
            id_microcycle = int(microcycle[0])

            # Переход на предыдущий или следующий микроцикл
            if id_microcycle == self.id_current_microcycle:
                microcycle = self.time_ranges_microcycles[index + step]

                self.id_current_microcycle  = int(microcycle[0])
                id_microcycle               = int(microcycle[0])
                start_time_microcycle       = int(microcycle[1])
                end_time_microcycle         = int(microcycle[2])

                self.fill_microcycle_container(id_microcycle=id_microcycle)
                self.fill_microcycle_time_ranges_row(start_time_microcycle, end_time_microcycle)   

                self.previous_microcycle_button.disabled = bool((index + step) == 0)
                self.next_microcycle_button.disabled     = bool((index + step) == (len(self.time_ranges_microcycles) - 1))
                
                break
    

    def determine_data_ranges(self, start_time_microcycle: int, end_time_microcycle: int):
        return [
            ft.Text(
                value=datetime.datetime.fromtimestamp(start_time_microcycle).date().strftime("%d.%m.%Y") \
                if start_time_microcycle != 0 else "",
                size=14,
                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
            ),
            ft.Text(
                value=" - ",
                size=14,
                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
            ),
            ft.Text(
                value=datetime.datetime.fromtimestamp(end_time_microcycle).date().strftime("%d.%m.%Y") \
                if end_time_microcycle != 0 else "",
                size=14,
                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
            )
        ] 
            

    