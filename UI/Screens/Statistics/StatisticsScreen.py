import flet as ft
import flet_charts as fch

import random
import itertools
import datetime


from AppState import AppState
from UI.Screens.BaseView import BaseView

from Classes.TrainingMetrics import TrainingMetrics


class StatisticsScreen(BaseView):
    def __init__(self, page: ft.Page, navigate_callback, app_state: AppState, previous_screen_name: str | None = None):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        self.labels = self.translator.statistics_screen_labels

        self.app_state.data_changed_subscribe(self._init_data_)

        # Набор цветов для отрисовки графиков
        self.chart_colors = [
            ft.Colors.RED_ACCENT_700, 
            ft.Colors.PINK_ACCENT_700, 
            ft.Colors.PURPLE_ACCENT_700,
            ft.Colors.DEEP_PURPLE_ACCENT_700,
            ft.Colors.INDIGO_ACCENT_700,
            ft.Colors.BLUE_ACCENT_700,
            ft.Colors.LIGHT_BLUE_ACCENT_700,
            ft.Colors.CYAN_ACCENT_700,
            ft.Colors.TEAL_ACCENT_700,
            ft.Colors.GREEN_ACCENT_700,
            ft.Colors.LIGHT_GREEN_ACCENT_700,
            ft.Colors.LIME_ACCENT_700,
            ft.Colors.YELLOW_ACCENT_700,
            ft.Colors.AMBER_ACCENT_700,
            ft.Colors.ORANGE_ACCENT_700,
            ft.Colors.DEEP_ORANGE_ACCENT_700
        ]
        self.random_color_list = itertools.cycle(random.sample(self.chart_colors, len(self.chart_colors)))
        
        # Переменные данных экрана статистики
        self.workout_statuses_piechart_sections     = []
        self.workout_statuses_piechart_legend_list  = []


        self._init_data_()




    def _init_data_(self):
        self.training_metrics = TrainingMetrics()

        self.workout_statuses_piechart_sections.clear()
        self.workout_statuses_piechart_legend_list.clear()


        # Создание логической и визуальной компановки базовых метрик
        self.base_metrics_block = ft.Container(
            expand=False,
            height=None,
            width=500,

            padding=ft.Padding.all(15),

            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            # gradient=self.colors.Gradients.BUTTON_PRIMARY,
            border_radius=10
        )

        
        self.percentage_of_completion_block = ft.Container(
            expand=True,
            height=100,
            padding=ft.Padding.all(10),
            content=ft.Column(
                spacing=5,
                controls=
                [
                    ft.Text(
                        value=self.labels["base_metrics"]["percentage_of_completion"],
                        size=12,
                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER
                    ),
                    
                    ft.Text(
                        value=f"{self.training_metrics.percentage_of_completion}",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER
                    ),

                    ft.Text(
                        value="%",
                        size=12,
                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),

            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border_radius=10
        )

        self.total_volume_block = ft.Container(
            expand=True,
            height=100,
            padding=ft.Padding.all(10),
            content=ft.Column(
                spacing=5,
                controls=
                [
                    ft.Text(
                        value=self.labels["base_metrics"]["total_volume"],
                        size=12,
                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER
                    ),
                    
                    ft.Text(
                        value=f"{self.training_metrics.total_volume}",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER
                    ),

                    ft.Text(
                        value=self.labels["base_metrics"]["total_volume_units"],
                        size=12,
                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),

            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            # gradient=self.colors.Gradients.BUTTON_PRIMARY,
            border_radius=10
        )

        self.workouts_count_block = ft.Container(
            expand=True,
            height=100,
            padding=ft.Padding.all(10),
            content=ft.Column(
                spacing=5,
                controls=
                [
                    ft.Text(
                        value=self.labels["base_metrics"]["workouts_count"],
                        size=12,
                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER
                    ),
                    
                    ft.Text(
                        value=f"{self.training_metrics.workouts_count}",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER
                    ),

                    ft.Text(
                        value=self.labels["base_metrics"]["workouts_count_time_range"],
                        size=12,
                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),

            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border_radius=10
        )

        self.workout_avg_duration_block = ft.Container(
            expand=True,
            height=100,
            padding=ft.Padding.all(10),
            content=ft.Column(
                spacing=5,
                controls=
                [
                    ft.Text(
                        value=self.labels["base_metrics"]["workout_avg_duration"],
                        size=12,
                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER
                    ),
    
                    ft.Text(
                        value=f"{self.training_metrics.workout_avg_duration}",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER
                    ),

                    ft.Text(
                        value=self.labels["base_metrics"]["workout_avg_duration_unit"]["minuts"],
                        size=12,
                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER
                    ),
                    
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),

            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border_radius=10
        )


        self.base_metrics_block.content = ft.Column(
            controls=
            [
                ft.Row(
                    controls=
                    [
                        self.percentage_of_completion_block,
                        self.workouts_count_block
                    ],
                    
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=
                    [
                        self.total_volume_block,
                        self.workout_avg_duration_block
                    ],
                    
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )




        # Текущая и лучшая серия тренировок
        self.best_and_current_workout_streak_block = ft.Container(
            expand=True,
            height=None,
            width=500,

            padding=ft.Padding.all(15),

            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            # gradient=self.colors.Gradients.HEADER,
            border_radius=10
        )


        self.current_workout_streak_block = ft.Container(
            expand=True,
            height=None,
            padding=ft.Padding.all(15),
            content=ft.Row(
                spacing=0,
                controls=
                [
                    ft.Column(
                        expand=1,
                        controls=
                        [
                            ft.Icon(
                                icon=ft.Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED,
                                size=35,
                                color=next(self.random_color_list)
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Column(
                        expand=10,
                        spacing=5,
                        controls=
                        [
                            ft.Text(
                                value=self.labels["current_streak"],
                                size=12,
                                color=ft.Colors.ON_SURFACE,
                                text_align=ft.TextAlign.CENTER
                            ),
                            
                            ft.Text(
                                value=f"{self.training_metrics.length_current_streak}",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.ON_SURFACE,
                                text_align=ft.TextAlign.CENTER
                            ),
                            
                            ft.Text(
                                value=
                                f"{datetime.datetime.fromtimestamp(self.training_metrics.date_range_current_streak[0]).strftime("%d.%m.%Y")}" + 
                                f" - " +
                                f"{datetime.datetime.fromtimestamp(self.training_metrics.date_range_current_streak[1]).strftime("%d.%m.%Y")}"
                                if self.training_metrics.date_range_current_streak != [] else self.labels["current_streak_subtitle"],
                                size=10,
                                color=ft.Colors.ON_SURFACE,
                                text_align=ft.TextAlign.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),

            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border_radius=10
        )

        self.best_workout_streak_block = ft.Container(
            expand=True,
            height=None,
            padding=ft.Padding.all(15),
            content=ft.Row(
                spacing=0,
                controls=
                [
                    ft.Column(
                        expand=1,
                        controls=
                        [
                            ft.Icon(
                                icon=ft.Icons.WORKSPACE_PREMIUM_ROUNDED,
                                size=35,
                                color=next(self.random_color_list)
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Column(
                        expand=10,
                        spacing=5,
                        controls=
                        [
                            ft.Text(
                                value=self.labels["best_streak"],
                                size=12,
                                color=ft.Colors.ON_SURFACE,
                                text_align=ft.TextAlign.CENTER
                            ),

                            ft.Text(
                                value=f"{self.training_metrics.length_best_streak}",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.ON_SURFACE,
                                text_align=ft.TextAlign.CENTER
                            ),
                            
                            ft.Text(
                                value=
                                f"{datetime.datetime.fromtimestamp(self.training_metrics.date_range_best_streak[0]).strftime("%d.%m.%Y")}" + 
                                f" - " +
                                f"{datetime.datetime.fromtimestamp(self.training_metrics.date_range_best_streak[1]).strftime("%d.%m.%Y")}"
                                if self.training_metrics.date_range_best_streak != [] else self.labels["best_streak_subtitle"],
                                size=10,
                                color=ft.Colors.ON_SURFACE,
                                text_align=ft.TextAlign.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),

            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border_radius=10
        )


        self.best_and_current_workout_streak_block.content = ft.Row(
            controls=
            [
                self.current_workout_streak_block,
                self.best_workout_streak_block
            ],
            
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )




        # График распределения статусов тренировок
        if (self.training_metrics.id_current_mesocycle is not None) and (self.training_metrics.id_current_mesocycle != 0):
            self.determine_workout_statuses_piechart_sections_and_legend()

        self.workout_statuses_chart = ft.Container(
            expand=True,
            height=None,
            width=500,

            content=ft.Column(
                expand=True,
                spacing=5,
                controls=
                [
                    ft.Text(
                        value=f"{self.labels["workout_statuses_piechart_title"]}" ,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Row(
                        spacing=15,
                        controls=
                        [
                            fch.PieChart(
                                expand=5,
                                center_space_radius=15,
                                sections_space=5,
                                sections=self.workout_statuses_piechart_sections,
                            ),
                            ft.Container(
                                expand=3,
                                width=300,
                                padding=ft.Padding.all(10),
                                content=ft.Column(
                                    controls=self.workout_statuses_piechart_legend_list,
                                    scroll=ft.ScrollMode.AUTO
                                ),
                                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                                border_radius=10,
                                
                                on_tap_down=self._init_data_,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ],
                scroll=ft.ScrollMode.AUTO,

                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
                
            if self.workout_statuses_piechart_sections != []
            else ft.Container(
                height=150,
                content=ft.Text(
                    expand=True,
                    value=self.labels["workout_statuses_piechart_no_data"],
                    size=14,
                    width=400,
                    max_lines=3,
                    color=ft.Colors.ON_SURFACE,
                    text_align=ft.TextAlign.CENTER
                ),
                
                alignment=ft.Alignment.CENTER
            ),

            padding=ft.Padding.all(25),

            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            # gradient=self.colors.Gradients.BUTTON_PRIMARY,

            border_radius=10,

            alignment=ft.Alignment.CENTER
        )



        self.main_container.alignment = ft.Alignment.TOP_CENTER
        self.main_container.content = ft.Column(
            spacing=15,
            controls=
            [
                self.base_metrics_block,
                self.best_and_current_workout_streak_block,
                self.workout_statuses_chart
            ],

            scroll=ft.ScrollMode.AUTO
        )


    
    def determine_workout_statuses_piechart_sections_and_legend(self):        
        self.workout_statuses_piechart_sections.clear()
        self.workout_statuses_piechart_legend_list.clear()

        workout_statuses = self.database.get_mesocycle_workout_statuses(
            id_user=self.settings.current_user,
            id_mesocycle=self.training_metrics.id_current_mesocycle
        )


        for workout_status in workout_statuses:
            id_workout_status       = workout_status[0]
            title_workout_status    = self.translator.workout_statuses.get(workout_status[1], workout_status[1])
            count_workout_status    = workout_status[2]
            color_workout_status    = next(self.random_color_list)

            if count_workout_status <= 0:
                continue

            self.workout_statuses_piechart_sections.append(
                fch.PieChartSection(
                    value=count_workout_status,
                    title=str(count_workout_status),
                    title_style=ft.TextStyle(
                        size=14,
                        color=ft.Colors.ON_SURFACE,
                        weight=ft.FontWeight.BOLD
                    ),
                    radius=75,
                    color=color_workout_status
                )
            )

            self.workout_statuses_piechart_legend_list.append(
                ft.Row(
                    spacing=5,
                    controls=
                    [
                        ft.Icon(
                            icon=ft.Icons.WATER_DROP_ROUNDED,#ft.Icons.CIRCLE_ROUNDED,
                            size=15,
                            color=color_workout_status
                        ),
                        ft.Text(
                            expand=True,
                            value=title_workout_status,
                            size=12,
                            max_lines=3,
                            color=ft.Colors.ON_SURFACE
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
