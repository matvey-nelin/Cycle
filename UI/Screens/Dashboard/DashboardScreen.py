import flet as ft
import datetime

from AppState import AppState
from UI.Screens.BaseView import BaseView

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
                color=ft.Colors.TERTIARY,
            ),
            menu_position=ft.PopupMenuPosition.UNDER
        )

        self.users_button_menu_label = ft.Container(
            content=ft.Text(
                value="",
                text_align=ft.TextAlign.CENTER,
                size=14,
                color=ft.Colors.ON_SURFACE
            ),
            alignment=ft.Alignment.CENTER
        )

        self.app_bar = ft.Container(
            height=50,
            margin=ft.Margin.only(top=10) if self.app_state.platform in ['ios', 'android'] else None,
            
            content=ft.Row(
                controls=
                [
                    self.users_button_menu_label,
                    self.users_button_menu
                ],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ), 
            
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border_radius=10,

            shadow=[
                ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=12, 
                    color=ft.Colors.SHADOW,
                    offset=ft.Offset(0, 4)
                )
            ],

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
                                color=ft.Colors.ON_SURFACE
                            )
                        ),

                        border=ft.Border.all(
                            width=1,
                            color=ft.Colors.OUTLINE
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

            style=ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: ft.Colors.ON_PRIMARY,
                    ft.ControlState.DISABLED: ft.Colors.GREY_500
                }
            ),


            on_click=self.change_time_period
        )
        self.next_time_period = ft.IconButton(
            data={"time_period" : day_period},

            icon=ft.Icons.KEYBOARD_ARROW_RIGHT_ROUNDED,
            icon_size=30,

            style=ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: ft.Colors.ON_PRIMARY,
                    ft.ControlState.DISABLED: ft.Colors.GREY_500
                }
            ),

            on_click=self.change_time_period
        )

        self.time_period_row = ft.Container(
            expand=False,
            margin=ft.Margin.symmetric(horizontal=50),
            width=300,

            content=ft.Row(
                expand=True,
                spacing=25,
                controls=
                [
                    self.previous_time_period,
                    self.next_time_period
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),

            gradient=self.colors.Gradients.HEADER_PRIMARY,

            border_radius=25
        )


        self.timetable = ft.Container(
            expand=True,
            margin=ft.Margin.symmetric(vertical=25, horizontal=10),
            padding=ft.Padding.symmetric(vertical=10, horizontal=10),
            content=self.workouts_list,

            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,

            border_radius=10,

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

        self.fill_timetable(date=self.current_date, period=day_period)
    
        time_periods = self.determine_time_period(int(self.current_date), day_period)
        
        if isinstance(self.time_period_row.content, ft.Row):
            self.time_period_row.content.controls = [
                self.previous_time_period,
                *time_periods,
                self.next_time_period
            ]
        

    
    def fill_timetable(self, date: int, period: int):
        self.workouts_list.controls.clear()
        workouts = self.database.get_workouts_near_to_date(date, abs(period)) 

        if workouts == []:
            self.timetable.content = ft.Text(
                value=self.labels["no_workouts_today"],
                size=16,
                width=None,
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.ON_SURFACE
            )
            return

        for workout in workouts:
            id_workout  = workout[0]
            username    = workout[1]
            workout_status  = self.translator.workout_statuses[workout[2]]
            start_str_time  = datetime.datetime.fromtimestamp(workout[3]).time().strftime("%H:%M")
            end_str_time    = datetime.datetime.fromtimestamp(workout[4]).time().strftime("%H:%M")

            current_workout_bgcolor = ft.Colors.PRIMARY

            self.workouts_list.controls.append(
                ft.Container(
                    data={"id": id_workout}, 
                    bgcolor=current_workout_bgcolor if self.settings.current_workout == id_workout else ft.Colors.SURFACE_CONTAINER_HIGH,
                    content=ft.ListTile(
                        expand=True,
                        content_padding=ft.Padding.only(left=10, right=10),
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
                                    color=ft.Colors.ON_SURFACE
                                ),
                                ft.Column(
                                    controls=
                                    [
                                        ft.Text(
                                            value=start_str_time,
                                            size=14,
                                            color=ft.Colors.ON_SURFACE
                                        ),
                                        ft.Text(
                                            value=end_str_time,
                                            size=14,
                                            color=ft.Colors.ON_SURFACE
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
                            color=ft.Colors.ON_SURFACE
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

        self.fill_timetable(int(self.current_date), time_period)
        time_periods = self.determine_time_period(int(self.current_date), time_period)
        
        if isinstance(self.time_period_row.content, ft.Row):
            self.time_period_row.content.controls = [
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
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.ON_PRIMARY
                )
            ]
        else:
            return [
                ft.Text(
                    value=datetime.datetime.fromtimestamp(date).date().strftime("%d.%m.%Y") if period > 0 
                        else datetime.datetime.fromtimestamp(date + period).date().strftime("%d.%m.%Y"),
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.ON_PRIMARY
                ),
                ft.Text(
                    value=" - ",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.ON_PRIMARY
                ),
                ft.Text(
                    value=datetime.datetime.fromtimestamp(date + period).date().strftime("%d.%m.%Y") if period > 0 
                        else datetime.datetime.fromtimestamp(date).date().strftime("%d.%m.%Y"),
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.ON_PRIMARY
                )
            ]


    def _on_list_tile_hover(self, e):
        e.control.bgcolor = ft.Colors.OUTLINE_VARIANT if e.data == True else ft.Colors.SURFACE_CONTAINER_HIGH



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
        # Создание навигации по микроциклам
        self.previous_microcycle_button = ft.IconButton(
            data={"step" : -1}, 
            icon=ft.Icons.KEYBOARD_ARROW_LEFT_ROUNDED,
            icon_size=30,

            style=ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: ft.Colors.ON_PRIMARY,
                    ft.ControlState.DISABLED: ft.Colors.GREY_500
                }
            ),

            on_click=self.microcycle_navigation
        )
        self.next_microcycle_button = ft.IconButton(
            data={"step" : 1},
            icon=ft.Icons.KEYBOARD_ARROW_RIGHT_ROUNDED,
            icon_size=30,

            style=ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: ft.Colors.ON_PRIMARY,
                    ft.ControlState.DISABLED: ft.Colors.GREY_500
                }
            ),

            on_click=self.microcycle_navigation
        )

        self.microcycle_time_ranges_row = ft.Container(
            expand=False,
            margin=ft.Margin.symmetric(horizontal=10),
            width=500,

            content=ft.Row(
                expand=False,
                spacing=0,
                controls=
                [
                    self.previous_microcycle_button,
                    self.next_microcycle_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),

            gradient=self.colors.Gradients.HEADER_PRIMARY,

            border_radius=25
        )

        # Создание контейнера тренировок
        self.workouts_list = ft.Column(
            expand=True,
            width=500,
            spacing=10,
            controls=[],

            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            scroll=ft.ScrollMode.AUTO
        )

        self.microcycle_container = ft.Container(
            expand=True,
            content=self.workouts_list,

            bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,

            border_radius=10,

            alignment=ft.Alignment.CENTER
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
                color=ft.Colors.ON_SURFACE
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
                color=ft.Colors.ON_SURFACE
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
        workouts = self.database.get_workouts_by_microcycle(id_microcycle)

        for workout in workouts:
            id_workout = workout[0]
            workout_card = self.training_process._create_workout_card_(
                screen=self, 
                id_workout=id_workout,
                planned_info=False,
                on_card_click=lambda id: self.on_workout_card_click(id),
                delete_from_list_function=None
            )
            # Отступ первой карточки для исправления эффекта обрезания тени
            if len(self.workouts_list.controls) == 0:
                workout_card.margin = ft.Margin.only(top=10)
            if len(self.workouts_list.controls) == (len(workouts) - 1):
                workout_card.margin = ft.Margin.only(bottom=10)

            self.workouts_list.controls.append(workout_card)


    def fill_microcycle_time_ranges_row(self, start_time_microcycle: int, end_time_microcycle: int):
        if isinstance(self.microcycle_time_ranges_row.content, ft.Row):
            self.microcycle_time_ranges_row.content.controls.clear()
        
        data_ranges = self.determine_data_ranges(start_time_microcycle, end_time_microcycle)

        if isinstance(self.microcycle_time_ranges_row.content, ft.Row):
            self.microcycle_time_ranges_row.content.controls = [
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
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.ON_PRIMARY
            ),
            ft.Text(
                value=" - ",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.ON_PRIMARY
            ),
            ft.Text(
                value=datetime.datetime.fromtimestamp(end_time_microcycle).date().strftime("%d.%m.%Y") \
                if end_time_microcycle != 0 else "",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.ON_PRIMARY
            )
        ] 
            

    