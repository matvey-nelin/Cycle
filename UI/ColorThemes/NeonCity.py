import flet as ft

class NeonCity:
    def __init__(self) -> None:
        
        # ==========================================
        # ТЁМНАЯ ТЕМА (NeonCity - Неоновый дождь)
        # ==========================================
        
        # --- Основные акценты (Циан, Маджента, Желтый) ---
        self.DARK_PRIMARY =                     ft.Colors.CYAN_500
        self.DARK_ON_PRIMARY =                  "#000000"
        self.DARK_PRIMARY_CONTAINER =           ft.Colors.CYAN_800
        self.DARK_ON_PRIMARY_CONTAINER =        ft.Colors.CYAN_100
        self.DARK_PRIMARY_FIXED =               ft.Colors.CYAN_600
        self.DARK_PRIMARY_FIXED_DIM =           ft.Colors.CYAN_700
        self.DARK_ON_PRIMARY_FIXED =            "#000000"
        self.DARK_ON_PRIMARY_FIXED_VARIANT =    "#052026"
        
        self.DARK_SECONDARY =                   ft.Colors.PINK_500
        self.DARK_ON_SECONDARY =                "#000000"
        self.DARK_SECONDARY_CONTAINER =         ft.Colors.PINK_800
        self.DARK_ON_SECONDARY_CONTAINER =      ft.Colors.PINK_100
        self.DARK_SECONDARY_FIXED =             ft.Colors.PINK_600
        self.DARK_SECONDARY_FIXED_DIM =         ft.Colors.PINK_700
        self.DARK_ON_SECONDARY_FIXED =          "#000000"
        self.DARK_ON_SECONDARY_FIXED_VARIANT =  "#260515"
        
        self.DARK_TERTIARY =                    ft.Colors.YELLOW_400
        self.DARK_ON_TERTIARY =                 "#000000"
        self.DARK_TERTIARY_CONTAINER =          ft.Colors.YELLOW_800
        self.DARK_ON_TERTIARY_CONTAINER =       ft.Colors.YELLOW_100
        self.DARK_TERTIARY_FIXED =              ft.Colors.YELLOW_600
        self.DARK_TERTIARY_FIXED_DIM =          ft.Colors.YELLOW_700
        self.DARK_ON_TERTIARY_FIXED =           "#000000"
        self.DARK_ON_TERTIARY_FIXED_VARIANT =   "#221B00"
        
        # --- Ошибки ---
        self.DARK_ERROR =                       ft.Colors.RED_400
        self.DARK_ON_ERROR =                    "#000000"
        self.DARK_ERROR_CONTAINER =             ft.Colors.RED_800
        self.DARK_ON_ERROR_CONTAINER =          ft.Colors.RED_100
        
        # --- Поверхности (Абсолютный черный с оттенком) ---
        self.DARK_SURFACE =                     "#05050A"
        self.DARK_ON_SURFACE =                  "#E6E1E5"
        self.DARK_ON_SURFACE_VARIANT =          "#C4C7C5"
        self.DARK_SURFACE_TINT =                ft.Colors.CYAN_500
        
        self.DARK_SURFACE_DIM =                 "#000000"
        self.DARK_SURFACE_BRIGHT =              "#202025"
        self.DARK_SURFACE_CONTAINER_LOWEST =    "#020205"
        self.DARK_SURFACE_CONTAINER_LOW =       "#05050A"
        self.DARK_SURFACE_CONTAINER =           "#0A0A12"
        self.DARK_SURFACE_CONTAINER_HIGH =      "#10101A"
        self.DARK_SURFACE_CONTAINER_HIGHEST =   "#151522"
        
        # --- Границы, Инверсия, Тени ---
        self.DARK_OUTLINE =                     "#938F99"
        self.DARK_OUTLINE_VARIANT =             "#49454F"
        self.DARK_SHADOW =                      "#000A14"
        self.DARK_SCRIM =                       "#000000"
        self.DARK_INVERSE_SURFACE =             "#E6E1E5"
        self.DARK_ON_INVERSE_SURFACE =          "#000000"
        self.DARK_INVERSE_PRIMARY =             ft.Colors.CYAN_600

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
        # СВЕТЛАЯ ТЕМА (NeonCity - Дневной бетон)
        # ==========================================
        
        # --- Основные акценты ---
        self.LIGHT_PRIMARY =                    ft.Colors.CYAN_600
        self.LIGHT_ON_PRIMARY =                 ft.Colors.WHITE
        self.LIGHT_PRIMARY_CONTAINER =          ft.Colors.CYAN_100
        self.LIGHT_ON_PRIMARY_CONTAINER =       ft.Colors.CYAN_900
        self.LIGHT_PRIMARY_FIXED =              ft.Colors.CYAN_600
        self.LIGHT_PRIMARY_FIXED_DIM =          ft.Colors.CYAN_700
        self.LIGHT_ON_PRIMARY_FIXED =           "#000000"
        self.LIGHT_ON_PRIMARY_FIXED_VARIANT =   "#052026"
        
        self.LIGHT_SECONDARY =                  ft.Colors.PINK_600
        self.LIGHT_ON_SECONDARY =               ft.Colors.WHITE
        self.LIGHT_SECONDARY_CONTAINER =        ft.Colors.PINK_100
        self.LIGHT_ON_SECONDARY_CONTAINER =     ft.Colors.PINK_900
        self.LIGHT_SECONDARY_FIXED =            ft.Colors.PINK_600
        self.LIGHT_SECONDARY_FIXED_DIM =        ft.Colors.PINK_700
        self.LIGHT_ON_SECONDARY_FIXED =         "#000000"
        self.LIGHT_ON_SECONDARY_FIXED_VARIANT = "#260515"
        
        self.LIGHT_TERTIARY =                   ft.Colors.YELLOW_600
        self.LIGHT_ON_TERTIARY =                ft.Colors.WHITE
        self.LIGHT_TERTIARY_CONTAINER =         ft.Colors.YELLOW_100
        self.LIGHT_ON_TERTIARY_CONTAINER =      ft.Colors.YELLOW_900
        self.LIGHT_TERTIARY_FIXED =             ft.Colors.YELLOW_600
        self.LIGHT_TERTIARY_FIXED_DIM =         ft.Colors.YELLOW_700
        self.LIGHT_ON_TERTIARY_FIXED =          "#000000"
        self.LIGHT_ON_TERTIARY_FIXED_VARIANT =  "#221B00"
        
        # --- Ошибки ---
        self.LIGHT_ERROR =                      ft.Colors.RED_600
        self.LIGHT_ON_ERROR =                   ft.Colors.WHITE
        self.LIGHT_ERROR_CONTAINER =            ft.Colors.RED_100
        self.LIGHT_ON_ERROR_CONTAINER =         ft.Colors.RED_900
        
        # --- Поверхности (Холодный бетон) ---
        self.LIGHT_SURFACE =                    "#FAFAFA"
        self.LIGHT_ON_SURFACE =                 "#1D1B20"
        self.LIGHT_ON_SURFACE_VARIANT =         "#49454F"
        self.LIGHT_SURFACE_TINT =               ft.Colors.CYAN_600
        
        self.LIGHT_SURFACE_DIM =                "#E0E0E5"
        self.LIGHT_SURFACE_BRIGHT =             "#FAFAFA"
        self.LIGHT_SURFACE_CONTAINER_LOWEST =   "#FFFFFF"
        self.LIGHT_SURFACE_CONTAINER_LOW =      "#F2F2F7"
        self.LIGHT_SURFACE_CONTAINER =          "#EAEAF0"
        self.LIGHT_SURFACE_CONTAINER_HIGH =     "#E2E2E9"
        self.LIGHT_SURFACE_CONTAINER_HIGHEST =  "#DADADF"
        
        # --- Границы, Инверсия, Тени ---
        self.LIGHT_OUTLINE =                    "#79747E"
        self.LIGHT_OUTLINE_VARIANT =            "#CAC4D0"
        self.LIGHT_SHADOW =                     "#052026"
        self.LIGHT_SCRIM =                      "#000000"
        self.LIGHT_INVERSE_SURFACE =            "#322F35"
        self.LIGHT_ON_INVERSE_SURFACE =         "#F5EFF7"
        self.LIGHT_INVERSE_PRIMARY =            ft.Colors.CYAN_200

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