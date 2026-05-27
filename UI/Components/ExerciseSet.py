import asyncio

import flet as ft
import re

from UI.Components.DropZone import DropZone
from UI.Screens.BaseView import BaseView


class ExerciseSet(ft.Container):
    def __init__(
        self,
        sets_list,
        screen: BaseView, 
        title: str,
        index: int,
        id_workout_type: int,
        reps:   int | str | None = None, 
        weight: float | str | int | None = None,
        sets_count: int = 0,
        planned_reps: int | str | None = None,
        planned_weight: float | str | int | None = None,
        id_composition: int | None = None
    ) -> None:
        super().__init__(ft.Row()) # Заглушка для создание потомка
        
        """
        :param sets_count : Индикатор того, что это строка упражнения шаблона
        """

        if ((reps is None) or (weight is None)) and (sets_count == 0):
            raise ValueError("Invalid data of exercise")

        if not isinstance(sets_count, int):
            raise ValueError("Invalid data of count of set")

        self.screen     = screen

        self.settings   = self.screen.settings
        self.database   = self.screen.database
        self.translator = self.screen.translator
        self.colors     = self.screen.colors

        self.labels = self.translator.exercise_set_labels

        self.title = title
        self.sets_list = sets_list
        self._on_set_will_accept_ = self._on_set_accept_
        self._on_delete_exercise_ = lambda e: self.sets_list._on_delete_exercise_(self)

        self.data = index # Индентификатор сета в списке
        self.group = "exercise_set"

        self.id_composition = id_composition

        self.planned_reps   = planned_reps
        self.planned_weight = planned_weight

        self.all_exercises = self.screen.database.get_exercises()

        
        self.content_container = ft.Container(
            padding=0,
            margin=0,
            height=40,

            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border_radius=10,

            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color=ft.Colors.SHADOW,
                offset=ft.Offset(0, 2)
            ),

            animate=ft.Animation(
                duration=300,
                curve=ft.AnimationCurve.EASE_IN_OUT
            ),
            
            animate_scale=ft.Animation(
                duration=400, 
                curve=ft.AnimationCurve.EASE_OUT_BACK
            )
        )

        self.opacity_content_container = ft.Container(
            expand=True,
            content=None,
            padding=0,
            margin=0,
            height=None,

            border=ft.Border().all(
                width=1,
                color=ft.Colors.OUTLINE_VARIANT
            ),
            border_radius=10,

            bgcolor = ft.Colors.SECONDARY_CONTAINER,
            opacity = 0.5
        )
        

        # 1. Создаем красивую строку для перетаскивания
        self.feedback_row = ft.Row(
            expand=True,
            spacing=10,  # Больше воздуха между элементами
            controls=[
                # Иконка ручки
                ft.Icon(
                    icon=ft.Icons.DRAG_HANDLE_ROUNDED,
                    size=28,
                    color=ft.Colors.PRIMARY
                ),
                
                # Название упражнения (жирный текст)
                ft.Text(
                    self.title,
                    size=15,
                    weight=ft.FontWeight.W_600,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        # 2. Обернутый контейнер с эффектами
        self.feedback_container = ft.Container(
            content=self.feedback_row,
            height=40,
            padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            
            # Фон (контрастный, но не яркий)
            bgcolor=ft.Colors.SURFACE,
            
            # Тень для эффекта «парения»
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.SHADOW,
                offset=ft.Offset(0, 2),
            ),
            
            # Скругление и рамка
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            
            # Полупрозрачность для эффекта «под пальцем»
            opacity=0.95,
        )
        
        # Draggable IconButton для перетаскивания сетов в списке
        self.handle_icon_button = ft.Draggable(
            expand=True,
            group="exercise_set",
            data=self.data,
            content=ft.Icon(
                expand=1,
                icon=ft.Icons.DRAG_HANDLE_ROUNDED,
                size=20,
                width=15,
                align=ft.Alignment.CENTER_LEFT
            ),

            content_feedback=self.feedback_container,
            # Заглушка на старом месте
            content_when_dragging=ft.Container(
                height=40,
                bgcolor=ft.Colors.SURFACE_TINT,
                border=ft.Border.all(2, ft.Colors.PRIMARY),
                border_radius=10,
                opacity=0.5,
            ),
        )


        # Dropdown со списом упражнений
        self.__init_dropdown_options__(id_workout_type)
        self.exercise_dropdown = ft.Dropdown(
            expand=10,
            content_padding=ft.Padding.only(left=10, top=5, right=10, bottom=15), 

            value=self.chosen_dropdown_exercise,
            text_style=ft.TextStyle(
                size=10,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.ON_SURFACE
            ),
            options=self.dropdown_exercises_options,

            hint_text = self.labels["set_name"], 

            text_align=ft.TextAlign.START,
            border=ft.InputBorder.NONE,
            focused_border_color=ft.Colors.PRIMARY,
            color=ft.Colors.ON_SURFACE,

            on_select=self.exercise_dropdown_on_select
        )


        # TextField с количеством подходов
        self.count_text_field = ft.TextField(
            expand=3,
            margin=ft.Margin.only(bottom=1, left=5, right=5),
            content_padding=ft.Padding.only(bottom=5),

            helper=self.labels["set_count"],
            helper_style=ft.TextStyle(
                size=8,
                color=ft.Colors.ON_SURFACE
            ),

            value=str(sets_count), 
            text_style=ft.TextStyle(
                size=12,
                color=ft.Colors.ON_SURFACE
            ),
            text_align=ft.TextAlign.CENTER,
            
            
            border=ft.InputBorder.NONE,
            border_color=ft.Colors.OUTLINE,
            focused_border_color=ft.Colors.PRIMARY,
            
            max_lines=1,
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        # TextField с количеством потворений
        self.reps_text_field = ft.TextField(
            expand=3,
            margin=ft.Margin.only(bottom=1, left=5, right=5),
            content_padding=ft.Padding.only(bottom=5),

            hint_text=str(planned_reps) if planned_reps is not None else None,
            helper=self.labels["set_repetitions"],
            helper_style=ft.TextStyle(
                size=8,
                color=ft.Colors.ON_SURFACE
            ),

            value=str(reps), 
            text_style=ft.TextStyle(
                size=12,
                color=ft.Colors.ON_SURFACE
            ),
            text_align=ft.TextAlign.CENTER,
            
            border=ft.InputBorder.NONE,
            border_color=ft.Colors.OUTLINE,
            focused_border_color=ft.Colors.PRIMARY,
            
            max_lines=1,
            keyboard_type=ft.KeyboardType.NUMBER, 

            on_change=self.change_and_save_reps if (self.settings.current_workout != 0) else self.change_composition_status
        )

        # TextField с весом
        self.weight_text_field = ft.TextField(
            expand=3,
            margin=ft.Margin.only(bottom=1, left=5, right=5),
            content_padding=ft.Padding.only(bottom=5),

            hint_text=str(planned_weight) if planned_weight is not None else None,
            helper=self.labels["set_weight"],
            helper_style=ft.TextStyle(
                size=8,
                color=ft.Colors.ON_SURFACE
            ),

            value=str("0" if (str(weight) == "0.0") else weight), 
            text_style=ft.TextStyle( 
                size=12,
                color=ft.Colors.ON_SURFACE
            ),
            text_align=ft.TextAlign.CENTER,
            
            border=ft.InputBorder.NONE,
            border_color=ft.Colors.OUTLINE,
            focused_border_color=ft.Colors.PRIMARY,
            
            max_lines=1,
            keyboard_type=ft.KeyboardType.NUMBER,

            on_change=self.change_and_save_weight if (self.settings.current_workout != 0) else None
        )

        # IconButton для удаления сета из списка
        self.delete_button = ft.Container(
            expand=True,
            content=ft.Icon(
                expand=1,
                width=15,

                icon=ft.Icons.DELETE_ROUNDED,
                size=20,
                color=ft.Colors.ON_SURFACE,
    
                align=ft.Alignment.CENTER
            ),
            
            on_click=self._on_delete_exercise_
        )



        if sets_count != 0:    
            # Код для шаблона тренировки        
            self.content_container.content = ft.Row(
                expand=True,
                margin=ft.Margin.only(left=10, right=10),
                spacing=12,
                controls=
                [
                    self.handle_icon_button,
                    self.exercise_dropdown,
                    # ft.VerticalDivider(1), 
                    self.count_text_field,
                    # ft.VerticalDivider(1), 
                    self.delete_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )

        
        else:
            # Код для тренировки
            self.content_container.content = ft.Row(
                expand=True,
                margin=ft.Margin.only(left=10, right=10),
                spacing=10,
                controls=
                [
                    self.handle_icon_button,
                    self.exercise_dropdown,
                    # ft.VerticalDivider(1), 
                    self.reps_text_field,
                    # ft.VerticalDivider(1), 
                    self.weight_text_field,
                    # ft.VerticalDivider(1), 
                    self.delete_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
            pass

        
        self._init_dropzones_()



    def _init_dropzones_(self):
        self.dropzone_before = DropZone(self, self.data, height=15)
        self.dropzone_after  = DropZone(self, self.data + 1)
            
        set_controls = [self.content_container, self.dropzone_after]

        if self.data == 0:
            set_controls = [self.dropzone_before, *set_controls]
        elif self.data == len(self.sets_list.excercises_list) - 1:
            set_controls = [self.content_container, DropZone(self, self.data + 1, height=15)]

        self.content = ft.Column(
            spacing=0,
            controls=set_controls
        )
        


    def exercise_dropdown_on_select(self, e):
        for exercise in self.all_exercises:
            exercise_id     = str(exercise[0])
            exercise_title  = str(self.translator.exercises.get(exercise[1], exercise[2]))

            if exercise_id == e.data:
                self.chosen_dropdown_exercise = exercise_id
                self.title = exercise_title
                return


    def __init_dropdown_options__(self, id_workout_type: int):
        self.chosen_dropdown_exercise = ""

        dropdown_exercises_options = []
        list_exercises = self.screen.database.get_exercises(id_workout_type)

        if isinstance(list_exercises, Exception):
            raise ValueError("Invalid data of exercises")
        
        list_exercises = list_exercises if list_exercises != [] else self.all_exercises
        
        for exercise in list_exercises:
            exercise_id     = str(exercise[0])
            exercise_title  = str(self.translator.exercises.get(exercise[1], exercise[2]))

            if exercise_title == self.title:
                self.chosen_dropdown_exercise = exercise_id


            agonists_tooltip = self.screen.database.get_agonists(int(exercise_id))
            if isinstance(agonists_tooltip, Exception):
                raise ValueError("Invalid data of agonists")
            agonists_tooltip = [self.translator.agonists[agonist[1]] for agonist in agonists_tooltip]
            agonists_tooltip = ", ".join(agonists_tooltip)
            
            
            dropdown_exercises_options.append(
                ft.DropdownOption(
                    key=exercise_id,
                    text=exercise_title,
                    
                    content=ft.Container(
                        content=ft.Text(
                            expand=True,

                            value=exercise_title,
                            size=12,
                            width=None,
                            
                            no_wrap=False,
                            max_lines=3,
                            overflow=ft.TextOverflow.ELLIPSIS,

                            color=ft.Colors.ON_SURFACE,
                        ),

                        # bgcolor=ft.Colors.with_opacity(opacity=0.5, color=ft.Colors.SECONDARY_CONTAINER),
                        # blur=(0, 10)
                    ),

                    tooltip=ft.Tooltip(message=agonists_tooltip)
                )
            ) 

        dropdown_exercises_options = sorted(dropdown_exercises_options, key=lambda x: x.content.content.value)
       
        
        if self.chosen_dropdown_exercise == "":
            if isinstance(self.all_exercises, Exception):
                raise ValueError("Imposible download data of the exercises")
            
            for exercise in self.all_exercises:
                exercise_id     = str(exercise[0])
                exercise_title  = self.translator.exercises.get(exercise[1], exercise[2])

                if exercise_title == self.title:
                    self.chosen_dropdown_exercise = exercise_id

                    dropdown_exercises_options.insert(
                        0,
                        ft.DropdownOption(
                            key=exercise_id,
                            text=exercise_title,
                            
                            content=ft.Container(
                                content=ft.Text(
                                    expand=True,

                                    value=exercise_title,
                                    size=12,
                                    width=None,
                                    
                                    no_wrap=False,
                                    max_lines=3,
                                    overflow=ft.TextOverflow.ELLIPSIS,

                                    color=ft.Colors.ON_SURFACE,
                                ),

                                # bgcolor=ft.Colors.with_opacity(opacity=0.5, color=ft.Colors.SECONDARY_CONTAINER),
                                # blur=(0, 10)
                            ),

                            tooltip=ft.Tooltip(message=agonists_tooltip)
                        )
                    )

                    break

        self.dropdown_exercises_options = dropdown_exercises_options

        if hasattr(self, "exercise_dropdown"):
            self.exercise_dropdown.options = self.dropdown_exercises_options
            self.exercise_dropdown.update()
        



    def change_and_save_reps(self, e):
        if self.id_composition is None:
            return
        
        reps_value = re.sub(r'[^0-9]', '', e.control.value.strip())

        self.database.update_workout_composition_by_id_composition(
            id_composition=self.id_composition,
            reps=int(reps_value) if reps_value != "" else 0
        )

        self.screen.app_state.data_changed_notify()
        
    
    def change_and_save_weight(self, e):
        if self.id_composition is None:
            return
        
        weight_value = re.sub(r'[^0-9,.]', '', e.control.value.strip()).replace(",", ".")

        self.database.update_workout_composition_by_id_composition(
            id_composition=self.id_composition,
            weight=float(weight_value) if weight_value != "" else 0
        )
        
        self.screen.app_state.data_changed_notify()


    def change_composition_status(self):
        if hasattr(self.screen, "composition_changed"):
            self.screen.composition_changed = True # pyright: ignore[reportAttributeAccessIssue]





    def _on_set_accept_(self, e):
        self.sets_list._on_set_will_accept_(e)

        
    async def reset(self):
        self.content_container.bgcolor  = ft.Colors.PRIMARY_CONTAINER
        self.content_container.update()

        await asyncio.sleep(0.1)

        self.content_container.scale    = 1.005
        self.content_container.update()

        await asyncio.sleep(0.5)
        
        self.content_container.scale    = 1.0
        self.content_container.bgcolor  = ft.Colors.SURFACE_CONTAINER_HIGH
        self.content_container.update()