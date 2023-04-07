from src.plugin_interface import PluginInterface
from .controller.control_main import Controller


class MoilDashCamera(PluginInterface):
    def __init__(self):
        super().__init__()
        self.widget = None
        self.description = "Applications"

    def set_plugin_widget(self, model):
        self.widget = Controller(model)
        return self.widget

    def set_icon_apps(self):
        return "icon/moil.png"

    def change_stylesheet(self):
        self.widget.set_stylesheet()