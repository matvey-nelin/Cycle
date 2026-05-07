import flet as ft

from UI.ColorThemes.AppColors import AppColors


class NavigationOption(ft.Container):
    def __init__(self, colors: AppColors, text: str, navigation_screen_name: str, navigation_callback, data = None) -> None:
        super().__init__()

        self.object_data = data
        self.colors = colors

        self.on_click = self.open_screen
        self.navigate = navigation_callback
        self.navigation_screen_name = navigation_screen_name


        self.border = ft.Border().all(
            width=2, 
            color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE
        )
        self.border_radius = 10

        self.padding = 15

        self.alignment = ft.Alignment.CENTER


        self.text = ft.Text(
            expand=True,
            value=text,
            size=16,
            color=self.colors.LIGHT_ON_SURFACE if self.colors.theme == "light" else self.colors.DARK_ON_SURFACE,
            no_wrap=False,
            max_lines=3,
        )

        self.arrow_icon = ft.Icon(
            icon=ft.Icons.KEYBOARD_ARROW_RIGHT_ROUNDED,
            color=self.colors.LIGHT_SECONDARY if self.colors.theme == "light" else self.colors.DARK_SECONDARY,
            size=35
        )

        self.content = ft.Row(
            controls=
            [
                self.text,
                self.arrow_icon
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )


    def open_screen(self):
        self.navigate(self.navigation_screen_name)

    def navigation_option_on_hover(self, e):
        navigation_option_bgcolor = self.colors.LIGHT_OUTLINE_VARIANT if self.colors.theme == 'light' else self.colors.DARK_OUTLINE_VARIANT
        e.control.bgcolor = navigation_option_bgcolor if e.data else None