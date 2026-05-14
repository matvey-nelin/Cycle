import flet as ft

from AppState import AppState


class BaseView:
    def __init__(self, 
            page: ft.Page, 
            navigate_callback,
            app_state: AppState,
            previous_screen_name: str | None = None
        ):
        super().__init__()

        self.page = page 

        self.__on_page_resize__(None)

        self.app_state = app_state

        self.database   = self.app_state.database
        self.settings   = self.app_state.settings
        self.translator = self.app_state.translator
        self.colors     = self.app_state.colors

        self.navigate   = navigate_callback
        self.previous_screen_name = previous_screen_name



        self.open_previous_screen_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK_ROUNDED,
            on_click=self.return_previous_screen
        )


        self.appbar = ft.Container(
            margin=ft.Margin.symmetric(horizontal=5),
            content=ft.Row(
                controls=[self.open_previous_screen_button],
                alignment=ft.MainAxisAlignment.START
            ),
            visible=(self.previous_screen_name is not None)
        )
            

        self.main_container = ft.Container(
            expand=True,
            content=ft.Text(
                value="Default main container content",
                color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
            ), 
            alignment=ft.Alignment.CENTER 
        )

        self.content = ft.Column(
            spacing=0,
            controls=[
                self.appbar,
                self.main_container
            ], 
            expand=True, 
            scroll=None,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        

            
    def return_previous_screen(self):
        self.navigate(self.previous_screen_name)

     
    def _on_state_change(self):
        pass

    def __on_page_resize__(self, e):
        self.page_width = self.page.width
        if self.page_width is None:
            raise ValueError("Invalid min width of the page")

        self.page_height = self.page.height
        if self.page_height is None:
            raise ValueError("Invalid min height of the page")
        
        self.page.update()