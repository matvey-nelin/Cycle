# Библиотеки фактического импорта
import flet as ft

from AppState import AppState
from UI.CycleApp import CycleApp

import time



def main(page: ft.Page):

    try:
        # Инициализация объекта храненящего состояние приложения
        app_state = AppState(page)
    
    except Exception as ex:
        page.clean()
        page.add(ft.Text(f"Exception: {ex}"))
        return

    # Закрытие соединения с БД при закрытии     
    page.clean()
    page.on_close = lambda e: app_state.database._close_connection_()

    CycleApp(page, app_state)


ft.run(
    main=main,
    assets_dir="assets"
)
