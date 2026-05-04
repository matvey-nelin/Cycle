-- Файл служит для автоматического ввода первичных записей в некоторые справочники.


-- Статус пользователя
INSERT OR IGNORE INTO user_status(title, slug)
VALUES  
    ("Active",          "active"),
    ("Inactive",        "inactive"),
    ("Sick",            "sick"),
    ("Injured",         "injured"),
    ("On Vacation",     "on_vacation");


-- Тип тренировки
INSERT OR IGNORE INTO workout_type(title, slug)
VALUES  
    ("LISS",            "liss"),
    ("Cardio",          "cardio"),
    ("CrossFit",        "crossfit"),
    ("Bodybuilding",    "bodybuilding"), 
    ("HIIT",            "hiit"),
    ("Cycling",         "cycling"),
    ("Aerobics",        "aerobics"),
    ("Martial Arts",    "martial_arts"),
    ("Yoga",            "yoga"),
    ("Full Body",       "full_body"),
    ("Powerlifting",    "powerlifting"),
    ("Calisthenics",    "calisthenics"),
    ("Strength",        "strength"),
    ("Endurance",       "endurance"),
    ("Flexibility",     "flexibility"),
    ("Recovery",        "recovery"),
    ("Swimming",        "swimming"),
    ("Running",         "running");


-- Статус тренировки
INSERT OR IGNORE INTO workout_status(title, slug)
VALUES  
    ("Scheduled",           "scheduled"),
    ("Overcompleted",       "overcompleted"),
    ("Completed",           "completed"),
    ("Partially Completed", "partially_completed"),
    ("Cancelled",           "cancelled"),
    ("In Progress",         "in_progress"),
    ("Skipped",             "skipped");


-- Гипертрофия
INSERT OR IGNORE INTO hypertrophy_type(title, slug)
VALUES  
    ("Sarcoplasmic Hypertrophy",    "sarcoplasmic"),
    ("Myofibrillar Hypertrophy",    "myofibrillar"),
    ("Mixed",                       "mixed"),
    ("Neural Adaptation",           "neural");







