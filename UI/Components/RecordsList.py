import flet as ft

from AppState import AppState
from UI.Components.InvalidDataAlertDialog import InvalidDataAlertDialog
from UI.Components.ManagerDialog import ManagerDialog
from Classes.TrainingMetrics import TrainingMetrics


class RecordsList(ft.ListView):
	def __init__(self, page: ft.Page, app_state: AppState, table_name: str, navigate_callback) -> None:
		super().__init__()

		self.training_metrics = TrainingMetrics()

		self._page = page
		self.table_name = table_name
		self.navigate 	= navigate_callback


		self.app_state 	= app_state
        
		self.database 	= self.app_state.database
		self.settings	= self.app_state.settings
		self.translator = self.app_state.translator
		self.colors     = self.app_state.colors

		self.labels = self.translator.records_list_labels

		self.unchangeable_record_icon = ft.Icon(
			icon=ft.Icons.LOCK_OUTLINE_ROUNDED,
			size=20,
			color=self.colors.LIGHT_TERTIARY_CONTAINER if self.colors.theme == 'light' else self.colors.DARK_TERTIARY_CONTAINER
		)


		self.entities = {
			"users"             : {
				"icon"		: ft.Icon(
					icon=ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
					size=20,
					color=self.colors.LIGHT_SECONDARY_CONTAINER if self.colors.theme == 'light' else self.colors.DARK_SECONDARY_CONTAINER,
				),
				"screen"	: "user_management_screen",
				"unchangeable_records" : [],
				"data" 		: self.database.get_users,
				"subtitle"	: lambda id: self.user_subtitle(id),
				"add_info" 	: None,
				"delete"	: lambda id: self.database.delete_user(id),
				"arguments" : {
					"page": 				self._page, 
					"app_state":			self.app_state,
        			"navigate_callback": 	self.navigate,
        			"previous_screen_name": "users_screen",
				},
				"entity"	: "users"
			},
			"user_statuses"     : {
				"icon"		: ft.Icon(
					icon=ft.Icons.VERIFIED_USER_ROUNDED, # Можно в будущем пересмотреть иконку
					size=20,
					color=self.colors.LIGHT_SECONDARY_CONTAINER if self.colors.theme == 'light' else self.colors.DARK_SECONDARY_CONTAINER,
				),
				"screen"	: "universal_record_management_screen",
				"unchangeable_records" : self.settings.unchangeable_user_statuses,
				"data" 		: self.database.get_user_statuses,
				"subtitle"	: None,
				"add_info" 	: None,
				"delete"	: lambda id: self.database.delete_user_status(id),
				"arguments" : {
					"page": 				self._page, 
					"app_state":			self.app_state,
        			"navigate_callback": 	self.navigate,
        			"previous_screen_name": "user_statuses_screen",
        			"entity": 				"user_statuses",
					"field_max_length": 	50
				},
				"entity"	: "user_statuses"
			},

			"workout_statuses"    : {
				"icon"		: ft.Icon(
					icon=ft.Icons.ASSIGNMENT_ROUNDED,
					size=20,
					color=self.colors.LIGHT_SECONDARY_CONTAINER if self.colors.theme == 'light' else self.colors.DARK_SECONDARY_CONTAINER,
				),
				"screen"	: "universal_record_management_screen",
				"unchangeable_records" : self.settings.unchangeable_workout_statuses,
				"data" 		: self.database.get_workout_statuses,
				"subtitle"	: None,
				"add_info" 	: None,
				"delete"	: lambda id: self.database.delete_workout_status(id),
				"arguments" : {
					"page": 				self._page, 
					"app_state":			self.app_state,
        			"navigate_callback": 	self.navigate,
        			"previous_screen_name": "workout_statuses_screen",
        			"entity": 				"workout_statuses",
					"field_max_length": 	50
				},
				"entity"	: "workout_statuses"
			},
			"workout_types"      : {
				"icon"		: ft.Icon(
					icon=ft.Icons.VIEW_LIST_ROUNDED,
					size=20,
					color=self.colors.LIGHT_SECONDARY_CONTAINER if self.colors.theme == 'light' else self.colors.DARK_SECONDARY_CONTAINER,
				),
				"screen"	: "universal_record_management_screen",
				"unchangeable_records" : self.settings.unchangeable_workout_types,
				"data" 		: self.database.get_workout_types,
				"subtitle"	: None,
				"add_info" 	: None,
				"delete"	: lambda id: self.database.delete_workout_type(id),
				"arguments" : {
					"page": 				self._page, 
					"app_state":			self.app_state,
        			"navigate_callback": 	self.navigate,
        			"previous_screen_name": "workout_types_screen",
        			"entity": 				"workout_types",
					"field_max_length":	 	50
				},
				"entity"	: "workout_types"
			},
			"hypertrophy_types"  : {
				"icon"		: ft.Icon(
					icon=ft.Icons.BIOTECH_ROUNDED,
					size=20,
					color=self.colors.LIGHT_SECONDARY_CONTAINER if self.colors.theme == 'light' else self.colors.DARK_SECONDARY_CONTAINER,
				),
				"screen"	: "universal_record_management_screen",
				"unchangeable_records" : self.settings.unchangeable_hypertrophy_types,
				"data" 		: self.database.get_hypertrophy_types,
				"subtitle"	: None,
				"add_info" 	: None,
				"delete"	: lambda id: self.database.delete_hypertrophy_type(id),
				"arguments" : {
					"page": 				self._page, 
					"app_state":			self.app_state,
        			"navigate_callback": 	self.navigate,
        			"previous_screen_name": "hypertrophy_types_screen",
        			"entity": 				"hypertrophy_types",
					"field_max_length": 	50
				},
				"entity"	: "hypertrophy_types"
			},

			"exercises"         : {
				"icon"		: ft.Icon(
					icon=ft.Icons.FITNESS_CENTER,
					size=20,
					color=self.colors.LIGHT_SECONDARY_CONTAINER if self.colors.theme == 'light' else self.colors.DARK_SECONDARY_CONTAINER,
				),
				"screen"	: "exercise_management_screen",
				"unchangeable_records" : self.settings.unchangeable_exercises,
				"data" 		: self.database.get_exercises,
				"subtitle"	: lambda id: self.exercise_subtitle(id),
				"add_info" 	: None,
				"delete"	: lambda id: self.database.delete_exercise(id),
				"arguments" : {
					"page": 				self._page, 
					"app_state":			self.app_state,
        			"navigate_callback": 	self.navigate,
        			"previous_screen_name": "exercises_screen",
				},
				"entity"	: "exercises"
			},
			"agonists"          : {
				"icon"		: ft.Icon(
					icon=ft.Icons.MONITOR_HEART,
					size=20,
					color=self.colors.LIGHT_SECONDARY_CONTAINER if self.colors.theme == 'light' else self.colors.DARK_SECONDARY_CONTAINER,
				),
				"screen"	: "agonist_management_screen",
				"unchangeable_records" : self.settings.unchangeable_agonists,
				"data" 		: self.database.get_agonists,
				"subtitle"	: None,
				"add_info" 	: lambda id: self.agonist_additional_info(id),
				"delete"	: lambda id: self.database.delete_agonist(id),
				"arguments" : {
					"page": 				self._page, 
					"app_state":			self.app_state,
        			"navigate_callback": 	self.navigate,
        			"previous_screen_name": "agonists_screen",
				},
				"entity"	: "agonists"
			},
		}

		if self.table_name not in list(self.entities.keys()):
			raise ValueError("Incorrect value of 'table_name'")
		

		self.margin	 = 0
		self.spacing = 5

		self._init_data_()


	def _init_data_(self):
		self.controls = []
		self.data = self.entities[self.table_name]["data"]()


		if self.data != []:
			if (self.table_name != "users"):
				data_labels = self.translator.data_labels[self.table_name]

			for record in self.data:
				id_list_tile = record[0]
				try:
					title_list_tile = record[2] if (self.table_name == "users") else data_labels[record[1]]
				except KeyError:
					continue
				
				is_unchangeable = bool(id_list_tile in self.entities[self.table_name]["unchangeable_records"])
				subtitle_list_tile 	= self.entities[self.table_name]["subtitle"](id_list_tile) if self.entities[self.table_name]["subtitle"] is not None else None
				add_info_list_tile 	= self.entities[self.table_name]["add_info"](id_list_tile) if self.entities[self.table_name]["add_info"] is not None else None
				icon_list_tile 		= self.entities[self.table_name]["icon"]

				self.controls.append(
					ft.Container(
						expand=False,
						content=ft.ListTile(
							expand=False,

							title=title_list_tile,
							title_text_style=ft.TextStyle(
								size=16,
								weight=ft.FontWeight.W_400
							),
							title_alignment=ft.ListTileTitleAlignment.CENTER,

							subtitle=subtitle_list_tile,
							subtitle_text_style=ft.TextStyle(
								size=12,
								weight=ft.FontWeight.W_400
							),

							trailing=add_info_list_tile,

							text_color=ft.Colors.ON_SURFACE,
							
							data={
								"id"		: id_list_tile,
								"slug"		: None if (self.table_name == "users") else record[1],
								"add_info"	: add_info_list_tile
			 				},
							 
							leading=self.unchangeable_record_icon if is_unchangeable else icon_list_tile,

							on_click=(
								self.show_is_unchangeable_record_dialog 
								if is_unchangeable and (self.table_name not in ["exercises", "agonists"]) 
								else self.open_info_manage_screen
							),
							on_long_press=(
								None 
								if is_unchangeable and (self.table_name not in ["exercises", "agonists", "workout_types"])
								else self.show_manager_dialog
							)
						),

						border=ft.Border.all(
							width=1,
							color=ft.Colors.OUTLINE
						),
						border_radius=5,

						alignment=ft.Alignment.CENTER
					)
				)
		else:
			self.return_no_data_label()

		try:
			self.update()
		except:
			pass



	def open_info_manage_screen(self, e):
		id = e.control.data["id"]

		kwargs = self.entities[self.table_name]["arguments"]

		self.navigate(
			screen_name=			self.entities[self.table_name]["screen"],
			is_temporary_screen=	True,
			**kwargs,
			id=						id
		)


	def return_no_data_label(self):
		return ft.Text(
			value=self.labels["no_data"],
			size=18, 
			text_align=ft.TextAlign.CENTER,
			color=ft.Colors.ON_SURFACE
		)
	



	# Методы получения значения дополнительной информации записи
	def agonist_additional_info(self, id_agonist: int):
		involvement_level_colors_table = {
			'low': 		ft.Colors.RED_800,
			'medium': 	ft.Colors.YELLOW_800,
			'good': 	ft.Colors.GREEN_800,
			'great': 	ft.Colors.LIGHT_BLUE_800
		}

		add_info = self.training_metrics.determine_agonist_involvement_level(id_agonist=id_agonist)

		if add_info is not None:
			level 	= add_info[0]
			sets 	= add_info[1]

			add_info = ft.Text(
				value=f"{sets}",
				size=18,
				weight=ft.FontWeight.W_500,
				color=involvement_level_colors_table[level]
			)

		return add_info





	# Методы получения подзаголовка записи
	def user_subtitle(self, id_user: int):
		id_user_status = self.database.get_users(id_user)[0][1]
		return f"{self.translator.user_statuses[self.database.get_user_statuses(id_user_status)[0][1]]}" 
	

	def exercise_subtitle(self, id_exercise: int):
		agonists = self.database.get_agonists(id_exercise)
		if agonists == []:
			return None
		
		subtitle = []
		for agonist in agonists:
			subtitle.append(self.translator.agonists[agonist[1]])

		return ", ".join(subtitle)
	




	# Методы управления записями
	def show_manager_dialog(self, e):
		id_list_tile 	= e.control.data["id"]
		slug_list_tile 	= e.control.data["slug"]
		title_list_tile = ft.Text(
			value=e.control.title,
			text_align=ft.TextAlign.CENTER
		)

		def delete_record_and_slug():
			self.delete_record(id_list_tile)
			if slug_list_tile is not None:
				self.translator.delete_slug(
					slug=		slug_list_tile, 
					essence=	self.table_name
				)

		manager_dialog = ManagerDialog(
			app_state=			self.app_state, 
			id=					id_list_tile, 
			title=				title_list_tile, 
			essence=			self.entities[self.table_name]["entity"],
			delete_function=	delete_record_and_slug
		)

		self._page.show_dialog(manager_dialog)


	def show_is_unchangeable_record_dialog(self):
		self._page.show_dialog(
			InvalidDataAlertDialog(self.app_state, self.labels["imposible_change_the_record"])
		)
	


	def delete_record(self, id_list_tile: int):
		if self.table_name == "users":
			if len(self.data) == 1:
				self._page.show_dialog(
					InvalidDataAlertDialog(self.app_state, self.labels["imposible_delete_last_user"])
				)
				return

		self.entities[self.table_name]["delete"](id_list_tile)
		

		if self.table_name == "users":
			if self.settings.current_user == id_list_tile:
				self.app_state.change_user(self.database.get_users()[0][0])


		self.app_state.data_changed_notify()