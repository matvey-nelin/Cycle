import flet as ft

from UI.Screens.BaseView import BaseView
from UI.Components.TemplateCard import TemplateCard



class TemplateContainer(ft.Container):
    def __init__(self, screen: BaseView) -> None:
        super().__init__()

        self.screen = screen
        self.colors = self.screen.colors

        self.data = None

        self.expand=6
        self.margin=ft.Margin.only(left=5, right=5)

        self.border=ft.Border().all(
            width=3,
            color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE
        )
        self.border_radius=4

        self.templates = ft.Column(
            expand=True,
            margin=ft.Margin.symmetric(vertical=10),
            controls=[],

            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            scroll=ft.ScrollMode.AUTO
        )

        self.content = self.templates

    
    def insert_template_card(self, template_card: TemplateCard, position: int = -1, update_container: bool = False):
        
        if position == -1:
            self.templates.controls.append(template_card)
        else:
            self.templates.controls.insert(position, template_card)
        
        if update_container:
            self.templates.update()