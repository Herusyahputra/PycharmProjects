from src.plugin_interface import PluginInterface
from .controller import Controller

class Monitoring_System(PluginInterface):
    def __init__(self):
        super().__init__()
        self.widget = None
        self.description = "Applications"

    def set_plugin_widget(self, model):
        self.widget = Controller(model)
        return self.widget

    def set_icon_apps(self):
        return "icon/Detection-1.png"

    def change_stylesheet(self):
        # pass
        self.widget.set_stylesheet()