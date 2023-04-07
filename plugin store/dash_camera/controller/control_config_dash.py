import yaml


class ControlConfigDash(object):
    def __init__(self, config_file, main_ui):
        self.ui = main_ui
        self.cached_file = config_file

    def set_load_config_file(self, path):
        self.cached_file = path

    def change_rotation_original_image_dash(self):
        with open(self.cached_file, "r") as file:
            cache_config = yaml.safe_load(file)
        cache_config["Dash_Camera"]["Rotate"] = self.ui.spinBox_rotate_image_original.value()
        with open(self.cached_file, "w") as outfile:
            yaml.dump(cache_config, outfile, default_flow_style=False)

    def block_signal_properties_dash_camera(self):
        self.ui.spinBox_alpha_max.blockSignals(True)
        self.ui.spinBox_alpha_dash.blockSignals(True)
        self.ui.spinBox_beta_dash.blockSignals(True)
        self.ui.doubleSpinBox_crop_left.blockSignals(True)
        self.ui.doubleSpinBox_crop_right.blockSignals(True)
        self.ui.doubleSpinBox_crop_top.blockSignals(True)
        self.ui.doubleSpinBox_crop_bottom.blockSignals(True)

    def unblock_signal_properties_dash_camera(self):
        self.ui.spinBox_alpha_max.blockSignals(False)
        self.ui.spinBox_alpha_dash.blockSignals(False)
        self.ui.spinBox_beta_dash.blockSignals(False)
        self.ui.doubleSpinBox_crop_left.blockSignals(False)
        self.ui.doubleSpinBox_crop_right.blockSignals(False)
        self.ui.doubleSpinBox_crop_top.blockSignals(False)
        self.ui.doubleSpinBox_crop_bottom.blockSignals(False)

    def block_signal_properties_anypoint(self):
        self.ui.spinBox_alpha_anypoint_view.blockSignals(True)
        self.ui.spinBox_beta_anypoint_view.blockSignals(True)
        self.ui.doubleSpinBox_roll_anypoint_view.blockSignals(True)
        self.ui.spinBox_zoom_anypoint_view.blockSignals(True)

    def unblock_signal_properties_anypoint(self):
        self.ui.spinBox_alpha_anypoint_view.blockSignals(False)
        self.ui.spinBox_beta_anypoint_view.blockSignals(False)
        self.ui.doubleSpinBox_roll_anypoint_view.blockSignals(False)
        self.ui.spinBox_zoom_anypoint_view.blockSignals(False)

    def showing_config_anypoint(self, view):
        with open(self.cached_file, "r") as file:
            dash_config = yaml.safe_load(file)
        self.block_signal_properties_anypoint()
        self.ui.spinBox_alpha_anypoint_view.setValue(dash_config["Dash_Camera"]["View"][view]["alpha"])
        self.ui.spinBox_beta_anypoint_view.setValue(dash_config["Dash_Camera"]["View"][view]["beta"])
        self.ui.doubleSpinBox_roll_anypoint_view.setValue(dash_config["Dash_Camera"]["View"][view]["roll"])
        self.ui.spinBox_zoom_anypoint_view.setValue(dash_config["Dash_Camera"]["View"][view]["zoom"])
        self.unblock_signal_properties_anypoint()

    def showing_config_dash_image(self, view):
        with open(self.cached_file, "r") as file:
            dash_config = yaml.safe_load(file)
        self.block_signal_properties_dash_camera()
        self.ui.spinBox_alpha_max.setValue(int(dash_config["Dash_Camera"]["View"][view]["alpha_max"]))
        self.ui.spinBox_alpha_dash.setValue(int(dash_config["Dash_Camera"]["View"][view]["alpha"]))
        self.ui.spinBox_beta_dash.setValue(int(dash_config["Dash_Camera"]["View"][view]["beta"]))
        self.ui.doubleSpinBox_crop_left.setValue(dash_config["Dash_Camera"]["View"][view]["crop_left"])
        self.ui.doubleSpinBox_crop_right.setValue(dash_config["Dash_Camera"]["View"][view]["crop_right"])
        self.ui.doubleSpinBox_crop_top.setValue(dash_config["Dash_Camera"]["View"][view]["crop_top"])
        self.ui.doubleSpinBox_crop_bottom.setValue(dash_config["Dash_Camera"]["View"][view]["crop_bottom"])
        self.unblock_signal_properties_dash_camera()

    def change_properties_crop_image(self, view):
        with open(self.cached_file, "r") as file:
            cache_config = yaml.safe_load(file)
        cache_config["Dash_Camera"]["View"][f'{view}']["crop_top"] = self.ui.doubleSpinBox_crop_top.value()
        cache_config["Dash_Camera"]["View"][f'{view}']["crop_bottom"] = self.ui.doubleSpinBox_crop_bottom.value()
        cache_config["Dash_Camera"]["View"][f'{view}']["crop_left"] = self.ui.doubleSpinBox_crop_left.value()
        cache_config["Dash_Camera"]["View"][f'{view}']["crop_right"] = self.ui.doubleSpinBox_crop_right.value()
        with open(self.cached_file, "w") as outfile:
            yaml.dump(cache_config, outfile, default_flow_style=False)

    def change_properties_dash_image(self, view):
        with open(self.cached_file, "r") as file:
            cache_config = yaml.safe_load(file)
        cache_config["Dash_Camera"]["View"][f'{view}']["alpha_max"] = self.ui.spinBox_alpha_max.value()
        cache_config["Dash_Camera"]["View"][f'{view}']["alpha"] = self.ui.spinBox_alpha_dash.value()
        cache_config["Dash_Camera"]["View"][f'{view}']["beta"] = self.ui.spinBox_beta_dash.value()
        with open(self.cached_file, "w") as outfile:
            yaml.dump(cache_config, outfile, default_flow_style=False)

    def change_properties_anypoint(self, view):
        with open(self.cached_file, "r") as file:
            cache_config = yaml.safe_load(file)
        cache_config["Dash_Camera"]["View"][f'{view}']["alpha"] = self.ui.spinBox_alpha_anypoint_view.value()
        cache_config["Dash_Camera"]["View"][f'{view}']["beta"] = self.ui.spinBox_beta_anypoint_view.value()
        cache_config["Dash_Camera"]["View"][f'{view}']["roll"] = self.ui.doubleSpinBox_roll_anypoint_view.value()
        cache_config["Dash_Camera"]["View"][f'{view}']["zoom"] = self.ui.spinBox_zoom_anypoint_view.value()
        with open(self.cached_file, "w") as outfile:
            yaml.dump(cache_config, outfile, default_flow_style=False)

    def change_properties_rotate_dash_image(self):
        with open(self.cached_file, "r") as file:
            cache_config = yaml.safe_load(file)
        cache_config["Dash_Camera"]["Rotate"] = self.ui.spinBox_rotate_image_original.value()
        with open(self.cached_file, "w") as outfile:
            yaml.dump(cache_config, outfile, default_flow_style=False)
