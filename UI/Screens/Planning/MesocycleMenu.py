import flet as ft
from datetime import datetime

from AppState import AppState
from UI.Components.TemplateCard import TemplateCard
from UI.Screens.BaseView import BaseView

from UI.Components.InvalidDataAlertDialog import InvalidDataAlertDialog



class MesocycleMenu(BaseView):
    def __init__(
        self, 
        page: ft.Page, 
        navigate_callback, 
        app_state: AppState, 
        selection_function = None,
        previous_screen_name: str | None = None
    ):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)

        self.app_state.resize_subscribe(self.__on_resize__)
        self.app_state.data_changed_subscribe(self._init_mesocycle_cards_)


        if (selection_function is not None):
            self.on_card_click = lambda id: selection_function(id)
            self.is_choosable_menu = True
        else:
            self.on_card_click  = lambda id: self.open_mesocycle_screen(id)
            self.is_choosable_menu = False


        self.labels = self.translator.mesocycle_menu_labels

        self.cards = []

        self.main_container.content = ft.Text(
            self.labels["loading"], 
            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
        )


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
            on_click=self._create_new_mesocycle_
        )
        
        self.actions_menu = ft.Column(
            expand=1,
            controls=
            [
                self.add_mesocycle_button
            ]
        )
        

        self._init_mesocycle_cards_()
        


    def __on_resize__(self, e):
        if self.mesocycles_info == []:
            self.main_container.content = ft.Column(
                controls=
                    [
                        ft.Text(
                            self.labels["no_data"], 
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
                        ),
                        self.actions_menu
                    ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            )
            return
        
        self.screen_width    = self.page.width
        # Значения из Template_card
        self.one_card_width_terms  = [300, 0, 10] # 10 - стандартный spaccing для строки


        if self.screen_width is None:
            raise AttributeError("Unable to get window width value")
        
        if None in self.one_card_width_terms:
            raise AttributeError("Unable to get template card width value")

        self.one_card_width = sum(self.one_card_width_terms)
        self.cards_in_row = int(self.screen_width // self.one_card_width)


        rows = ft.Column(
            expand=True,
            margin=ft.Margin.symmetric(vertical=25),
            controls=[],

            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        for row_index in range(0, len(self.cards), self.cards_in_row):
            start_row_index = row_index
            end_row_index   = row_index + self.cards_in_row \
                            if (row_index + self.cards_in_row) < len(self.cards) \
                            else len(self.cards) 

            row = []

            for index in range(start_row_index, end_row_index):
                row.append(self.cards[index])
            
            rows.controls.append(
                ft.Row(
                    controls=row,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

                
        if not self.is_choosable_menu:
            rows.controls.append(self.actions_menu)

        self.templates = ft.Container(
            expand=12,
            content=rows
        )

        self.main_container.content = self.templates



    def _on_hover_add_button_(self, e):
        try:
            if e:
                self.add_mesocycle_button.gradient = self.colors.Gradients.BUTTON_HOVER if e.data == True else self.colors.Gradients.BUTTON_PRIMARY
                self.add_mesocycle_button.update()
        except:
            return
        
           
    def _create_new_mesocycle_(self):
        if self.settings.current_user == 0:
            self.page.show_dialog(
                InvalidDataAlertDialog(self.app_state, self.labels["no_user"])
            )
            return
            
        self.database.create_mesocycle(self.settings.current_user)
        id_new_mesocycle = self.database.get_mesocycles(self.settings.current_user)[-1][0]

        self.app_state.data_changed_notify()
        self.navigate(
            screen_name=            "mesocycle_screen",
            is_universal_screen=    True,
            previous_screen_name=   "mesocycle_menu",
            id_mesocycle=           id_new_mesocycle,
        )



    def open_mesocycle_screen(self, id: int):
        self.navigate(
            screen_name=            "mesocycle_screen",
            is_universal_screen=    True,
            previous_screen_name=   "mesocycle_menu",
            id_mesocycle=           id,
        )


    def delete_mesocycle(self, id: int):
        self.database.delete_mesocycle(id)
        self.app_state.data_changed_notify()
        self.page.update()



    def _init_mesocycle_cards_(self):
        self.cards = []

        self.mesocycles_info = self.database.get_mesocycles(self.settings.current_user)
        
        if self.mesocycles_info == []:
            self.main_container.content = ft.Column(
                controls=
                    [
                        ft.Text(
                            self.labels["no_data"], 
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND,
                            text_align=ft.TextAlign.CENTER
                        ),
                        self.actions_menu
                    ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            return
        

        for mesocycle in self.mesocycles_info:
            id_mesocycle = int(mesocycle[0])

            ranges = self.database.get_mesocycle_range(id_mesocycle)
            start_mesocycle_range   = ""
            end_mesocycle_range     = ""
            
            if ranges != []:
                ranges = ranges[0]
                start_mesocycle_range = str(datetime.fromtimestamp(ranges[0]).date())   if ranges[0] != 0 else ""
                end_mesocycle_range   = str(datetime.fromtimestamp(ranges[1]).date())   if ranges[1] != 0 else ""

            mesocycle_statuses = self.database.get_mesocycle_workout_statuses(self.settings.current_user, id_mesocycle)

            self.cards.append(
                self._create_mesocycle_card_(
                    id_mesocycle, 
                    start_mesocycle_range,
                    end_mesocycle_range,
                    mesocycle_statuses
                )
            )

        self.__on_resize__(None)

    

    def _create_mesocycle_card_(self, id_mesocycle: int, start_range: str | None, end_range: str | None, statuses: list):
        mesocycle_card_info = []


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
            on_card_click=  lambda id: self.on_card_click(id),
            delete_function=lambda id: self.delete_mesocycle(id)
        )