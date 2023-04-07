import os
import yaml


class AnypointConfig(object):
    def __init__(self, main_ui):
        self.ui = main_ui
        path_file = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        self.__cached_file = path_file + "/src/models/cached/cache_config.yaml"
        with open(self.__cached_file, "r") as file:
            self.__anypoint_config = yaml.safe_load(file)

    def __block_signal(self):
        self.ui.doubleSpinBox_alpha.blockSignals(True)
        self.ui.doubleSpinBox_beta.blockSignals(True)
        self.ui.doubleSpinBox_roll.blockSignals(True)
        self.ui.doubleSpinBox_zoom.blockSignals(True)

    def __unblock_signal(self):
        self.ui.doubleSpinBox_alpha.blockSignals(False)
        self.ui.doubleSpinBox_beta.blockSignals(False)
        self.ui.doubleSpinBox_roll.blockSignals(False)
        self.ui.doubleSpinBox_zoom.blockSignals(False)

    def showing_config_mode_1(self):
        with open(self.__cached_file, "r") as file:
            self.__anypoint_config = yaml.safe_load(file)
        self.__block_signal()
        self.ui.doubleSpinBox_alpha.setValue(self.__anypoint_config["Mode_1"]["alpha"])
        self.ui.doubleSpinBox_beta.setValue(self.__anypoint_config["Mode_1"]["beta"])
        self.ui.doubleSpinBox_zoom.setValue(self.__anypoint_config["Mode_1"]["zoom"])
        self.__unblock_signal()

    def showing_config_mode_2(self):
        with open(self.__cached_file, "r") as file:
            self.__anypoint_config = yaml.safe_load(file)
        self.__block_signal()
        self.ui.doubleSpinBox_alpha.setValue(self.__anypoint_config["Mode_2"]["pitch"])
        self.ui.doubleSpinBox_beta.setValue(self.__anypoint_config["Mode_2"]["yaw"])
        self.ui.doubleSpinBox_roll.setValue(self.__anypoint_config["Mode_2"]["roll"])
        self.ui.doubleSpinBox_zoom.setValue(self.__anypoint_config["Mode_2"]["zoom"])
        self.__unblock_signal()

    def change_properties_mode_1(self):
        self.__anypoint_config["Mode_1"]["alpha"] = self.ui.doubleSpinBox_alpha.value()
        self.__anypoint_config["Mode_1"]["beta"] = self.ui.doubleSpinBox_beta.value()
        self.__anypoint_config["Mode_1"]["zoom"] = round(self.ui.doubleSpinBox_zoom.value(), 3)
        with open(self.__cached_file, "w") as outfile:
            yaml.dump(self.__anypoint_config, outfile, default_flow_style=False)

    def change_properties_mode_2(self):
        self.__anypoint_config["Mode_2"]["pitch"] = self.ui.doubleSpinBox_alpha.value()
        self.__anypoint_config["Mode_2"]["yaw"] = self.ui.doubleSpinBox_beta.value()
        self.__anypoint_config["Mode_2"]["roll"] = self.ui.doubleSpinBox_roll.value()
        self.__anypoint_config["Mode_2"]["zoom"] = round(self.ui.doubleSpinBox_zoom.value(), 3)
        with open(self.__cached_file, "w") as outfile:
            yaml.dump(self.__anypoint_config, outfile, default_flow_style=False)


