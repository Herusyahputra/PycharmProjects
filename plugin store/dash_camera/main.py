from src.plugin_interface import PluginInterface
from src.controllers.plugins.dash_camera.controller.controller import Controller


class DashCamera(PluginInterface):
    def __init__(self):
        super().__init__()
        self.widget = None

    def set_plugin_widget(self, model):
        self.widget = Controller(model)

        return self.widget

    def set_icon_apps(self):
        return "assets/icon.png"

    def change_stylesheet(self):
        self.widget.change_stylesheets()
