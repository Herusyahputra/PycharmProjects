import os

import numpy as np
import yaml


class ConfigFile(object):
    def __init__(self, main_ui):
        super().__init__()
        self.ui = main_ui
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.cached_file = parent_dir + "/model/cached/cache_config.yaml"
        self.clear_maps_history()
        self.init_config_file()

    def change_project_name(self, project_name):
        with open(self.cached_file, "r") as file:
            cache_config = yaml.safe_load(file)

        cache_config["Project_name"] = project_name
        with open(self.cached_file, "w") as outfile:
            yaml.dump(cache_config, outfile, default_flow_style=False)

    def set_load_config_file(self, path):
        self.cached_file = path

    def clear_maps_history(self):
        for filename in os.listdir(os.path.dirname(self.cached_file)):
            if filename.endswith(".npy"):
                with open(f'{os.path.dirname(self.cached_file)}/{filename}', 'wb') as file:
                    np.save(file, None)

            else:
                continue

    def init_config_file(self):
        cache_config = {"Project_name": None,
                        "Dash_Camera": {
                            "Source": None,
                            "Parameter_name": None,
                            "Brightness": None,
                            "Contrast": None,
                            "Rotate": self.ui.spinBox_rotate_image_original.value(),
                            "View": {
                                "Dash_front_view": {
                                    "alpha_max": self.ui.spinBox_alpha_max.value(),
                                    "alpha": self.ui.spinBox_alpha_dash.value(),
                                    "beta": self.ui.spinBox_beta_dash.value(),
                                    "crop_top": self.ui.doubleSpinBox_crop_top.value(),
                                    "crop_bottom": self.ui.doubleSpinBox_crop_bottom.value(),
                                    "crop_left": self.ui.doubleSpinBox_crop_left.value(),
                                    "crop_right": self.ui.doubleSpinBox_crop_right.value()},
                                "Dash_driver_view": {
                                    "alpha_max": self.ui.spinBox_alpha_max.value(),
                                    "alpha": self.ui.spinBox_alpha_dash.value(),
                                    "beta": self.ui.spinBox_beta_dash.value(),
                                    "crop_top": self.ui.doubleSpinBox_crop_top.value(),
                                    "crop_bottom": self.ui.doubleSpinBox_crop_bottom.value(),
                                    "crop_left": self.ui.doubleSpinBox_crop_left.value(),
                                    "crop_right": self.ui.doubleSpinBox_crop_right.value()},
                                "Left Window": {
                                    "alpha": self.ui.spinBox_alpha_anypoint_view.value(),
                                    "beta": self.ui.spinBox_beta_anypoint_view.value(),
                                    "roll": self.ui.doubleSpinBox_roll_anypoint_view.value(),
                                    "zoom": self.ui.spinBox_zoom_anypoint_view.value()},
                                "Right Window": {
                                    "alpha": self.ui.spinBox_alpha_anypoint_view.value(),
                                    "beta": self.ui.spinBox_beta_anypoint_view.value(),
                                    "roll": self.ui.doubleSpinBox_roll_anypoint_view.value(),
                                    "zoom": self.ui.spinBox_zoom_anypoint_view.value()},
                                "Steering View": {
                                    "alpha": self.ui.spinBox_alpha_anypoint_view.value(),
                                    "beta": self.ui.spinBox_beta_anypoint_view.value(),
                                    "roll": self.ui.doubleSpinBox_roll_anypoint_view.value(),
                                    "zoom": self.ui.spinBox_zoom_anypoint_view.value()},
                                "Second Driver View": {
                                    "alpha": self.ui.spinBox_alpha_anypoint_view.value(),
                                    "beta": self.ui.spinBox_beta_anypoint_view.value(),
                                    "roll": self.ui.doubleSpinBox_roll_anypoint_view.value(),
                                    "zoom": self.ui.spinBox_zoom_anypoint_view.value()},
                                "For comparison View": {
                                    "alpha": self.ui.spinBox_alpha_anypoint_view.value(),
                                    "beta": self.ui.spinBox_beta_anypoint_view.value(),
                                    "roll": self.ui.doubleSpinBox_roll_anypoint_view.value(),
                                    "zoom": self.ui.spinBox_zoom_anypoint_view.value()},
                            }
                        },
                        "Bird_View": {
                            "Mode_calib": None,
                            "Gradient_mode": "O",
                            "Image": {
                                "Image_1": {
                                    "Source": None,
                                    "Parameter_name": None,
                                    "alpha": self.ui.spinBox_val_icx_image_1.value(),
                                    "beta": self.ui.spinBox_val_icy_image_1.value(),
                                    "zoom": self.ui.doubleSpinBox_val_zoom_image_1.value(),
                                    "rotate": self.ui.doubleSpinBox_val_rotate_image_1.value(),
                                    "x_axis": self.ui.spinBox_val_coordinate_x_image_1.value(),
                                    "y_axis": self.ui.spinBox_val_coordinate_y_image_1.value(),
                                    "crop_top": self.ui.spinBox_val_crop_top_image_1.value(),
                                    "crop_bottom": self.ui.spinBox_val_crop_bottom_image_1.value(),
                                    "crop_left": self.ui.spinBox_val_crop_left_image_1.value(),
                                    "crop_right": self.ui.spinBox_val_crop_right_image_1.value()},
                                "Image_2": {
                                    "Source": None,
                                    "Parameter_name": None,
                                    "alpha": self.ui.spinBox_val_icx_image_2.value(),
                                    "beta": self.ui.spinBox_val_icy_image_2.value(),
                                    "zoom": self.ui.doubleSpinBox_val_zoom_image_2.value(),
                                    "rotate": self.ui.doubleSpinBox_val_rotate_image_2.value(),
                                    "x_axis": self.ui.spinBox_val_coordinate_x_image_2.value(),
                                    "y_axis": self.ui.spinBox_val_coordinate_y_image_2.value(),
                                    "crop_top": self.ui.spinBox_val_crop_top_image_2.value(),
                                    "crop_bottom": self.ui.spinBox_val_crop_bottom_image_2.value(),
                                    "crop_left": self.ui.spinBox_val_crop_left_image_2.value(),
                                    "crop_right": self.ui.spinBox_val_crop_right_image_2.value()},
                                "Image_3": {
                                    "Source": None,
                                    "Parameter_name": None,
                                    "alpha": self.ui.spinBox_val_icx_image_3.value(),
                                    "beta": self.ui.spinBox_val_icy_image_3.value(),
                                    "zoom": self.ui.doubleSpinBox_val_zoom_image_3.value(),
                                    "rotate": self.ui.doubleSpinBox_val_rotate_image_3.value(),
                                    "x_axis": self.ui.spinBox_val_coordinate_x_image_3.value(),
                                    "y_axis": self.ui.spinBox_val_coordinate_y_image_3.value(),
                                    "crop_top": self.ui.spinBox_val_crop_top_image_3.value(),
                                    "crop_bottom": self.ui.spinBox_val_crop_bottom_image_3.value(),
                                    "crop_left": self.ui.spinBox_val_crop_left_image_3.value(),
                                    "crop_right": self.ui.spinBox_val_crop_right_image_3.value()},
                                "Image_4": {
                                    "Source": None,
                                    "Parameter_name": None,
                                    "alpha": self.ui.spinBox_val_icx_image_4.value(),
                                    "beta": self.ui.spinBox_val_icy_image_4.value(),
                                    "zoom": self.ui.doubleSpinBox_val_zoom_image_4.value(),
                                    "rotate": self.ui.doubleSpinBox_val_rotate_image_4.value(),
                                    "x_axis": self.ui.spinBox_val_coordinate_x_image_4.value(),
                                    "y_axis": self.ui.spinBox_val_coordinate_y_image_4.value(),
                                    "crop_top": self.ui.spinBox_val_crop_top_image_4.value(),
                                    "crop_bottom": self.ui.spinBox_val_crop_bottom_image_4.value(),
                                    "crop_left": self.ui.spinBox_val_crop_left_image_4.value(),
                                    "crop_right": self.ui.spinBox_val_crop_right_image_4.value()}
                                }
                            }
                        }

        with open(self.cached_file, "w") as outfile:
            yaml.dump(cache_config, outfile, default_flow_style=False)
