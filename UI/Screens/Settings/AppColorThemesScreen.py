import flet as ft

from AppState import AppState
from UI.Screens.BaseView import BaseView

from UI.ColorThemes import SupportedColorThemes




class AppColorThemesScreen(BaseView):
    def __init__(self, page: ft.Page, navigate_callback, app_state: AppState, previous_screen_name: str | None = None):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        self.labels = self.translator.app_color_themes_screen

        self.color_themes_list_view = ft.ListView(
            margin=0,
		    spacing=5,
            controls=[],
        )
        
        self.main_container.alignment   = ft.Alignment.TOP_CENTER
        self.main_container.content     = self.color_themes_list_view

        self._init_data_()


    
    def _init_data_(self):
        for color_theme in SupportedColorThemes.COLOR_THEMES:
            title_list_tile = self.translator.app_colors_labels["color_themes"].get(color_theme, color_theme)

            background_list_tile    = None
            title_color_list_tile   = ft.Colors.ON_SURFACE

            if color_theme == self.settings.color_theme:
                background_list_tile = ft.Colors.PRIMARY_CONTAINER
                title_color_list_tile = ft.Colors.ON_PRIMARY_CONTAINER


            self.color_themes_list_view.controls.append(
                ft.Container(
                    data={"color_theme": color_theme},
                    expand=False,
                    content=ft.ListTile(
                        expand=False,
                        bgcolor=background_list_tile,
                        title=title_list_tile,
                        title_text_style=ft.TextStyle(
                            size=16,
                            weight=ft.FontWeight.W_400,
                            color=title_color_list_tile
                        ),
                        title_alignment=ft.ListTileTitleAlignment.CENTER,
                        leading=ft.Icon(
                            icon=ft.Icons.COLOR_LENS_ROUNDED,
                            size=20,
                            color=self.colors.LIGHT_SECONDARY if self.colors.theme == 'light' else self.colors.DARK_SECONDARY
                        )
                    ),
                    on_click=self.color_theme_list_tile_on_click,
                    on_hover=self.color_theme_list_tile_on_hover,

                    border=ft.Border.all(
                        width=1,
                        color=self.colors.LIGHT_OUTLINE if self.colors.theme == 'light' else self.colors.DARK_OUTLINE
                    ),
                    border_radius=5,

                    alignment=ft.Alignment.CENTER
                )
            )

    
    def color_theme_list_tile_on_click(self, e):
        self.app_state.change_color_theme(e.control.data["color_theme"])

    
    def color_theme_list_tile_on_hover(self, e):
        # Не меняю фон текущей темы
        if e.control.data["color_theme"] == self.settings.color_theme:
            return

        color_theme_list_tile_bgcolor = self.colors.LIGHT_OUTLINE_VARIANT if self.colors.theme == 'light' else self.colors.DARK_OUTLINE_VARIANT
        e.control.bgcolor = color_theme_list_tile_bgcolor if e.data == True else None