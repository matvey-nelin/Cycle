# Библиотеки фактического импорта
import flet as ft

from AppState import AppState
from UI.CycleApp import CycleApp


def main(page: ft.Page):

    try:
        # Инициализация объекта хранящего состояние приложения
        app_state = AppState(page)
    
    except Exception as ex:
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
        page.add(ft.Text(f"Exception: {ex}"))
        return
    
    page.clean()

    CycleApp(page, app_state)


ft.run(
    main=main,
    assets_dir="assets"
)
