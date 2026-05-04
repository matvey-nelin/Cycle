INSERT OR IGNORE INTO target_muscles(id_workout_type, id_agonist)
VALUES 
-- Powerlifting (id=11): грудь, спина, ноги
(11, 1),  -- Pectoralis major
(11, 3),  -- Latissimus dorsi
(11, 42), -- Quadriceps femoris
(11, 28), -- Gluteus maximus

-- Bodybuilding (id=4): все основные группы
(4, 1), (4, 3), (4, 11), (4, 14), (4, 15), (4, 23), (4, 28), (4, 42),

-- Cardio (id=2): ноги, кор
(2, 42), (2, 28), (2, 23), (2, 44),

-- Full Body (id=10): всё тело
(10, 1), (10, 3), (10, 11), (10, 14), (10, 23), (10, 28), (10, 42);

INSERT OR IGNORE INTO workout_templates(id_workout_type, id_hypertrophy_type, title, slug)
VALUES 
(11, 2, "Powerlifting - Heavy Squat Day", "powerlifting_heavy_squat_day"),
(11, 2, "Powerlifting - Heavy Bench Day", "powerlifting_heavy_bench_day"),
(11, 2, "Powerlifting - Heavy Deadlift Day", "powerlifting_heavy_deadlift_day"),
(4, 1, "Bodybuilding - Chest & Triceps", "bodybuilding_chest_triceps"),
(4, 1, "Bodybuilding - Back & Biceps", "bodybuilding_back_biceps"),
(4, 1, "Bodybuilding - Legs & Shoulders", "bodybuilding_legs_shoulders"),
(10, 3, "Full Body - General Fitness", "full_body_general_fitness"),
(2, 4, "Cardio - Endurance Session", "cardio_endurance_session"),
(12, 3, "Calisthenics - Upper Body", "calisthenics_upper_body"),
(1, 4, "LISS - Recovery Walk", "liss_recovery_walk");

INSERT OR IGNORE INTO workout_template_composition(id_workout_template, id_exercise)
VALUES 
-- Шаблон 1: Powerlifting - Heavy Squat Day
(1, 2), (1, 20), (1, 13), (1, 15),

-- Шаблон 2: Powerlifting - Heavy Bench Day
(2, 1), (2, 11), (2, 9), (2, 19),

-- Шаблон 3: Powerlifting - Heavy Deadlift Day
(3, 3), (3, 21), (3, 22), (3, 16),

-- Шаблон 4: Bodybuilding - Chest & Triceps
(4, 1), (4, 11), (4, 25), (4, 9), (4, 27),

-- Шаблон 5: Bodybuilding - Back & Biceps
(5, 4), (5, 12), (5, 7), (5, 10), (5, 26),

-- Шаблон 6: Bodybuilding - Legs & Shoulders
(6, 2), (6, 8), (6, 6), (6, 19), (6, 15),

-- Шаблон 7: Full Body - General Fitness
(7, 1), (7, 4), (7, 2), (7, 16), (7, 30),

-- Шаблон 8: Cardio - Endurance Session
(8, 30), (8, 16), (8, 8),

-- Шаблон 9: Calisthenics - Upper Body
(9, 4), (9, 5), (9, 16), (9, 29),

-- Шаблон 10: LISS - Recovery Walk
(10, 16), (10, 29);

INSERT OR IGNORE INTO microcycle_templates(title, slug)
VALUES 
("Week 1 - Foundation", "week_1_foundation"),
("Week 2 - Volume Build", "week_2_volume_build"),
("Week 3 - Intensity Peak", "week_3_intensity_peak"),
("Week 4 - Deload", "week_4_deload"),
("5x5 Strength Cycle", "5x5_strength_cycle"),
("Hypertrophy Block A", "hypertrophy_block_a"),
("Hypertrophy Block B", "hypertrophy_block_b"),
("Powerlifting Meet Prep", "powerlifting_meet_prep"),
("General Fitness Week", "general_fitness_week"),
("Active Recovery Week", "active_recovery_week");


INSERT OR IGNORE INTO microcycle_template_composition(id_microcycle_template, id_workout_template)
VALUES 
-- Микроцикл 1: Foundation (3 тренировки)
(1, 1), (1, 2), (1, 3),

-- Микроцикл 2: Volume Build (4 тренировки)
(2, 4), (2, 5), (2, 6), (2, 7),

-- Микроцикл 3: Intensity Peak (3 тренировки)
(3, 1), (3, 2), (3, 3),

-- Микроцикл 4: Deload (2 лёгкие тренировки)
(4, 7), (4, 10),

-- Микроцикл 5: 5x5 Strength (3 тренировки)
(5, 1), (5, 2), (5, 3),

-- Микроцикл 6: Hypertrophy A (4 тренировки)
(6, 4), (6, 5), (6, 6), (6, 7),

-- Микроцикл 7: Hypertrophy B (4 тренировки)
(7, 4), (7, 5), (7, 6), (7, 9),

-- Микроцикл 8: Meet Prep (3 тренировки)
(8, 1), (8, 2), (8, 3),

-- Микроцикл 9: General Fitness (3 тренировки)
(9, 7), (9, 8), (9, 10),

-- Микроцикл 10: Active Recovery (2 тренировки)
(10, 8), (10, 10);