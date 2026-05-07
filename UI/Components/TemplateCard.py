import flet as ft

from UI.Components.ManagerDialog import ManagerDialog
from UI.Screens.BaseView import BaseView


class TemplateCard(ft.Container):
    def __init__(self, screen: BaseView, id: int, data: list, width: int | None, height: int | None, on_card_click, delete_function = None, delete_from_list_function = None) -> None:
        super().__init__()

        self.id     = id
        self.data   = data
        self.screen = screen
        self.colors = self.screen.colors
        
        self.margin     = 0
        self.width      = width
        self.height     = height


        self.bgcolor = self.colors.LIGHT_SURFACE if self.colors.theme == "light" else self.colors.DARK_SURFACE
        self.border_radius = 10

        if self.colors.theme == "light":
            self.shadow = [
                ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE,
                    offset=ft.Offset(0, 2)
                )
            ]
        else:
            self.border = ft.Border().all(
                width=1,
                color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE
            )
        

        self.delete_function = None

        self.on_click = lambda: on_card_click(self.id)
        # self.on_hover = self.change_gradient_on_hover

        if delete_function is not None:
            self.on_long_press = self.show_manager_dialog
            self.delete_function = lambda: delete_function(self.id)

        if delete_from_list_function is not None:
            self.on_long_press = self.show_manager_dialog
            self.delete_function = lambda: delete_from_list_function(self)


        self.alignment = ft.Alignment.TOP_CENTER

        card_controls = []
        for index, card_data in enumerate(data):
            if isinstance(card_data, str):
                card_data = ft.Text(
                    margin=ft.Margin.symmetric(vertical=5),
                    value=card_data,
                    text_align= (ft.TextAlign.CENTER if index == 0 else ft.TextAlign.START),
                    color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND,
                    size=(14 if index == 0 else 12), # Размер первого тайтла в списке (14) и размер остальных тайтлов (12)
                    width=self.width,
                    max_lines=5
                ) 
            
            card_controls.append(card_data)

            if index == 0:
                card_controls.append(
                    ft.Divider(
                        color=self.colors.LIGHT_OUTLINE_VARIANT if self.colors.theme == "light" else self.colors.DARK_OUTLINE_VARIANT
                    )
                )


        self.content = ft.Container(
            padding=5,
            content=
                ft.Column(
                    spacing=0, 
                    controls = card_controls,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START
                )
        )      
        


    


    def show_manager_dialog(self):
        self.screen.page.show_dialog(
            ManagerDialog(
                app_state=self.screen.app_state,
                id=self.id, 
                title=self.data[0], 
                essence="workout_templates",
                delete_function=self.delete_function
            )
        )


    def change_gradient_on_hover(self, e):
        pass
        # self.gradient = self.colors.Gradients.CARD_HOVER if e.data == True else self.colors.Gradients.CARD_DEFAULT
        # self.update()
    