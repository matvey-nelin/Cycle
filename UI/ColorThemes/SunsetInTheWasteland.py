import flet as ft

class SunsetInTheWasteland:
    def __init__(self) -> None:
        
        # ==========================================
        # ТЁМНАЯ ТЕМА (SunsetInTheWasteland - Пустынная ночь)
        # ==========================================
        
        # --- Основные акценты (Охра, Янтарь, Терракот) ---
        self.DARK_PRIMARY =                     ft.Colors.DEEP_ORANGE_400
        self.DARK_ON_PRIMARY =                  "#140F0A"
        self.DARK_PRIMARY_CONTAINER =           ft.Colors.DEEP_ORANGE_800
        self.DARK_ON_PRIMARY_CONTAINER =        ft.Colors.DEEP_ORANGE_100
        self.DARK_PRIMARY_FIXED =               ft.Colors.DEEP_ORANGE_700
        self.DARK_PRIMARY_FIXED_DIM =           ft.Colors.DEEP_ORANGE_800
        self.DARK_ON_PRIMARY_FIXED =            "#140F0A"
        self.DARK_ON_PRIMARY_FIXED_VARIANT =    "#2A1F14"
        
        self.DARK_SECONDARY =                   ft.Colors.AMBER_400
        self.DARK_ON_SECONDARY =                "#140F0A"
        self.DARK_SECONDARY_CONTAINER =         ft.Colors.AMBER_800
        self.DARK_ON_SECONDARY_CONTAINER =      ft.Colors.AMBER_100
        self.DARK_SECONDARY_FIXED =             ft.Colors.AMBER_700
        self.DARK_SECONDARY_FIXED_DIM =         ft.Colors.AMBER_800
        self.DARK_ON_SECONDARY_FIXED =          "#140F0A"
        self.DARK_ON_SECONDARY_FIXED_VARIANT =  "#282114"
        
        self.DARK_TERTIARY =                    ft.Colors.ORANGE_400
        self.DARK_ON_TERTIARY =                 "#140F0A"
        self.DARK_TERTIARY_CONTAINER =          ft.Colors.ORANGE_800
        self.DARK_ON_TERTIARY_CONTAINER =       ft.Colors.ORANGE_100
        self.DARK_TERTIARY_FIXED =              ft.Colors.ORANGE_700
        self.DARK_TERTIARY_FIXED_DIM =          ft.Colors.ORANGE_800
        self.DARK_ON_TERTIARY_FIXED =           "#140F0A"
        self.DARK_ON_TERTIARY_FIXED_VARIANT =   "#282014"
        
        # --- Ошибки ---
        self.DARK_ERROR =                       ft.Colors.RED_400
        self.DARK_ON_ERROR =                    "#140F0A"
        self.DARK_ERROR_CONTAINER =             ft.Colors.RED_800
        self.DARK_ON_ERROR_CONTAINER =          ft.Colors.RED_100
        
        # --- Поверхности (Тёмная ржавчина) ---
        self.DARK_SURFACE =                     "#16100C"
        self.DARK_ON_SURFACE =                  "#E6E1E5"
        self.DARK_ON_SURFACE_VARIANT =          "#C4C7C5"
        self.DARK_SURFACE_TINT =                ft.Colors.DEEP_ORANGE_400
        
        self.DARK_SURFACE_DIM =                 "#0E0A07"
        self.DARK_SURFACE_BRIGHT =              "#2E2620"
        self.DARK_SURFACE_CONTAINER_LOWEST =    "#120D09"
        self.DARK_SURFACE_CONTAINER_LOW =       "#16100C"
        self.DARK_SURFACE_CONTAINER =           "#1A1410"
        self.DARK_SURFACE_CONTAINER_HIGH =      "#201A16"
        self.DARK_SURFACE_CONTAINER_HIGHEST =   "#27211D"
        
        # --- Границы, Инверсия, Тени ---
        self.DARK_OUTLINE =                     "#938F99"
        self.DARK_OUTLINE_VARIANT =             "#49454F"
        self.DARK_SHADOW =                      "#140804"
        self.DARK_SCRIM =                       "#000000"
        self.DARK_INVERSE_SURFACE =             "#E6E1E5"
        self.DARK_ON_INVERSE_SURFACE =          "#140F0A"
        self.DARK_INVERSE_PRIMARY =             ft.Colors.DEEP_ORANGE_700

        self.dark_color_scheme = ft.ColorScheme(
            primary=                        self.DARK_PRIMARY,
            on_primary=                     self.DARK_ON_PRIMARY,
            primary_container=              self.DARK_PRIMARY_CONTAINER,
            on_primary_container=           self.DARK_ON_PRIMARY_CONTAINER,
            primary_fixed=                  self.DARK_PRIMARY_FIXED,
            primary_fixed_dim=              self.DARK_PRIMARY_FIXED_DIM,
            on_primary_fixed=               self.DARK_ON_PRIMARY_FIXED,
            on_primary_fixed_variant=       self.DARK_ON_PRIMARY_FIXED_VARIANT,
            secondary=                      self.DARK_SECONDARY,
            on_secondary=                   self.DARK_ON_SECONDARY,
            secondary_container=            self.DARK_SECONDARY_CONTAINER,
            on_secondary_container=         self.DARK_ON_SECONDARY_CONTAINER,
            secondary_fixed=                self.DARK_SECONDARY_FIXED,
            secondary_fixed_dim=            self.DARK_SECONDARY_FIXED_DIM,
            on_secondary_fixed=             self.DARK_ON_SECONDARY_FIXED,
            on_secondary_fixed_variant=     self.DARK_ON_SECONDARY_FIXED_VARIANT,
            tertiary=                       self.DARK_TERTIARY,
            on_tertiary=                    self.DARK_ON_TERTIARY,
            tertiary_container=             self.DARK_TERTIARY_CONTAINER,
            on_tertiary_container=          self.DARK_ON_TERTIARY_CONTAINER,
            tertiary_fixed=                 self.DARK_TERTIARY_FIXED,
            tertiary_fixed_dim=             self.DARK_TERTIARY_FIXED_DIM,
            on_tertiary_fixed=              self.DARK_ON_TERTIARY_FIXED,
            on_tertiary_fixed_variant=      self.DARK_ON_TERTIARY_FIXED_VARIANT,
            error=                          self.DARK_ERROR,
            on_error=                       self.DARK_ON_ERROR,
            error_container=                self.DARK_ERROR_CONTAINER,
            on_error_container=             self.DARK_ON_ERROR_CONTAINER,
            surface=                        self.DARK_SURFACE,
            on_surface=                     self.DARK_ON_SURFACE,
            on_surface_variant=             self.DARK_ON_SURFACE_VARIANT,
            surface_tint=                   self.DARK_SURFACE_TINT,
            surface_dim=                    self.DARK_SURFACE_DIM,
            surface_bright=                 self.DARK_SURFACE_BRIGHT,
            surface_container_lowest=       self.DARK_SURFACE_CONTAINER_LOWEST,
            surface_container_low=          self.DARK_SURFACE_CONTAINER_LOW,
            surface_container=              self.DARK_SURFACE_CONTAINER,
            surface_container_high=         self.DARK_SURFACE_CONTAINER_HIGH,
            surface_container_highest=      self.DARK_SURFACE_CONTAINER_HIGHEST,
            outline=                        self.DARK_OUTLINE,
            outline_variant=                self.DARK_OUTLINE_VARIANT,
            shadow=                         self.DARK_SHADOW,
            scrim=                          self.DARK_SCRIM,
            inverse_surface=                self.DARK_INVERSE_SURFACE,
            on_inverse_surface=             self.DARK_ON_INVERSE_SURFACE,
            inverse_primary=                self.DARK_INVERSE_PRIMARY,
        )

        # ==========================================
        # СВЕТЛАЯ ТЕМА (SunsetInTheWasteland - Дневной зной)
        # ==========================================
        
        # --- Основные акценты ---
        self.LIGHT_PRIMARY =                    ft.Colors.DEEP_ORANGE_600
        self.LIGHT_ON_PRIMARY =                 ft.Colors.WHITE
        self.LIGHT_PRIMARY_CONTAINER =          ft.Colors.DEEP_ORANGE_100
        self.LIGHT_ON_PRIMARY_CONTAINER =       ft.Colors.DEEP_ORANGE_900
        self.LIGHT_PRIMARY_FIXED =              ft.Colors.DEEP_ORANGE_700
        self.LIGHT_PRIMARY_FIXED_DIM =          ft.Colors.DEEP_ORANGE_800
        self.LIGHT_ON_PRIMARY_FIXED =           "#140F0A"
        self.LIGHT_ON_PRIMARY_FIXED_VARIANT =   "#2A1F14"
        
        self.LIGHT_SECONDARY =                  ft.Colors.AMBER_600
        self.LIGHT_ON_SECONDARY =               ft.Colors.WHITE
        self.LIGHT_SECONDARY_CONTAINER =        ft.Colors.AMBER_100
        self.LIGHT_ON_SECONDARY_CONTAINER =     ft.Colors.AMBER_900
        self.LIGHT_SECONDARY_FIXED =            ft.Colors.AMBER_700
        self.LIGHT_SECONDARY_FIXED_DIM =        ft.Colors.AMBER_800
        self.LIGHT_ON_SECONDARY_FIXED =         "#140F0A"
        self.LIGHT_ON_SECONDARY_FIXED_VARIANT = "#282114"
        
        self.LIGHT_TERTIARY =                   ft.Colors.ORANGE_600
        self.LIGHT_ON_TERTIARY =                ft.Colors.WHITE
        self.LIGHT_TERTIARY_CONTAINER =         ft.Colors.ORANGE_100
        self.LIGHT_ON_TERTIARY_CONTAINER =      ft.Colors.ORANGE_900
        self.LIGHT_TERTIARY_FIXED =             ft.Colors.ORANGE_700
        self.LIGHT_TERTIARY_FIXED_DIM =         ft.Colors.ORANGE_800
        self.LIGHT_ON_TERTIARY_FIXED =          "#140F0A"
        self.LIGHT_ON_TERTIARY_FIXED_VARIANT =  "#282014"
        
        # --- Ошибки ---
        self.LIGHT_ERROR =                      ft.Colors.RED_600
        self.LIGHT_ON_ERROR =                   ft.Colors.WHITE
        self.LIGHT_ERROR_CONTAINER =            ft.Colors.RED_100
        self.LIGHT_ON_ERROR_CONTAINER =         ft.Colors.RED_900
        
        # --- Поверхности (Песок и глина) ---
        self.LIGHT_SURFACE =                    "#FDF8F4"
        self.LIGHT_ON_SURFACE =                 "#1D1B20"
        self.LIGHT_ON_SURFACE_VARIANT =         "#49454F"
        self.LIGHT_SURFACE_TINT =               ft.Colors.DEEP_ORANGE_600
        
        self.LIGHT_SURFACE_DIM =                "#E2D9D1"
        self.LIGHT_SURFACE_BRIGHT =             "#FDF8F4"
        self.LIGHT_SURFACE_CONTAINER_LOWEST =   "#FFFFFF"
        self.LIGHT_SURFACE_CONTAINER_LOW =      "#F5EEEB"
        self.LIGHT_SURFACE_CONTAINER =          "#EDE6E2"
        self.LIGHT_SURFACE_CONTAINER_HIGH =     "#E5DED9"
        self.LIGHT_SURFACE_CONTAINER_HIGHEST =  "#DDD6D0"
        
        # --- Границы, Инверсия, Тени ---
        self.LIGHT_OUTLINE =                    "#79747E"
        self.LIGHT_OUTLINE_VARIANT =            "#CAC4D0"
        self.LIGHT_SHADOW =                     "#2A1F14"
        self.LIGHT_SCRIM =                      "#000000"
        self.LIGHT_INVERSE_SURFACE =            "#322F35"
        self.LIGHT_ON_INVERSE_SURFACE =         "#F5EFF7"
        self.LIGHT_INVERSE_PRIMARY =            ft.Colors.DEEP_ORANGE_200

        self.light_color_scheme = ft.ColorScheme(
            primary=                        self.LIGHT_PRIMARY,
            on_primary=                     self.LIGHT_ON_PRIMARY,
            primary_container=              self.LIGHT_PRIMARY_CONTAINER,
            on_primary_container=           self.LIGHT_ON_PRIMARY_CONTAINER,
            primary_fixed=                  self.LIGHT_PRIMARY_FIXED,
            primary_fixed_dim=              self.LIGHT_PRIMARY_FIXED_DIM,
            on_primary_fixed=               self.LIGHT_ON_PRIMARY_FIXED,
            on_primary_fixed_variant=       self.LIGHT_ON_PRIMARY_FIXED_VARIANT,
            secondary=                      self.LIGHT_SECONDARY,
            on_secondary=                   self.LIGHT_ON_SECONDARY,
            secondary_container=            self.LIGHT_SECONDARY_CONTAINER,
            on_secondary_container=         self.LIGHT_ON_SECONDARY_CONTAINER,
            secondary_fixed=                self.LIGHT_SECONDARY_FIXED,
            secondary_fixed_dim=            self.LIGHT_SECONDARY_FIXED_DIM,
            on_secondary_fixed=             self.LIGHT_ON_SECONDARY_FIXED,
            on_secondary_fixed_variant=     self.LIGHT_ON_SECONDARY_FIXED_VARIANT,
            tertiary=                       self.LIGHT_TERTIARY,
            on_tertiary=                    self.LIGHT_ON_TERTIARY,
            tertiary_container=             self.LIGHT_TERTIARY_CONTAINER,
            on_tertiary_container=          self.LIGHT_ON_TERTIARY_CONTAINER,
            tertiary_fixed=                 self.LIGHT_TERTIARY_FIXED,
            tertiary_fixed_dim=             self.LIGHT_TERTIARY_FIXED_DIM,
            on_tertiary_fixed=              self.LIGHT_ON_TERTIARY_FIXED,
            on_tertiary_fixed_variant=      self.LIGHT_ON_TERTIARY_FIXED_VARIANT,
            error=                          self.LIGHT_ERROR,
            on_error=                       self.LIGHT_ON_ERROR,
            error_container=                self.LIGHT_ERROR_CONTAINER,
            on_error_container=             self.LIGHT_ON_ERROR_CONTAINER,
            surface=                        self.LIGHT_SURFACE,
            on_surface=                     self.LIGHT_ON_SURFACE,
            on_surface_variant=             self.LIGHT_ON_SURFACE_VARIANT,
            surface_tint=                   self.LIGHT_SURFACE_TINT,
            surface_dim=                    self.LIGHT_SURFACE_DIM,
            surface_bright=                 self.LIGHT_SURFACE_BRIGHT,
            surface_container_lowest=       self.LIGHT_SURFACE_CONTAINER_LOWEST,
            surface_container_low=          self.LIGHT_SURFACE_CONTAINER_LOW,
            surface_container=              self.LIGHT_SURFACE_CONTAINER,
            surface_container_high=         self.LIGHT_SURFACE_CONTAINER_HIGH,
            surface_container_highest=      self.LIGHT_SURFACE_CONTAINER_HIGHEST,
            outline=                        self.LIGHT_OUTLINE,
            outline_variant=                self.LIGHT_OUTLINE_VARIANT,
            shadow=                         self.LIGHT_SHADOW,
            scrim=                          self.LIGHT_SCRIM,
            inverse_surface=                self.LIGHT_INVERSE_SURFACE,
            on_inverse_surface=             self.LIGHT_ON_INVERSE_SURFACE,
            inverse_primary=                self.LIGHT_INVERSE_PRIMARY,
        )