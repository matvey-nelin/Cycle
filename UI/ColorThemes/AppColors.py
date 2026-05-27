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

		# === Тёмная тема (Arabian Night) ===
		
		# --- Основные акценты (Primary) ---
		self.DARK_PRIMARY                     = self.color_theme.DARK_PRIMARY
		self.DARK_ON_PRIMARY                  = self.color_theme.DARK_ON_PRIMARY
		self.DARK_PRIMARY_CONTAINER           = self.color_theme.DARK_PRIMARY_CONTAINER
		self.DARK_ON_PRIMARY_CONTAINER        = self.color_theme.DARK_ON_PRIMARY_CONTAINER
		self.DARK_PRIMARY_FIXED               = self.color_theme.DARK_PRIMARY_FIXED
		self.DARK_PRIMARY_FIXED_DIM           = self.color_theme.DARK_PRIMARY_FIXED_DIM
		self.DARK_ON_PRIMARY_FIXED            = self.color_theme.DARK_ON_PRIMARY_FIXED
		self.DARK_ON_PRIMARY_FIXED_VARIANT    = self.color_theme.DARK_ON_PRIMARY_FIXED_VARIANT

		# --- Вторичные акценты (Secondary) ---
		self.DARK_SECONDARY                   = self.color_theme.DARK_SECONDARY
		self.DARK_ON_SECONDARY                = self.color_theme.DARK_ON_SECONDARY
		self.DARK_SECONDARY_CONTAINER         = self.color_theme.DARK_SECONDARY_CONTAINER
		self.DARK_ON_SECONDARY_CONTAINER      = self.color_theme.DARK_ON_SECONDARY_CONTAINER
		self.DARK_SECONDARY_FIXED             = self.color_theme.DARK_SECONDARY_FIXED
		self.DARK_SECONDARY_FIXED_DIM         = self.color_theme.DARK_SECONDARY_FIXED_DIM
		self.DARK_ON_SECONDARY_FIXED          = self.color_theme.DARK_ON_SECONDARY_FIXED
		self.DARK_ON_SECONDARY_FIXED_VARIANT  = self.color_theme.DARK_ON_SECONDARY_FIXED_VARIANT

		# --- Третичные акценты (Tertiary) ---
		self.DARK_TERTIARY                    = self.color_theme.DARK_TERTIARY
		self.DARK_ON_TERTIARY                 = self.color_theme.DARK_ON_TERTIARY
		self.DARK_TERTIARY_CONTAINER          = self.color_theme.DARK_TERTIARY_CONTAINER
		self.DARK_ON_TERTIARY_CONTAINER       = self.color_theme.DARK_ON_TERTIARY_CONTAINER
		self.DARK_TERTIARY_FIXED              = self.color_theme.DARK_TERTIARY_FIXED
		self.DARK_TERTIARY_FIXED_DIM          = self.color_theme.DARK_TERTIARY_FIXED_DIM
		self.DARK_ON_TERTIARY_FIXED           = self.color_theme.DARK_ON_TERTIARY_FIXED
		self.DARK_ON_TERTIARY_FIXED_VARIANT   = self.color_theme.DARK_ON_TERTIARY_FIXED_VARIANT

		# --- Ошибки (Error) ---
		self.DARK_ERROR                       = self.color_theme.DARK_ERROR
		self.DARK_ON_ERROR                    = self.color_theme.DARK_ON_ERROR
		self.DARK_ERROR_CONTAINER             = self.color_theme.DARK_ERROR_CONTAINER
		self.DARK_ON_ERROR_CONTAINER          = self.color_theme.DARK_ON_ERROR_CONTAINER

		# --- Поверхности (Surface) ---
		self.DARK_SURFACE                     = self.color_theme.DARK_SURFACE
		self.DARK_ON_SURFACE                  = self.color_theme.DARK_ON_SURFACE
		self.DARK_ON_SURFACE_VARIANT          = self.color_theme.DARK_ON_SURFACE_VARIANT
		self.DARK_SURFACE_TINT                = self.color_theme.DARK_SURFACE_TINT
		self.DARK_SURFACE_DIM                 = self.color_theme.DARK_SURFACE_DIM
		self.DARK_SURFACE_BRIGHT              = self.color_theme.DARK_SURFACE_BRIGHT
		self.DARK_SURFACE_CONTAINER_LOWEST    = self.color_theme.DARK_SURFACE_CONTAINER_LOWEST
		self.DARK_SURFACE_CONTAINER_LOW       = self.color_theme.DARK_SURFACE_CONTAINER_LOW
		self.DARK_SURFACE_CONTAINER           = self.color_theme.DARK_SURFACE_CONTAINER
		self.DARK_SURFACE_CONTAINER_HIGH      = self.color_theme.DARK_SURFACE_CONTAINER_HIGH
		self.DARK_SURFACE_CONTAINER_HIGHEST   = self.color_theme.DARK_SURFACE_CONTAINER_HIGHEST

		# --- Границы, Инверсия, Тени ---
		self.DARK_OUTLINE                     = self.color_theme.DARK_OUTLINE
		self.DARK_OUTLINE_VARIANT             = self.color_theme.DARK_OUTLINE_VARIANT
		self.DARK_SHADOW                      = self.color_theme.DARK_SHADOW
		self.DARK_SCRIM                       = self.color_theme.DARK_SCRIM
		self.DARK_INVERSE_SURFACE             = self.color_theme.DARK_INVERSE_SURFACE
		self.DARK_ON_INVERSE_SURFACE          = self.color_theme.DARK_ON_INVERSE_SURFACE
		self.DARK_INVERSE_PRIMARY             = self.color_theme.DARK_INVERSE_PRIMARY


		# === Светлая тема (Arabian Day) ===
		
		# --- Основные акценты (Primary) ---
		self.LIGHT_PRIMARY                    = self.color_theme.LIGHT_PRIMARY
		self.LIGHT_ON_PRIMARY                 = self.color_theme.LIGHT_ON_PRIMARY
		self.LIGHT_PRIMARY_CONTAINER          = self.color_theme.LIGHT_PRIMARY_CONTAINER
		self.LIGHT_ON_PRIMARY_CONTAINER       = self.color_theme.LIGHT_ON_PRIMARY_CONTAINER
		self.LIGHT_PRIMARY_FIXED              = self.color_theme.LIGHT_PRIMARY_FIXED
		self.LIGHT_PRIMARY_FIXED_DIM          = self.color_theme.LIGHT_PRIMARY_FIXED_DIM
		self.LIGHT_ON_PRIMARY_FIXED           = self.color_theme.LIGHT_ON_PRIMARY_FIXED
		self.LIGHT_ON_PRIMARY_FIXED_VARIANT   = self.color_theme.LIGHT_ON_PRIMARY_FIXED_VARIANT

		# --- Вторичные акценты (Secondary) ---
		self.LIGHT_SECONDARY                  = self.color_theme.LIGHT_SECONDARY
		self.LIGHT_ON_SECONDARY               = self.color_theme.LIGHT_ON_SECONDARY
		self.LIGHT_SECONDARY_CONTAINER        = self.color_theme.LIGHT_SECONDARY_CONTAINER
		self.LIGHT_ON_SECONDARY_CONTAINER     = self.color_theme.LIGHT_ON_SECONDARY_CONTAINER
		self.LIGHT_SECONDARY_FIXED            = self.color_theme.LIGHT_SECONDARY_FIXED
		self.LIGHT_SECONDARY_FIXED_DIM        = self.color_theme.LIGHT_SECONDARY_FIXED_DIM
		self.LIGHT_ON_SECONDARY_FIXED         = self.color_theme.LIGHT_ON_SECONDARY_FIXED
		self.LIGHT_ON_SECONDARY_FIXED_VARIANT = self.color_theme.LIGHT_ON_SECONDARY_FIXED_VARIANT

		# --- Третичные акценты (Tertiary) ---
		self.LIGHT_TERTIARY                   = self.color_theme.LIGHT_TERTIARY
		self.LIGHT_ON_TERTIARY                = self.color_theme.LIGHT_ON_TERTIARY
		self.LIGHT_TERTIARY_CONTAINER         = self.color_theme.LIGHT_TERTIARY_CONTAINER
		self.LIGHT_ON_TERTIARY_CONTAINER      = self.color_theme.LIGHT_ON_TERTIARY_CONTAINER
		self.LIGHT_TERTIARY_FIXED             = self.color_theme.LIGHT_TERTIARY_FIXED
		self.LIGHT_TERTIARY_FIXED_DIM         = self.color_theme.LIGHT_TERTIARY_FIXED_DIM
		self.LIGHT_ON_TERTIARY_FIXED          = self.color_theme.LIGHT_ON_TERTIARY_FIXED
		self.LIGHT_ON_TERTIARY_FIXED_VARIANT  = self.color_theme.LIGHT_ON_TERTIARY_FIXED_VARIANT

		# --- Ошибки (Error) ---
		self.LIGHT_ERROR                      = self.color_theme.LIGHT_ERROR
		self.LIGHT_ON_ERROR                   = self.color_theme.LIGHT_ON_ERROR
		self.LIGHT_ERROR_CONTAINER            = self.color_theme.LIGHT_ERROR_CONTAINER
		self.LIGHT_ON_ERROR_CONTAINER         = self.color_theme.LIGHT_ON_ERROR_CONTAINER

		# --- Поверхности (Surface) ---
		self.LIGHT_SURFACE                    = self.color_theme.LIGHT_SURFACE
		self.LIGHT_ON_SURFACE                 = self.color_theme.LIGHT_ON_SURFACE
		self.LIGHT_ON_SURFACE_VARIANT         = self.color_theme.LIGHT_ON_SURFACE_VARIANT
		self.LIGHT_SURFACE_TINT               = self.color_theme.LIGHT_SURFACE_TINT
		self.LIGHT_SURFACE_DIM                = self.color_theme.LIGHT_SURFACE_DIM
		self.LIGHT_SURFACE_BRIGHT             = self.color_theme.LIGHT_SURFACE_BRIGHT
		self.LIGHT_SURFACE_CONTAINER_LOWEST   = self.color_theme.LIGHT_SURFACE_CONTAINER_LOWEST
		self.LIGHT_SURFACE_CONTAINER_LOW      = self.color_theme.LIGHT_SURFACE_CONTAINER_LOW
		self.LIGHT_SURFACE_CONTAINER          = self.color_theme.LIGHT_SURFACE_CONTAINER
		self.LIGHT_SURFACE_CONTAINER_HIGH     = self.color_theme.LIGHT_SURFACE_CONTAINER_HIGH
		self.LIGHT_SURFACE_CONTAINER_HIGHEST  = self.color_theme.LIGHT_SURFACE_CONTAINER_HIGHEST

		# --- Границы, Инверсия, Тени ---
		self.LIGHT_OUTLINE                    = self.color_theme.LIGHT_OUTLINE
		self.LIGHT_OUTLINE_VARIANT            = self.color_theme.LIGHT_OUTLINE_VARIANT
		self.LIGHT_SHADOW                     = self.color_theme.LIGHT_SHADOW
		self.LIGHT_SCRIM                      = self.color_theme.LIGHT_SCRIM
		self.LIGHT_INVERSE_SURFACE            = self.color_theme.LIGHT_INVERSE_SURFACE
		self.LIGHT_ON_INVERSE_SURFACE         = self.color_theme.LIGHT_ON_INVERSE_SURFACE
		self.LIGHT_INVERSE_PRIMARY            = self.color_theme.LIGHT_INVERSE_PRIMARY


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

		# === КНОПКИ (Buttons) ===
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
		
		# === КАРТОЧКИ (Cards) ===
		self.CARD_DEFAULT = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_SURFACE_CONTAINER_LOW, colors.DARK_SURFACE_CONTAINER],
		)
		
		self.CARD_HOVER = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_SURFACE_CONTAINER, colors.DARK_SURFACE_CONTAINER_HIGH],
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

		self.CARD_ELEVATED = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.DARK_SURFACE_CONTAINER_HIGH, colors.DARK_SURFACE_CONTAINER_HIGHEST],
		)
		
		# === ПРОГРЕСС (Progress) ===
		self.PROGRESS = ft.LinearGradient(
			begin=ft.Alignment.CENTER_LEFT,
			end=ft.Alignment.CENTER_RIGHT,
			colors=[colors.DARK_PRIMARY, colors.DARK_TERTIARY],
		)
		
		self.PROGRESS_BACKGROUND = ft.LinearGradient(
			begin=ft.Alignment.CENTER_LEFT,
			end=ft.Alignment.CENTER_RIGHT,
			colors=[colors.DARK_SURFACE_CONTAINER_LOW, colors.DARK_SURFACE_CONTAINER],
		)
		
		# === ХЕДЕРЫ (Headers) ===
		self.HEADER_PRIMARY = ft.LinearGradient(
			begin=ft.Alignment.CENTER_LEFT,
			end=ft.Alignment.CENTER_RIGHT,
			colors=[colors.DARK_PRIMARY, colors.DARK_SECONDARY, colors.DARK_TERTIARY],
		)

		self.HEADER_VERTICAL = ft.LinearGradient(
			begin=ft.Alignment.BOTTOM_CENTER,
			end=ft.Alignment.TOP_CENTER,
			colors=[colors.DARK_SURFACE_DIM, colors.DARK_TERTIARY_CONTAINER],
		)
		
		# === ДОСТИЖЕНИЯ И НАГРАДЫ (Achievements & Rewards) ===
		self.ACHIEVEMENT = ft.RadialGradient(
			center=ft.Alignment.CENTER,
			radius=0.8,
			colors=[colors.DARK_SECONDARY, colors.DARK_SURFACE_DIM],
		)

		self.GLOW_RADIAL = ft.RadialGradient(
			center=ft.Alignment.CENTER,
			radius=1.2,
			colors=[colors.DARK_TERTIARY, colors.DARK_SURFACE],
		)

		self.REWARD_SWEEP = ft.SweepGradient(
			center=ft.Alignment.CENTER,
			colors=[colors.DARK_SECONDARY, colors.DARK_PRIMARY, colors.DARK_SECONDARY],
		)
		
		# === СТАТУСЫ (Status) ===
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

		# === РАЗДЕЛИТЕЛИ (Dividers) ===
		self.DIVIDER_FADE = ft.LinearGradient(
			begin=ft.Alignment.CENTER_LEFT,
			end=ft.Alignment.CENTER_RIGHT,
			colors=[colors.DARK_SURFACE, colors.DARK_OUTLINE_VARIANT, colors.DARK_SURFACE],
		)


class LightGradients:
	def __init__(self, colors: AppColors) -> None:
		"""Градиенты для светлой темы"""
	
		# === КНОПКИ (Buttons) ===
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
		
		# === КАРТОЧКИ (Cards) ===
		self.CARD_DEFAULT = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_SURFACE_CONTAINER_LOWEST, colors.LIGHT_SURFACE_CONTAINER_LOW],
		)
		
		self.CARD_HOVER = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_SURFACE_CONTAINER_LOW, colors.LIGHT_SURFACE_CONTAINER],
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

		self.CARD_ELEVATED = ft.LinearGradient(
			begin=ft.Alignment.TOP_LEFT,
			end=ft.Alignment.BOTTOM_RIGHT,
			colors=[colors.LIGHT_SURFACE_CONTAINER_HIGH, colors.LIGHT_SURFACE_CONTAINER_HIGHEST],
		)
		
		# === ПРОГРЕСС (Progress) ===
		self.PROGRESS = ft.LinearGradient(
			begin=ft.Alignment.CENTER_LEFT,
			end=ft.Alignment.CENTER_RIGHT,
			colors=[colors.LIGHT_PRIMARY, colors.LIGHT_TERTIARY],
		)
		
		self.PROGRESS_BACKGROUND = ft.LinearGradient(
			begin=ft.Alignment.CENTER_LEFT,
			end=ft.Alignment.CENTER_RIGHT,
			colors=[colors.LIGHT_SURFACE_CONTAINER_LOW, colors.LIGHT_SURFACE_CONTAINER],
		)
		
		# === ХЕДЕРЫ (Headers) ===
		self.HEADER_PRIMARY = ft.LinearGradient(
			begin=ft.Alignment.CENTER_LEFT,
			end=ft.Alignment.CENTER_RIGHT,
			colors=[colors.LIGHT_PRIMARY, colors.LIGHT_SECONDARY, colors.LIGHT_TERTIARY],
		)

		self.HEADER_VERTICAL = ft.LinearGradient(
			begin=ft.Alignment.BOTTOM_CENTER,
			end=ft.Alignment.TOP_CENTER,
			colors=[colors.LIGHT_SURFACE_BRIGHT, colors.LIGHT_PRIMARY_CONTAINER],
		)
		
		# === ДОСТИЖЕНИЯ И НАГРАДЫ (Achievements & Rewards) ===
		self.ACHIEVEMENT = ft.RadialGradient(
			center=ft.Alignment.CENTER,
			radius=0.8,
			colors=[colors.LIGHT_SECONDARY, colors.LIGHT_SURFACE_CONTAINER_LOWEST],
		)

		self.GLOW_RADIAL = ft.RadialGradient(
			center=ft.Alignment.CENTER,
			radius=1.2,
			colors=[colors.LIGHT_TERTIARY_CONTAINER, colors.LIGHT_SURFACE],
		)

		self.REWARD_SWEEP = ft.SweepGradient(
			center=ft.Alignment.CENTER,
			colors=[colors.LIGHT_SECONDARY, colors.LIGHT_PRIMARY, colors.LIGHT_SECONDARY],
		)
		
		# === СТАТУСЫ (Status) ===
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

		# === РАЗДЕЛИТЕЛИ (Dividers) ===
		self.DIVIDER_FADE = ft.LinearGradient(
			begin=ft.Alignment.CENTER_LEFT,
			end=ft.Alignment.CENTER_RIGHT,
			colors=[ft.Colors.TRANSPARENT, colors.LIGHT_OUTLINE_VARIANT, ft.Colors.TRANSPARENT],
		)