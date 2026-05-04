-- Этот файл предназначен для графического отображение (подсветки синтаксиса) команд SQL.
-- Это позволит легче ориентироваться в командах и предотвращать ошибки в коде.
-- Файл служит для автоматического создания БД.


CREATE TABLE IF NOT EXISTS user_status (
    id_user_status INTEGER PRIMARY KEY AUTOINCREMENT,
    title          TEXT(50) NOT NULL,
    slug           TEXT(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    id_user         INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user_status  INTEGER NOT NULL,
    username        TEXT(100) NOT NULL UNIQUE,
    phone           TEXT(50),

    FOREIGN KEY (id_user_status) REFERENCES user_status(id_user_status)
    ON UPDATE CASCADE
    ON DELETE NO ACTION
);



CREATE TABLE IF NOT EXISTS workout_status (
    id_workout_status   INTEGER PRIMARY KEY AUTOINCREMENT,
    title               TEXT(50) NOT NULL,
    slug                TEXT(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS workout_type (
    id_workout_type INTEGER PRIMARY KEY AUTOINCREMENT,
    title           TEXT(50) NOT NULL,
    slug            TEXT(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS hypertrophy_type (
    id_hypertrophy_type INTEGER PRIMARY KEY AUTOINCREMENT,
    title               TEXT(50) NOT NULL,
    slug                TEXT(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS agonists (
    id_agonist  INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT(50) NOT NULL,
    slug        TEXT(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS exercises (
    id_exercise INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT(100) NOT NULL,
    slug        TEXT(100) NOT NULL UNIQUE
);



CREATE TABLE IF NOT EXISTS agonist_exercises (
    id_agonist_exercise INTEGER PRIMARY KEY AUTOINCREMENT,
    id_agonist          INTEGER NOT NULL,
    id_exercise         INTEGER NOT NULL,

    FOREIGN KEY (id_agonist) REFERENCES agonists(id_agonist)
    ON UPDATE CASCADE
    ON DELETE CASCADE,

    FOREIGN KEY (id_exercise) REFERENCES exercises(id_exercise)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS one_rep_maximum (
    id_maximum      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_exercise     INTEGER NOT NULL,
    one_rep_weight  REAL NOT NULL,
    one_rep_date    INTEGER(15) NOT NULL,

    FOREIGN KEY (id_exercise) REFERENCES exercises(id_exercise)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);




CREATE TABLE IF NOT EXISTS target_muscles (
    id_muscle       INTEGER PRIMARY KEY AUTOINCREMENT,
    id_workout_type INTEGER NOT NULL,
    id_agonist      INTEGER NOT NULL,

    FOREIGN KEY (id_workout_type) REFERENCES workout_type(id_workout_type)
    ON UPDATE CASCADE
    ON DELETE NO ACTION,

    FOREIGN KEY (id_agonist) REFERENCES agonists(id_agonist)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);




CREATE TABLE IF NOT EXISTS workout_templates (
    id_workout_template INTEGER PRIMARY KEY AUTOINCREMENT,
    id_workout_type     INTEGER NOT NULL,
    id_hypertrophy_type INTEGER NOT NULL,
    title               TEXT(100) NOT NULL,
    slug                TEXT(100) NOT NULL UNIQUE,

    FOREIGN KEY (id_workout_type) REFERENCES workout_type(id_workout_type)
    ON UPDATE CASCADE
    ON DELETE NO ACTION,

    FOREIGN KEY (id_hypertrophy_type) REFERENCES hypertrophy_type(id_hypertrophy_type)
    ON UPDATE CASCADE
    ON DELETE NO ACTION
);


CREATE TABLE IF NOT EXISTS workout_template_composition (
    id_composition      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_workout_template INTEGER NOT NULL,
    id_exercise         INTEGER NOT NULL,

    FOREIGN KEY (id_workout_template) REFERENCES workout_templates(id_workout_template)
    ON UPDATE CASCADE
    ON DELETE NO ACTION,

    FOREIGN KEY (id_exercise) REFERENCES exercises(id_exercise)
    ON UPDATE CASCADE
    ON DELETE NO ACTION
);




CREATE TABLE IF NOT EXISTS microcycle_templates (
    id_microcycle_template  INTEGER PRIMARY KEY AUTOINCREMENT,
    title                   TEXT(100) NOT NULL,
    slug                    TEXT(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS microcycle_template_composition (
    id_composition          INTEGER PRIMARY KEY AUTOINCREMENT,
    id_microcycle_template  INTEGER NOT NULL,
    id_workout_template     INTEGER NOT NULL,

    FOREIGN KEY (id_microcycle_template) REFERENCES microcycle_templates(id_microcycle_template)
    ON UPDATE CASCADE
    ON DELETE CASCADE,

    FOREIGN KEY (id_workout_template) REFERENCES workout_templates(id_workout_template)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);




CREATE TABLE IF NOT EXISTS macrocycles (
    id_macrocycle   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user         INTEGER NOT NULL,

    FOREIGN KEY (id_user) REFERENCES users(id_user)
    ON UPDATE CASCADE
    ON DELETE NO ACTION
);


CREATE TABLE IF NOT EXISTS mesocycles (
    id_mesocycle    INTEGER PRIMARY KEY AUTOINCREMENT,
    id_macrocycle   INTEGER,
    id_user         INTEGER NOT NULL,

    FOREIGN KEY (id_macrocycle) REFERENCES macrocycles(id_macrocycle)
    ON UPDATE CASCADE
    ON DELETE SET NULL,

    FOREIGN KEY (id_user) REFERENCES users(id_user)
    ON UPDATE CASCADE
    ON DELETE NO ACTION
);



CREATE TABLE IF NOT EXISTS microcycles (
    id_microcycle INTEGER PRIMARY KEY AUTOINCREMENT,
    id_mesocycle  INTEGER NOT NULL,
    is_unloading  INTEGER(1) NOT NULL,

    FOREIGN KEY (id_mesocycle) REFERENCES mesocycles(id_mesocycle)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS workouts (
    id_workout                      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_microcycle                   INTEGER NOT NULL,
    id_workout_template             INTEGER,
    id_workout_status               INTEGER NOT NULL,
    planned_workout_start_datetime  INTEGER(15) NOT NULL,
    planned_workout_end_datetime    INTEGER(15) NOT NULL,
    actual_workout_start_datetime   INTEGER(15) NOT NULL,
    actual_workout_end_datetime     INTEGER(15) NOT NULL,

    FOREIGN KEY (id_microcycle) REFERENCES microcycles(id_microcycle)
    ON UPDATE CASCADE
    ON DELETE CASCADE,

    FOREIGN KEY (id_workout_template) REFERENCES workout_templates(id_workout_template)
    ON UPDATE CASCADE
    ON DELETE SET NULL,

    FOREIGN KEY (id_workout_status) REFERENCES workout_status(id_workout_status)
    ON UPDATE CASCADE
    ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS workout_composition (
    id_composition      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_workout          INTEGER NOT NULL,
    id_exercise         INTEGER NOT NULL,
    planned_repetitions INTEGER NOT NULL,
    planned_weight      REAL NOT NULL,
    actual_repetitions  INTEGER,
    actual_weight       REAL,

    FOREIGN KEY (id_workout) REFERENCES workouts(id_workout)
    ON UPDATE CASCADE
    ON DELETE CASCADE,

    FOREIGN KEY (id_exercise) REFERENCES exercises(id_exercise)
    ON UPDATE CASCADE
    ON DELETE NO ACTION
);