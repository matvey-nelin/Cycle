import flet as ft

class SunsetInTheWasteland:
    def __init__(self) -> None:
        """Цвета для тёмной версии темы 'Закат в Пустоши'"""

        # === ОСНОВНАЯ ПАЛИТРА (для кнопок действий) ===
        self.DARK_PRIMARY = ft.Colors.DEEP_ORANGE_400
        self.DARK_PRIMARY_CONTAINER = ft.Colors.DEEP_ORANGE_300
        self.DARK_ON_PRIMARY = ft.Colors.GREY_900
        self.DARK_ON_PRIMARY_CONTAINER = ft.Colors.GREY_900
        
        self.DARK_SECONDARY = ft.Colors.AMBER_400
        self.DARK_SECONDARY_CONTAINER = ft.Colors.AMBER_300
        self.DARK_ON_SECONDARY = ft.Colors.GREY_900
        self.DARK_ON_SECONDARY_CONTAINER = ft.Colors.GREY_900
        
        self.DARK_TERTIARY = ft.Colors.ORANGE_400
        self.DARK_TERTIARY_CONTAINER = ft.Colors.ORANGE_300
        self.DARK_ON_TERTIARY = ft.Colors.GREY_900
        self.DARK_ON_TERTIARY_CONTAINER = ft.Colors.GREY_900
        
        # === ФОН И ПОВЕРХНОСТИ ===
        self.DARK_SURFACE = ft.Colors.BROWN_800
        self.DARK_ON_SURFACE = ft.Colors.ORANGE_50
        self.DARK_SURFACE_TINT = ft.Colors.DEEP_ORANGE_400
        self.DARK_BACKGROUND = ft.Colors.BROWN_900
        self.DARK_ON_BACKGROUND = ft.Colors.ORANGE_50
        
        # === СТАТУСЫ ===
        self.DARK_ERROR = ft.Colors.RED_400
        self.DARK_ERROR_CONTAINER = ft.Colors.RED_300
        self.DARK_ON_ERROR = ft.Colors.GREY_900
        self.DARK_ON_ERROR_CONTAINER = ft.Colors.GREY_900
        
        self.DARK_WARNING = ft.Colors.AMBER_400
        self.DARK_ON_WARNING = ft.Colors.GREY_900
        
        # === ГРАНИЦЫ ===
        self.DARK_OUTLINE = ft.Colors.BROWN_600
        self.DARK_OUTLINE_VARIANT = ft.Colors.BROWN_700

        # Создание ColorScheme
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


        """Цвета для светлой версии темы 'Закат в Пустоши'"""

        # === ОСНОВНАЯ ПАЛИТРА (для кнопок действий) ===
        self.LIGHT_PRIMARY = ft.Colors.DEEP_ORANGE_600
        self.LIGHT_PRIMARY_CONTAINER = ft.Colors.DEEP_ORANGE_500
        self.LIGHT_ON_PRIMARY = ft.Colors.WHITE
        self.LIGHT_ON_PRIMARY_CONTAINER = ft.Colors.DEEP_ORANGE_100
        
        self.LIGHT_SECONDARY = ft.Colors.AMBER_600
        self.LIGHT_SECONDARY_CONTAINER = ft.Colors.AMBER_500
        self.LIGHT_ON_SECONDARY = ft.Colors.WHITE
        self.LIGHT_ON_SECONDARY_CONTAINER = ft.Colors.AMBER_100
        
        self.LIGHT_TERTIARY = ft.Colors.ORANGE_600
        self.LIGHT_TERTIARY_CONTAINER = ft.Colors.ORANGE_500
        self.LIGHT_ON_TERTIARY = ft.Colors.WHITE
        self.LIGHT_ON_TERTIARY_CONTAINER = ft.Colors.ORANGE_100
        
        # === ФОН И ПОВЕРХНОСТИ ===
        self.LIGHT_SURFACE = ft.Colors.ORANGE_50
        self.LIGHT_ON_SURFACE = ft.Colors.BROWN_900
        self.LIGHT_SURFACE_TINT = ft.Colors.DEEP_ORANGE_600
        self.LIGHT_BACKGROUND = ft.Colors.AMBER_50
        self.LIGHT_ON_BACKGROUND = ft.Colors.BROWN_900
        
        # === СТАТУСЫ ===
        self.LIGHT_ERROR = ft.Colors.RED_600
        self.LIGHT_ERROR_CONTAINER = ft.Colors.RED_500
        self.LIGHT_ON_ERROR = ft.Colors.WHITE
        self.LIGHT_ON_ERROR_CONTAINER = ft.Colors.RED_100
        
        self.LIGHT_WARNING = ft.Colors.AMBER_600
        self.LIGHT_ON_WARNING = ft.Colors.WHITE
        
        # === ГРАНИЦЫ ===
        self.LIGHT_OUTLINE = ft.Colors.BROWN_300
        self.LIGHT_OUTLINE_VARIANT = ft.Colors.BROWN_200

        # Создание ColorScheme
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