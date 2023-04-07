import yaml


class ControlConfigBirdsView(object):
    def __init__(self, config_file, main_ui):
        self.ui = main_ui
        self.cached_file = config_file

    def set_load_config_file(self, path):
        self.cached_file = path

    def change_config_anypoint_properties_bird_view(self, index):
        with open(self.cached_file, "r") as file:
            config = yaml.safe_load(file)
        config["Bird_View"]["Image"][f"Image_{index}"]["alpha"] = \
            getattr(self.ui, f"spinBox_val_icx_image_{index}").value()
        config["Bird_View"]["Image"][f"Image_{index}"]["beta"] = \
            getattr(self.ui, f'spinBox_val_icy_image_{index}').value()
        config["Bird_View"]["Image"][f"Image_{index}"]["zoom"] = \
            getattr(self.ui, f'doubleSpinBox_val_zoom_image_{index}').value()
        config["Bird_View"]["Image"][f"Image_{index}"]["rotate"] = \
            getattr(self.ui, f'doubleSpinBox_val_rotate_image_{index}').value()
        with open(self.cached_file, "w") as outfile:
            yaml.dump(config, outfile, default_flow_style=False)

    def change_properties_shift_birds_image(self, index):
        with open(self.cached_file, "r") as file:
            config = yaml.safe_load(file)
        config["Bird_View"]["Image"][f"Image_{index}"]["x_axis"] = \
            getattr(self.ui, f"spinBox_val_coordinate_x_image_{index}").value()
        config["Bird_View"]["Image"][f"Image_{index}"]["y_axis"] = \
            getattr(self.ui, f"spinBox_val_coordinate_y_image_{index}").value()
        with open(self.cached_file, "w") as outfile:
            yaml.dump(config, outfile, default_flow_style=False)

    def change_crop_properties_image_bird_view(self, index):
        with open(self.cached_file, "r") as file:
            config = yaml.safe_load(file)
        config["Bird_View"]["Image"][f"Image_{index}"]["crop_top"] = \
            getattr(self.ui, f"spinBox_val_crop_top_image_{index}").value()
        config["Bird_View"]["Image"][f"Image_{index}"]["crop_bottom"] = \
            getattr(self.ui, f"spinBox_val_crop_bottom_image_{index}").value()
        config["Bird_View"]["Image"][f"Image_{index}"]["crop_left"] = \
            getattr(self.ui, f"spinBox_val_crop_left_image_{index}").value()
        config["Bird_View"]["Image"][f"Image_{index}"]["crop_right"] = \
            getattr(self.ui, f"spinBox_val_crop_right_image_{index}").value()
        with open(self.cached_file, "w") as outfile:
            yaml.dump(config, outfile, default_flow_style=False)

    def showing_confing_to_ui(self):
        self.__block_signals()
        with open(self.cached_file, "r") as file:
            config_view = yaml.safe_load(file)
        for i in range(1, 5):
            alpha = config_view["Bird_View"]["Image"][f"Image_{i}"]["alpha"]
            beta = config_view["Bird_View"]["Image"][f"Image_{i}"]["beta"]

            alpha_widget = getattr(self.ui, f"spinBox_val_icx_image_{i}")
            beta_widget = getattr(self.ui, f"spinBox_val_icy_image_{i}")
            alpha_widget.setValue(alpha)
            beta_widget.setValue(beta)

            zoom = config_view["Bird_View"]["Image"][f"Image_{i}"]["zoom"]
            rotate = config_view["Bird_View"]["Image"][f"Image_{i}"]["rotate"]

            zoom_widget = getattr(self.ui, f"doubleSpinBox_val_zoom_image_{i}")
            rotate_widget = getattr(self.ui, f"doubleSpinBox_val_rotate_image_{i}")
            zoom_widget.setValue(zoom)
            rotate_widget.setValue(rotate)

            x_axis = config_view["Bird_View"]["Image"][f"Image_{i}"]["x_axis"]
            y_axis = config_view["Bird_View"]["Image"][f"Image_{i}"]["y_axis"]

            x_axis_widget = getattr(self.ui, f"spinBox_val_coordinate_x_image_{i}")
            y_axis_widget = getattr(self.ui, f"spinBox_val_coordinate_y_image_{i}")
            x_axis_widget.setValue(x_axis)
            y_axis_widget.setValue(y_axis)

            crop_top = config_view["Bird_View"]["Image"][f"Image_{i}"]["crop_top"]
            crop_bottom = config_view["Bird_View"]["Image"][f"Image_{i}"]["crop_bottom"]
            crop_left = config_view["Bird_View"]["Image"][f"Image_{i}"]["crop_left"]
            crop_right = config_view["Bird_View"]["Image"][f"Image_{i}"]["crop_right"]

            crop_top_widget = getattr(self.ui, f"spinBox_val_crop_top_image_{i}")
            crop_bottom_widget = getattr(self.ui, f"spinBox_val_crop_bottom_image_{i}")
            crop_left_widget = getattr(self.ui, f"spinBox_val_crop_left_image_{i}")
            crop_right_widget = getattr(self.ui, f"spinBox_val_crop_right_image_{i}")
            crop_top_widget.setValue(crop_top)
            crop_bottom_widget.setValue(crop_bottom)
            crop_left_widget.setValue(crop_left)
            crop_right_widget.setValue(crop_right)

        self.__block_signals(False)

    def __block_signals(self, block=True):
        for i in range(1, 5):
            icx_widget = getattr(self.ui, f"spinBox_val_icx_image_{i}")
            icy_widget = getattr(self.ui, f"spinBox_val_icy_image_{i}")
            zoom_widget = getattr(self.ui, f"doubleSpinBox_val_zoom_image_{i}")
            rotate_widget = getattr(self.ui, f"doubleSpinBox_val_rotate_image_{i}")
            shift_x_widget = getattr(self.ui, f"spinBox_val_coordinate_x_image_{i}")
            shift_y_widget = getattr(self.ui, f"spinBox_val_coordinate_y_image_{i}")
            crop_top_widget = getattr(self.ui, f"spinBox_val_crop_top_image_{i}")
            crop_bottom_widget = getattr(self.ui, f"spinBox_val_crop_bottom_image_{i}")
            crop_left_widget = getattr(self.ui, f"spinBox_val_crop_left_image_{i}")
            crop_right_widget = getattr(self.ui, f"spinBox_val_crop_right_image_{i}")
            icx_widget.blockSignals(block)
            icy_widget.blockSignals(block)
            zoom_widget.blockSignals(block)
            rotate_widget.blockSignals(block)
            shift_x_widget.blockSignals(block)
            shift_y_widget.blockSignals(block)
            crop_top_widget.blockSignals(block)
            crop_bottom_widget.blockSignals(block)
            crop_left_widget.blockSignals(block)
            crop_right_widget.blockSignals(block)
