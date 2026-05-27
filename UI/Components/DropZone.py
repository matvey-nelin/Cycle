import flet as ft



class DropZone(ft.DragTarget):
    def __init__(self, exercise_set, index: int, height: int | float = 10):
        super().__init__(ft.Row())

        self.exercise_set = exercise_set

        
        self.data = index
        self.group = "exercise_set"
        self.on_accept      = self._on_accept_
        self.on_will_accept = self._on_will_accept_
        self.on_leave       = self._on_leave_
        


        self.indicator = ft.Container(
            height=4,
            opacity=0.0,

            bgcolor=ft.Colors.with_opacity(opacity=0.5, color=ft.Colors.PRIMARY),
            border_radius=5,

            animate_opacity=ft.Animation(
                duration=200,
                curve=ft.AnimationCurve.EASE_IN_OUT
            )
        )

        self.content = ft.Container(
            height=height,
            content=self.indicator,
        )


        

 
    def _on_accept_(self, e):
        if hasattr(self.exercise_set, "_on_set_will_accept_"):
            self.exercise_set._on_set_will_accept_(e)

        if isinstance(self.content, ft.Container):
            self.content.gradient   = None
            self.indicator.opacity  = 0.0
            self.content.update()
 

    def _on_will_accept_(self, e):
        if e and isinstance(self.content, ft.Container):
            self.content.gradient   = self.exercise_set.colors.Gradients.DIVIDER_FADE
            self.indicator.opacity  = 1.0
            self.content.update()


    def _on_leave_(self, e):
        if hasattr(self.exercise_set, "_on_set_leave_"):
            self.exercise_set._on_set_leave_(e)

        if isinstance(self.content, ft.Container):
            self.content.gradient   = None
            self.indicator.opacity  = 0.0
            self.content.update()
