import flet as ft

from UI.Screens.BaseView import BaseView

from UI.Components.ExerciseSet import ExerciseSet


class SetsList(ft.Container):
    def __init__(
        self,
        screen: BaseView, 
        is_template: bool,
        is_planned: bool,
        id: int
    ) -> None:
        super().__init__()
        
        self.screen = screen

        self.app_state  = self.screen.app_state

        self.settings   = self.screen.settings
        self.database   = self.screen.database
        self.translator = self.screen.translator
        self.colors     = self.screen.colors


        self.id = id
        self.excercises_list = []
        self.is_template    = is_template
        self.is_planned     = is_planned


        result = self.database.get_workout_types()
        self.id_workout_type = result[0][0]

        self.expand=6
        # self.margin=ft.Margin.only(left=5, right=5)

        self.bgcolor = ft.Colors.SURFACE_CONTAINER_LOW

        self.border_radius=10


        
        self.add_exercise_set_button = ft.Container(
            margin=10,
            gradient=self.colors.Gradients.BUTTON_SUCCESS,
            shape=ft.BoxShape.CIRCLE,
            content=ft.IconButton(
                icon=ft.Icons.ADD_ROUNDED,
                icon_size=25,
                icon_color=ft.Colors.ON_TERTIARY,

                on_click=self._add_exercise_set_button_on_click_,
                on_hover=self._add_exercise_set_button_on_hover_
            ),
            alignment=ft.Alignment.CENTER
        )
        
        self.sets = []

        self.sets_list = ft.Column(
            margin=5, 
            spacing=0, # Т.к. между элементами прослойка dropzone
            controls=[*self.sets, self.add_exercise_set_button],
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START
        )



        if is_template:
            if self.id != 0:
                # Получение списка упражнений шаблона
                result = self.database.get_workout_template_exercises(self.id)

                if result != []:
                    self.excercises_list = []

                    temp_slug   = result[0][1]
                    temp_count  = 1

                    for exercise in result[1:]:
                        exercise = exercise[1]
                        if (exercise != temp_slug):
                            self.excercises_list.append((temp_slug, temp_count))

                            temp_slug   = exercise
                            temp_count  = 0
                        
                        temp_count += 1

                    self.excercises_list.append((temp_slug, temp_count))

                    # Получение id типа тренировки шаблона
                    get_template_info = f"""
                        SELECT wt.id_workout_type
                        FROM workout_templates AS wt
                        WHERE wt.id_workout_template = {id}
                    """

                    result = self.database.__select_request__(get_template_info)
                    
                    self.id_workout_type = int(result[0][0])
            
        else:
            # Логика для списка конкретной тренировки
            request = f"""
                SELECT  wt.id_workout_template, ws.slug
                FROM    workouts AS wt
                JOIN    workout_status AS ws ON ws.id_workout_status = wt.id_workout_status
                WHERE   id_workout = {self.id}
            """
            workout_info = self.database.__select_request__(request)[0]

            workout_template_info   = self.database.get_workout_template_info(workout_info[0])[0]
            self.id_workout_type    = self.database.get_workout_types(slug=workout_template_info[1])[0][0]

            
            self.excercises_list = []
            planned_exercises_info = self.database.get_workout_exercises(self.id, get_planned=True)
            actual_exercises_info  = self.database.get_workout_exercises(self.id, get_planned=False)

            if (planned_exercises_info != []) and (actual_exercises_info != []):
                for index in range(len(planned_exercises_info)):
                    planned_exercise = planned_exercises_info[index]
                    actual_exercise  = actual_exercises_info[index]
                    
                    id_composition  = planned_exercise[0]
                    ex_slug         = planned_exercise[2]

                    ex_planned_reps     = planned_exercise[3]
                    ex_planned_weight   = planned_exercise[4]
                    ex_actual_reps      = actual_exercise[3]
                    ex_actual_weight    = actual_exercise[4]

                    self.excercises_list.append((id_composition, ex_slug, ex_planned_reps, ex_planned_weight, ex_actual_reps, ex_actual_weight))


        
        if self.excercises_list != []:
            if is_template:
                for exercise in self.excercises_list:
                    excercises_title = str(self.screen.translator.exercises[exercise[0]])
                    exercise_sets_count = int(exercise[1]) if len(exercise) > 1 else 1

                    self.sets.append(
                        ExerciseSet(
                            sets_list=self,
                            screen=self.screen, 
                            title=excercises_title,
                            index=len(self.sets),
                            id_workout_type=self.id_workout_type,
                            sets_count=exercise_sets_count
                        )
                    )

            else:
                for exercise in self.excercises_list:
                    id_composition   = exercise[0]
                    excercises_title = str(self.screen.translator.exercises[exercise[1]])

                    planned_exercise_reps       = int(exercise[2])      if exercise[2] is not None else str("NULL")
                    planned_exercise_weight     = float(exercise[3])    if exercise[3] is not None else str("NULL")
                    actual_exercise_reps        = int(exercise[4])      if exercise[4] is not None else str("NULL")
                    actual_exercise_weight      = float(exercise[5])    if exercise[5] is not None else str("NULL")

                    self.sets.append(
                        ExerciseSet(
                            sets_list=self,
                            screen=self.screen, 
                            title=excercises_title,
                            index=len(self.sets),
                            id_workout_type=self.id_workout_type,
                            reps=actual_exercise_reps,
                            weight=actual_exercise_weight,
                            planned_reps=planned_exercise_reps,
                            planned_weight=planned_exercise_weight,
                            id_composition=id_composition
                        )
                    )
            
        self.sets_list.controls = self.sets
        if self.is_planned or (self.id == self.settings.current_workout):
            self.sets_list.controls = [*self.sets, self.add_exercise_set_button]
        
        
        if self.is_planned:
            self.disabled = False
        elif (not self.is_planned) and (self.settings.current_workout == 0):
            self.disabled = True

        self.content = self.sets_list
        


    
    def _add_exercise_set_button_on_click_(self):
        """
        Добавляет новую запись сета в конец списка
        """
        if self.is_template:
            self.sets.append(
                ExerciseSet(
                    sets_list=self, 
                    screen=self.screen,
                    title="",
                    index=len(self.sets), # Запись уникального номера сета для его управления
                    id_workout_type=self.id_workout_type,
                    sets_count=1
                )
            )
        else:
            self.sets.append(
                ExerciseSet(
                    sets_list=self, 
                    screen=self.screen,
                    title="",
                    index=len(self.sets), # Запись уникального номера сета для его управления
                    id_workout_type=self.id_workout_type,
                    reps=0,
                    weight=0.0
                )
            )
        self.sets_list.controls = [*self.sets, self.add_exercise_set_button]
        self.sets_list.update()


    def _add_exercise_set_button_on_hover_(self, e):
        self.add_exercise_set_button.gradient = self.colors.Gradients.BUTTON_SUCCESS_HOVER if e.data == True else self.colors.Gradients.BUTTON_SUCCESS
        self.add_exercise_set_button.update()


    
    def __init_sets_dropdown_menu__(self, e):
        self.id_workout_type = int(e.data)

        for exercise_set in self.sets:
            exercise_set.__init_dropdown_options__(self.id_workout_type)



    def _on_set_will_accept_(self, e):
        if e:
            target_idx = int(e.control.data)
            source_idx = int(e.src.data)

            # Если навели на соседний элемент, ничего не делаем
            if source_idx == target_idx:
                return
            
            if (source_idx < target_idx) and (abs(target_idx - source_idx) <= 1):
                return


            item = self.sets.pop(source_idx)
            self.sets.insert(
                target_idx if source_idx > target_idx else (target_idx - 1), 
                item    
            )

            # Обновляем индексы и перерисовываем список
            for index_set in range(len(self.sets)):
                self.sets[index_set].data = index_set
                self.sets[index_set].handle_icon_button.data = index_set
                self.sets[index_set]._init_dropzones_()

                self.screen.page.run_task(item.reset)

            
            self.sets_list.controls = [*self.sets, self.add_exercise_set_button]
            self.sets_list.update()

            # Сразу сохранить
            if self.settings.current_workout != 0:
                self.change_and_save_workout_composition()

        
    def _on_delete_exercise_(self, e):
        # Удаляет элемент из списка сетов и обновляет столбец с экземплярами класса ExerciseSet
        self.sets.remove(e)
        self.sets_list.controls.remove(e)

        # Перестройка индексов на последовательные
        for index_set in range(len(self.sets)):
            self.sets[index_set].data = index_set
            self.sets[index_set].handle_icon_button.data = index_set
            self.sets[index_set]._init_dropzones_()

        self.sets_list.update()

        # Сразу сохранить
        if self.settings.current_workout != 0:
            self.change_and_save_workout_composition()



    def change_and_save_workout_composition(self):
        self.database.delete_workout_composition(self.id)

        for set in self.sets:
            if isinstance(set, ExerciseSet):
                self.database.create_workout_composition(
                    id_workout=     self.id, 
                    id_exercise=    int(set.chosen_dropdown_exercise), 
                    reps=           int(set.reps_text_field.value),
                    weight=         float(set.weight_text_field.value),
                    # Указываю так, чтобы исключить возможность передачи в int() и float() None 
                    # UPD: Это нужно для интерпретатора, в моей логике здесь не может быть None 
                    planned_reps=   int(set.planned_reps)       if (set.planned_reps is not None)   else int(set.reps_text_field.value),
                    planned_weight= float(set.planned_weight)   if (set.planned_weight is not None) else float(set.weight_text_field.value)
                )

        self.app_state.data_changed_notify()