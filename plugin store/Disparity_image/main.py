import os

from src.plugin_interface import PluginInterface
from src.controllers.plugins.Disparity_image.controller.controller import Controller
from src.controllers.plugins.Disparity_image.model.model import ModelPlugin


class DisparityImage(PluginInterface):
    def __init__(self):
        super().__init__()
        self.widget = None

    def set_plugin_widget(self, model):
        model_plugin = ModelPlugin(model)
        self.widget = Controller(model, model_plugin)

        return self.widget

    def set_icon_apps(self):
        print(os.getcwd())
        return "assets/icon.png"

    def change_stylesheet(self):
        self.widget.themes.change_stylesheets()
