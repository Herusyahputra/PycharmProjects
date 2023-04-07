import os

import yaml

from src.plugin_interface import PluginInterface
from PyQt6.QtWidgets import QWidget
from .ui_main import Ui_Form
from .ctrl_config_file import ConfigFileApps
import cv2


class Controller(QWidget):
    def __init__(self, model):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.model = model
        self.ctr_config_file = ConfigFileApps(self.ui)

        self.icx = None
        self.icy = None
        self.image = None
        self.pano_image = None
        self.moildev = None
        self.image_rec = None
        self.__width_image_result = 1000

        self.__configuration_view = None
        self.open_image(False)

        self.change_stylesheet()
        self.ui.pushButton.clicked.connect(lambda: self.open_image(True))
        self.ui.pushButton_zoom_in.clicked.connect(lambda: self.zoom_image("zoom_in"))
        self.ui.pushButton_zoom_out.clicked.connect(lambda: self.zoom_image("zoom_out"))
        self.ui.spinBox.valueChanged.connect(self.change_value_center_x)
        self.ui.spinBox_2.valueChanged.connect(self.change_value_center_y)
        self.ui.spinBox_3.valueChanged.connect(self.panorama_tube)
        self.ui.spinBox_4.valueChanged.connect(self.panorama_tube)
        self.ui.c_top.valueChanged.connect(self.show_panorama)
        self.ui.c_left.valueChanged.connect(self.show_panorama)
        self.ui.c_right.valueChanged.connect(self.show_panorama)
        self.ui.c_btn.valueChanged.connect(self.show_panorama)
        self.ui.checkBox.stateChanged.connect(self.change_pano_mode)

    def change_stylesheet(self):
        self.ui.frame_main.setStyleSheet(self.model.style_frame_main())
        self.ui.frame_button_control.setStyleSheet(self.model.style_frame_object())
        self.ui.frame.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_2.setStyleSheet(self.model.style_frame_object())
        self.ui.spinBox.setStyleSheet(self.model.style_spinbox())
        self.ui.spinBox_2.setStyleSheet(self.model.style_spinbox())
        self.ui.spinBox_3.setStyleSheet(self.model.style_spinbox())
        self.ui.spinBox_4.setStyleSheet(self.model.style_spinbox())
        self.ui.c_top.setStyleSheet(self.model.style_double_spin_box())
        self.ui.c_btn.setStyleSheet(self.model.style_double_spin_box())
        self.ui.c_left.setStyleSheet(self.model.style_double_spin_box())
        self.ui.c_right.setStyleSheet(self.model.style_double_spin_box())
        self.ui.checkBox.setStyleSheet(self.model.style_checkbox())
        self.ui.scrollArea.setStyleSheet(self.model.style_scroll_area())
        self.ui.pushButton.setStyleSheet(self.model.style_pushbutton())
        self.ui.pushButton_zoom_in.setStyleSheet(self.model.style_pushbutton())
        self.ui.pushButton_zoom_out.setStyleSheet(self.model.style_pushbutton())
        self.ui.radioButton.setStyleSheet(self.model.style_radio_button())
        self.ui.radioButton_2.setStyleSheet(self.model.style_radio_button())

    def open_image(self, onclick=True):
        if onclick:
            _, media_path, parameter_name = self.model.select_media_source()
            if media_path:
                self.__configuration_view["Media_path"] = media_path
                self.__configuration_view["Parameter_name"] = parameter_name
                self.process_image(media_path, parameter_name)
                path_file = os.path.dirname(os.path.realpath(__file__))
                config_file = path_file + "/cached/cache_config.yaml"
                with open(config_file, "w") as outfile:
                    yaml.dump(self.__configuration_view, outfile, default_flow_style=False)

        else:
            path_file = os.path.dirname(os.path.realpath(__file__))
            config_file = path_file + "/cached/cache_config.yaml"
            if os.path.exists(config_file):
                with open(config_file, "r") as file:
                    self.__configuration_view = yaml.safe_load(file)
                if self.__configuration_view["Media_path"] is not None:
                    self.process_image(self.__configuration_view["Media_path"],
                                       self.__configuration_view["Parameter_name"])

    def process_image(self, media_path, parameter_name):
        self.image = cv2.imread(media_path)
        self.moildev = self.model.connect_to_moildev(parameter_name=parameter_name)
        self.icx = self.moildev.icx
        self.icy = self.moildev.icy
        self.ui.spinBox.setValue(self.icx)
        self.ui.spinBox_2.setValue(self.icy)
        self.change_value_center_x()
        self.show_image_ori()
        self.show_recenter_image(self.image)
        self.panorama_tube()

    def show_image_ori(self):
        image = self.model.marker.point(self.image.copy(), (self.icx, self.icy))
        self.model.show_image_to_label(self.ui.label, image, 400)

    def change_pano_mode(self):
        if self.ui.checkBox.isChecked():
            # this is panorama Car
            self.ui.checkBox.setText("Pano Tube")
            self.ui.label_6.setText("Alpha:")
            self.ui.spinBox_3.setMinimum(0)
            self.ui.spinBox_3.setValue(0)
            self.ui.spinBox_4.setValue(0)
            self.ui.label_7.setText("Beta:")

        else:
            # this is panorama Tube
            self.ui.checkBox.setText("Pano Car")

            self.ui.spinBox_3.blockSignals(True)
            self.ui.spinBox_4.blockSignals(True)
            self.ui.spinBox_3.setMinimum(12)
            self.ui.spinBox_3.setValue(12)
            self.ui.spinBox_4.setValue(110)
            self.ui.spinBox_3.blockSignals(False)
            self.ui.spinBox_4.blockSignals(False)
            self.ui.label_6.setText("Alpha min:")
            self.ui.label_7.setText("Alpha max:")

        self.panorama_tube()

    def panorama_tube(self):
        if self.ui.checkBox.isChecked():
            alpha_min = self.ui.spinBox_3.value()
            alpha_max = self.ui.spinBox_4.value()
            self.pano_image = self.moildev.panorama_car(self.image_rec, 110, alpha_min,
                                                        alpha_max, 0, 1, 0, 1)
        else:
            alpha_min = self.ui.spinBox_3.value()
            alpha_max = self.ui.spinBox_4.value()
            self.pano_image = self.moildev.panorama_tube(self.image_rec, alpha_min, alpha_max)

        self.show_panorama()

    @staticmethod
    def zoom_in(current_size):
        """Increases the current size by 100 and returns the new size.

        Args:
            current_size (int): The current size.

        Returns:
            int: The new size after increasing by 100.
        """
        # If the current size of the image is larger than 6000, no changes made
        if current_size > 6000:
            pass
        # Else, increase the size by 100
        else:
            current_size += 100
        # Return the new size
        return current_size

    @staticmethod
    def zoom_out(current_size):
        """Decreases the `current_size` by 100, unless it's already below 640.

        Args:
            current_size (int): The current size to decrease by 100.

        Returns:
            int: The new size after decreasing by 100, or the original `current_size` if it's already below 640.
        """
        if current_size < 640:
            pass
        else:
            current_size -= 100
        return current_size

    def zoom_image(self, operation):
        """Zooms in or out on the result image.

        Args:
            operation (str): The zoom operation to perform. Must be one of "zoom_in" or "zoom_out".
        """
        if operation == "zoom_in":
            self.__width_image_result = self.zoom_in(self.__width_image_result)
        elif operation == "zoom_out":
            self.__width_image_result = self.zoom_out(self.__width_image_result)
        self.show_panorama()

    def show_panorama(self):
        if self.pano_image is not None:
            image = self.model.cropping_image(self.pano_image, self.ui.c_left.value(), self.ui.c_right.value(),
                                              self.ui.c_top.value(), self.ui.c_btn.value())
            cv2.imwrite("front.jpg", image)
            self.model.show_image_to_label(self.ui.label_3, image, self.__width_image_result)

    def change_value_center_x(self):
        if self.image is not None:
            self.icx = self.ui.spinBox.value()
            alpha, beta = self.moildev.get_alpha_beta(self.icx, self.icy)
            self.image_rec = self.moildev.recenter(self.image, 110, alpha, beta)
            self.show_recenter_image(self.image_rec)
            self.show_image_ori()
            self.panorama_tube()

    def change_value_center_y(self):
        if self.image is not None:
            self.icy = self.ui.spinBox_2.value()
            alpha, beta = self.moildev.get_alpha_beta(self.icx, self.icy)
            self.image_rec = self.moildev.recenter(self.image, 110, alpha, beta)
            self.show_recenter_image(self.image_rec)
            self.show_image_ori()
            self.panorama_tube()

    def show_recenter_image(self, image):
        image = self.model.marker.crosshair(image.copy(), (self.moildev.icx, self.moildev.icy))
        self.model.show_image_to_label(self.ui.label_2, image, 400)


class SurroundViewThreeD(PluginInterface):
    def __init__(self):
        super().__init__()
        self.widget = None

    def set_plugin_widget(self, model):
        self.widget = Controller(model)
        return self.widget

    def set_icon_apps(self):
        return "./icon_car.png"

    def change_stylesheet(self):
        self.widget.change_stylesheet()
