import os
import yaml


class PanoramaConfig(object):
    def __init__(self, main_ui):
        self.ui = main_ui
        path_file = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        self.__cached_file = path_file + "/src/models/cached/cache_config.yaml"
        with open(self.__cached_file, "r") as file:
            self.__panorama_config = yaml.safe_load(file)

    def __block_signal_pano_tube(self):
        self.ui.spinBox_pano_tube_alpha_min.blockSignals(True)
        self.ui.spinBox_pano_tube_alpha_max.blockSignals(True)
        self.ui.doubleSpinBox_pano_tube_crop_top.blockSignals(True)
        self.ui.doubleSpinBox_pano_tube_crop_buttom.blockSignals(True)

    def __unblock_signal_pano_tube(self):
        self.ui.spinBox_pano_tube_alpha_min.blockSignals(False)
        self.ui.spinBox_pano_tube_alpha_max.blockSignals(False)
        self.ui.doubleSpinBox_pano_tube_crop_top.blockSignals(False)
        self.ui.doubleSpinBox_pano_tube_crop_buttom.blockSignals(False)

    def __block_signal_pano_car(self):
        self.ui.spinBox_pano_car_alpha.blockSignals(True)
        self.ui.spinBox_pano_car_beta.blockSignals(True)
        self.ui.doubleSpinBox_pano_car_crop_left.blockSignals(True)
        self.ui.doubleSpinBox_pano_car_crop_right.blockSignals(True)
        self.ui.doubleSpinBox_pano_car_crop_top.blockSignals(True)
        self.ui.doubleSpinBox_pano_car_crop_bottom.blockSignals(True)

    def __unblock_signal_pano_car(self):
        self.ui.spinBox_pano_car_alpha.blockSignals(False)
        self.ui.spinBox_pano_car_beta.blockSignals(False)
        self.ui.doubleSpinBox_pano_car_crop_left.blockSignals(False)
        self.ui.doubleSpinBox_pano_car_crop_right.blockSignals(False)
        self.ui.doubleSpinBox_pano_car_crop_top.blockSignals(False)
        self.ui.doubleSpinBox_pano_car_crop_bottom.blockSignals(False)

    def showing_config_panorama_tube(self):
        with open(self.__cached_file, "r") as file:
            self.__panorama_config = yaml.safe_load(file)
        self.__block_signal_pano_tube()
        self.ui.spinBox_pano_tube_alpha_min.setValue(self.__panorama_config["Pano_tube"]["alpha_min"])
        self.ui.spinBox_pano_tube_alpha_max.setValue(self.__panorama_config["Pano_tube"]["alpha_max"])
        self.ui.doubleSpinBox_pano_tube_crop_top.setValue(self.__panorama_config["Pano_tube"]["crop_top"])
        self.ui.doubleSpinBox_pano_tube_crop_buttom.setValue(self.__panorama_config["Pano_tube"]["crop_bottom"])
        self.__unblock_signal_pano_tube()

    def showing_config_panorama_car(self):
        with open(self.__cached_file, "r") as file:
            self.__panorama_config = yaml.safe_load(file)
        self.__block_signal_pano_car()
        self.ui.spinBox_pano_car_alpha.setValue(self.__panorama_config["Pano_car"]["alpha"])
        self.ui.spinBox_pano_car_beta.setValue(self.__panorama_config["Pano_car"]["beta"])
        self.ui.doubleSpinBox_pano_car_crop_left.setValue(self.__panorama_config["Pano_car"]["crop_left"])
        self.ui.doubleSpinBox_pano_car_crop_right.setValue(self.__panorama_config["Pano_car"]["crop_right"])
        self.ui.doubleSpinBox_pano_car_crop_top.setValue(self.__panorama_config["Pano_car"]["crop_top"])
        self.ui.doubleSpinBox_pano_car_crop_bottom.setValue(self.__panorama_config["Pano_car"]["crop_bottom"])
        self.__unblock_signal_pano_car()

    def change_properties_panorama_tube(self):
        self.__panorama_config["Pano_tube"]["alpha_min"] = self.ui.spinBox_pano_tube_alpha_min.value()
        self.__panorama_config["Pano_tube"]["alpha_max"] = self.ui.spinBox_pano_tube_alpha_max.value()
        self.__panorama_config["Pano_tube"]["crop_top"] = round(self.ui.doubleSpinBox_pano_tube_crop_top.value(), 3)
        self.__panorama_config["Pano_tube"]["crop_bottom"] = round(self.ui.doubleSpinBox_pano_tube_crop_buttom.value(), 3)
        with open(self.__cached_file, "w") as outfile:
            yaml.dump(self.__panorama_config, outfile, default_flow_style=False)

    def change_properties_panorama_car(self):
        self.__panorama_config["Pano_car"]["alpha"] = self.ui.spinBox_pano_car_alpha.value()
        self.__panorama_config["Pano_car"]["beta"] = self.ui.spinBox_pano_car_beta.value()
        self.__panorama_config["Pano_car"]["crop_left"] = self.ui.doubleSpinBox_pano_car_crop_left.value()
        self.__panorama_config["Pano_car"]["crop_right"] = round(self.ui.doubleSpinBox_pano_car_crop_right.value(), 3)
        self.__panorama_config["Pano_car"]["crop_top"] = round(self.ui.doubleSpinBox_pano_car_crop_top.value(), 3)
        self.__panorama_config["Pano_car"]["crop_bottom"] = round(self.ui.doubleSpinBox_pano_car_crop_bottom.value(), 3)
        with open(self.__cached_file, "w") as outfile:
            yaml.dump(self.__panorama_config, outfile, default_flow_style=False)

