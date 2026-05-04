import flet as ft

class AuroraBorealis:
    def __init__(self) -> None:
        """Цвета для темной темы"""
        # === ОСНОВНАЯ ПАЛИТРА (для кнопок действий) ===
        self.DARK_PRIMARY = ft.Colors.CYAN_400              # ✅ Кнопки действий, акценты
        self.DARK_PRIMARY_CONTAINER = ft.Colors.CYAN_300    # ✅ Hover кнопок, индикаторы
        self.DARK_ON_PRIMARY = ft.Colors.GREY_900           # ✅ Текст на кнопках действий
        self.DARK_ON_PRIMARY_CONTAINER = ft.Colors.GREY_900 # ✅ Текст на контейнерах primary
        
        self.DARK_SECONDARY = ft.Colors.PURPLE_400          # ✅ Градиент кнопок (в паре с PRIMARY)
        self.DARK_SECONDARY_CONTAINER = ft.Colors.PURPLE_300 # ✅ Hover вторичных элементов
        self.DARK_ON_SECONDARY = ft.Colors.GREY_900         # ✅ Текст на secondary
        self.DARK_ON_SECONDARY_CONTAINER = ft.Colors.GREY_900 # ✅ Текст на контейнерах secondary
        
        self.DARK_TERTIARY = ft.Colors.TEAL_400             # ✅ Градиент success-кнопок, иконки в карточках
        self.DARK_TERTIARY_CONTAINER = ft.Colors.TEAL_300   # ✅ Hover success-элементов
        self.DARK_ON_TERTIARY = ft.Colors.GREY_900          # ✅ Текст на tertiary
        self.DARK_ON_TERTIARY_CONTAINER = ft.Colors.GREY_900 # ✅ Текст на контейнерах tertiary
        
        # === ФОН И ПОВЕРХНОСТИ (для карточек и контейнеров) ===
        self.DARK_SURFACE = ft.Colors.GREY_800              # ✅ Фон карточек, панелей
        self.DARK_ON_SURFACE = ft.Colors.GREY_50            # ✅ Текст в карточках (основной)
        self.DARK_SURFACE_TINT = ft.Colors.CYAN_400         # ✅ Тонирование поверхностей
        self.DARK_BACKGROUND = ft.Colors.GREY_900           # ✅ Фон страницы
        self.DARK_ON_BACKGROUND = ft.Colors.GREY_50         # ✅ Текст на фоне страницы
        
        # === СТАТУСЫ ===
        self.DARK_ERROR = ft.Colors.RED_400                 # ✅ Кнопки удаления, ошибки
        self.DARK_ERROR_CONTAINER = ft.Colors.RED_300       # ✅ Hover danger-кнопок
        self.DARK_ON_ERROR = ft.Colors.GREY_900             # ✅ Текст на кнопках удаления
        self.DARK_ON_ERROR_CONTAINER = ft.Colors.GREY_900   # ✅ Текст на контейнерах error
        
        self.DARK_WARNING = ft.Colors.AMBER_400             # ✅ Предупреждения
        self.DARK_ON_WARNING = ft.Colors.GREY_900           # ✅ Текст на warning
        
        # === ГРАНИЦЫ (для вторичных кнопок и карточек) ===
        self.DARK_OUTLINE = ft.Colors.GREY_600              # ✅ Границы карточек, outline-кнопки
        self.DARK_OUTLINE_VARIANT = ft.Colors.GREY_700      # ✅ Второстепенные границы



    # Создание ColorScheme из атрибутов класса
        self.dark_color_scheme = ft.ColorScheme(
            primary=                self.DARK_PRIMARY,
            primary_container=      self.DARK_PRIMARY_CONTAINER,
            on_primary=             self.DARK_ON_PRIMARY,
            on_primary_container=   self.DARK_ON_PRIMARY_CONTAINER,
            secondary=              self.DARK_SECONDARY, 
            secondary_container=    self.DARK_SECONDARY_CONTAINER,
            on_secondary=           self.DARK_ON_SECONDARY,
            on_secondary_container= self.DARK_ON_SECONDARY_CONTAINER,
            tertiary=               self.DARK_TERTIARY,
            tertiary_container=     self.DARK_TERTIARY_CONTAINER,
            on_tertiary=            self.DARK_ON_TERTIARY,
            on_tertiary_container=  self.DARK_ON_TERTIARY_CONTAINER,
            error=                  self.DARK_ERROR,
            error_container=        self.DARK_ERROR_CONTAINER,
            on_error=               self.DARK_ON_ERROR,
            on_error_container=     self.DARK_ON_ERROR_CONTAINER,
            surface=                self.DARK_SURFACE,
            on_surface=             self.DARK_ON_SURFACE,
            surface_tint=           self.DARK_SURFACE_TINT,
            outline=                self.DARK_OUTLINE,
            outline_variant=        self.DARK_OUTLINE_VARIANT,
        )


        """Цвета для светлой темы"""
        # === ОСНОВНАЯ ПАЛИТРА (для кнопок действий) ===
        self.LIGHT_PRIMARY = ft.Colors.CYAN_600              # ✅ Кнопки действий, акценты
        self.LIGHT_PRIMARY_CONTAINER = ft.Colors.CYAN_500    # ✅ Hover кнопок, индикаторы
        self.LIGHT_ON_PRIMARY = ft.Colors.WHITE              # ✅ Текст на кнопках действий
        self.LIGHT_ON_PRIMARY_CONTAINER = ft.Colors.CYAN_100 # ✅ Текст на контейнерах primary
        
        self.LIGHT_SECONDARY = ft.Colors.PURPLE_600          # ✅ Градиент кнопок (в паре с PRIMARY)
        self.LIGHT_SECONDARY_CONTAINER = ft.Colors.PURPLE_500 # ✅ Hover вторичных элементов
        self.LIGHT_ON_SECONDARY = ft.Colors.WHITE            # ✅ Текст на secondary
        self.LIGHT_ON_SECONDARY_CONTAINER = ft.Colors.PURPLE_100 # ✅ Текст на контейнерах secondary
        
        self.LIGHT_TERTIARY = ft.Colors.TEAL_600             # ✅ Градиент success-кнопок, иконки в карточках
        self.LIGHT_TERTIARY_CONTAINER = ft.Colors.TEAL_500   # ✅ Hover success-элементов
        self.LIGHT_ON_TERTIARY = ft.Colors.WHITE             # ✅ Текст на tertiary
        self.LIGHT_ON_TERTIARY_CONTAINER = ft.Colors.TEAL_100 # ✅ Текст на контейнерах tertiary
        
        # === ФОН И ПОВЕРХНОСТИ (для карточек и контейнеров) ===
        self.LIGHT_SURFACE = ft.Colors.WHITE                 # ✅ Фон карточек, панелей
        self.LIGHT_ON_SURFACE = ft.Colors.GREY_900           # ✅ Текст в карточках (основной)
        self.LIGHT_SURFACE_TINT = ft.Colors.CYAN_600         # ✅ Тонирование поверхностей
        self.LIGHT_BACKGROUND = ft.Colors.GREY_50            # ✅ Фон страницы
        self.LIGHT_ON_BACKGROUND = ft.Colors.GREY_900        # ✅ Текст на фоне страницы
        
        # === СТАТУСЫ ===
        self.LIGHT_ERROR = ft.Colors.RED_600                 # ✅ Кнопки удаления, ошибки
        self.LIGHT_ERROR_CONTAINER = ft.Colors.RED_500       # ✅ Hover danger-кнопок
        self.LIGHT_ON_ERROR = ft.Colors.WHITE                # ✅ Текст на кнопках удаления
        self.LIGHT_ON_ERROR_CONTAINER = ft.Colors.RED_100    # ✅ Текст на контейнерах error
        
        self.LIGHT_WARNING = ft.Colors.AMBER_600             # ✅ Предупреждения
        self.LIGHT_ON_WARNING = ft.Colors.WHITE              # ✅ Текст на warning
        
        # === ГРАНИЦЫ (для вторичных кнопок и карточек) ===
        self.LIGHT_OUTLINE = ft.Colors.GREY_300              # ✅ Границы карточек, outline-кнопки
        self.LIGHT_OUTLINE_VARIANT = ft.Colors.GREY_200      # ✅ Второстепенные границы


        # Создание ColorScheme из атрибутов класса
        self.light_color_scheme = ft.ColorScheme(
            primary=                self.LIGHT_PRIMARY,
            primary_container=      self.LIGHT_PRIMARY_CONTAINER,
            on_primary=             self.LIGHT_ON_PRIMARY,
            on_primary_container=   self.LIGHT_ON_PRIMARY_CONTAINER,
            secondary=              self.LIGHT_SECONDARY,
            secondary_container=    self.LIGHT_SECONDARY_CONTAINER,
            on_secondary=           self.LIGHT_ON_SECONDARY,
            on_secondary_container= self.LIGHT_ON_SECONDARY_CONTAINER,
            tertiary=               self.LIGHT_TERTIARY,
            tertiary_container=     self.LIGHT_TERTIARY_CONTAINER,
            on_tertiary=            self.LIGHT_ON_TERTIARY,
            on_tertiary_container=  self.LIGHT_ON_TERTIARY_CONTAINER,
            error=                  self.LIGHT_ERROR,
            error_container=        self.LIGHT_ERROR_CONTAINER,
            on_error=               self.LIGHT_ON_ERROR,
            on_error_container=     self.LIGHT_ON_ERROR_CONTAINER,
            surface=                self.LIGHT_SURFACE,
            on_surface=             self.LIGHT_ON_SURFACE,
            surface_tint=           self.LIGHT_SURFACE_TINT,
            outline=                self.LIGHT_OUTLINE,
            outline_variant=        self.LIGHT_OUTLINE_VARIANT,
        )