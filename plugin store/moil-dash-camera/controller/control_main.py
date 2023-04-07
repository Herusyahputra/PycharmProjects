import cv2
import numpy as np
import time
from PyQt6.QtWidgets import QWidget
from PyQt6 import QtCore, QtWidgets, QtGui
from .control_icon_ui import ControlIconInUI
from ..models.model_main import Model
from ..views.ui_main import Ui_Form


class Controller(QWidget):
    def __init__(self, model):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.model_main = Model()
        self.model = model

        self.image = None
        self.feature_mode_option = ["setting", "home", "panorama_view", "left_window", "right_window",
                                    "driver_view", "second_driver_view", "original_view", ]

        self.ui.stackedWidget.setCurrentIndex(3)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.create_panorama_car)

        # init zoom view
        self.size = self.width() - 20
        self.zoom_anypoint_2 = self.width() - 20
        self.zoom_x_panorama = self.width() - 20
        self.resize_result_image()
        self.set_stylesheet()
        ControlIconInUI(self)

        self.connect_button()

    def set_stylesheet(self):
        self.setStyleSheet(self.model.style_label())
        self.setStyleSheet(self.model.style_pushbutton())

    def connect_button(self):
        self.ui.btn_source_config_dash.clicked.connect(self.onclick_select_media)
        self.ui.btn_parameter_form_dash.clicked.connect(self.onclick_modify_camera_parameter)
        self.ui.btn_change_camera_type_dash.clicked.connect(self.onclick_camera_type)

        self.ui.btn_home_dash.clicked.connect(self.onclick_home_button)
        self.ui.btn_panorama_view_dash.clicked.connect(self.onclick_panorama_view)
        self.ui.btn_left_window_dash.clicked.connect(self.onclick_left_window_view)
        self.ui.btn_driver_view_dash.clicked.connect(self.onclick_driver_view)
        self.ui.btn_second_driver_view_dash.clicked.connect(self.onclick_second_driver_view)
        self.ui.btn_right_window_dash.clicked.connect(self.onclick_right_window_view)
        self.ui.btn_original_view_dash.clicked.connect(self.onclick_original_view)

        self.ui.lbl_panorama_image_dash.mousePressEvent = self.onclick_lbl_panorama_image
        self.ui.label_left_window_dash.mousePressEvent = self.onclick_lbl_left_dash
        self.ui.label_right_window_dash.mousePressEvent = self.onclick_lbl_right_dash
        self.ui.label_driver_view_dash.mousePressEvent = self.onclick_lbl_steering_dash
        self.ui.label_second_driver_view_dash.mousePressEvent = self.onclick_lbl_original_dash
        self.ui.lbl_image_single_view_dash.mousePressEvent = self.onclick_lbl_image_single_view

        self.ui.spinBox_alpha_max_dash.valueChanged.connect(self.create_panorama_car)
        self.ui.doubleSpinBox_alpha_dash.valueChanged.connect(self.create_panorama_car)
        self.ui.doubleSpinBox_beta_dash.valueChanged.connect(self.create_panorama_car)
        self.ui.doubleSpinBox_crop_left_dash.valueChanged.connect(self.create_panorama_car)
        self.ui.doubleSpinBox_crop_right_dash.valueChanged.connect(self.create_panorama_car)
        self.ui.doubleSpinBox_crop_top_dash.valueChanged.connect(self.create_panorama_car)

        self.ui.spinBox_alpha_anypoint_view_dash.valueChanged.connect(self.create_driver_View)
        self.ui.spinBox_beta_anypoint_view_dash.valueChanged.connect(self.create_driver_View)
        self.ui.spinBox_roll_anypoint_view_dash.valueChanged.connect(self.create_driver_View)
        self.ui.spinBox_zoom_anypoint_view_dash.valueChanged.connect(self.create_driver_View)

        self.ui.spinBox_alpha_anypoint_view_dash.valueChanged.connect(self.create_second_driver_View)
        self.ui.spinBox_beta_anypoint_view_dash.valueChanged.connect(self.create_second_driver_View)
        self.ui.spinBox_roll_anypoint_view_dash.valueChanged.connect(self.create_second_driver_View)
        self.ui.spinBox_zoom_anypoint_view_dash.valueChanged.connect(self.create_second_driver_View)

        self.ui.spinBox_alpha_anypoint_view_dash.valueChanged.connect(self.create_left_window)
        self.ui.spinBox_beta_anypoint_view_dash.valueChanged.connect(self.create_left_window)
        self.ui.spinBox_roll_anypoint_view_dash.valueChanged.connect(self.create_left_window)
        self.ui.spinBox_zoom_anypoint_view_dash.valueChanged.connect(self.create_left_window)

        self.ui.spinBox_alpha_anypoint_view_dash.valueChanged.connect(self.create_right_window)
        self.ui.spinBox_beta_anypoint_view_dash.valueChanged.connect(self.create_right_window)
        self.ui.spinBox_roll_anypoint_view_dash.valueChanged.connect(self.create_right_window)
        self.ui.spinBox_zoom_anypoint_view_dash.valueChanged.connect(self.create_right_window)

        self.ui.btn_play_pause_dash.clicked.connect(self.onclick_play_pause_video)
        self.ui.btn_stop_dash.clicked.connect(self.onclick_stop_video)
        self.ui.btn_rewind_dash.clicked.connect(self.onclick_rewind_video)
        self.ui.btn_forward_dash.clicked.connect(self.onclick_forward_video)
        self.ui.slider_video_dash.valueChanged.connect(self.onclick_slider_video)

        self.ui.btn_zoom_in_dash.clicked.connect(self.zoom_in_view)
        self.ui.btn_zoom_out_dash.clicked.connect(self.zoom_out_view)

        # self.ui.btn_record_dash.clicked.connect(self.record_video)
        # self.ui.btn_screenshot_active_image_dash.clicked.connect(self.save_image)

        self.ui.btn_dash_setting_dash.clicked.connect(self.onclick_button_settings)

    def zoom_in_view(self):
        if self.ui.comboBox_setting_select_main_view_dash.currentIndex() == 0:
            if self.size == self.width() - 20:
                pass
            else:
                print("oke")
                self.size += 100

        elif self.ui.comboBox_setting_select_main_view_dash.currentIndex() == 1:
            print("anypoint-2-zoom")
            if self.zoom_anypoint_2 == self.width() - 20:
                pass
            else:
                self.zoom_anypoint_2 += 100

        else:
            print("x-panorama-zoom")
            if self.zoom_x_panorama == self.width() - 20:
                pass
            else:
                self.zoom_x_panorama += 100

        self.create_panorama_car()

    def zoom_out_view(self):
        if self.ui.comboBox_setting_select_main_view_dash.currentIndex() == 0:
            if self.size == 400:
                pass
            else:
                self.size -= 100

        elif self.ui.comboBox_setting_select_main_view_dash.currentIndex() == 1:
            if self.zoom_anypoint_2 < 400:
                pass
            else:
                self.zoom_anypoint_2 -= 100

        else:
            if self.zoom_x_panorama < 400:
                pass
            else:
                self.zoom_x_panorama -= 100

        self.create_panorama_car()

    def resize_result_image(self):
        if self.width() % 4 == 0:
            self.size = round(self.width() - 20)
            self.zoom_anypoint_2 = self.width() - 20
            self.zoom_x_panorama = self.width() - 20
        else:
            self.size = self.size
            self.zoom_anypoint_2 = self.zoom_anypoint_2
            self.zoom_x_panorama = self.zoom_x_panorama

    def onclick_modify_camera_parameter(self):
        self.model.form_camera_parameter()

    def onclick_camera_type(self):
        self.model.select_parameter_name()

    def onclick_lbl_original_dash(self, event):
        self.onclick_original_view()

    def onclick_lbl_panorama_image(self):
        self.onclick_panorama_view()

    def onclick_lbl_left_dash(self, event):
        self.onclick_left_window_view()

    def onclick_lbl_right_dash(self, event):
        self.onclick_right_window_view()

    def onclick_lbl_steering_dash(self, event):
        self.onclick_driver_view()

    def onclick_lbl_image_single_view(self, event):
        self.set_unchecked_btn()
        self.feature_mode = self.feature_mode_option[1]
        self.ui.btn_home_dash.setChecked(True)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.showing_image_to_ui()

    def onclick_select_media(self):
        cam_type, media_source, params_name = self.model.select_media_source()
        if cam_type:
            if params_name:
                print("Media Source")
                self.moildev = self.model.connect_to_moildev(parameter_name=params_name)
                self.image = cv2.imread(media_source)
                self.image_copy = self.image.copy()
                self.show_properties_camera()
                self.create_panorama_car()
                self.create_driver_View()
                self.create_second_driver_View()
                self.create_left_window()
                self.create_right_window()

    def onclick_home_button(self):
        if self.image is None:
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.btn_home_dash.setChecked(False)
            self.setWindowTitle("Moil Dash Camera")

        else:
            self.ui.stackedWidget.setCurrentIndex(0)
            self.set_unchecked_btn()
            self.feature_mode = self.feature_mode_option[1]
            self.ui.btn_dash_setting_dash.setChecked(False)
            self.ui.btn_home_dash.setChecked(True)
            self.showing_image_to_ui()
            self.onclick_button_settings()

    def onclick_panorama_view(self):
        if self.image is None:
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.btn_home_dash.setChecked(False)
        else:
            self.set_unchecked_btn()
            self.ui.btn_panorama_view_dash.setChecked(True)
            self.ui.stackedWidget.setCurrentIndex(1)
            self.feature_mode = self.feature_mode_option[2]
            self.create_panorama_car()
            self.setWindowTitle("Panorama View - Moil Dash Camera")

    def onclick_left_window_view(self):
        if self.image is None:
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.btn_home_dash.setChecked(False)
        else:
            self.set_unchecked_btn()
            self.ui.btn_left_window_dash.setChecked(True)
            self.ui.stackedWidget.setCurrentIndex(1)
            self.feature_mode = self.feature_mode_option[3]
            self.create_left_window()
            self.setWindowTitle("Left Window View - Moil Dash Camera")

    def onclick_right_window_view(self):
        if self.image is None:
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.btn_home_dash.setChecked(False)
        else:
            self.set_unchecked_btn()
            self.ui.btn_right_window_dash.setChecked(True)
            self.ui.stackedWidget.setCurrentIndex(1)
            self.feature_mode = self.feature_mode_option[4]
            self.create_right_window()
            self.setWindowTitle("Right Window View - Moil Dash Camera")

    def onclick_driver_view(self):
        if self.image is None:
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.btn_home_dash.setChecked(False)
        else:
            self.set_unchecked_btn()
            self.ui.btn_driver_view_dash.setChecked(True)
            self.ui.stackedWidget.setCurrentIndex(1)
            self.feature_mode = self.feature_mode_option[5]
            self.create_driver_View()
            self.setWindowTitle("Driver View - Moil Dash Camera")

    def onclick_second_driver_view(self):
        if self.image is None:
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.btn_home_dash.setChecked(False)
        else:
            self.set_unchecked_btn()
            self.ui.btn_second_driver_view_dash.setChecked(True)
            self.ui.stackedWidget.setCurrentIndex(1)
            self.feature_mode = self.feature_mode_option[6]
            self.create_second_driver_View()
            self.setWindowTitle("Second Driver View - Moil Dash Camera")

    def onclick_original_view(self):
        if self.image is None:
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.btn_home_dash.setChecked(False)
        else:
            self.set_unchecked_btn()
            self.ui.btn_original_view_dash.setChecked(True)
            self.ui.stackedWidget.setCurrentIndex(1)
            self.feature_mode = self.feature_mode_option[7]
            self.showing_image_to_ui()
            self.setWindowTitle("Original View - Moil Dash Camera")

    def onclick_button_settings(self):
        if self.ui.btn_dash_setting_dash.isChecked():
            self.set_unchecked_btn()
            self.ui.btn_dash_setting_dash.setChecked(True)
            self.ui.stackedWidget.setCurrentIndex(2)
            self.feature_mode = self.feature_mode_option[0]
            self.setWindowTitle("setting - Moil Dash Camera")

        else:
            self.onclick_close_setting_mode()
        # self.showing_image_to_ui()

    def onclick_close_setting_mode(self):
        if self.image is None:
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.btn_dash_setting_dash.setChecked(False)
            self.setWindowTitle("Moil Dash Camera")

        else:
            self.ui.stackedWidget.setCurrentIndex(0)
            self.feature_mode = self.feature_mode_option[1]
            self.ui.btn_dash_setting_dash.setChecked(False)
            self.ui.btn_home_dash.setChecked(True)
            self.setWindowTitle("Home - Moil Dash Camera")
            self.showing_image_to_ui()

    def set_unchecked_btn(self):
        self.ui.btn_home_dash.setChecked(False)
        self.ui.btn_panorama_view_dash.setChecked(False)
        self.ui.btn_second_driver_view_dash.setChecked(False)
        self.ui.btn_driver_view_dash.setChecked(False)
        self.ui.btn_left_window_dash.setChecked(False)
        self.ui.btn_right_window_dash.setChecked(False)
        self.ui.btn_original_view_dash.setChecked(False)
        self.ui.btn_dash_setting_dash.setChecked(False)

    # def record_video(self):
    #     self.ui.btn_record_dash.setChecked(False)
    #     self

    def update_to_user_interface(self):
        if self.model.image is None:
            print("No Source Media")
            self.timer.stop()
            self.feature_mode = self.feature_mode_option[0]
            self.onclick_select_media()
            self.ui.btn_play_pause_dash.setChecked(False)

        else:
            self.model.next_frame_process()
            self.showing_image_to_ui()

    def create_panorama_car(self):
        start = time.time()
        self.timer.start()
        alpha_max = self.ui.spinBox_alpha_max_dash.value()
        alpha = self.ui.doubleSpinBox_alpha_dash.value()
        beta = self.ui.doubleSpinBox_beta_dash.value()
        left = self.ui.doubleSpinBox_crop_left_dash.value()
        right = self.ui.doubleSpinBox_crop_right_dash.value()
        top = self.ui.doubleSpinBox_crop_top_dash.value()
        bottom = self.ui.doubleSpinBox_crop_bottom_dash.value()

        self.remap = self.moildev.panorama_car(self.image, alpha_max, alpha, beta, left, right, top, bottom)
        print("test video here")
        self.model.show_image_to_label(self.ui.lbl_image_dash_main_dash, self.remap, 1040)
        self.model.show_image_to_label(self.ui.lbl_panorama_image_dash, self.remap, 1040)
        self.model.show_image_to_label(self.ui.lbl_image_single_view_dash, self.remap, 1040)

        print("Processing endless loop")
        end = time.time()
        second = end - start
        print("image Mode, time:{}".format(second))

    def create_driver_View(self):
        if self.ui.comboBox_select_view_dash.currentIndex() == 2:
            alpha = self.ui.spinBox_alpha_anypoint_view_dash.value()
            beta = self.ui.spinBox_beta_anypoint_view_dash.value()
            roll = self.ui.spinBox_roll_anypoint_view_dash.value()
            zoom = self.ui.spinBox_zoom_anypoint_view_dash.value()

            # self.map_x , self.map_y = self.moildev.maps_anypoint_mode2(20, -45, 0, 4)
            self.map_x, self.map_y = self.moildev.maps_anypoint_mode2(alpha, beta, roll, zoom)
            self.remap = self.model.remap_image(self.image, self.map_x, self.map_y)
            self.model.show_image_to_label(self.ui.lbl_image_anypoint_view_dash, self.remap, 240)
            self.model.show_image_to_label(self.ui.label_driver_view_dash, self.remap, 240)
            self.model.show_image_to_label(self.ui.lbl_image_single_view_dash, self.remap, 1040)

    def create_second_driver_View(self):
        if self.ui.comboBox_select_view_dash.currentIndex() == 3:
            alpha = self.ui.spinBox_alpha_anypoint_view_dash.value()
            beta = self.ui.spinBox_beta_anypoint_view_dash.value()
            roll = self.ui.spinBox_roll_anypoint_view_dash.value()
            zoom = self.ui.spinBox_zoom_anypoint_view_dash.value()

            # self.map_x , self.map_y = self.moildev.maps_anypoint_mode2(20, 45, 0, 4)
            self.map_x, self.map_y = self.moildev.maps_anypoint_mode2(alpha, beta, roll, zoom)
            self.remap = self.model.remap_image(self.image, self.map_x, self.map_y)
            self.model.show_image_to_label(self.ui.lbl_image_original_dash_dash, self.remap, 240)
            self.model.show_image_to_label(self.ui.label_second_driver_view_dash, self.remap, 240)
            self.model.show_image_to_label(self.ui.lbl_image_single_view_dash, self.remap, 1040)

    def create_left_window(self):
        self.map_x, self.map_y = self.moildev.maps_anypoint_mode2(0, -60, 0, 4)
        self.remap = self.model.remap_image(self.image, self.map_x, self.map_y)
        self.model.show_image_to_label(self.ui.label_left_window_dash, self.remap, 240)
        self.model.show_image_to_label(self.ui.lbl_image_single_view_dash, self.remap, 1040)

    def create_right_window(self):
        self.map_x, self.map_y = self.moildev.maps_anypoint_mode2(0, 60, 0, 4)
        self.remap= self.model.remap_image(self.image, self.map_x, self.map_y)
        self.model.show_image_to_label(self.ui.label_right_window_dash, self.remap, 240)
        self.model.show_image_to_label(self.ui.lbl_image_single_view_dash, self.remap, 1040)

    def showing_image_to_ui(self):
        self.model.show_image_to_label(self.ui.lbl_image_single_view_dash, self.image, 1040)



    def onclick_play_pause_video(self):
        print("test video player")
        if self.ui.btn_play_pause_dash.isChecked():
            self.timer.start()

        else:
            self.timer.stop()

    def onclick_stop_video(self):
        self.ui.btn_play_pause_dash.isChecked(False)
        self.model_main.stop_video()
        self.set_value_slider_video()
        self.timer.stop()
        self.update_to_user_interface()

    def onclick_rewind_video(self):
        self.model_main.rewind_video()
        self.set_value_slider_video()
        self.update_to_user_interface()

    def onclick_forward_video(self):
        self.model_main.forward_video()
        self.set_value_slider_video()
        self.update_to_user_interface()

    def onclick_slider_video(self, value):
        value_max = self.ui.slider_video_dash.maximum()
        self.model.slider_controller(value, value_max)

    def set_value_slider_video(self):
        value = self.ui.slider_video_dash.maximum()
        if not self.model.frame_count <= 0:
            current_position = self.model_main.get_value_slider_video(value)
            self.ui.slider_video_dash.blockSignals(True)
            self.ui.slider_video_dash.setValue(current_position)
            self.ui.slider_video_dash.blockSignals(False)

    def set_time_video(self):
        total_minute = self.model_main.total_minute
        total_second = self.model_main.total_second
        current_minute = self.model_main.current_minute
        current_second = self.model_main.current_second
        self.ui.lbl_current_time.setText("%02d:%02d" % (current_minute, current_second))
        if total_minute <0:
            self.ui.lbl_total_time.setText("--:--")
        else:
            self.ui.lbl_total_time.setText("%02d:%02d" % (total_minute, total_second))

    def show_properties_camera(self):
        self.ui.lbl_info_camera_type_dash.setText(self.moildev.camera_name)
        self.ui.lbl_info_source_dash.setText(self.model_main.media_source_type)
        self.ui.lbl_info_width_image_dash.setText(str(self.moildev.image_width))
        self.ui.lbl_info_height_image_dash.setText(str(self.moildev.image_height))
        self.ui.lbl_info_icx_dash.setText(str(self.moildev.icx))
        self.ui.lbl_info_icy_dash.setText(str(self.moildev.icy))

    @staticmethod
    def boundary_fov(image: np.ndarray, moildev, fov: int = 90,
                     color: tuple = (255, 255, 0)) -> np.ndarray:
        icx = moildev.icx
        icy = moildev.icy
        center = (icx, icy)

        boundary_radius = int(moildev.get_rho_from_alpha(fov))
        thickness = int(5)

        cv2.circle(image, center, radius=boundary_radius, color=color, thickness=thickness)

        return image

    def blockSignals(self):
        self.ui.spinBox_alpha_max_dash.blockSignals(True)
        self.ui.doubleSpinBox_alpha_dash.blockSignals(True)
        self.ui.doubleSpinBox_beta_dash.blockSignals(True)
        self.ui.doubleSpinBox_crop_left_dash.blockSignals(True)
        self.ui.doubleSpinBox_crop_right_dash.blockSignals(True)
        self.ui.doubleSpinBox_crop_top_dash.blockSignals(True)
        self.ui.doubleSpinBox_crop_bottom_dash.blockSignals(True)

        self.ui.spinBox_alpha_anypoint_view_dash.blockSignals(True)
        self.ui.spinBox_beta_anypoint_view_dash.blockSignals(True)
        self.ui.spinBox_roll_anypoint_view_dash.blockSignals(True)
        self.ui.spinBox_zoom_anypoint_view_dash.blockSignals(True)
        self.ui.spinBox_rotate_image_original_dash.blockSignals(True)

        self.ui.spinBox_brighness_dash.blockSignals(True)
        self.ui.spinBox_contrast_dash.blockSignals(True)

    def unblockSignals(self):
        self.ui.spinBox_alpha_max_dash.blockSignals(False)
        self.ui.doubleSpinBox_alpha_dash.blockSignals(False)
        self.ui.doubleSpinBox_beta_dash.blockSignals(False)
        self.ui.doubleSpinBox_crop_left_dash.blockSignals(False)
        self.ui.doubleSpinBox_crop_right_dash.blockSignals(False)
        self.ui.doubleSpinBox_crop_top_dash.blockSignals(False)
        self.ui.doubleSpinBox_crop_bottom_dash.blockSignals(False)

        self.ui.spinBox_alpha_anypoint_view_dash.blockSignals(False)
        self.ui.spinBox_beta_anypoint_view_dash.blockSignals(False)
        self.ui.spinBox_roll_anypoint_view_dash.blockSignals(False)
        self.ui.spinBox_zoom_anypoint_view_dash.blockSignals(False)
        self.ui.spinBox_rotate_image_original_dash.blockSignals(False)

        self.ui.spinBox_brighness_dash.blockSignals(False)
        self.ui.spinBox_contrast_dash.blockSignals(False)



