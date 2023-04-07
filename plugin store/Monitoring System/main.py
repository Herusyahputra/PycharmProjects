from src.plugin_interface import PluginInterface
# from .models.model import Model
from .controller.controller import Controller

class MonitoringSystemApps(PluginInterface):
    def __init__(self):
        super().__init__()
        self.widget = None
        self.description = "This is Detection of Plural Vehicle-Plates Using a Fisheye Camera Applications"

    def set_plugin_widget(self, model):
        self.widget = Controller(model)
        return self.widget

    def set_icon_apps(self):
        return "icon/Detection-1.png"

    def change_stylesheet(self):
        # pass
        self.widget.set_stylesheet()