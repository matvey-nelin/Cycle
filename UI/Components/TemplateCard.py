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


        self.bgcolor = ft.Colors.SURFACE_CONTAINER_HIGH
        self.border_radius = 10

        self.shadow = [
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.SHADOW,
                offset=ft.Offset(0, 4)
            )
        ]


        self.animate = ft.Animation(
            duration=200,
            curve=ft.AnimationCurve.BOUNCE_IN_OUT
        )
        

        
        self.on_click = lambda: on_card_click(self.id)
        self.on_hover = self.change_bgcolor_on_hover
        

        # Определение функции удаления
        self.delete_function = None

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
                    color=ft.Colors.ON_SURFACE,
                    size=(14 if index == 0 else 12), # Размер первого тайтла в списке (14) и размер остальных тайтлов (12)
                    width=self.width,
                    max_lines=5
                ) 
            
            card_controls.append(card_data)

            if index == 0:
                card_controls.append(
                    ft.Divider(
                        color=ft.Colors.OUTLINE_VARIANT
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
                delete_function=self.perform_deletion
            )
        )

    def perform_deletion(self):
        if self.delete_function is not None:
            self.delete_function()



    def change_bgcolor_on_hover(self, e): 
        self.bgcolor = ft.Colors.SURFACE_CONTAINER_LOW if e.data == True else ft.Colors.SURFACE_CONTAINER_HIGH
        self.update()
    