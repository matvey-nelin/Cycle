import flet as ft

from AppState import AppState
from UI.Screens.BaseView import BaseView
from UI.Components.TemplateCard import TemplateCard


class MicrocycleTemplateMenu(BaseView):
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
        self.app_state.data_changed_subscribe(self._init_microcycle_templates_cards_)


        if (selection_function is not None):
            self.on_card_click = lambda id: selection_function(id)
            self.is_choosable_menu = True
        else:
            self.on_card_click  = lambda id: self.open_template_screen(id)
            self.is_choosable_menu = False


        self.labels = self.translator.microcycle_template_menu_labels
        
        self.cards = []

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

            on_hover=self._on_hover_add_button_,
            on_click=self._create_new_template_
        )
        
        self.actions_menu = ft.Column(
            expand=1,
            controls=
            [
                self.add_template_button
            ]
        )
        
        self._init_microcycle_templates_cards_()
        


    def __on_resize__(self, e):
        self.screen_width    = self.page.width
        # Значения из Template_card
        self.one_card_width_terms  = [200, 0, 10] # 10 - стандартный spaccing для строки


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
            controls=main_conteiner_controls,
            margin=ft.Margin.symmetric(vertical=25),
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )


    def _on_hover_add_button_(self, e):
        try:
            if e:
                self.add_template_button.gradient = self.colors.Gradients.BUTTON_HOVER if e.data == True else self.colors.Gradients.BUTTON_PRIMARY
                self.add_template_button.update()
        except:
            return
        
           
    def _create_new_template_(self):
        self.navigate(
            screen_name=            "microcycle_template_screen",
            is_universal_screen=    True,
            id_microcycle_template= 0
        )



    def _init_microcycle_templates_cards_(self):
        request = """
        SELECT mt.id_microcycle_template, mt.slug, wt.slug

        FROM microcycle_templates AS mt
        JOIN microcycle_template_composition AS mtc ON mtc.id_microcycle_template = mt.id_microcycle_template
        JOIN workout_templates   AS wt ON wt.id_workout_template = mtc.id_workout_template

        ORDER BY mt.id_microcycle_template DESC;
        """

        
        self.cards = []

        microcycle_templates_info = self.database.__select_request__(request)
        
        if microcycle_templates_info == []:
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


        # Инициализация данных шаблонов
        temp_template_id = None
        template_labels = []

        for template_info in microcycle_templates_info:
            template_id = int(template_info[0])
            try:
                template_title = self.translator.microcycle_templates[template_info[1]]
            
            
                if template_id != temp_template_id:
                    if (temp_template_id == int(microcycle_templates_info[0][0])) or (template_labels != []):
                        template_labels.append(temp_template_labels)

                    temp_template_labels = [template_id, template_title]
                    temp_template_id = template_id

                temp_template_labels.append(self.translator.workout_templates[template_info[2]])
            except KeyError:
                    continue
        # Добавление последнего шаблона в список
        template_labels.append(temp_template_labels)
        

        # Создание карточек шаблонов
        for microcycle_template_info in template_labels:
            template_id = microcycle_template_info[0]
            labels      = [
                microcycle_template_info[1],
                *[f"{index+1}: {additional_label}" for index, additional_label in enumerate(microcycle_template_info[2:])]
            ]
            
            self.cards.append(
                TemplateCard(
                    screen=self,
                    id=template_id,
                    data=labels,
                    width=200, 
                    height=225,
                    on_card_click=self.on_card_click,
                    delete_function=lambda id: self.delete_template(id)
                )
            )
        
        self.__on_resize__(None)


    
    def open_template_screen(self, id: int):
        self.navigate(
            screen_name=            "microcycle_template_screen",
            is_universal_screen=    True,
            id_microcycle_template= id
        )


    
    def delete_template(self, id: int):
        slug = self.database.get_microcycle_template_info(id)[0][1]
        self.translator.delete_slug(slug, "microcycle_templates")

        self.database.delete_microcycle_template(id, True)
        self.app_state.data_changed_notify()
    