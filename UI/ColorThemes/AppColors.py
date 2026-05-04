import flet as ft

from UI.ColorThemes.SupportedColorThemes import COLOR_THEMES


class AppColors:
	def __init__(self, theme_mode: str | ft.ThemeMode, color_theme: str) -> None:
		self.color_themes = COLOR_THEMES

		if color_theme not in list(self.color_themes.keys()):
			raise ValueError("Insupported color theme")

		self.color_theme = self.color_themes[color_theme]()
		self.init_all_colors(theme_mode)

		


	def init_all_colors(self, e):
		if isinstance(e, ft.ThemeMode) or isinstance(e, ft.Brightness):
			self.theme = e.value
		elif isinstance(e, ft.Event):
			self.theme = e.data
		elif isinstance(e, str):
			self.theme = e
		else: 
			raise ValueError(f"Invalid value of parameter 'theme_mode': {e}")
		
		# Назначение цветов приложения из выбранной темы

		# === Тёмная тема ===
		self.DARK_PRIMARY 				= self.color_theme.DARK_PRIMARY
		self.DARK_PRIMARY_CONTAINER 	= self.color_theme.DARK_PRIMARY_CONTAINER
		self.DARK_ON_PRIMARY 			= self.color_theme.DARK_ON_PRIMARY
		self.DARK_ON_PRIMARY_CONTAINER 	= self.color_theme.DARK_ON_PRIMARY_CONTAINER

		self.DARK_SECONDARY 				= self.color_theme.DARK_SECONDARY
		self.DARK_SECONDARY_CONTAINER 		= self.color_theme.DARK_SECONDARY_CONTAINER
		self.DARK_ON_SECONDARY 				= self.color_theme.DARK_ON_SECONDARY
		self.DARK_ON_SECONDARY_CONTAINER	= self.color_theme.DARK_ON_SECONDARY_CONTAINER

		self.DARK_TERTIARY 				= self.color_theme.DARK_TERTIARY
		self.DARK_TERTIARY_CONTAINER 	= self.color_theme.DARK_TERTIARY_CONTAINER
		self.DARK_ON_TERTIARY 			= self.color_theme.DARK_ON_TERTIARY
		self.DARK_ON_TERTIARY_CONTAINER = self.color_theme.DARK_ON_TERTIARY_CONTAINER

		self.DARK_SURFACE 		= self.color_theme.DARK_SURFACE
		self.DARK_ON_SURFACE 	= self.color_theme.DARK_ON_SURFACE
		self.DARK_SURFACE_TINT 	= self.color_theme.DARK_SURFACE_TINT
		self.DARK_BACKGROUND 	= self.color_theme.DARK_BACKGROUND
		self.DARK_ON_BACKGROUND = self.color_theme.DARK_ON_BACKGROUND

		self.DARK_ERROR 				= self.color_theme.DARK_ERROR
		self.DARK_ERROR_CONTAINER 		= self.color_theme.DARK_ERROR_CONTAINER
		self.DARK_ON_ERROR 				= self.color_theme.DARK_ON_ERROR
		self.DARK_ON_ERROR_CONTAINER 	= self.color_theme.DARK_ON_ERROR_CONTAINER

		self.DARK_WARNING 		= self.color_theme.DARK_WARNING
		self.DARK_ON_WARNING 	= self.color_theme.DARK_ON_WARNING

		self.DARK_OUTLINE 			= self.color_theme.DARK_OUTLINE
		self.DARK_OUTLINE_VARIANT 	= self.color_theme.DARK_OUTLINE_VARIANT

		# === Светлая тема ===
		self.LIGHT_PRIMARY 				= self.color_theme.LIGHT_PRIMARY
		self.LIGHT_PRIMARY_CONTAINER 	= self.color_theme.LIGHT_PRIMARY_CONTAINER
		self.LIGHT_ON_PRIMARY 			= self.color_theme.LIGHT_ON_PRIMARY
		self.LIGHT_ON_PRIMARY_CONTAINER = self.color_theme.LIGHT_ON_PRIMARY_CONTAINER

		self.LIGHT_SECONDARY 				= self.color_theme.LIGHT_SECONDARY
		self.LIGHT_SECONDARY_CONTAINER 		= self.color_theme.LIGHT_SECONDARY_CONTAINER
		self.LIGHT_ON_SECONDARY 			= self.color_theme.LIGHT_ON_SECONDARY
		self.LIGHT_ON_SECONDARY_CONTAINER 	= self.color_theme.LIGHT_ON_SECONDARY_CONTAINER

		self.LIGHT_TERTIARY 				= self.color_theme.LIGHT_TERTIARY
		self.LIGHT_TERTIARY_CONTAINER 		= self.color_theme.LIGHT_TERTIARY_CONTAINER
		self.LIGHT_ON_TERTIARY 				= self.color_theme.LIGHT_ON_TERTIARY
		self.LIGHT_ON_TERTIARY_CONTAINER 	= self.color_theme.LIGHT_ON_TERTIARY_CONTAINER

		self.LIGHT_SURFACE 			= self.color_theme.LIGHT_SURFACE
		self.LIGHT_ON_SURFACE 		= self.color_theme.LIGHT_ON_SURFACE
		self.LIGHT_SURFACE_TINT 	= self.color_theme.LIGHT_SURFACE_TINT
		self.LIGHT_BACKGROUND 		= self.color_theme.LIGHT_BACKGROUND
		self.LIGHT_ON_BACKGROUND 	= self.color_theme.LIGHT_ON_BACKGROUND

		self.LIGHT_ERROR 				= self.color_theme.LIGHT_ERROR
		self.LIGHT_ERROR_CONTAINER 		= self.color_theme.LIGHT_ERROR_CONTAINER
		self.LIGHT_ON_ERROR 			= self.color_theme.LIGHT_ON_ERROR
		self.LIGHT_ON_ERROR_CONTAINER 	= self.color_theme.LIGHT_ON_ERROR_CONTAINER

		self.LIGHT_WARNING 		= self.color_theme.LIGHT_WARNING
		self.LIGHT_ON_WARNING 	= self.color_theme.LIGHT_ON_WARNING

		self.LIGHT_OUTLINE 			= self.color_theme.LIGHT_OUTLINE
		self.LIGHT_OUTLINE_VARIANT 	= self.color_theme.LIGHT_OUTLINE_VARIANT


		self.dark_color_scheme 	= self.color_theme.dark_color_scheme
		self.light_color_scheme = self.color_theme.light_color_scheme 

		self.set_gradients()

	

	


	def set_gradients(self):
		dark_gradients 	= DarkGradients(self)
		light_gradients = LightGradients(self)

		if self.theme == 'dark':
			self.Gradients = dark_gradients
		elif self.theme == 'light':
			self.Gradients = light_gradients



class DarkGradients:
	def __init__(self, colors: AppColors) -> None:
		"""Градиенты для темной темы"""

		# === ГЛАВНЫЕ ДЕЙСТВИЯ (Primary → Secondary) ===
		self.BUTTON_PRIMARY = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_PRIMARY, colors.DARK_SECONDARY],
		)
		
		self.BUTTON_HOVER = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_PRIMARY_CONTAINER, colors.DARK_SECONDARY_CONTAINER],
		)
		
		# === ПОЗИТИВНЫЕ ДЕЙСТВИЯ (Primary → Tertiary) ===
		self.BUTTON_SUCCESS = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_PRIMARY, colors.DARK_TERTIARY],
		)
		
		self.BUTTON_SUCCESS_HOVER = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_PRIMARY_CONTAINER, colors.DARK_TERTIARY_CONTAINER],
		)
		
		# === НЕГАТИВНЫЕ ДЕЙСТВИЯ (Error) ===
		self.BUTTON_DANGER = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_ERROR, colors.DARK_ERROR_CONTAINER],
		)
		
		self.BUTTON_DANGER_HOVER = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_ERROR_CONTAINER, colors.DARK_ERROR],
		)
		
		# === КАРТОЧКИ (Surface → Background) ===
		self.CARD_DEFAULT = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_SURFACE, colors.DARK_BACKGROUND],
		)
		
		self.CARD_HOVER = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_SURFACE, colors.DARK_OUTLINE],
		)
		
		self.CARD_HIGHLIGHT = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_SURFACE, colors.DARK_PRIMARY_CONTAINER],
		)
		
		self.CARD_ACTIVE = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_PRIMARY_CONTAINER, colors.DARK_SECONDARY_CONTAINER],
		)
		
		# === ПРОГРЕСС (горизонтальный) ===
		self.PROGRESS = ft.LinearGradient(
			begin=ft.Alignment.CENTER_LEFT,
			end=ft.Alignment.CENTER_RIGHT,
			colors=[colors.DARK_PRIMARY, colors.DARK_TERTIARY],
		)
		
		self.PROGRESS_BACKGROUND = ft.LinearGradient(
			begin=ft.Alignment.CENTER_LEFT,
			end=ft.Alignment.CENTER_RIGHT,
			colors=[colors.DARK_SURFACE, colors.DARK_OUTLINE],
		)
		
		# === ХЕДЕРЫ ===
		self.HEADER = ft.LinearGradient(
			begin=ft.Alignment.CENTER_LEFT,
			end=ft.Alignment.CENTER_RIGHT,
			colors=[colors.DARK_PRIMARY, colors.DARK_SECONDARY, colors.DARK_TERTIARY],
		)
		
		# === ДОСТИЖЕНИЯ ===
		self.ACHIEVEMENT = ft.RadialGradient(
			center=ft.Alignment.CENTER,
			radius=0.7,
			colors=[colors.DARK_SECONDARY, colors.DARK_BACKGROUND],
		)
		
		# === СТАТУСЫ ===
		self.STATUS_SUCCESS = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_TERTIARY, colors.DARK_TERTIARY_CONTAINER],
		)
		
		self.STATUS_ERROR = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_ERROR, colors.DARK_ERROR_CONTAINER],
		)


class LightGradients:
	def __init__(self, colors: AppColors) -> None:
		"""Градиенты для светлой темы"""
	
		# === ГЛАВНЫЕ ДЕЙСТВИЯ (Primary → Secondary) ===
		self.BUTTON_PRIMARY = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_PRIMARY, colors.LIGHT_SECONDARY],
		)
		
		self.BUTTON_HOVER = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_PRIMARY_CONTAINER, colors.LIGHT_SECONDARY_CONTAINER],
		)
		
		# === ПОЗИТИВНЫЕ ДЕЙСТВИЯ (Primary → Tertiary) ===
		self.BUTTON_SUCCESS = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_PRIMARY, colors.LIGHT_TERTIARY],
		)
		
		self.BUTTON_SUCCESS_HOVER = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_PRIMARY_CONTAINER, colors.LIGHT_TERTIARY_CONTAINER],
		)
		
		# === НЕГАТИВНЫЕ ДЕЙСТВИЯ (Error) ===
		self.BUTTON_DANGER = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_ERROR, colors.LIGHT_ERROR_CONTAINER],
		)
		
		self.BUTTON_DANGER_HOVER = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_ERROR_CONTAINER, colors.LIGHT_ERROR],
		)
		
		# === КАРТОЧКИ (Surface → Background) ===
		self.CARD_DEFAULT = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_SURFACE, colors.LIGHT_BACKGROUND],
		)
		
		self.CARD_HOVER = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_OUTLINE_VARIANT, colors.LIGHT_OUTLINE],
		)
		
		self.CARD_HIGHLIGHT = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_SURFACE, colors.LIGHT_PRIMARY_CONTAINER],
		)
		
		self.CARD_ACTIVE = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_PRIMARY_CONTAINER, colors.LIGHT_SECONDARY_CONTAINER],
		)
		
		# === ПРОГРЕСС (горизонтальный) ===
		self.PROGRESS = ft.LinearGradient(
			begin=ft.Alignment.CENTER_LEFT,
			end=ft.Alignment.CENTER_RIGHT,
			colors=[colors.LIGHT_PRIMARY, colors.LIGHT_TERTIARY],
		)
		
		self.PROGRESS_BACKGROUND = ft.LinearGradient(
			begin=ft.Alignment.CENTER_LEFT,
			end=ft.Alignment.CENTER_RIGHT,
			colors=[colors.LIGHT_BACKGROUND, colors.LIGHT_OUTLINE],
		)
		
		# === ХЕДЕРЫ ===
		self.HEADER = ft.LinearGradient(
			begin=ft.Alignment.CENTER_LEFT,
			end=ft.Alignment.CENTER_RIGHT,
			colors=[colors.LIGHT_PRIMARY, colors.LIGHT_SECONDARY, colors.LIGHT_TERTIARY],
		)
		
		# === ДОСТИЖЕНИЯ ===
		self.ACHIEVEMENT = ft.RadialGradient(
			center=ft.Alignment.CENTER,
			radius=0.7,
			colors=[colors.LIGHT_SECONDARY, colors.LIGHT_BACKGROUND],
		)
		
		# === СТАТУСЫ ===
		self.STATUS_SUCCESS = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_TERTIARY, colors.LIGHT_TERTIARY_CONTAINER],
		)
		
		self.STATUS_ERROR = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_ERROR, colors.LIGHT_ERROR_CONTAINER],
		)