import yaml
import os


class ConfigFileApps(object):
    def __init__(self, main_ui):
        self.ui = main_ui
        path_file = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        self.__cached_file = path_file + "/src/models/cached/cache_config.yaml"
        self.__cache_config = {}
        self.__init_config_file()

    def __init_config_file(self):
        if not os.path.exists(self.__cached_file):
            self.__cache_config["Media_path"] = None
            self.__cache_config["Parameter_name"] = None
            self.__cache_config["Mode_1"] = {}
            self.__cache_config["Mode_1"]["coord"] = [None, None]
            self.__cache_config["Mode_1"]["alpha"] = self.ui.doubleSpinBox_alpha.value()
            self.__cache_config["Mode_1"]["beta"] = self.ui.doubleSpinBox_beta.value()
            self.__cache_config["Mode_1"]["zoom"] = round(self.ui.doubleSpinBox_zoom.value(), 3)
            self.__cache_config["Mode_2"] = {}
            self.__cache_config["Mode_2"]["coord"] = [None, None]
            self.__cache_config["Mode_2"]["pitch"] = self.ui.doubleSpinBox_alpha.value()
            self.__cache_config["Mode_2"]["yaw"] = self.ui.doubleSpinBox_beta.value()
            self.__cache_config["Mode_2"]["roll"] = self.ui.doubleSpinBox_roll.value()
            self.__cache_config["Mode_2"]["zoom"] = round(self.ui.doubleSpinBox_zoom.value(), 3)
            self.__cache_config["Pano_tube"] = {}
            self.__cache_config["Pano_tube"]["alpha_min"] = round(self.ui.spinBox_pano_tube_alpha_min.value(), 3)
            self.__cache_config["Pano_tube"]["alpha_max"] = round(self.ui.spinBox_pano_tube_alpha_max.value(), 3)
            self.__cache_config["Pano_tube"]["crop_top"] = round(self.ui.doubleSpinBox_pano_tube_crop_top.value(), 3)
            self.__cache_config["Pano_tube"]["crop_bottom"] = round(self.ui.doubleSpinBox_pano_tube_crop_buttom.value(), 3)
            self.__cache_config["Pano_car"] = {}
            self.__cache_config["Pano_car"]["coord"] = [None, None]
            self.__cache_config["Pano_car"]["alpha"] = round(self.ui.spinBox_pano_car_alpha.value(), 3)
            self.__cache_config["Pano_car"]["beta"] = round(self.ui.spinBox_pano_car_beta.value(), 3)
            self.__cache_config["Pano_car"]["crop_left"] = round(self.ui.doubleSpinBox_pano_car_crop_left.value(), 3)
            self.__cache_config["Pano_car"]["crop_right"] = round(self.ui.doubleSpinBox_pano_car_crop_right.value(), 3)
            self.__cache_config["Pano_car"]["crop_top"] = round(self.ui.doubleSpinBox_pano_car_crop_top.value(), 3)
            self.__cache_config["Pano_car"]["crop_bottom"] = round(self.ui.doubleSpinBox_pano_car_crop_bottom.value(), 3)

            with open(self.__cached_file, "w") as outfile:
                yaml.dump(self.__cache_config, outfile, default_flow_style=False)
