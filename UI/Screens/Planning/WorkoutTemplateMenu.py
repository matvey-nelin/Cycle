import flet as ft

from AppState import AppState
from UI.Screens.BaseView import BaseView

from UI.Components.TemplateCard import TemplateCard


class WorkoutTemplateMenu(BaseView):
    def __init__(
        self, 
        page: ft.Page, 
        navigate_callback, 
        app_state: AppState, 
        selection_function = None,
        previous_screen_name: str | None = None,
    ):
        super().__init__(page, navigate_callback, app_state, previous_screen_name)
        
        self.app_state.resize_subscribe(self.__on_resize__)
        self.app_state.data_changed_subscribe(self._init_workout_templates_cards_)
    
        if (selection_function is not None):
            self.on_card_click = lambda id: selection_function(id)
            self.is_choosable_menu = True
        else:
            self.on_card_click  = lambda id: self.open_template_screen(id)
            self.is_choosable_menu = False
        

        self.labels = self.translator.workout_template_menu_labels

        self.main_container.content = ft.Text(
            self.labels["loading"], 
            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND
        )


        self.add_template_button = ft.Container(
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

            on_hover=self.__on_hover_add_button,
            on_click=self.__create_new_template__
        )
        
        self.actions_menu = ft.Column(
            expand=1,
            controls=
            [
                self.add_template_button
            ]
        )
        
        self._init_workout_templates_cards_()
        


    def __on_resize__(self, e):
        self.screen_width    = self.page.width
        # Значения из Template_card
        self.one_card_width_terms  = [150, 0, 10] # 10 - стандартный spaccing для строки


        if self.screen_width is None:
            raise AttributeError("Unable to get window width value")
        
        if None in self.one_card_width_terms:
            raise AttributeError("Unable to get template card width value")

        self.one_card_width = sum(self.one_card_width_terms)

        self.cards_in_row = int(self.screen_width // self.one_card_width)

        rows = ft.Column(
            expand=True,
            controls=[]
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
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
            )

        self.templates = ft.Container(
            expand=12,
            content=rows
        )

        main_conteiner_controls : list[ft.Control] = [self.templates]
        if self.is_choosable_menu == False:
            main_conteiner_controls.append(self.actions_menu)

        self.main_container.content = ft.Column(
            expand=True,
            margin=ft.Margin.symmetric(vertical=25),

            controls=main_conteiner_controls,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )


    def __on_hover_add_button(self, e):
        try:
            if e:
                self.add_template_button.gradient = self.colors.Gradients.BUTTON_HOVER if e.data == True else self.colors.Gradients.BUTTON_PRIMARY
                self.add_template_button.update()
        except:
            return
        
           
    def __create_new_template__(self):
        self.navigate(
            screen_name=            "workout_template_screen",
            is_temporary_screen=    True,
            id_workout_template=    0, # Id для указания нового шаблона
            page=                   self.page, 
            navigate_callback=      self.navigate, 
            app_state=              self.app_state
        )



    def _init_workout_templates_cards_(self):
        request = """
        SELECT wt.id_workout_template, wt.title, wtype.slug, htype.slug

        FROM workout_templates  AS wt
        JOIN workout_type       AS wtype ON wtype.id_workout_type = wt.id_workout_type
        JOIN hypertrophy_type   AS htype ON htype.id_hypertrophy_type = wt.id_hypertrophy_type

        ORDER BY wt.id_workout_template DESC;
        """

        workout_templates_info = self.app_state.database.__select_request__(request)

        if isinstance(workout_templates_info, Exception):
            raise workout_templates_info
        
        if workout_templates_info == []:
            self.main_container.content = ft.Column(
                controls=
                    [
                        ft.Text(
                            self.labels["no_data"], 
                            color=self.colors.LIGHT_ON_BACKGROUND if self.colors.theme == "light" else self.colors.DARK_ON_BACKGROUND,
                            align=ft.Alignment.CENTER
                        ),
                        self.actions_menu
                    ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            )
            return
        

        self.cards = []
        for template_info in workout_templates_info:
            template_id     = int(template_info[0])
            template_labels = [
                template_info[1],
                self.app_state.translator.workout_types[template_info[2]],
                self.app_state.translator.hypertrophy_types[template_info[3]]
            ]

            

            self.cards.append(
                TemplateCard(
                    screen=self,
                    id=template_id,
                    data=template_labels,
                    width=150, 
                    height=200,
                    on_card_click=self.on_card_click,
                    delete_function=lambda id: self.delete_template(id)
                )
            )
        
        self.__on_resize__(None)


    def open_template_screen(self, id: int):
        self.navigate(
            screen_name=            "workout_template_screen",
            is_temporary_screen=    True,
            id_workout_template=    id, 
            page=                   self.page, 
            navigate_callback=      self.navigate, 
            app_state=              self.app_state
        )


    def delete_template(self, id: int):
        slug = self.database.get_workout_template_info(id)[0][0]
        self.translator.delete_slug(slug, "workout_templates")

        self.database.delete_workout_template(id, True)
        self.app_state.data_changed_notify()