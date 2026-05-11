import flet as ft
import platform
import os

import utils

from AppState import AppState

from UI.Layouts import DesktopLayout, MobileLayout, ClearLayout


from UI.Screens.SetupWizard import SetupWizard


from UI.Screens.Dashboard.DashboardScreen import DashboardScreen


from UI.Screens.Planning.PlanningScreen import PlanningScreen

from UI.Screens.Planning.WorkoutTemplateMenu        import WorkoutTemplateMenu
from UI.Screens.Planning.WorkoutTemplateScreen      import WorkoutTemplateScreen
from UI.Screens.Planning.MicrocycleTemplateMenu     import MicrocycleTemplateMenu
from UI.Screens.Planning.MicrocycleTemplateScreen   import MicrocycleTemplateScreen
from UI.Screens.Planning.MesocycleMenu              import MesocycleMenu
from UI.Screens.Planning.MesocycleScreen            import MesocycleScreen
from UI.Screens.Planning.WorkoutScreen              import WorkoutScreen
from UI.Screens.Planning.MacrocycleMenu             import MacrocycleMenu
from UI.Screens.Planning.MacrocycleScreen           import MacrocycleScreen


from UI.Screens.ReferenceInformation.ReferenceInformationScreen import ReferenceInformationScreen

from UI.Screens.ReferenceInformation.UserInformationScreen  import UserInformationScreen
from UI.Screens.ReferenceInformation.UsersScreen            import UsersScreen
from UI.Screens.ReferenceInformation.UserStatusesScreen     import UserStatusesScreen
from UI.Screens.ReferenceInformation.WorkoutStatusesScreen  import WorkoutStatusesScreen
from UI.Screens.ReferenceInformation.WorkoutTypesScreen     import WorkoutTypesScreen
from UI.Screens.ReferenceInformation.HypertrophyTypesScreen import HypertrophyTypesScreen
from UI.Screens.ReferenceInformation.ExercisesScreen        import ExercisesScreen
from UI.Screens.ReferenceInformation.AgonistsScreen         import AgonistsScreen

from UI.Screens.ReferenceInformation.UniversalRecordManagementScreen    import UniversalRecordManagementScreen
from UI.Screens.ReferenceInformation.UserManagementScreen               import UserManagementScreen
from UI.Screens.ReferenceInformation.ExerciseManagementScreen           import ExerciseManagementScreen
from UI.Screens.ReferenceInformation.AgonistManagementScreen            import AgonistManagementScreen


from UI.Screens.Settings.SettingsScreen             import SettingsScreen

from UI.Screens.Settings.ActiveUserStatusesScreen   import ActiveUserStatusesScreen
from UI.Screens.Settings.AppColorThemesScreen       import AppColorThemesScreen




class CycleApp:
    def __init__(self, page: ft.Page, app_state: AppState) -> None:
        self.app_state 	= app_state
        self.app_state.change_orientation(page)
        
        self.database 	= self.app_state.database
        self.settings	= self.app_state.settings
        self.translator = self.app_state.translator
        self.colors     = self.app_state.colors


        self.page = page
        self.page.window.min_width  = 360
        self.page.window.min_height = 480
        self.page.padding = 0
        self.app_state.resize_subscribe(self._on_resize_page_)
        self.page.on_resize = self.app_state.resize_notify

        self.page.title = "Cycle"
        self.page.window.icon = self.get_icon_path()

        # Назначение шрифтов приложения
        self.page.fonts = {
            "Nunito"            : "assets/fonts/Nunito-Regular.ttf",
            "Nunito-Bold"       : "assets/fonts/Nunito-Bold.ttf",
            "Nunito-SemiBold"   : "assets/fonts/Nunito-SemiBold.ttf",
        }

        self.text_theme = ft.TextTheme(
            # --- Заголовки ---
            display_large=ft.TextStyle(
                font_family="Nunito-Bold",
                size=32,
                weight=ft.FontWeight.W_700,
            ),
            headline_medium=ft.TextStyle(
                font_family="Nunito-SemiBold",
                size=24,
                weight=ft.FontWeight.W_600,
            ),
            title_large=ft.TextStyle(
                font_family="Nunito-SemiBold",
                size=20,
                weight=ft.FontWeight.W_600,
            ),
            
            # --- Основной текст ---
            body_large=ft.TextStyle(
                font_family="Nunito",
                size=16,
                weight=ft.FontWeight.W_400,
            ),
            body_medium=ft.TextStyle(
                font_family="Nunito",
                size=14,
                weight=ft.FontWeight.W_400,
            ),
            body_small=ft.TextStyle(
                font_family="Nunito",
                size=12,
                weight=ft.FontWeight.W_400,
                color=self.colors.LIGHT_ON_SECONDARY if self.colors.theme == "light" else self.colors.DARK_ON_SECONDARY,  # Для второстепенной информации
            ),
            
            # --- Кнопки и метки ---
            label_large=ft.TextStyle(
                font_family="Nunito-Bold",
                size=16,
                weight=ft.FontWeight.W_700,
            ),
            label_medium=ft.TextStyle(
                font_family="Nunito",
                size=14,
                weight=ft.FontWeight.W_500,
            )
        )

        # Назначение цветов приложения
        self.page.theme         = ft.Theme(color_scheme=self.colors.light_color_scheme, text_theme=self.text_theme)
        self.page.dark_theme    = ft.Theme(color_scheme=self.colors.dark_color_scheme, text_theme=self.text_theme)
        self.page.theme_mode    = ft.ThemeMode(self.app_state.settings.theme_mode)

        if self.app_state.settings.theme_mode == "system":
            self.page.on_platform_brightness_change = self.colors.init_all_colors
            self.colors.init_all_colors(self.page.platform_brightness)


        self.current_layout = "global"
        self.screen_name    = "dashboard_screen"


        self.app_state.hot_restart_methods.append(self.initialisation_all_screens)
        self.initialisation_all_screens()

        self.app_state.hot_restart_methods.append(self.initialisation_all_layouts)
        self.initialisation_all_layouts()

        

        # Вызов мастера настройки приложения в первый запуск
        if self.app_state.settings.first_launch:
            self.current_layout = 'local'
            self.screen_name    = "setup_wizard"
            SetupWizard(self.page, self.navigate, self.app_state)
        elif self.settings.current_workout != 0:
            self.navigate(
                screen_name=            "planning_workout_screen",
                is_temporary_screen=    True,
                id_workout=             self.settings.current_workout, 
                is_planning_screen=     False,
                page=                   self.page, 
                navigate_callback=      self.navigate, 
                app_state=              self.app_state, 
                previous_screen_name=   "dashboard_screen"
            )

        else:
            self.navigate(self.screen_name)
        


    def navigate(self, screen_name: str, is_temporary_screen: bool = False, is_universal_screen: bool = False, **kwargs):
        """
        :param is_temporary_screen : Временный экран, существует только во время отображения на экране
        :param is_universal_screen : Универсальный экран с переопределяемыми данными
        :param screen_name         : Имя экрана для открытия
        """

        if is_temporary_screen and is_universal_screen:
            raise ValueError("Must be only one value of the type screen")
        
        
        self.screen_name = screen_name

        if self.screen_name in list(self.global_screens.keys()):
            screens_list        = self.global_screens
            self.layout         = self.global_layout

            if self.current_layout == "local":
                self.determine_selected_navigation_option()
                
                if self.layout is self.mobile_layout:
                    self.page.bottom_appbar = self.mobile_layout.bottom_appbar

                self.page.controls.clear()
                self.page.add(self.layout.layout_container)
                self.current_layout = "global"
                

        elif self.screen_name in list(self.local_screens.keys()):
            screens_list        = self.local_screens
            self.layout         = self.local_layout

            if self.current_layout == "global":
                self.page.bottom_appbar = None

                self.page.controls.clear()
                self.page.add(self.layout.layout_container)
                self.current_layout = "local"

        else:
            raise ValueError(f"Incorrect screen name value: {self.screen_name}")
        

        if is_universal_screen:
            screens_list[self.screen_name]._init_data_(**kwargs)
        
            # Обычный экран, создается при инициализации списка экранов
        self.screen =  (screens_list[self.screen_name](**kwargs) if is_temporary_screen 
                else    screens_list[self.screen_name])

        self.layout.change_screen(self.screen)

        try:
            self.page.update() 
        except:
            pass 



    def _on_resize_page_(self, e):
        change_layout = self.app_state.change_orientation(self.page)

        # Изменение лэйаута с меню для глобальных экранов (или назначение в первый запуск)
            # Назначение лэйаута если экран пуст или масштаб изменился
        if change_layout:
            self.determine_selected_navigation_option()
                    
            self.global_layout = self.mobile_layout if self.app_state.is_mobile else self.desktop_layout

            if self.current_layout == "global":
                self.page.bottom_appbar = self.global_layout.bottom_appbar if isinstance(self.global_layout, MobileLayout.MobileLayout) \
                    else None

                self.page.controls.clear()
                self.page.add(self.global_layout.layout_container)

                self.navigate(self.screen_name)

        # Назначение лэйаута для локальных экранов 
        self.local_layout   = self.clear_layout

        try:
            self.page.update() 
        except:
            pass 




    def get_icon_path(self):
        """Определяем оптимальную иконку для текущей ОС"""
        system = platform.system()
        
        if system == "Windows":
            # Для Windows используем ICO
            icon_path = utils.resource_path(r"assets/icons/windows_icon.ico")
            if os.path.exists(icon_path):
                return icon_path
            # Fallback на PNG
            return utils.resource_path(r"assets/icons/app_icon.png")
        
        elif system == "Darwin":  # macOS
            # Для macOS пробуем ICNS
            icon_path = utils.resource_path(r"assets/icons/apple_app_icon.icns")
            if os.path.exists(icon_path):
                return icon_path
            # Fallback на PNG
            return utils.resource_path(r"assets/icons/app_icon.png")
        
        else:  # Linux и другие
            return utils.resource_path(r"assets/icons/app_icon.png")
        


    def determine_selected_navigation_option(self):
        # Сохранение позиции кнопки при ресайзе
        if self.screen_name in self.global_screens:
            self.desktop_layout.navigation_rail.selected_index = list(self.global_screens.keys()).index(self.screen_name)
            
            if isinstance(self.mobile_layout.bottom_appbar.content, ft.Row):
                for index, bottom_appbar_option in enumerate(self.mobile_layout.bottom_appbar.content.controls):
                    if isinstance(bottom_appbar_option, ft.IconButton):
                        bottom_appbar_option.selected = True if index == list(self.global_screens.keys()).index(self.screen_name) \
                            else False
        

    
    def initialisation_all_layouts(self):
        self.page.controls.clear()

        self.desktop_layout = DesktopLayout.DesktopLayout(self.page, self.app_state, self.translator, self.navigate)
        self.mobile_layout  = MobileLayout.MobileLayout(self.page, self.app_state, self.translator, self.navigate)
        self.clear_layout   = ClearLayout.ClearLayout(self.page,self.translator, self.navigate)

        self.determine_selected_navigation_option()

        
        self.app_state.subscribe(self.desktop_layout._on_state_changes)
        
        if self.app_state.is_mobile:
            self.global_layout = self.mobile_layout
            self.page.bottom_appbar = self.global_layout.bottom_appbar
        else:
            self.global_layout = self.desktop_layout

        self.local_layout   = self.clear_layout


        if self.current_layout == "global":
            self.page.bottom_appbar = self.global_layout.bottom_appbar if isinstance(self.global_layout, MobileLayout.MobileLayout) \
                else None
            self.page.add(self.global_layout.layout_container)

        elif self.current_layout == "local":
            self.page.add(self.clear_layout.layout_container)
            self.page.bottom_appbar = None


        self.navigate(self.screen_name)
    


    def initialisation_all_screens(self):
        self.global_screens = \
        {
            "dashboard_screen"              : DashboardScreen(self.page, self.navigate, self.app_state),
            "planning_screen"               : PlanningScreen(self.page, self.navigate, self.app_state),
            "reference_information_screen"  : ReferenceInformationScreen(self.page, self.navigate, self.app_state),
            "settings_screen"               : SettingsScreen(self.page, self.navigate, self.app_state)
        }

        self.local_screens = \
        {
            # planning screens
            "workout_template_menu"     : WorkoutTemplateMenu(self.page, self.navigate, self.app_state, previous_screen_name="planning_screen"),
                "workout_template_screen"           : WorkoutTemplateScreen,
            "microcycle_template_menu"  : MicrocycleTemplateMenu(self.page, self.navigate, self.app_state, previous_screen_name="planning_screen"),
                "microcycle_template_screen"        : MicrocycleTemplateScreen(0, self.page, self.navigate, self.app_state),
                "choosable_workout_template_menu"   : WorkoutTemplateMenu,
            "mesocycle_menu"            : MesocycleMenu(self.page, self.navigate, self.app_state, previous_screen_name="planning_screen"),
                "mesocycle_screen"                  : MesocycleScreen(0, self.page, self.navigate, self.app_state),
                "choosable_microcycle_template_menu": MicrocycleTemplateMenu,
                "planning_workout_screen"           : WorkoutScreen,
            "macrocycle_menu"           : MacrocycleMenu(self.page, self.navigate, self.app_state, "planning_screen"),
                "macrocycle_screen"                 : MacrocycleScreen(0, self.page, self.navigate, self.app_state),
                "choosable_mesocycle_menu"          : MesocycleMenu,

            
            # reference information screens
            "user_information_screen"   : UserInformationScreen(self.page, self.navigate, self.app_state, "reference_information_screen"),
                "users_screen"                      :  UsersScreen(self.page, self.navigate, self.app_state, "user_information_screen"),
                "user_statuses_screen"              :  UserStatusesScreen(self.page, self.navigate, self.app_state, "user_information_screen"),
            "workout_statuses_screen"   : WorkoutStatusesScreen(self.page, self.navigate, self.app_state, "reference_information_screen"),
            "workout_types_screen"      : WorkoutTypesScreen(self.page, self.navigate, self.app_state, "reference_information_screen"),
            "hypertrophy_types_screen"  : HypertrophyTypesScreen(self.page, self.navigate, self.app_state, "reference_information_screen"),
            "exercises_screen"          : ExercisesScreen(self.page, self.navigate, self.app_state, "reference_information_screen"),
            "agonists_screen"           : AgonistsScreen(self.page, self.navigate, self.app_state, "reference_information_screen"),
            # information management screens
            "universal_record_management_screen"    : UniversalRecordManagementScreen,
            "user_management_screen"                : UserManagementScreen,
            "exercise_management_screen"            : ExerciseManagementScreen,
            "agonist_management_screen"             : AgonistManagementScreen,


            # settings screen
            "active_user_statuses_screen"   : ActiveUserStatusesScreen(self.page, self.navigate, self.app_state, "settings_screen"),
            "app_color_themes_screen"       : AppColorThemesScreen(self.page, self.navigate, self.app_state, "settings_screen")
        }


            