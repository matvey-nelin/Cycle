import flet as ft

class AuroraBorealis:
    def __init__(self) -> None:
        
        # ==========================================
        # ТЁМНАЯ ТЕМА (AuroraBorealis - Полярная ночь)
        # ==========================================
        
        # --- Основные акценты (Сияние: Цинк, Зелень, Фиолет) ---
        self.DARK_PRIMARY =                     ft.Colors.CYAN_400
        self.DARK_ON_PRIMARY =                  "#0A0F14"
        self.DARK_PRIMARY_CONTAINER =           ft.Colors.CYAN_800
        self.DARK_ON_PRIMARY_CONTAINER =        ft.Colors.CYAN_100
        self.DARK_PRIMARY_FIXED =               ft.Colors.CYAN_700
        self.DARK_PRIMARY_FIXED_DIM =           ft.Colors.CYAN_800
        self.DARK_ON_PRIMARY_FIXED =            "#0A0F14"
        self.DARK_ON_PRIMARY_FIXED_VARIANT =    "#1A2B30"
        
        self.DARK_SECONDARY =                   ft.Colors.GREEN_400
        self.DARK_ON_SECONDARY =                "#0A0F14"
        self.DARK_SECONDARY_CONTAINER =         ft.Colors.GREEN_800
        self.DARK_ON_SECONDARY_CONTAINER =      ft.Colors.GREEN_100
        self.DARK_SECONDARY_FIXED =             ft.Colors.GREEN_700
        self.DARK_SECONDARY_FIXED_DIM =         ft.Colors.GREEN_800
        self.DARK_ON_SECONDARY_FIXED =          "#0A0F14"
        self.DARK_ON_SECONDARY_FIXED_VARIANT =  "#14281A"
        
        self.DARK_TERTIARY =                    ft.Colors.PURPLE_400
        self.DARK_ON_TERTIARY =                 "#0A0F14"
        self.DARK_TERTIARY_CONTAINER =          ft.Colors.PURPLE_800
        self.DARK_ON_TERTIARY_CONTAINER =       ft.Colors.PURPLE_100
        self.DARK_TERTIARY_FIXED =              ft.Colors.PURPLE_700
        self.DARK_TERTIARY_FIXED_DIM =          ft.Colors.PURPLE_800
        self.DARK_ON_TERTIARY_FIXED =           "#0A0F14"
        self.DARK_ON_TERTIARY_FIXED_VARIANT =   "#241A28"
        
        # --- Ошибки ---
        self.DARK_ERROR =                       ft.Colors.RED_400
        self.DARK_ON_ERROR =                    "#0A0F14"
        self.DARK_ERROR_CONTAINER =             ft.Colors.RED_800
        self.DARK_ON_ERROR_CONTAINER =          ft.Colors.RED_100
        
        # --- Поверхности (Глубокий космос) ---
        self.DARK_SURFACE =                     "#0B0E14"
        self.DARK_ON_SURFACE =                  "#E6E1E5"
        self.DARK_ON_SURFACE_VARIANT =          "#C4C7C5"
        self.DARK_SURFACE_TINT =                ft.Colors.CYAN_400
        
        self.DARK_SURFACE_DIM =                 "#05070A"
        self.DARK_SURFACE_BRIGHT =              "#2A2D33"
        self.DARK_SURFACE_CONTAINER_LOWEST =    "#080A0F"
        self.DARK_SURFACE_CONTAINER_LOW =       "#0B0E14"
        self.DARK_SURFACE_CONTAINER =           "#11141A"
        self.DARK_SURFACE_CONTAINER_HIGH =      "#171A20"
        self.DARK_SURFACE_CONTAINER_HIGHEST =   "#1E2127"
        
        # --- Границы, Инверсия, Тени ---
        self.DARK_OUTLINE =                     "#938F99"
        self.DARK_OUTLINE_VARIANT =             "#49454F"
        self.DARK_SHADOW =                      "#000A14"
        self.DARK_SCRIM =                       "#000000"
        self.DARK_INVERSE_SURFACE =             "#E6E1E5"
        self.DARK_ON_INVERSE_SURFACE =          "#0A0F14"
        self.DARK_INVERSE_PRIMARY =             ft.Colors.CYAN_700

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
        # СВЕТЛАЯ ТЕМА (AuroraBorealis - Полярный день)
        # ==========================================
        
        # --- Основные акценты ---
        self.LIGHT_PRIMARY =                    ft.Colors.CYAN_700
        self.LIGHT_ON_PRIMARY =                 ft.Colors.WHITE
        self.LIGHT_PRIMARY_CONTAINER =          ft.Colors.CYAN_100
        self.LIGHT_ON_PRIMARY_CONTAINER =       ft.Colors.CYAN_900
        self.LIGHT_PRIMARY_FIXED =              ft.Colors.CYAN_700
        self.LIGHT_PRIMARY_FIXED_DIM =          ft.Colors.CYAN_800
        self.LIGHT_ON_PRIMARY_FIXED =           "#0A0F14"
        self.LIGHT_ON_PRIMARY_FIXED_VARIANT =   "#1A2B30"
        
        self.LIGHT_SECONDARY =                  ft.Colors.GREEN_700
        self.LIGHT_ON_SECONDARY =               ft.Colors.WHITE
        self.LIGHT_SECONDARY_CONTAINER =        ft.Colors.GREEN_100
        self.LIGHT_ON_SECONDARY_CONTAINER =     ft.Colors.GREEN_900
        self.LIGHT_SECONDARY_FIXED =            ft.Colors.GREEN_700
        self.LIGHT_SECONDARY_FIXED_DIM =        ft.Colors.GREEN_800
        self.LIGHT_ON_SECONDARY_FIXED =         "#0A0F14"
        self.LIGHT_ON_SECONDARY_FIXED_VARIANT = "#14281A"
        
        self.LIGHT_TERTIARY =                   ft.Colors.PURPLE_700
        self.LIGHT_ON_TERTIARY =                ft.Colors.WHITE
        self.LIGHT_TERTIARY_CONTAINER =         ft.Colors.PURPLE_100
        self.LIGHT_ON_TERTIARY_CONTAINER =      ft.Colors.PURPLE_900
        self.LIGHT_TERTIARY_FIXED =             ft.Colors.PURPLE_700
        self.LIGHT_TERTIARY_FIXED_DIM =         ft.Colors.PURPLE_800
        self.LIGHT_ON_TERTIARY_FIXED =          "#0A0F14"
        self.LIGHT_ON_TERTIARY_FIXED_VARIANT =  "#241A28"
        
        # --- Ошибки ---
        self.LIGHT_ERROR =                      ft.Colors.RED_600
        self.LIGHT_ON_ERROR =                   ft.Colors.WHITE
        self.LIGHT_ERROR_CONTAINER =            ft.Colors.RED_100
        self.LIGHT_ON_ERROR_CONTAINER =         ft.Colors.RED_900
        
        # --- Поверхности (Ледяная свежесть) ---
        self.LIGHT_SURFACE =                    "#F8FAFC"
        self.LIGHT_ON_SURFACE =                 "#1D1B20"
        self.LIGHT_ON_SURFACE_VARIANT =         "#49454F"
        self.LIGHT_SURFACE_TINT =               ft.Colors.CYAN_700
        
        self.LIGHT_SURFACE_DIM =                "#D8DDE3"
        self.LIGHT_SURFACE_BRIGHT =             "#F8FAFC"
        self.LIGHT_SURFACE_CONTAINER_LOWEST =   "#FFFFFF"
        self.LIGHT_SURFACE_CONTAINER_LOW =      "#F0F4F8"
        self.LIGHT_SURFACE_CONTAINER =          "#E8EDF2"
        self.LIGHT_SURFACE_CONTAINER_HIGH =     "#E0E5EB"
        self.LIGHT_SURFACE_CONTAINER_HIGHEST =  "#D8DDE3"
        
        # --- Границы, Инверсия, Тени ---
        self.LIGHT_OUTLINE =                    "#79747E"
        self.LIGHT_OUTLINE_VARIANT =            "#CAC4D0"
        self.LIGHT_SHADOW =                     "#1A2B30"
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