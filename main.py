# Библиотеки фактического импорта
import flet as ft

from AppState import AppState
from UI.CycleApp import CycleApp




def main(page: ft.Page):
    # Предотавращает мгновенное закрытие при багах навигации
    page.on_close = lambda: None

    app_state = AppState(page)
    CycleApp(page, app_state)


ft.run(
    main=main,
    assets_dir="assets",
    name="Cycle"
)
