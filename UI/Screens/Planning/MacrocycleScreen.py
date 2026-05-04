import datetime

import flet as ft

from AppState               import AppState
from UI.Screens.BaseView    import BaseView

from UI.Components.TemplateCard             import TemplateCard
from UI.Components.InvalidDataAlertDialog   import InvalidDataAlertDialog

class MacrocycleScreen(BaseView):
    def __init__(
            self, 
            id_macrocycle: int, 
            page: ft.Page, 
            navigate_callback, 
            app_state: AppState, 
            previous_screen_name: str | None = "macrocycle_menu"
        ):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        self.id = id_macrocycle
        self.labels = self.translator.macrocycle_screen_labels
        self.app_state.data_changed_subscribe(self._init_data_)


        self.add_mesocycle_button = ft.Container(
            height=40,
            width=150,
            
            gradient=self.colors.Gradients.BUTTON_PRIMARY,

            content=ft.Icon(
                icon=ft.Icons.ADD_ROUNDED,
                color=self.colors.LIGHT_ON_PRIMARY if self.colors.theme == "light" else self.colors.DARK_ON_PRIMARY
            ),

            border=ft.Border().all(
                width=1,
                color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE
            ),
            border_radius=15,

            alignment=ft.Alignment.CENTER,

            on_hover=self._on_hover_add_button_,
            on_click=self._add_mesocycle_
        )

        self.mesocycles = []



        self.mesocycles_container = ft.Column(
            width=400,
            controls=
            [
                *self.mesocycles, 
                self.add_mesocycle_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )

        self.main_container.content = self.mesocycles_container
        self.main_container.border = ft.Border.all(
            width=5,
            color=self.colors.LIGHT_OUTLINE if self.colors.theme == "light" else self.colors.DARK_OUTLINE
        )
        self.main_container.border_radius = 10



    def _init_data_(self, id_macrocycle: int):
        # Переопределение данных элементов страницы
        if id_macrocycle != self.id:
            try:
                self.app_state._data_changed_listeners.remove(lambda: self._init_data_(self.id))
            except ValueError:
                pass

            self.id = id_macrocycle
            self.app_state.data_changed_subscribe(lambda: self._init_data_(self.id))

        self.mesocycles = []
        
        for mesocycle in self.database.get_mesocycles(self.settings.current_user, id_macrocycle=self.id):
            id_mesocycle   = int(mesocycle[0])
            mesocycle_card  = self.create_mesocycle_card(id_mesocycle)
            self.mesocycles.append(mesocycle_card)
        

        if self.mesocycles != []:
            self.mesocycles_container.controls = [*self.mesocycles, self.add_mesocycle_button]
            self.main_container.content = self.mesocycles_container
        else:
            self.main_container.content = ft.Column(
                width=400,
                controls=
                [
                    ft.Text(
                        value=self.labels["no_data"],
                        size=16,
                        color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == 'light' else self.colors.DARK_ON_BACKGROUND
                    ), 
                    self.add_mesocycle_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
            )
    

    def choose_mesocycle(self, e):
        id_mesocycle = e
        self.database.update_mesocycle(id_mesocycle, self.id)

        mesocycle_card  = self.create_mesocycle_card(id_mesocycle)
        self.mesocycles.append(mesocycle_card)

        self.mesocycles_container.controls = [*self.mesocycles, self.add_mesocycle_button]

        self.app_state.data_changed_notify()
        self.navigate("macrocycle_screen")
        self.mesocycles_container.update()


    def remove_mesocycle(self, e):
        self.mesocycles.remove(e)
                        
        self.database.update_mesocycle(e.id, 0)

        self.mesocycles_container.update()
        self.app_state.data_changed_notify()



    def create_mesocycle_card(self, id_mesocycle: int):
        mesocycle_card_info = []

        ranges = self.database.get_mesocycle_range(id_mesocycle)
        if ranges == []:
            self.page.show_dialog(InvalidDataAlertDialog(self.app_state, self.labels["invalid_mesocycle_data"]))
            return

        start_range   = datetime.datetime.fromtimestamp(ranges[0][0]).date().strftime("%d.%m.%Y") if ranges[0][0] != 0 else None
        end_range     = datetime.datetime.fromtimestamp(ranges[0][1]).date().strftime("%d.%m.%Y") if ranges[0][1] != 0 else None
        statuses      = self.database.get_mesocycle_workout_statuses(self.settings.current_user, id_mesocycle)


        if (start_range is not None) and (end_range is not None):
            mesocycle_card_info.append(
                ft.Row(
                    controls=
                    [
                        ft.Text(
                            value=start_range,
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                        ),
                        
                        ft.Text(
                            value=" - ",
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                        ),
                        ft.Text(
                            value=end_range,
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            )


        count_all_statuses = sum([status[2] for status in statuses])

        for status in statuses:
            title_status = self.translator.workout_statuses[status[1]]
            count_status = str(status[2]) 

            mesocycle_card_info.append(
                ft.Row(
                    expand=True,
                    controls=
                    [
                        ft.Text(
                            value=title_status,
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                        ),
                        
                        ft.Text(
                            value=f"{count_status} / {count_all_statuses}",
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        if mesocycle_card_info == []:
            mesocycle_card_info.append(
                ft.Row(
                    controls=
                    [
                        ft.Text(
                            value=self.labels["mesocycle_no_data"],
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND,
                            text_align=ft.TextAlign.CENTER
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        
        return TemplateCard(
            screen=         self,
            id=             id_mesocycle,
            data=           mesocycle_card_info,
            width=          300,
            height=         200,
            on_card_click=  lambda id: self.open_mesocycle_screen(id),
            delete_from_list_function=lambda e: self.remove_mesocycle(e)
        )





    def open_mesocycle_screen(self, id_mesocycle: int):
        self.navigate(
            screen_name=            "mesocycle_screen",
            is_universal_screen=    True,
            id_mesocycle=           id_mesocycle,
            previous_screen_name=   "macrocycle_screen"
        )




    def _on_hover_add_button_(self, e):
        try:
            if e:
                self.add_mesocycle_button.gradient =self.colors.Gradients.BUTTON_HOVER if e.data == True else self.colors.Gradients.BUTTON_PRIMARY
                self.add_mesocycle_button.update()
        except:
            return
        

    def _add_mesocycle_(self):
        self.navigate(
            screen_name=            "choosable_mesocycle_menu",
            is_temporary_screen=    True,
            page=                   self.page, 
            navigate_callback=      self.navigate, 
            app_state=              self.app_state,
            selection_function=     lambda id: self.choose_mesocycle(id),
            previous_screen_name=   "macrocycle_screen"
        )