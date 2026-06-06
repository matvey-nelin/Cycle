# Библиотеки фактического импорта
import flet as ft

from AppState import AppState
from UI.CycleApp import CycleApp


def main(page: ft.Page):
    # Инициализация объекта хранящего состояние приложения
    app_state = AppState(page)
    CycleApp(page, app_state)


ft.run(
    main=main,
    assets_dir="assets"
)
