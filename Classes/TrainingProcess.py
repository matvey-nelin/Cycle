import flet as ft
import datetime

from AppState import AppState
from UI.Components.TemplateCard import TemplateCard
from UI.Screens.BaseView import BaseView


class TrainingProcess:
    def __init__(self, app_state: AppState) -> None:
        self.app_state = app_state

        self.database   = self.app_state.database
        self.settings   = self.app_state.settings
        self.colors     = self.app_state.colors
        self.translator = self.app_state.translator

        self.labels = self.translator.training_process_labels


    def create_microcycle_from_template(self, id_microcycle_template: int, id_mesocycle: int):
        # Проверка id на наличие такового в БД
        microcycle_templates = self.database.get_microcycle_templates()
        microcycle_templates_ids = [template[0] for template in microcycle_templates]
        
        if id_microcycle_template not in microcycle_templates_ids:
            raise ValueError("Incorrect value of 'id_microcycle_template'")
        
        # Создание микроцикла
        self.database.insert_microcycle(id_mesocycle, is_unloading=False)

        id_microcycle = self.database.get_microcycles(id_mesocycle)[-1][0]
        id_workout_status = self.database.get_workout_statuses(status_slug="scheduled")
        id_workout_status = int(id_workout_status[0][0]) if (id_workout_status != []) else int(self.database.get_workout_statuses()[-1][0])

        for workout_template_info in self.database.get_microcycle_workout_templates(id_microcycle_template):
            id_workout_template = workout_template_info[0]
            self._create_workout_(id_microcycle, id_workout_template, id_workout_status)
            



    def _create_workout_(self, id_microcycle: int, id_workout_template: int, id_workout_status: int):
        self.database.insert_workout(id_microcycle, id_workout_template, id_workout_status)
        id_workout = int(self.database.get_workouts(id_microcycle)[-1][0])

        exercises = self.database.get_workout_template_exercises(id_workout_template)

        for exercise in exercises:
            id_exercise     = exercise[0]
            slug_exercise   = exercise[1]
            title_exercise  = self.translator.exercises[slug_exercise]

            self.database.create_workout_composition(id_workout, id_exercise)



    def _create_workout_card_(self, screen: BaseView, id_workout: int, planned_info: bool, on_card_click, delete_from_list_function):
        exercises = self.database.get_workout_exercises(id_workout, planned_info) 

        def create_row(exercise_title: str, planned_repetitions: int | str, planned_weight: float | str):
            return ft.Row(
                spacing=5,
                margin=0,
                controls=
                [
                    ft.Text(
                        str(exercise_title),
                        size=12,
                        expand=True,
                        max_lines=3,
                        color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                    ),
                    ft.Row(
                        expand=False,
                        wrap=False,
                        controls=
                        [
                            ft.Text(
                                str(planned_repetitions),
                                size=12,
                                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                            ),
                            ft.Text(
                                str(planned_weight),
                                size=12,
                                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        
        card_info = []


        # Время тренировки
        workout_ranges = self.database.get_all_workout_datetimes(id_workout)[0]
        if self.settings.trainer_mode:
            start_time_workout  = workout_ranges[2]
            end_time_workout    = workout_ranges[3]

            start_date_workout  = datetime.datetime.fromtimestamp(start_time_workout).date().strftime("%d.%m.%Y")   if start_time_workout != 0 else ""
            start_time_workout  = datetime.datetime.fromtimestamp(start_time_workout).time().strftime("%H:%M")      if start_time_workout != 0 else ""

            end_date_workout    = datetime.datetime.fromtimestamp(end_time_workout).date().strftime("%d.%m.%Y")     if end_time_workout != 0 else ""
            end_time_workout    = datetime.datetime.fromtimestamp(end_time_workout).time().strftime("%H:%M")        if end_time_workout != 0 else ""

            card_info.append(
                ft.Row(
                    controls=[
                        ft.Column(
                            spacing=1, 
                            controls=
                            [
                                ft.Text(
                                    start_date_workout,
                                    size=14,
                                    color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                                ),
                                ft.Text(
                                    start_time_workout,
                                    size=14,
                                    color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ), 
                        ft.Text(
                            " - ",
                            size=14,
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                        ),
                        ft.Column(
                            spacing=1,
                            controls=
                            [
                                ft.Text(
                                    end_date_workout,
                                    size=14,
                                    color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                                ),
                                ft.Text(
                                    end_time_workout,
                                    size=14,
                                    color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            )   
        else:
            start_time_workout  = workout_ranges[2]
            start_time_workout  = datetime.datetime.fromtimestamp(start_time_workout).date().strftime("%d.%m.%Y")\
                                if (start_time_workout != 0)   else ""
            
            card_info.append(
                ft.Row(
                    controls=[
                        ft.Text(
                            start_time_workout,
                            size=12,
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        title_workout_status = self.translator.workout_statuses[self.database.get_workout_statuses(id_workout=id_workout)[0][1]]
        card_info.append(
            ft.Row(
                margin=ft.Margin.only(bottom=10),
                controls=
                [
                    ft.Text(
                        value=title_workout_status,
                        size=14,
                        color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        card_info.append(
            ft.Divider(
                height=1,
                color=self.colors.LIGHT_OUTLINE_VARIANT if self.colors.theme == 'light' else self.colors.DARK_OUTLINE_VARIANT
            )
        )

        card_info.append(
            create_row(self.labels["exercise_title"], self.labels["exercise_repetitions"], self.labels["exercise_weight"])
        )
        



        for exercise in exercises:
            id_exercise = int(exercise[1])
            title_exercise = self.translator.exercises[exercise[2]]

            planned_repetitions = int(exercise[3])
            planned_weight      = float(exercise[4])
            
            card_info.append(create_row(title_exercise, planned_repetitions, planned_weight))

        workout_card = TemplateCard(
            screen=         screen,
            id=             id_workout,
            data=           card_info,
            width=          250,
            height=         None,
            on_card_click=  on_card_click,
            delete_from_list_function=delete_from_list_function 
        )
        workout_card.border = ft.Border().all(
            width=2,
            color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE
        )
        workout_card.border_radius = 5
        workout_card.padding = 0

        return workout_card