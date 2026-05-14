-- =====================================================
-- 2. ШАБЛОНЫ ТРЕНИРОВОК (минимум: 2 штуки)
--    Зависит: workout_type ✓, hypertrophy_type ✓
-- =====================================================

-- Шаблон 1: "Push - Сила" (грудь/дельты/трицепс, миозиллярная гипертрофия)
INSERT INTO workout_templates(id_workout_type, id_hypertrophy_type, title, slug)
VALUES (13, 2, 'Push - Strength', 'push_strength');

-- Шаблон 2: "Pull - Объём" (спина/бицепс, саркоплазматическая гипертрофия)
INSERT INTO workout_templates(id_workout_type, id_hypertrophy_type, title, slug)
VALUES (13, 1, 'Pull - Volume', 'pull_volume');


-- =====================================================
-- 3. СОСТАВ ШАБЛОНОВ (какие упражнения входят)
--    Зависит: workout_templates ✓, exercises ✓
-- =====================================================

-- Push-шаблон: 4 базовых упражнения
INSERT INTO workout_template_composition(id_workout_template, id_exercise) VALUES
    (1, 1),   -- Bench Press
    (1, 6),   -- Overhead Press
    (1, 19),  -- Lateral Raise
    (1, 9);   -- Skull Crusher

-- Pull-шаблон: 4 базовых упражнения
INSERT INTO workout_template_composition(id_workout_template, id_exercise) VALUES
    (2, 4),   -- Pull-ups
    (2, 7),   -- Bent Over Row
    (2, 12),  -- Lat Pulldown
    (2, 10);  -- Barbell Curl


-- =====================================================
-- 4. ПЕРИОДИЗАЦИЯ (Макро → Мезо → Микро)
--    Зависит: users ✓
-- =====================================================

-- Макроцикл: "Подготовка к лету 2026"
INSERT INTO macrocycles(id_user) VALUES (1);

-- Мезоцикл: "Набор силы" (привязан к макроциклу)
INSERT INTO mesocycles(id_macrocycle, id_user) VALUES (1, 1);

-- Микроциклы: 3 недели (1 обычная, 1 разгрузка, 1 пиковая)
INSERT INTO microcycles(id_mesocycle, is_unloading) VALUES
    (1, 0),  -- id=1: Неделя 1 (обычная)
    (1, 1),  -- id=2: Неделя 2 (РАЗГРУЗКА 🔥)
    (1, 0);  -- id=3: Неделя 3 (прогрессия нагрузки)


-- =====================================================
-- 5. РЕАЛЬНЫЕ ТРЕНИРОВКИ
--    Зависит: microcycles ✓, workout_templates ✓, workout_status ✓
--    Даты: база 1778400000 ≈ 6 мая 2026, шаг ~2-3 дня
-- =====================================================
INSERT INTO workouts(
    id_microcycle, id_workout_template, id_workout_status,
    planned_workout_start_datetime, planned_workout_end_datetime,
    actual_workout_start_datetime, actual_workout_end_datetime
) VALUES
    -- 📅 Микроцикл 1 (Обычная нагрузка)
    (1, 1, 3, 1778400000, 1778403600, 1778400300, 1778403900), -- W1: Push, Completed, ~60 мин
    (1, 2, 3, 1778659200, 1778662800, 1778659400, 1778663000), -- W2: Pull, Completed, ~60 мин
    
    -- 📅 Микроцикл 2 (Разгрузка 🔥)
    (2, 1, 3, 1779004800, 1779007200, 1779005000, 1779007400), -- W3: Push-light, Completed, ~40 мин
    
    -- 📅 Микроцикл 3 (Прогрессия + краевые случаи)
    (3, 1, 3, 1779609600, 1779613200, 1779609900, 1779613500), -- W4: Push-heavy, Completed, рост весов
    (3, 2, 4, 1779868800, 1779872400, 1779869000, 1779871000), -- W5: Pull, Partially Completed (бросил)
    (3, NULL, 6, 1780128000, 1780131600, 1780128300, 1780128300); -- W6: Free workout, In Progress


-- =====================================================
-- 6. ФАКТИЧЕСКОЕ ВЫПОЛНЕНИЕ (workout_composition)
--    Зависит: workouts ✓, exercises ✓
--    🔥 Тест-кейсы: weight=0, NULL actuals, прогрессия, перевыполнение
-- =====================================================

-- 🏋️ W1: Push по шаблону (вес=0 для разминки)
INSERT INTO workout_composition(id_workout, id_exercise, planned_repetitions, planned_weight, actual_repetitions, actual_weight) VALUES
    (1, 1, 2, 0.0, 2, 0.0),      -- Жим разминка (вес=0 → считаем как 1)
    (1, 1, 4, 80.0, 4, 80.0),    -- Жим рабочий 1: 320 кг
    (1, 1, 4, 80.0, 5, 80.0),    -- Жим рабочий 2 (+1 реп): 400 кг
    (1, 6, 3, 50.0, 3, 50.0),    -- Армейский жим: 150 кг
    (1, 19, 3, 12.5, 3, 12.5),   -- Махи: 37.5 кг
    (1, 9, 3, 40.0, 3, 40.0),    -- Французский жим: 120 кг
    (1, 27, 3, 30.0, NULL, NULL);-- Разгибания на блоке (пропустил → NULL)

-- 🏋️ W2: Pull по шаблону (упражнения с весом тела)
INSERT INTO workout_composition(id_workout, id_exercise, planned_repetitions, planned_weight, actual_repetitions, actual_weight) VALUES
    (2, 4, 4, 0.0, 4, 0.0),      -- Подтягивания: 4×0 = 4 (вес тела)
    (2, 4, 4, 0.0, 5, 0.0),      -- Подтягивания доп. подход: 5×0 = 5
    (2, 7, 4, 70.0, 4, 70.0),    -- Тяга штанги: 280 кг
    (2, 12, 3, 60.0, 3, 60.0),   -- Тяга блока: 180 кг
    (2, 10, 3, 35.0, 3, 35.0),   -- Бицепс штанга: 105 кг
    (2, 16, 3, 0.0, 3, 0.0);     -- Планка: 3×0 = 3

-- 🏋️ W3: РАЗГРУЗКА 🔥 (низкие веса, меньше подходов)
INSERT INTO workout_composition(id_workout, id_exercise, planned_repetitions, planned_weight, actual_repetitions, actual_weight) VALUES
    (3, 1, 3, 50.0, 3, 50.0),    -- Жим легкий: 150 кг
    (3, 6, 2, 40.0, 2, 40.0),    -- Армейский легкий: 80 кг
    (3, 19, 2, 10.0, 2, 10.0),   -- Махи легкие: 20 кг
    (3, 9, 2, 30.0, 2, 30.0),    -- Французский легкий: 60 кг
    (3, 30, 3, 0.0, 3, 0.0),     -- Берпи: 3×0 = 3
    (3, 29, 2, 0.0, 2, 0.0);     -- Боковая планка: 2×0 = 2

-- 🏋️ W4: ПРОГРЕССИЯ (рост рабочих весов!)
INSERT INTO workout_composition(id_workout, id_exercise, planned_repetitions, planned_weight, actual_repetitions, actual_weight) VALUES
    (4, 1, 4, 85.0, 4, 85.0),    -- Жим: 340 кг (+20 к прошлой!)
    (4, 1, 3, 75.0, 3, 75.0),    -- Жим бэк-офф: 225 кг
    (4, 6, 4, 55.0, 4, 55.0),    -- Армейский: 220 кг (+70!)
    (4, 11, 3, 30.0, 3, 30.0),   -- Жим гантелей под углом: 90 кг
    (4, 25, 3, 20.0, 3, 20.0),   -- Разводка: 60 кг
    (4, 26, 3, 17.5, 3, 17.5);   -- Бицепс гантели: 52.5 кг

-- 🏋️ W5: ЧАСТИЧНО ВЫПОЛНЕННАЯ (бросил тренировку)
INSERT INTO workout_composition(id_workout, id_exercise, planned_repetitions, planned_weight, actual_repetitions, actual_weight) VALUES
    (5, 4, 4, 0.0, 3, 0.0),      -- Подтягивания: сделал 3 из 4 = 3
    (5, 7, 4, 70.0, 2, 70.0),    -- Тяга: сделал 2 из 4 = 140
    (5, 12, 3, 60.0, NULL, NULL),-- Тяга блока: вообще не сделал
    (5, 10, 3, 35.0, 3, 35.0),   -- Бицепс: успел = 105
    (5, 14, 3, 45.0, NULL, NULL);-- Сгибания ног: не сделал (добавил лишнее для теста)

-- 🏋️ W6: IN PROGRESS (только начал, actual_end = actual_start)
INSERT INTO workout_composition(id_workout, id_exercise, planned_repetitions, planned_weight, actual_repetitions, actual_weight) VALUES
    (6, 2, 5, 110.0, 1, 110.0),  -- Присед: сделал 1 подход из 5 = 110
    (6, 20, 4, 130.0, NULL, NULL);-- Жим ногами: ещё не начал