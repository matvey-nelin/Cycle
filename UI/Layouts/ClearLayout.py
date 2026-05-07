import flet as ft

from Languages.Translator import Translator
from UI.Layouts.BaseLayout import BaseLayout


class ClearLayout(BaseLayout):
    def __init__(self, page: ft.Page, translator: Translator, navigate_callback) -> None:
        super().__init__(page, translator, navigate_callback)

        self.layout_container = self.content_container





