import sqlite3
import os

import utils



def get_app_data_dir() -> str:
    """Возвращает приватную директорию приложения (Android/Windows/Linux)"""
    return os.path.dirname(os.path.abspath(__file__))



class Database:
    def __init__(self):
        base_dir = get_app_data_dir()
        self.db_path = os.path.join(base_dir, "CycleDatabase.db")

        try:
            if not os.path.exists(self.db_path):
                sqlite3.connect(self.db_path, check_same_thread=False)
                
                with sqlite3.connect(self.db_path, check_same_thread=False) as conn:
                    cur  = conn.cursor()

                    # Создание базы данных (если не существует)
                    with open(utils.resource_path(r"assets/database/Requests/Creating a database.sql"), encoding='UTF-8') as file:
                        create_database_request = file.read()
                    cur.executescript(create_database_request)
                    

                    # Вставка первичных данных (если данных нет в таблице)
                    with open(utils.resource_path(r"assets/database/Requests/Inserting data/Inserting initial data.sql"), encoding='UTF-8') as file:
                        inserting_initial_data_request = file.read()
                    cur.executescript(inserting_initial_data_request)

        except Exception as _ex:
            self._exception = _ex


    def __insertion_secondary_data__(self, insert_agonists: bool, insert_exercises: bool):
        try:
            with sqlite3.connect(self.db_path, check_same_thread=False) as conn:
                cur  = conn.cursor()

                # Вставка вторичных данных (если данных нет в таблице)                    
                    # Вставка мышц-агонистов
                if insert_agonists:
                    with open(utils.resource_path(r"assets/database/Requests/Inserting data/Inserting agonists.sql"), encoding='UTF-8') as file:
                        inserting_agonists_data_request = file.read()
                    cur.executescript(inserting_agonists_data_request)
                    
                    # Вставка упражнений
                if insert_exercises:
                    with open(utils.resource_path(r"assets/database/Requests/Inserting data/Inserting exercices.sql"), encoding='UTF-8') as file:
                        inserting_exercices_data_request = file.read()
                    cur.executescript(inserting_exercices_data_request)

        except Exception as _ex:
            self._exception = _ex
            return _ex



    def __select_request__(self, request_string: str) -> list:        
        try:
            with sqlite3.connect(self.db_path, check_same_thread=False) as conn:
                cur  = conn.cursor()
                cur.execute(request_string)

                result = cur.fetchall()
                if isinstance(result, Exception):
                    raise result
                
                return result 

        except Exception as _ex:
            self._exception = _ex
            raise _ex
        

    def __insert_request__(self, request_string: str, data: list) -> None:   
        if not isinstance(data, list) :
            raise TypeError("Invalid data type for insertion.")

        try:
            with sqlite3.connect(self.db_path, check_same_thread=False) as conn:
                cur  = conn.cursor()
                cur.executemany(request_string, data)

        except Exception as _ex:
            self._exception = _ex
            raise _ex


    def __execute_request__(self, request_string: str):
        try:
            with sqlite3.connect(self.db_path, check_same_thread=False) as conn:
                cur  = conn.cursor()
                cur.execute(request_string)

        except Exception as _ex:
            self._exception = _ex
            raise _ex




    def insert_user(self, name: str, phone: str = "") -> None:
        """
        Method for creating a new user
        Parameters:
            user_info: [Name, Phone]
        """

        if name is None:
            raise TypeError("Invalid data to insert")
        
        user_info = [1, name, phone] # 1 - статус Активен

        request = f"""
            INSERT INTO users(id_user_status, username, phone) 
            VALUES ({user_info[0]}, '{user_info[1]}', '{user_info[2]}')
        """

        self.__execute_request__(request)

    
    def get_users(self, id_user: int | None = None, id_user_status: int | None = None):
        """
        Method for get the list of users.\n
        Info: (id_user, id_user_status, username, phone)\n
        Sorted by 'id_user' ASC\n
        Will be return one user by 'id_user' if it is not None.
        """

        request = f"""
            SELECT  id_user, id_user_status, username, phone
            FROM    users
            ORDER BY id_user ASC
        """

        if id_user is not None:
            request = f"""
                SELECT  id_user, id_user_status, username, phone
                FROM    users
                WHERE   id_user = {id_user}
                ORDER BY id_user ASC
        """
        elif id_user_status is not None:
            request = f"""
                SELECT  id_user, id_user_status, username, phone
                FROM    users
                WHERE   id_user_status = {id_user_status}
                ORDER BY id_user ASC
        """
        
        return self.__select_request__(request)
    

    def delete_user(self, id_user: int):
        """
        Method for deleting the user
        """

        request = f"""
            DELETE FROM users
            WHERE id_user = {id_user}
        """

        self.__execute_request__(request)
    


    def get_user_statuses(self, id_user_status: int | None = None):
        """
        Method for get the list of user statuses.\n
        Info: (id_user_status, slug)\n
        Sorted by 'id_user_status' ASC\n
        Will be return one user status by 'id_user_status' if it is not None.
        """

        request = f"""
            SELECT  id_user_status, slug
            FROM    user_status
            ORDER BY id_user_status ASC
        """

        if id_user_status is not None:
            request = f"""
            SELECT  id_user_status, slug
            FROM    user_status
            WHERE   id_user_status = {id_user_status}
        """
        
        return self.__select_request__(request)

    
    def get_exercises(self, id_workout_type: int | None = None, id_exercise: int | None = None):
        """
        Method for get the list of exercises (by the 'id_workout_type' if it's not None).\n
        Info: (id_exercise, slug)\n
        Sorted by 'ex.id_exercise' ASC
        """

        request = """
            SELECT DISTINCT id_exercise, slug
            FROM exercises

            ORDER BY id_exercise ASC
        """

        if id_workout_type is not None:
            request = f"""
                SELECT DISTINCT ex.id_exercise, ex.slug

                FROM exercises AS ex
                JOIN agonist_exercises AS ae ON ae.id_exercise = ex.id_exercise
                JOIN target_muscles AS tm ON tm.id_agonist = ae.id_agonist
                JOIN workout_type AS wtype ON wtype.id_workout_type = tm.id_workout_type

                WHERE wtype.id_workout_type = {id_workout_type}

                ORDER BY ex.id_exercise ASC
            """
        elif id_exercise is not None:
            request = f"""
                SELECT DISTINCT id_exercise, slug
                FROM exercises

                WHERE id_exercise = {id_exercise}
            """

        return self.__select_request__(request)
    

    def get_agonists(self, id_exercise: int | None = None, id_agonist: int | None = None):
        """
        Method for get the list of agonists of the exercise. Sorted by 'ae.id_agonist' ASC.\n
        Info: (id_agonist, slug)\n
        If 'id_exercise' is None: return all agonists, sorted by 'id_agonist'.
        """
        
        request = f"""
            SELECT id_agonist, slug
            FROM agonists

            ORDER BY id_agonist ASC
        """

        
        if id_exercise is not None:
            request = f"""
                SELECT a.id_agonist, a.slug
                FROM agonists AS a
                JOIN agonist_exercises AS ae ON ae.id_agonist = a.id_agonist

                WHERE ae.id_exercise = {id_exercise}
            """
        elif id_agonist is not None:
            request = f"""
                SELECT id_agonist, slug
                FROM agonists

                WHERE id_agonist = {id_agonist}
            """


        return self.__select_request__(request)

    
    def delete_agonist_exercises(self, id_exercise: int):
        """
        Method for deleting all agonists of the exercise.
        """
        
        request = f"""
            DELETE FROM 
                agonist_exercises
            WHERE
                id_exercise = {id_exercise}
        """

        self.__execute_request__(request)

    

    def get_workout_types(self, id: int | None = None, slug: str | None = None, id_agonist: int | None = None):
        """
        Method for get the information\n
        (id_workout_type, slug)\n
        of the workout types.\nSorted by 'id_workout_type' ASC
        """

        request = f"""
            SELECT id_workout_type, slug
            FROM workout_type
            ORDER BY id_workout_type ASC
        """
        
        if id is not None:
            request = f"""
                SELECT id_workout_type, slug
                FROM workout_type
                WHERE id_workout_type = {id}
            """
        elif slug is not None:
            request = f"""
                SELECT id_workout_type, slug
                FROM workout_type
                WHERE slug = '{slug}'
            """
        elif id_agonist is not None:
            request = f"""
                SELECT wtype.id_workout_type, wtype.slug
                FROM workout_type AS wtype
                JOIN target_muscles AS tm ON tm.id_workout_type = wtype.id_workout_type
                WHERE tm.id_agonist = {id_agonist}
            """

        return self.__select_request__(request)


    def delete_target_muscles(self, id_agonist: int):
        """
        Method for deleting all workout types of the agonist.
        """
        
        request = f"""
            DELETE FROM 
                target_muscles
            WHERE
                id_agonist = {id_agonist}
        """

        self.__execute_request__(request)
    

    def get_hypertrophy_types(self, id: int | None = None, slug: str | None = None):
        """
        Method for get the information\n
        (id_hypertrophy_type, slug)\n
        of the hypertrophy types.\n
        Sorted by 'id_hypertrophy_type' ASC
        """
        request = f"""
            SELECT id_hypertrophy_type, slug
            FROM hypertrophy_type
            ORDER BY id_hypertrophy_type ASC
        """
        
        if id is not None:
            request = f"""
                SELECT id_hypertrophy_type, slug
                FROM hypertrophy_type
                WHERE id_hypertrophy_type = {id}
            """

        elif slug is not None:
            request = f"""
                SELECT id_hypertrophy_type, slug
                FROM hypertrophy_type
                WHERE slug = '{slug}'
            """


        return self.__select_request__(request)
    

    def get_workout_statuses(self, id_workout_status: int | None = None,  status_slug: str | None = None, id_workout: int | None = None):
        """
        A method for get a list of workout statuses.\n
        (id_workout_status, slug)\n
        If status_slug is not None, it returns only the ID of this status.
        """

        request = """
            SELECT id_workout_status, slug
            FROM workout_status

            ORDER BY id_workout_status ASC
        """

        if id_workout_status is not None:
            request = f"""
                SELECT id_workout_status, slug
                FROM workout_status

                WHERE id_workout_status = {id_workout_status}
            """

        elif status_slug is not None:
            request = f"""
                SELECT id_workout_status, slug
                FROM workout_status

                WHERE slug = '{status_slug}'
            """
        elif id_workout is not None:
            request = f"""
                SELECT ws.id_workout_status, ws.slug
                FROM workout_status AS ws
                JOIN workouts AS wt ON wt.id_workout_status = ws.id_workout_status

                WHERE wt.id_workout = {id_workout}
            """


        return self.__select_request__(request)



    def get_workout_template_info(self, id: int):
        """
        Method for get the information\n
        (wt.slug, wtype.slug, htype.slug)\n
        of the workout template by 'id_workout_template'
        """

        request = f"""
            SELECT wt.slug, wtype.slug, htype.slug
            FROM workout_templates  AS wt
            JOIN workout_type       AS wtype ON wtype.id_workout_type = wt.id_workout_type
            JOIN hypertrophy_type   AS htype ON htype.id_hypertrophy_type = wt.id_hypertrophy_type
            
            WHERE id_workout_template = {id}
        """

        return self.__select_request__(request)


    def get_workout_templates(self):
        """
        Method for get the list of the workout templates. Sorted by 'id_workout_template' ASC
        """
        request = f"""
            SELECT id_workout_template, slug, id_workout_type, id_hypertrophy_type
            FROM workout_templates
            ORDER BY id_workout_template ASC
        """

        return self.__select_request__(request)
    

    def delete_workout_template(self, id: int, delete_workout_template: bool = True):
        """
        Method for delete the records of the tables 'workout_templates' and 'workout_template_composition'
        """

        request = f"""
            DELETE FROM workout_template_composition 
            WHERE id_workout_template = {id}
        """
        self.__execute_request__(request)

        if delete_workout_template:
            request = f"""
                DELETE FROM workout_templates 
                WHERE id_workout_template = {id}
            """
            self.__execute_request__(request)


    def get_microcycle_templates(self):
        """
        Method for get the list of the microcycle templates. Sorted by 'id_microcycle_template' ASC
        """
        request = f"""
            SELECT id_microcycle_template, title, slug
            FROM microcycle_templates
            ORDER BY id_microcycle_template ASC
        """

        return self.__select_request__(request)


    def get_microcycle_template_info(self, id: int):
        """
        Method for get the information 

        (mt.id_microcycle_template, mt.slug, 
        wt.id_workout_template, wt.slug, wt.id_workout_type, wt.id_hypertrophy_type) 

        of the microcycle template by 'id_microcycle_template'. Sorted by 'mtc.id_composition' ASC
        """

        request = f"""
            SELECT 
                mt.id_microcycle_template, mt.slug, 
                wt.id_workout_template, wt.slug, wt.id_workout_type, wt.id_hypertrophy_type
            FROM microcycle_templates AS mt
            JOIN microcycle_template_composition AS mtc ON mtc.id_microcycle_template = mt.id_microcycle_template
            JOIN workout_templates AS wt ON wt.id_workout_template = mtc.id_workout_template

            WHERE mt.id_microcycle_template = {id}
            
            ORDER BY mtc.id_composition ASC
        """

        return self.__select_request__(request)
    

    def get_microcycle_workout_templates(self, id_microcycle_template: int):
        """
        Method for get the workout templates information 

        (wt.id_workout_template) 

        by id_microcycle. Sorted by 'mtc.id_composition' ASC
        """

        request = f"""
            SELECT mtc.id_workout_template
            FROM microcycle_template_composition AS mtc
            WHERE id_microcycle_template = {id_microcycle_template}

            ORDER BY mtc.id_composition ASC
        """

        return self.__select_request__(request)
    

    def get_workout_template_exercises(self, id_workout_template: int):
        """
        Method for get the information 

        (ex.id_exercise, ex.slug) 

        of the exercises of template by 'id_workout_template'. Sorted by 'wtc.id_composition' ASC
        """

        request = f"""
            SELECT ex.id_exercise, ex.slug
            FROM workout_templates AS wt
            JOIN workout_template_composition   AS wtc  ON wtc.id_workout_template  = wt.id_workout_template
            JOIN exercises                      AS ex   ON ex.id_exercise           = wtc.id_exercise

            WHERE wt.id_workout_template = {id_workout_template}
            ORDER BY wtc.id_composition ASC
        """

        return self.__select_request__(request)
    

    def delete_microcycle_template(self, id: int, delete_microcycle_template: bool = True):
        """
        Method for delete the records of the tables 'microcycle_templates' and 'microcycle_template_composition'
        """

        request = f"""
            DELETE FROM microcycle_template_composition 
            WHERE id_microcycle_template = {id}
        """
        self.__execute_request__(request)

        if delete_microcycle_template:
            request = f"""
                DELETE FROM microcycle_templates 
                WHERE id_microcycle_template = {id}
            """
            self.__execute_request__(request)


    def get_macrocycles(self, id_user: int):
        """
        Method for get the information 

        (id_macrocycle) 

        of the mesocycles by 'id_user'. Sorted by 'id_macrocycle' ASC
        """

        request = f"""
            SELECT id_macrocycle
            FROM macrocycles

            WHERE id_user = {id_user}
            ORDER BY id_macrocycle ASC
        """

        return self.__select_request__(request)


    def get_mesocycles(self, id_user: int, id_macrocycle: int | None = None):
        """
        Method for get the information 

        (id_mesocycle, id_macrocycle) 

        of the mesocycles by 'id_user'. Sorted by 'id_mesocycle' ASC
        """

        request = f"""
            SELECT id_mesocycle, id_macrocycle
            FROM mesocycles

            WHERE id_user = {id_user}
            ORDER BY id_mesocycle ASC
        """

        if id_macrocycle is not None:
            request = f"""
                SELECT id_mesocycle
                FROM mesocycles

                WHERE id_macrocycle = {id_macrocycle}
                ORDER BY id_mesocycle ASC
            """
        

        return self.__select_request__(request)
    

    def get_mesocycle_workout_statuses(self, id_user: int, id_mesocycle: int | None = None):
        """
        Method for get the workout statuses

        (ws.id_workout_status, ws.slug, COUNT(ws.id_workout_status)) 

        by 'id_mesocycle' (all statuses if 'id_mesocycle' is None). Sorted by 'ws.id_workout_status' ASC
        """

        request = f"""
            SELECT ws.id_workout_status, ws.slug, COUNT(ws.id_workout_status)
            FROM mesocycles     AS ms
            JOIN microcycles    AS mc   ON mc.id_mesocycle      = ms.id_mesocycle
            JOIN workouts       AS wt   ON wt.id_microcycle     = mc.id_microcycle
            JOIN workout_status AS ws   ON ws.id_workout_status = wt.id_workout_status

            WHERE ms.id_user = {id_user}

            GROUP BY ws.id_workout_status
            ORDER BY ws.id_workout_status ASC
        """

        if id_mesocycle is not None:
            request = f"""
                SELECT ws.id_workout_status, ws.slug, COUNT(ws.id_workout_status)
                FROM mesocycles     AS ms
                JOIN microcycles    AS mc   ON mc.id_mesocycle      = ms.id_mesocycle
                JOIN workouts       AS wt   ON wt.id_microcycle     = mc.id_microcycle
                JOIN workout_status AS ws   ON ws.id_workout_status = wt.id_workout_status
                
                WHERE ms.id_mesocycle = {id_mesocycle}

                GROUP BY ws.id_workout_status
                ORDER BY ws.id_workout_status ASC
            """


        return self.__select_request__(request)
    

    def get_mesocycle_range(self, id_mesocycle: int | None = None):
        """
        Method for get the start datetime and end datetime of mesocycle

        (MIN(wt.planned_workout_start_datetime), MAX(wt.planned_workout_end_datetime)) 

        by 'id_mesocycle' (all mesocycles if 'id_mesocycle' is None). Sorted by 'ms.id_mesocycle' ASC
        """

        request = f"""
            SELECT ms.id_mesocycle, MIN(wt.planned_workout_start_datetime), MAX(wt.planned_workout_end_datetime)
            FROM mesocycles     AS ms
            JOIN microcycles    AS mc   ON mc.id_mesocycle      = ms.id_mesocycle
            JOIN workouts       AS wt   ON wt.id_microcycle     = mc.id_microcycle

            GROUP BY ms.id_mesocycle
            ORDER BY ms.id_mesocycle ASC
        """

        if id_mesocycle is not None:
            request = f"""
                SELECT MIN(wt.planned_workout_start_datetime), MAX(wt.planned_workout_end_datetime)
                FROM mesocycles     AS ms
                JOIN microcycles    AS mc   ON mc.id_mesocycle      = ms.id_mesocycle
                JOIN workouts       AS wt   ON wt.id_microcycle     = mc.id_microcycle

                WHERE ms.id_mesocycle = {id_mesocycle}

                GROUP BY ms.id_mesocycle
            """

        return self.__select_request__(request)
    

    def create_mesocycle(self, id_user: int):
        """
        Method for creating mesocycle record in database.
        """

        request = f"""
            INSERT INTO 
                mesocycles (id_user)
            VALUES
                ({id_user})
        """

        self.__execute_request__(request)


    def update_mesocycle(self, id_mesocycle: int, id_macrocycle: int | None):
        """
        Method for updating mesocycle record by rewrite 'id_macrocycle' field.
        """

        request = f"""
            UPDATE 
                mesocycles
            SET
                id_macrocycle = {id_macrocycle if id_macrocycle != 0 else 'NULL'}
            WHERE
                id_mesocycle = {id_mesocycle}
        """
        self.__execute_request__(request)
    

    def delete_mesocycle(self, id_mesocycle: int):
        """
        Method for deleting mesocycle by 'id_mesocycle'
        """

        request = f"""
            DELETE FROM mesocycles
            WHERE id_mesocycle = {id_mesocycle}
        """

        self.__execute_request__(request)


    def create_macrocycle(self, id_user: int):
        """
        Method for creating macrocycle record in database.
        """

        request = f"""
            INSERT INTO 
                macrocycles (id_user)
            VALUES
                ({id_user})
        """

        self.__execute_request__(request)


    def delete_macrocycle(self, id_macrocycle: int):
        """
        Method for deleting macrocycle by 'id_macrocycle'
        """

        request = f"""
            DELETE FROM macrocycles
            WHERE id_macrocycle = {id_macrocycle}
        """

        self.__execute_request__(request)

    
    def get_macrocycle_range(self, id_macrocycle: int | None = None):
        """
        Method for get the start datetime and end datetime of macrocycle

        (MIN(wt.planned_workout_start_datetime), MAX(wt.planned_workout_end_datetime)) 

        by 'id_macrocycle' (all macrocycles if 'id_macrocycle' is None). Sorted by 'mac.id_macrocycle' ASC
        """

        request = f"""
            SELECT mac.id_macrocycle, MIN(wt.planned_workout_start_datetime), MAX(wt.planned_workout_end_datetime)
            FROM macrocycles    AS mac
            JOIN mesocycles     AS ms   ON ms.id_macrocycle     = mac.id_macrocycle
            JOIN microcycles    AS mc   ON mc.id_mesocycle      = ms.id_mesocycle
            JOIN workouts       AS wt   ON wt.id_microcycle     = mc.id_microcycle

            GROUP BY mac.id_macrocycle
            ORDER BY mac.id_macrocycle ASC
        """

        if id_macrocycle is not None:
            request = f"""
                SELECT MIN(wt.planned_workout_start_datetime), MAX(wt.planned_workout_end_datetime)
                FROM macrocycles    AS mac
                JOIN mesocycles     AS ms   ON ms.id_macrocycle     = mac.id_macrocycle
                JOIN microcycles    AS mc   ON mc.id_mesocycle      = ms.id_mesocycle
                JOIN workouts       AS wt   ON wt.id_microcycle     = mc.id_microcycle

                WHERE mac.id_macrocycle = {id_macrocycle}

                GROUP BY mac.id_macrocycle
            """

        return self.__select_request__(request)
    

    def get_macrocycle_workout_statuses(self, id_user: int, id_macrocycle: int | None = None):
        """
        Method for get the workout statuses

        (ws.id_workout_status, ws.slug, COUNT(ws.id_workout_status)) 

        by 'id_macrocycle' (all statuses if 'id_macrocycle' is None). Sorted by 'ws.id_workout_status' ASC
        """

        request = f"""
            SELECT ws.id_workout_status, ws.slug, COUNT(ws.id_workout_status)
            FROM macrocycles    AS mac
            JOIN mesocycles     AS ms   ON ms.id_macrocycle     = mac.id_macrocycle
            JOIN microcycles    AS mc   ON mc.id_mesocycle      = ms.id_mesocycle
            JOIN workouts       AS wt   ON wt.id_microcycle     = mc.id_microcycle
            JOIN workout_status AS ws   ON ws.id_workout_status = wt.id_workout_status

            WHERE mac.id_user = {id_user}

            GROUP BY ws.id_workout_status
            ORDER BY ws.id_workout_status ASC
        """

        if id_macrocycle is not None:
            request = f"""
                SELECT ws.id_workout_status, ws.slug, COUNT(ws.id_workout_status)
                FROM macrocycles    AS mac
                JOIN mesocycles     AS ms   ON ms.id_macrocycle     = mac.id_macrocycle
                JOIN microcycles    AS mc   ON mc.id_mesocycle      = ms.id_mesocycle
                JOIN workouts       AS wt   ON wt.id_microcycle     = mc.id_microcycle
                JOIN workout_status AS ws   ON ws.id_workout_status = wt.id_workout_status
                
                WHERE mac.id_macrocycle = {id_macrocycle}

                GROUP BY ws.id_workout_status
                ORDER BY ws.id_workout_status ASC
            """


        return self.__select_request__(request)



    def insert_microcycle(self, id_mesocycle: int, is_unloading: bool = False):
        """
        Method for create new microcycle record
        """

        request = f"""
            INSERT INTO 
                microcycles (id_mesocycle, is_unloading)
            VALUES
                ({id_mesocycle}, {int(is_unloading)})
        """

        self.__execute_request__(request)


    def update_microcycle(self, id_microcycle: int, is_unloading: bool):
        """
        Method for change value of microcycle: 'is_unloading'
        """

        request = f"""
            UPDATE 
                microcycles
            SET
                is_unloading = {int(is_unloading)}
            WHERE 
                id_microcycle = {id_microcycle}
        """

        self.__execute_request__(request)


    def delete_microcycle(self, id_microcycle: int):
        """
        Method for deleting record of microcycle
        """

        request = f"""
            DELETE FROM 
                microcycles
            WHERE 
                id_microcycle = {id_microcycle}
        """

        self.__execute_request__(request)

    

    def insert_workout(self, id_microcycle: int, id_workout_template: int, id_workout_status: int):
        """
        Method for create new workout record
        """

        request = f"""
            INSERT INTO 
                workouts (
                id_microcycle, 
                id_workout_template, 
                id_workout_status, 
                planned_workout_start_datetime, 
                planned_workout_end_datetime,
                actual_workout_start_datetime,
                actual_workout_end_datetime
            )
            VALUES
                ({id_microcycle}, {id_workout_template}, {id_workout_status}, 0, 0, 0, 0)
        """

        self.__execute_request__(request)


    def update_workout_datetime(self, id_workout: int, field_name: str, workout_datetime: int):
        """
        Method for update datetime of workout.\n
        Available fields: \n
            'planned_workout_start_datetime', \n
            'planned_workout_end_datetime',\n
            'actual_workout_start_datetime',\n
            'actual_workout_end_datetime'
        """

        available_fields = [
            'planned_workout_start_datetime', 
            'planned_workout_end_datetime',
            'actual_workout_start_datetime',
            'actual_workout_end_datetime'
        ]

        if field_name not in available_fields:
            raise ValueError("Unavailable field name")
        
        request = f"""
            UPDATE  
                workouts
            SET
                {field_name} = {workout_datetime}
            WHERE
                id_workout = {id_workout}
        """

        self.__execute_request__(request)
    

    def get_all_workout_datetimes(self, id_workout: int):
        """
        Method for get all datetimes of workout.\n
        Available fields: \n
            'planned_workout_start_datetime', \n
            'planned_workout_end_datetime',\n
            'actual_workout_start_datetime',\n
            'actual_workout_end_datetime'
        """

        request = f"""
            SELECT  
                planned_workout_start_datetime, 
                planned_workout_end_datetime, 
                actual_workout_start_datetime, 
                actual_workout_end_datetime
            FROM    
                workouts
            WHERE   
                id_workout = {id_workout}
        """

        return self.__select_request__(request)
            


    def get_microcycles(self, id_mesocycle: int, id_microcycle: int | None = None):
        """
        Method for get all microcycles. Sorted by 'id_microcycle' ASC
        """

        request = f"""
            SELECT id_microcycle, is_unloading
            FROM microcycles
            
            WHERE id_mesocycle = {id_mesocycle}
            ORDER BY id_microcycle ASC
        """

        if id_microcycle is not None:
            request = f"""
            SELECT id_microcycle, is_unloading
            FROM microcycles
            
            WHERE id_mesocycle = {id_mesocycle} AND id_microcycle = {id_microcycle}
            ORDER BY id_microcycle ASC
        """

        return self.__select_request__(request)



    def create_workout_composition(
        self, 
        id_workout: int, 
        id_exercise: int, 
        reps: int | None = None, 
        weight: float | int | None = None, 
        planned_reps: int | None = None, 
        planned_weight: float | int | None = None
    ):
        """
        Method for creating an exercise entry in a workout. \n
        Must insert 'planned_reps' and 'planned_weight' ONLY AFTER 'reps' and 'weight'. \n
        If 'planned_reps' or 'planned_weight' is None: 'reps' and 'weight' will be used instead.
        """
        if reps is None or weight is None:
            request = f"""
                INSERT INTO workout_composition (
                    id_workout,
                    id_exercise,
                    planned_repetitions,
                    planned_weight,
                    actual_repetitions,
                    actual_weight
                )
                VALUES
                    ({id_workout}, {id_exercise}, 0, 0, 0, 0)
            """
        else:
            if planned_reps is None or planned_weight is None:
                request = f"""
                    INSERT INTO workout_composition (
                        id_workout,
                        id_exercise,
                        planned_repetitions,
                        planned_weight,
                        actual_repetitions,
                        actual_weight
                    )
                    VALUES
                        ({id_workout}, {id_exercise}, {reps}, {weight}, {reps}, {weight})
                """
            else:
                request = f"""
                    INSERT INTO workout_composition (
                        id_workout,
                        id_exercise,
                        planned_repetitions,
                        planned_weight,
                        actual_repetitions,
                        actual_weight
                    )
                    VALUES
                        ({id_workout}, {id_exercise}, {planned_reps}, {planned_weight}, {reps}, {weight})
                """

        self.__execute_request__(request)
    
    
    def delete_workout_composition(self, id_workout: int):
        """
        Method for deleting all sets of workout by 'id_workout'
        """

        request = f"""
            DELETE FROM
                workout_composition
            WHERE 
                id_workout = {id_workout}
        """

        self.__execute_request__(request)

    
    def update_workout_composition(self, id_workout: int, field_name: str, value: int | float):
        """
        Method for change the information of exercise entry in a workout.
        Available field:
            'planned_repetitions',
            'planned_weight',
            'actual_repetitions',
            'actual_weight'
        """

        available_fields = [
            'planned_repetitions',
            'planned_weight',
            'actual_repetitions',
            'actual_weight'
        ]
        
        if field_name not in available_fields:
            raise ValueError("Incorrect 'field_name'")
        
        request = f"""
            UPDATE 
                workout_composition
            SET 
                '{field_name}' = {value}
            WHERE 
                id_workout = {id_workout}
        """

        self.__execute_request__(request)

    
    def update_workout_status(self, id_workout: int, id_status: int):
        """
        Method for change the information of workout status.
        """
        
        request = f"""
            UPDATE 
                workouts
            SET 
                id_workout_status = {id_status}
            WHERE 
                id_workout = {id_workout}
        """

        self.__execute_request__(request)

    
    def delete_workout_status(self, id_workout_status: int):
        """
        Method for deleting workout status
        """

        request = f"""
            DELETE FROM workout_status
            WHERE id_workout_status = {id_workout_status}
        """

        self.__execute_request__(request)


    def get_workouts(self, id_microcycle: int):
        """
        Method for obtaining workouts by 'id_microcycle'.\n
        Sorted by 'id_workout' ASC.\n
        Info: 'id_workout'
        """

        request = f"""
            SELECT id_workout
            FROM workouts
            WHERE id_microcycle = {id_microcycle}

            ORDER BY id_workout ASC
        """

        return self.__select_request__(request)
    

    def delete_workout(self, id_workout: int):
        """
        Method for deleting workout record
        """

        request = f"""
            DELETE FROM workouts
            WHERE id_workout = {id_workout}
        """

        self.__execute_request__(request)
    
    

    def get_workout_exercises(self, id_workout: int, get_planned: bool):
        """
        Method for obtaining exercises of workout by 'id_workout'.\n
        Sorted by 'id_composition' ASC.\n
        Fields: 
        \t if 'get_planned' is True.\n
        'wtc.id_composition, ex.id_exercise, ex.slug, wtc.planned_repetitions, wtc.planned_weight' \n
        \t if 'get_planned' is False.
        'wtc.id_composition, ex.id_exercise, ex.slug, wtc.actual_repetitions, wtc.actual_weight' \n
        """

        request = f"""
            SELECT wtc.id_composition, ex.id_exercise, ex.slug, wtc.actual_repetitions, wtc.actual_weight
            FROM workout_composition AS wtc
            JOIN exercises AS ex ON ex.id_exercise = wtc.id_exercise

            WHERE wtc.id_workout = {id_workout}
            ORDER BY ex.id_exercise ASC
        """

        if get_planned:
            request = f"""
                SELECT wtc.id_composition, ex.id_exercise, ex.slug, wtc.planned_repetitions, wtc.planned_weight
                FROM workout_composition AS wtc
                JOIN exercises AS ex ON ex.id_exercise = wtc.id_exercise

                WHERE wtc.id_workout = {id_workout}
                ORDER BY wtc.id_composition ASC
            """

        return self.__select_request__(request)
    


    def delete_workout_type(self, id_workout_type: int):
        """
        Method for deleting workout type record
        """

        request = f"""
            DELETE FROM workout_type
            WHERE id_workout_type = {id_workout_type}
        """

        self.__execute_request__(request)

    
    
    def delete_hypertrophy_type(self, id_hypertrophy_type: int):
        """
        Method for deleting hypertrophy type record
        """

        request = f"""
            DELETE FROM hypertrophy_type
            WHERE id_hypertrophy_type = {id_hypertrophy_type}
        """

        self.__execute_request__(request)


    def delete_agonist(self, id_agonist: int):
        """
        Method for deleting agonist record
        """

        request = f"""
            DELETE FROM agonists
            WHERE id_agonist = {id_agonist}
        """

        self.__execute_request__(request)


    def delete_exercise(self, id_exercise: int):
        """
        Method for deleting exercise record
        """

        request = f"""
            DELETE FROM exercises
            WHERE id_exercise = {id_exercise}
        """

        self.__execute_request__(request)


    def delete_user_status(self, id_user_status: int):
        """
        Method for deleting user status record
        """

        request = f"""
            DELETE FROM user_status
            WHERE id_user_status = {id_user_status}
        """

        self.__execute_request__(request)


    def determine_time_ranges_mesocycle(self, id_mesocycle: int | None = None, id_user: int | None = None):
        """
        Method for get the time ranges (planned start and planned end time) of mesocycle\n
        Info: msc.id_mesocycle, \n
            MIN(wt.planned_workout_start_datetime)  AS planned_start_time, \n
            MAX(wt.planned_workout_end_datetime)    AS planned_end_time
        """
        
        request = f"""
            SELECT 
                msc.id_mesocycle, 
                MIN(wt.planned_workout_start_datetime)  AS planned_start_time, 
                MAX(wt.planned_workout_end_datetime)    AS planned_end_time
            FROM mesocycles     AS msc
            JOIN microcycles    AS mcc  ON mcc.id_mesocycle = msc.id_mesocycle
            JOIN workouts       AS wt   ON wt.id_microcycle = mcc.id_microcycle

            GROUP BY msc.id_mesocycle
            ORDER BY planned_start_time ASC, planned_end_time ASC
        """

        if id_mesocycle is not None:
                    request = f"""
            SELECT 
                msc.id_mesocycle, 
                MIN(wt.planned_workout_start_datetime)  AS planned_start_time, 
                MAX(wt.planned_workout_end_datetime)    AS planned_end_time
            FROM mesocycles     AS msc
            JOIN microcycles    AS mcc  ON mcc.id_mesocycle = msc.id_mesocycle
            JOIN workouts       AS wt   ON wt.id_microcycle = mcc.id_microcycle

            WHERE msc.id_mesocycle = {id_mesocycle}
            GROUP BY msc.id_mesocycle
            ORDER BY planned_start_time ASC, planned_end_time ASC
        """
        elif id_user is not None:
            request = f"""
                SELECT 
                    msc.id_mesocycle, 
                    MIN(wt.planned_workout_start_datetime)  AS planned_start_time, 
                    MAX(wt.planned_workout_end_datetime)    AS planned_end_time
                FROM mesocycles     AS msc
                JOIN microcycles    AS mcc  ON mcc.id_mesocycle = msc.id_mesocycle
                JOIN workouts       AS wt   ON wt.id_microcycle = mcc.id_microcycle

                WHERE msc.id_user = {id_user}
                GROUP BY msc.id_mesocycle
                ORDER BY planned_start_time ASC, planned_end_time ASC
            """

        return self.__select_request__(request)


    
    def determine_nearest_mesocycle(self, time: int, id_user: int):
        """
        Method for get the nearest mesocycle of time parameter.
        Info: (id_mesocycle)
        """

        request = f"""
            WITH Planned_mesocycles_ranges AS (
                SELECT 
                    msc.id_mesocycle                        AS id_mesocycle, 
                    MIN(wt.planned_workout_start_datetime)  AS planned_start_time, 
                    MAX(wt.planned_workout_end_datetime)    AS planned_end_time
                FROM mesocycles     AS msc
                JOIN microcycles    AS mcc  ON mcc.id_mesocycle = msc.id_mesocycle
                JOIN workouts       AS wt   ON wt.id_microcycle = mcc.id_microcycle

                WHERE msc.id_user = {id_user}
                GROUP BY msc.id_mesocycle
                ORDER BY planned_start_time ASC, planned_end_time ASC
            )


            SELECT  msc.id_mesocycle
            FROM    mesocycles                 AS msc
            JOIN    Planned_mesocycles_ranges  AS pmr ON pmr.id_mesocycle = msc.id_mesocycle

            WHERE   id_user = {id_user}
            ORDER BY 
                    MIN(
                        ABS(pmr.planned_start_time  - {time}), 
                        ABS(pmr.planned_end_time    - {time})
                    ) ASC
            LIMIT 1
        """

        return self.__select_request__(request)



    def determine_time_ranges_microcycle(self, id_mesocycle: int | None = None):
        """
         Method for get the time ranges (planned start and planned end time) of microcycles by 'id_mesocycle'\n
         Info: mcc.id_microcycle, \n
            MIN(wt.planned_workout_start_datetime)  AS planned_start_time, \n
            MAX(wt.planned_workout_end_datetime)    AS planned_end_time
        """ 

        request = f"""
            SELECT 
                mcc.id_microcycle, 
                MIN(wt.planned_workout_start_datetime)  AS planned_start_time, 
                MAX(wt.planned_workout_end_datetime)    AS planned_end_time
            FROM microcycles    AS mcc
            JOIN workouts       AS wt   ON wt.id_microcycle = mcc.id_microcycle

            GROUP BY mcc.id_microcycle
            ORDER BY planned_start_time ASC, planned_end_time ASC
        """

        if id_mesocycle is not None:
            request = f"""
                SELECT 
                    mcc.id_microcycle, 
                    MIN(wt.planned_workout_start_datetime)  AS planned_start_time, 
                    MAX(wt.planned_workout_end_datetime)    AS planned_end_time
                FROM microcycles    AS mcc
                JOIN workouts       AS wt   ON wt.id_microcycle = mcc.id_microcycle

                WHERE mcc.id_mesocycle = {id_mesocycle}
                GROUP BY mcc.id_microcycle
                ORDER BY planned_start_time ASC, planned_end_time ASC
            """

        return self.__select_request__(request)
    

    def determine_nearest_microcycle(self, time: int, id_mesocycle: int):
        """
        Method for get the nearest mesocycle of time parameter.
        Info: (id_mesocycle)
        """

        request = f"""
            WITH Planned_microcycles_ranges AS (
                SELECT 
                    mcc.id_microcycle                       AS id_microcycle, 
                    MIN(wt.planned_workout_start_datetime)  AS planned_start_time, 
                    MAX(wt.planned_workout_end_datetime)    AS planned_end_time
                FROM microcycles    AS mcc
                JOIN workouts       AS wt   ON wt.id_microcycle = mcc.id_microcycle

                WHERE mcc.id_mesocycle = {id_mesocycle}
                GROUP BY mcc.id_microcycle
                ORDER BY planned_start_time ASC, planned_end_time ASC
            )


            SELECT  mcc.id_microcycle
            FROM    microcycles                 AS mcc
            JOIN    Planned_microcycles_ranges  AS pmr ON pmr.id_microcycle = mcc.id_microcycle

            WHERE   mcc.id_mesocycle = {id_mesocycle}
            ORDER BY 
                    MIN(
                        ABS(pmr.planned_start_time  - {time}), 
                        ABS(pmr.planned_end_time    - {time})
                    ) ASC
            LIMIT 1
        """

        return self.__select_request__(request)
    

    def get_workouts_near_to_date(self, time: int, time_period: int):
        """
        Method for getting all workouts of all users with a time difference of no more than 'time_period' to 'time'\n
        Formula: \n (wt.actual_workout_start_datetime - {time}) >= time_period\n
        INFO: \n (wt.id_workout, users.username, wts.slug, wt.actual_workout_start_datetime, wt.actual_workout_end_datetime)
        """

        request = f"""
            SELECT wt.id_workout, users.username, wts.slug, wt.actual_workout_start_datetime, wt.actual_workout_end_datetime
            FROM workouts       AS wt
            JOIN workout_status AS wts  ON wts.id_workout_status = wt.id_workout_status
            JOIN microcycles    AS mcc  ON mcc.id_microcycle = wt.id_microcycle
            JOIN mesocycles     AS msc  ON msc.id_mesocycle  = mcc.id_mesocycle
            JOIN users                  ON users.id_user     = msc.id_user

            WHERE 
                (wt.actual_workout_start_datetime - {time}) >= 0 AND
                (wt.actual_workout_start_datetime - {time}) <= {time_period}

            ORDER BY wt.actual_workout_start_datetime ASC
        """

        return self.__select_request__(request)
    


    def update_workout_composition_by_id_composition(
            self, 
            id_composition: int, 
            reps: int | None = None, 
            weight: float | int | None = None,
            planned_reps: int | None = None, 
            planned_weight: float | int | None = None,
    ):
        """
        Method for update the workout composition with transferred values
        """

        planned_reps_string     = f"planned_repetitions   = {planned_reps}"     if planned_reps   is not None else ""
        planned_weight_string   = f"planned_weight        = {planned_weight}"   if planned_weight is not None else ""
        actual_reps_string      = f"actual_repetitions    = {reps}"             if reps           is not None else ""
        actual_weight_string    = f"actual_weight         = {weight}"           if weight         is not None else ""

        set_strings_list = [planned_reps_string, planned_weight_string, actual_reps_string, actual_weight_string]    
        set_string = ""

        for set_value_string in set_strings_list:
            if set_value_string != "":
                set_string += f", \n{set_value_string}" if (set_string != "") else set_value_string
            
        

        request = f"""
            UPDATE 
                workout_composition
            SET
                {set_string}
            WHERE
                id_composition = {id_composition}
        """

        self.__execute_request__(request)