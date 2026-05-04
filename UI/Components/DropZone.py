import flet as ft



class DropZone(ft.DragTarget):
    def __init__(self, exercise_set, index: int, height: int = 5):
        super().__init__(ft.Row())
        
        self.data = index
        self.group = "exercise_set"
        self.on_will_accept = exercise_set._on_set_will_accept_
        # self.on_leave       = exercise_set._on_set_leave_
        
        
        # Линия-индикатор (изначально прозрачная)
        self.indicator = ft.Container(
            height=4,
            bgcolor=exercise_set.colors.LIGHT_PRIMARY if exercise_set.colors.theme == "light" else exercise_set.colors.DARK_PRIMARY,
            visible=False,
            border_radius=2
        )
        
        # Контейнер зоны (минимальная высота для захвата)
        self.content = ft.Container(
            content=self.indicator,
            padding=ft.Padding.symmetric(vertical=height),  # Зона захвата 10px
            height=1  # Визуально почти не занимает места
        )

        

 
 
    def _on_will_accept_(self, e):
        if e:
            self.indicator.visible = True
            self.indicator.update()

    def _on_leave_(self, e):
        self.indicator.visible = False
        self.indicator.update()
