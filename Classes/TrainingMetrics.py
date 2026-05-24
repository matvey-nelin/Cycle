import datetime

from Database.Database import Database
from Settings import Settings



class TrainingMetrics:
    def __init__(self) -> None:
        self.database = Database()
        self.settings = Settings()


        # Переменные тренировочного процесса
        self.id_current_mesocycle   = None
        self.id_current_microcycle  = None
        self.get_current_mesocycle_and_microcycle()

        # Базовые метрики
        self.percentage_of_completion   = 0
        self.total_volume               = 0
        self.workouts_count             = 0
        self.workout_avg_duration       = 0
        self.get_base_metrics()

        # Таблица вовлеченности агонистов
        self.agonists_involvement_table = []

        # Данные о текущей и лучшей серии выполненных тренировок
        self.length_current_streak      = 0
        self.date_range_current_streak  = []

        self.length_best_streak         = 0
        self.date_range_best_streak     = []
        self.get_best_and_current_workout_streak()



    
    def get_base_metrics(self):
        nearest_mesocycle = self.database.determine_nearest_mesocycle(
            time=int(datetime.datetime.now().timestamp()), 
            id_user=self.settings.current_user
        )

        if nearest_mesocycle != []:
            current_mesocycle_ranges = self.database.get_mesocycle_range(nearest_mesocycle[0][0])

            self.total_volume = round(float(self.database.get_total_volume(
                id_user=    self.settings.current_user, 
                start_ts=   current_mesocycle_ranges[0][0], 
                end_ts=     current_mesocycle_ranges[0][1],
                get_planned=False
            )[0][0]), ndigits=2)

            planned_volume = round(float(self.database.get_total_volume(
                id_user=    self.settings.current_user, 
                start_ts=   current_mesocycle_ranges[0][0], 
                end_ts=     current_mesocycle_ranges[0][1],
                get_planned=True
            )[0][0]), ndigits=2) 
            planned_volume = planned_volume if planned_volume != 0 else 1

            self.percentage_of_completion = round((self.total_volume / planned_volume) * 100, ndigits=2)


            self.workouts_count = int(self.database.get_workouts_count(
                id_user=    self.settings.current_user, 
                start_ts=   current_mesocycle_ranges[0][0], 
                end_ts=     current_mesocycle_ranges[0][1]
            )[0][0])


            self.workout_avg_duration = round(float(self.database.get_workout_avg_duration(
                id_user=    self.settings.current_user, 
                start_ts=   current_mesocycle_ranges[0][0], 
                end_ts=     current_mesocycle_ranges[0][1]
            )[0][0]), ndigits=2)


        return {
            "total_volume"          : self.total_volume,
            "workouts_count"        : self.workouts_count,
            "workout_avg_duration"  : self.workout_avg_duration
        }
    

    
    def get_current_mesocycle_and_microcycle(self):
        # Текущий мезоцикл (по времени)
        nearest_mesocycle = self.database.determine_nearest_mesocycle(
            time=int(datetime.datetime.now().timestamp()), 
            id_user=self.settings.current_user
        )
        if nearest_mesocycle == []:
            self.id_current_mesocycle  = 0
            return
        self.id_current_mesocycle = int(nearest_mesocycle[0][0])


        # Текущий микроцикл (по времени)
        nearest_microcyle = self.database.determine_nearest_microcycle(
            time=int(datetime.datetime.now().timestamp()), 
            id_mesocycle=self.id_current_mesocycle
        )
        if nearest_microcyle == []:
            self.id_current_microcycle = 0
            return
        self.id_current_microcycle = int(nearest_microcyle[0][0])



    def calculate_agonists_involvement(self):
        if (self.id_current_mesocycle is None) and (self.id_current_microcycle is None):
            self.get_current_mesocycle_and_microcycle()

        if self.id_current_microcycle is not None and self.agonists_involvement_table == []:
            self.agonists_involvement_table = self.database.get_agonists_involvement_by_microcycle(
                id_microcycle=self.id_current_microcycle
            )


    def determine_agonist_involvement_level(self, id_agonist: int):
        def get_involvement_level(sets: int):
            if sets <= 0:
                return None
            
            if 1 <= sets and sets <= 5:
                return ("low", sets)
            
            if 6 <= sets and sets <= 10:
                return ("medium", sets)
            
            if 11 <= sets and sets <= 15:
                return ("good", sets)

            if 16 <= sets:
                return ("great", sets)
        
        # Проверка на наличие тренировочных данных
        self.calculate_agonists_involvement()

        
        for agonist in self.agonists_involvement_table:
            agonist_id   = agonist[0]
            agonist_slug = agonist[1]
            agonist_sets = agonist[2]

            if id_agonist == agonist_id:
                return get_involvement_level(sets=agonist_sets)

        return None
    


    def get_best_and_current_workout_streak(self):
        all_workouts = self.database.get_all_workouts(id_user=self.settings.current_user)

        current_streak  = []
        best_streak     = []


        for workout in all_workouts:
            id_workout       = workout[0]
            workout_status   = workout[1]
            datetime_workout = workout[2]

            if workout_status in ['in_progress', 'completed', 'partially_completed', 'overcompleted']:
                # Добавляю только дату тренировки в информацию о текущей серии
                current_streak.append(datetime_workout)

                if len(current_streak) > len(best_streak):
                    best_streak = [*current_streak]

            else:
                current_streak.clear()

            
        if (current_streak != []):
            self.length_current_streak      = len(current_streak)
            self.date_range_current_streak  = [current_streak[0], current_streak[-1]]

        if (best_streak != []):
            self.length_best_streak         = len(best_streak)
            self.date_range_best_streak     = [best_streak[0], best_streak[-1]]



    def get_workout_volume(self, id_workout: int):
        workout_info = self.database.get_workout_info(id_workout=id_workout)

        workout_start_time  = workout_info[0][3]
        workout_end_time    = workout_info[0][4]

        workout_planned_volume = round(self.database.get_total_volume(
            id_user=self.settings.current_user,
            start_ts=workout_start_time,
            end_ts=workout_end_time,
            get_planned=True
        )[0][0], ndigits=2)

        workout_actual_volume = round(self.database.get_total_volume(
            id_user=self.settings.current_user,
            start_ts=workout_start_time,
            end_ts=workout_end_time,
            get_planned=False
        )[0][0], ndigits=2)


        return {
            "workout_planned_volume" : workout_planned_volume,
            "workout_actual_volume" : workout_actual_volume
        }

        
