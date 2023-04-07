import os
import shutil

import numpy as np
from PyQt6 import QtCore, QtGui

from PyQt6.QtWidgets import QWidget, QMessageBox, QDialog, QLabel
from ..view.main_ui import Ui_Form
from ..model.model import ModelPlugin
from .icon_source import IconSource
from .setting_icon_apps import SetIconsUIDashCamera
from .set_theme_ui import SetThemeStylesheet
from .create_config_fle import ConfigFile
from .control_config_dash import ControlConfigDash
from .control_config_birds_view import ControlConfigBirdsView
from .show_image_original import ShowOriginalImageBirdView


class Controller(QWidget):
    def __init__(self, model):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.model = model
        self.add_additional_label()
        self.icon = IconSource()

        self.image_dash_camera_result = None
        self.image_result_birds_view = None
        self.image_result_overlap_view = None
        self.image_anypoint_dash = None
        self.list_original_image = [None] * 4

        self.show_original = ShowOriginalImageBirdView(self.model, self.list_original_image)

        self.set_icon = SetIconsUIDashCamera(self)
        self.change_style_ui = SetThemeStylesheet(self.ui, self.model)
        self.config = ConfigFile(self.ui)
        self.control_config_dash = ControlConfigDash(self.config.cached_file, self.ui)
        self.control_config_birds_view = ControlConfigBirdsView(self.config.cached_file, self.ui)
        self.change_stylesheets()
        self.model_plugin = ModelPlugin(model)
        self.model_plugin.set_mode_calibration(self.ui.comboBox.currentText())
        self.control_view_condition_car_moving()
        self.change_view_config_page()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(round(1000 / 24))
        self.timer.timeout.connect(self.model_plugin.next_frame_process)

        self.connect_event()

    def connect_event(self):
        # connect signal from emit_event
        self.model_plugin.original_image_dash_cam.connect(self.show_image_original)
        self.model_plugin.result_dash_image.connect(self.update_result_dash_image)
        self.model_plugin.result_anypoint_dash_cam.connect(self.show_result_anypoint_image)
        self.model_plugin.dash_camera_info.connect(self.show_dash_camera_info)
        self.model_plugin.signal_video_duration.connect(self.set_time_video)
        self.model_plugin.signal_video_slider_position.connect(self.set_value_slider_video)
        self.model_plugin.signal_show_config_to_ui.connect(self.show_info_dash_image_front)

        # begin signal birds view
        self.model_plugin.original_image_bird_view.connect(self.show_original_image_birds_view)
        self.model_plugin.result_bird_view.connect(self.show_result_image_birds_view)
        self.model_plugin.result_bird_view_overlap.connect(self.show_result_image_birds_view_overlap)

        # connect signal event from ui
        self.ui.btn_load_config.clicked.connect(self.onclick_load_config_project)
        self.ui.btn_save_config.clicked.connect(self.save_config_project)
        self.ui.btn_open_source.clicked.connect(self.open_media_source)
        self.ui.btn_parameter_form.clicked.connect(self.onclick_modify_camera_parameter)
        self.ui.radioButton_dash_front_view.toggled.connect(self.change_dash_image_result)
        self.ui.radioButton_dash_driver_view.toggled.connect(self.change_dash_image_result)
        self.ui.radioButton_low_speed.toggled.connect(self.control_view_condition_car_moving)
        self.ui.radioButton_high_speed.toggled.connect(self.control_view_condition_car_moving)
        self.ui.comboBox.activated.connect(self.control_setting_view)

        self.ui.btn_compare_panorama_anypoint.clicked.connect(self.onclick_compare_panorama_anypoint)
        self.ui.btn_close_config.clicked.connect(self.back_to_main_view)

        self.ui.btn_setting_configuration.clicked.connect(self.change_view_config_page)

        self.ui.btn_zoom_in.clicked.connect(lambda: self.zoom_image("zoom_in"))
        self.ui.btn_zoom_out.clicked.connect(lambda: self.zoom_image("zoom_out"))

        self.ui.spinBox_rotate_image_original.valueChanged.connect(self.rotate_original_image)

        self.ui.checkBox_show_fov.toggled.connect(self.show_fov_to_image_original_bird_view)
        self.ui.pushButton_show_original_image_bird_view.clicked.connect(self.onclick_open_original_image_bird_view)

        # control birds view
        self.ui.spinBox_val_icx_image_1.valueChanged.connect(lambda: self.change_anypoint_birds(1))
        self.ui.spinBox_val_icy_image_1.valueChanged.connect(lambda: self.change_anypoint_birds(1))
        self.ui.doubleSpinBox_val_zoom_image_1.valueChanged.connect(lambda: self.change_anypoint_birds(1))
        self.ui.doubleSpinBox_val_rotate_image_1.valueChanged.connect(lambda: self.onclick_change_rotate(1))
        self.ui.spinBox_val_coordinate_x_image_1.valueChanged.connect(lambda: self.change_shift_properties_birds(1))
        self.ui.spinBox_val_coordinate_y_image_1.valueChanged.connect(lambda: self.change_shift_properties_birds(1))
        self.ui.spinBox_val_crop_top_image_1.valueChanged.connect(lambda: self.change_properties_crop_birds(1))
        self.ui.spinBox_val_crop_bottom_image_1.valueChanged.connect(lambda: self.change_properties_crop_birds(1))
        self.ui.spinBox_val_crop_left_image_1.valueChanged.connect(lambda: self.change_properties_crop_birds(1))
        self.ui.spinBox_val_crop_right_image_1.valueChanged.connect(lambda: self.change_properties_crop_birds(1))

        self.ui.spinBox_val_icx_image_2.valueChanged.connect(lambda: self.change_anypoint_birds(2))
        self.ui.spinBox_val_icy_image_2.valueChanged.connect(lambda: self.change_anypoint_birds(2))
        self.ui.doubleSpinBox_val_zoom_image_2.valueChanged.connect(lambda: self.change_anypoint_birds(2))
        self.ui.doubleSpinBox_val_rotate_image_2.valueChanged.connect(lambda: self.onclick_change_rotate(2))
        self.ui.spinBox_val_coordinate_x_image_2.valueChanged.connect(lambda: self.change_shift_properties_birds(2))
        self.ui.spinBox_val_coordinate_y_image_2.valueChanged.connect(lambda: self.change_shift_properties_birds(2))
        self.ui.spinBox_val_crop_top_image_2.valueChanged.connect(lambda: self.change_properties_crop_birds(2))
        self.ui.spinBox_val_crop_bottom_image_2.valueChanged.connect(lambda: self.change_properties_crop_birds(2))
        self.ui.spinBox_val_crop_left_image_2.valueChanged.connect(lambda: self.change_properties_crop_birds(2))
        self.ui.spinBox_val_crop_right_image_2.valueChanged.connect(lambda: self.change_properties_crop_birds(2))

        self.ui.spinBox_val_icx_image_3.valueChanged.connect(lambda: self.change_anypoint_birds(3))
        self.ui.spinBox_val_icy_image_3.valueChanged.connect(lambda: self.change_anypoint_birds(3))
        self.ui.doubleSpinBox_val_zoom_image_3.valueChanged.connect(lambda: self.change_anypoint_birds(3))
        self.ui.doubleSpinBox_val_rotate_image_3.valueChanged.connect(lambda: self.onclick_change_rotate(3))
        self.ui.spinBox_val_coordinate_x_image_3.valueChanged.connect(lambda: self.change_shift_properties_birds(3))
        self.ui.spinBox_val_coordinate_y_image_3.valueChanged.connect(lambda: self.change_shift_properties_birds(3))
        self.ui.spinBox_val_crop_top_image_3.valueChanged.connect(lambda: self.change_properties_crop_birds(3))
        self.ui.spinBox_val_crop_bottom_image_3.valueChanged.connect(lambda: self.change_properties_crop_birds(3))
        self.ui.spinBox_val_crop_left_image_3.valueChanged.connect(lambda: self.change_properties_crop_birds(3))
        self.ui.spinBox_val_crop_right_image_3.valueChanged.connect(lambda: self.change_properties_crop_birds(3))

        self.ui.spinBox_val_icx_image_4.valueChanged.connect(lambda: self.change_anypoint_birds(4))
        self.ui.spinBox_val_icy_image_4.valueChanged.connect(lambda: self.change_anypoint_birds(4))
        self.ui.doubleSpinBox_val_zoom_image_4.valueChanged.connect(lambda: self.change_anypoint_birds(4))
        self.ui.doubleSpinBox_val_rotate_image_4.valueChanged.connect(lambda: self.onclick_change_rotate(4))
        self.ui.spinBox_val_coordinate_x_image_4.valueChanged.connect(lambda: self.change_shift_properties_birds(4))
        self.ui.spinBox_val_coordinate_y_image_4.valueChanged.connect(lambda: self.change_shift_properties_birds(4))
        self.ui.spinBox_val_crop_top_image_4.valueChanged.connect(lambda: self.change_properties_crop_birds(4))
        self.ui.spinBox_val_crop_bottom_image_4.valueChanged.connect(lambda: self.change_properties_crop_birds(4))
        self.ui.spinBox_val_crop_left_image_4.valueChanged.connect(lambda: self.change_properties_crop_birds(4))
        self.ui.spinBox_val_crop_right_image_4.valueChanged.connect(lambda: self.change_properties_crop_birds(4))

        self.ui.radioButton_horizontal_blend.toggled.connect(self.onclick_change_gradient_mode)
        self.ui.radioButton_vertical_blend.toggled.connect(self.onclick_change_gradient_mode)
        self.ui.radioButton_overlap_blend.toggled.connect(self.onclick_change_gradient_mode)
        self.ui.radioButton_horizontal_diagonal.toggled.connect(self.onclick_change_gradient_mode)

        # control view every conditional change
        self.ui.btn_forward.clicked.connect(self.onclick_btn_forward)
        self.ui.btn_turn_left.clicked.connect(self.onclick_btn_turn_left)
        self.ui.btn_turn_right.clicked.connect(self.onclick_btn_turn_right)
        self.ui.btn_reverse.clicked.connect(self.onclick_btn_reverse)
        self.ui.btn_dash_cam_front.clicked.connect(self.onclick_btn_dash_cam_front)
        self.ui.btn_dash_cam_driver.clicked.connect(self.onclick_btn_dash_cam_driver)
        self.ui.btn_driver.clicked.connect(self.onclick_btn_driver)
        self.ui.btn_second_driver.clicked.connect(self.onclick_btn_second_driver)

        # control video here
        self.ui.btn_play_pause.clicked.connect(self.onclick_play_pause_video)
        self.ui.btn_stop.clicked.connect(self.onclick_stop_video)
        self.ui.btn_backward_5_second.clicked.connect(self.onclick_rewind_video)
        self.ui.btn_forward_5_second.clicked.connect(self.onclick_forward_video)
        self.ui.slider_video.valueChanged.connect(self.onclick_slider_video)

        # properties dash camera
        self.ui.spinBox_alpha_max.valueChanged.connect(self.change_dash_properties)
        self.ui.spinBox_alpha_dash.valueChanged.connect(self.change_dash_properties)
        self.ui.spinBox_beta_dash.valueChanged.connect(self.change_dash_properties)

        # properties crop dash camera
        self.ui.doubleSpinBox_crop_left.valueChanged.connect(self.change_crop_dash_image)
        self.ui.doubleSpinBox_crop_right.valueChanged.connect(self.change_crop_dash_image)
        self.ui.doubleSpinBox_crop_top.valueChanged.connect(self.change_crop_dash_image)
        self.ui.doubleSpinBox_crop_bottom.valueChanged.connect(self.change_crop_dash_image)

        # properties anypoint camera
        self.ui.spinBox_alpha_anypoint_view.valueChanged.connect(self.change_anypoint_properties)
        self.ui.spinBox_beta_anypoint_view.valueChanged.connect(self.change_anypoint_properties)
        self.ui.doubleSpinBox_roll_anypoint_view.valueChanged.connect(self.change_anypoint_properties)
        self.ui.spinBox_zoom_anypoint_view.valueChanged.connect(self.change_anypoint_properties)
        self.ui.spinBox_rotate_image_original.valueChanged.connect(self.change_rotate_dash_camera)

        self.ui.comboBox_select_view.activated.connect(self.change_anypoint_image_result)

    def onclick_open_original_image_bird_view(self):
        self.show_original = ShowOriginalImageBirdView(self.model, self.list_original_image)
        self.show_original.show()
        self.show_original.showMaximized()
        self.show_original.raise_()
        print("open original")

    def add_additional_label(self):
        self.label_add_configuration = QLabel(self.ui.scrollArea_2)
        self.label_add_configuration.setStyleSheet("background-color: transparent;"
                                                   "color: rgb(200,80,50);"
                                                   "font-size: 24px;")
        self.label_add_configuration.setGeometry(25, 50, 500, 30)

        self.label_add_condition_high_speed = QLabel(self.ui.label_27)
        self.label_add_condition_high_speed.setStyleSheet("background-color: transparent;"
                                                          "color: rgb(200,80,50);"
                                                          "font-size: 24px bold;")
        self.label_add_condition_high_speed.setGeometry(25, 25, 500, 60)

        self.label_add_condition_low_speed = QLabel(self.ui.scrollArea_3)
        self.label_add_condition_low_speed.setStyleSheet("background-color: transparent;"
                                                         "color: rgb(200,80,50);"
                                                         "font-size: 24px bold;")
        self.label_add_condition_low_speed.setGeometry(25, 50, 500, 60)

    def show_fov_to_image_original_bird_view(self):
        if self.ui.checkBox_show_fov.isChecked():
            self.model_plugin.draw_fov_in_original_image(True)
        else:
            self.model_plugin.draw_fov_in_original_image(False)

    def open_media_source(self):
        self.ui.btn_play_pause.setChecked(False)
        self.onclick_play_pause_video()
        if self.ui.comboBox.currentText() == "Dash camera":
            cam_type, source_media, parameter_name = self.model.select_media_source()
            if source_media is not None:
                self.model_plugin.add_image_path_to_config_file(source_media, parameter_name)
                self.model_plugin.process_source_image(new_parameter=True)
                self.control_video_controller()
                self.showMaximized()

        else:
            # source_media = ["/home/anto/github/moilapp_new/example_source/videos/image_birds/front.jpg",
            #                 "/home/anto/github/moilapp_new/example_source/videos/image_birds/left.jpg",
            #                 "/home/anto/github/moilapp_new/example_source/videos/image_birds/right.jpg",
            #                 "/home/anto/github/moilapp_new/example_source/videos/image_birds/rear.jpg"]

            source_media = ["/home/heru-demo/PycharmProjects/moilapp/example_source/videos/video_3.avi",
                            "/home/heru-demo/PycharmProjects/moilapp/example_source/videos/video_2.avi",
                            "/home/heru-demo/PycharmProjects/moilapp/example_source/videos/video_1.avi",
                            "/home/heru-demo/PycharmProjects/moilapp/example_source/videos/video_4.avi"]

            # parameter_name = ["entaniya_vr220_7",
            #                   "entaniya_vr220_8",
            #                   "entaniya_vr220_11",
            #                   "entaniya_vr220_12"]

            for i in range(1, 5):
                cam_type, source_media, parameter_name = self.model.select_media_source()
                if source_media is not None:
                    self.model_plugin.add_image_path_to_config_file(source_media[i - 1], parameter_name[i - 1], i)
                    self.model_plugin.process_source_image(i, new_parameter=True)
                    self.model_plugin.create_bird_view_image()

                else:
                    break

    def save_config_project(self):
        name = self.ui.lineEdit_project_name.text()
        if name == "":
            QMessageBox.warning(None, "Warning", "Project name is empty!")
        else:
            parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            cached_file = parent_dir + "/model/saved_config/" + name + "/"
            if not os.path.isdir(cached_file):
                os.makedirs(os.path.dirname(cached_file))
                self.config.change_project_name(name)

                source_folder = f'{parent_dir}/model/cached/'
                dst_folder = cached_file
                files_to_move = ['map_x_image_dash_driver_view.npy',
                                 'map_y_image_dash_driver_view.npy',
                                 'map_x_image_dash_front_view.npy',
                                 'map_y_image_dash_front_view.npy',
                                 'map_x_image_left_window_view.npy',
                                 'map_y_image_left_window_view.npy',
                                 'map_x_image_second_driver_window_view.npy',
                                 'map_y_image_second_driver_window_view.npy',
                                 'map_x_image_driver_window_view.npy',
                                 'map_y_image_driver_window_view.npy',
                                 'map_x_image_right_window_view.npy',
                                 'map_y_image_right_window_view.npy',
                                 'map_x_image_compare_view.npy',
                                 'map_y_image_compare_view.npy',
                                 'map_x_anypoint_image_1_bird_view.npy',
                                 'map_y_anypoint_image_1_bird_view.npy',
                                 'map_x_anypoint_image_2_bird_view.npy',
                                 'map_y_anypoint_image_2_bird_view.npy',
                                 'map_x_anypoint_image_3_bird_view.npy',
                                 'map_y_anypoint_image_3_bird_view.npy',
                                 'map_x_anypoint_image_4_bird_view.npy',
                                 'map_y_anypoint_image_4_bird_view.npy']

                shutil.move(f'{source_folder}cache_config.yaml', f'{dst_folder}cache_config.yaml')

                for file in files_to_move:
                    source = f'{source_folder}{file}'
                    destination = f'{dst_folder}{file}'
                    shutil.copy(source, destination)

                self.config.set_load_config_file(f'{cached_file}cache_config.yaml')
                self.control_config_dash.set_load_config_file(f'{cached_file}cache_config.yaml')
                self.control_config_birds_view.set_load_config_file(f'{cached_file}cache_config.yaml')
                self.model_plugin.set_load_config_file(f'{cached_file}cache_config.yaml')
                QMessageBox.information(None, "Information", "Successfully save configuration!")

    def onclick_load_config_project(self):
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        path = parent_dir + "/model/saved_config/"
        file_path = self.model.select_file(title="Select Config", dir_path=path, file_filter="*.yaml")
        if file_path:
            self.config.set_load_config_file(file_path)
            self.control_config_dash.set_load_config_file(file_path)
            self.control_config_birds_view.set_load_config_file(file_path)
            self.model_plugin.set_load_config_file(file_path)
            self.model_plugin.process_source_image()
            self.control_video_controller()

    def control_video_controller(self):
        if self.model_plugin.media_source_type == "Image":
            self.ui.frame_video_controller.setEnabled(False)
        else:
            self.ui.frame_video_controller.setEnabled(True)

    def rotate_original_image(self):
        self.control_config_dash.change_rotation_original_image_dash()

    def change_crop_dash_image(self):
        if self.image_dash_camera_result is not None:
            self.control_config_dash.change_properties_crop_image(self.model_plugin.set_dash_image_mode)
            self.model_plugin.create_dash_image()

    def change_dash_properties(self):
        if self.image_dash_camera_result is not None:
            self.control_config_dash.change_properties_dash_image(self.model_plugin.set_dash_image_mode)
            self.model_plugin.create_maps_image_dash_view(self.model_plugin.set_dash_image_mode)
            self.model_plugin.create_dash_image()

    def change_anypoint_properties(self):
        if self.image_dash_camera_result is not None:
            self.control_config_dash.change_properties_anypoint(self.ui.comboBox_select_view.currentText())
            self.model_plugin.create_maps_anypoint_view(self.ui.comboBox_select_view.currentText())
            self.model_plugin.create_anypoint_image()

    def change_rotate_dash_camera(self):
        if self.image_dash_camera_result is not None:
            self.control_config_dash.change_properties_rotate_dash_image()
            self.model_plugin.rotate_original_image()
            self.model_plugin.create_dash_image()
            self.model_plugin.create_anypoint_image()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        if self.image_dash_camera_result is not None or self.image_result_birds_view is not None:
            self.show_result_image_to_ui()

    @classmethod
    def round_to_nearest_100(cls, num):
        return round(num / 20) * 20

    def zoom_image(self, operation):
        if self.image_dash_camera_result is not None:
            OPERATIONS = {"zoom_in": ModelPlugin.zoom_in, "zoom_out": ModelPlugin.zoom_out}
            if operation in OPERATIONS:
                func = OPERATIONS[operation]
                self.model_plugin.width_result_image = func(self.model_plugin.width_result_image)
                self.show_result_image_to_ui()

    def change_anypoint_image_result(self):
        if self.image_dash_camera_result is not None:
            self.model_plugin.set_anypoint_image_mode = self.ui.comboBox_select_view.currentText()
            self.control_config_dash.showing_config_anypoint(self.ui.comboBox_select_view.currentText())
            self.model_plugin.create_anypoint_image()

    def change_dash_image_result(self):
        if self.ui.radioButton_dash_front_view.isChecked():
            view_mode = "Dash_front_view"
        else:
            view_mode = "Dash_driver_view"

        if self.image_dash_camera_result is not None:
            self.model_plugin.set_dash_image_mode = view_mode
            self.model_plugin.create_dash_image()
            self.control_config_dash.showing_config_dash_image(view_mode)

    @QtCore.pyqtSlot(list)
    def show_original_image_birds_view(self, list_image):
        self.list_original_image = list_image
        # print("original")
        # if image[0] is not None:
        #     self.model.show_image_to_label(self.ui.label_28, image[0], self.model_plugin.width_result_image)

    @QtCore.pyqtSlot(object)
    def show_result_image_birds_view(self, image):
        self.image_result_birds_view = image
        self.show_result_image_to_ui()

    @QtCore.pyqtSlot(object)
    def show_result_image_birds_view_overlap(self, image):
        self.image_result_overlap_view = image
        self.show_result_image_to_ui()

    @QtCore.pyqtSlot(object)
    def update_result_dash_image(self, image):
        self.image_dash_camera_result = image
        self.show_result_image_to_ui()

    @QtCore.pyqtSlot(object)
    def show_result_anypoint_image(self, image):
        self.image_anypoint_dash = image
        self.show_result_image_to_ui()

    @QtCore.pyqtSlot(object)
    def show_image_original(self, image):
        self.model.show_image_to_label(self.ui.label_14, image, 320)

    @QtCore.pyqtSlot(bool)
    def show_info_dash_image_front(self, show_info):
        if show_info:
            self.control_config_dash.showing_config_dash_image(self.model_plugin.set_dash_image_mode)
            self.control_config_dash.showing_config_anypoint(self.ui.comboBox_select_view.currentText())

    def show_result_image_to_ui(self):
        if self.ui.btn_setting_configuration.isChecked():
            if self.ui.btn_compare_panorama_anypoint.isChecked():
                width_image_1 = self.round_to_nearest_100(self.ui.scrollArea.width() - 20)
                width_image_2 = self.round_to_nearest_100(self.ui.scrollArea_3.width() - 20)
                self.model.show_image_to_label(self.ui.label_25, self.image_dash_camera_result, width_image_1)
                self.model.show_image_to_label(self.ui.label_26, self.image_anypoint_dash, width_image_2)

            else:
                if self.model_plugin.mode_calibration == "Dash camera":
                    if self.image_anypoint_dash is not None:
                        self.model.show_image_to_label(self.ui.label_20, self.image_anypoint_dash, 320)
                    width = self.round_to_nearest_100(self.ui.scrollArea_2.width() - 20)
                    if self.ui.radioButton_dash_front_view.isChecked():
                        self.label_add_configuration.setText("- Configuration front dash camera")
                        self.model.show_image_to_label(self.ui.label_21, self.image_dash_camera_result, width)

                    else:
                        self.label_add_configuration.setText("- Configuration driver dash camera")
                        self.model.show_image_to_label(self.ui.label_21, self.image_dash_camera_result,
                                                       width, angle=180)

                else:
                    width = self.round_to_nearest_100(self.ui.scrollArea_6.width() - 20)
                    if self.image_result_overlap_view is not None:
                        self.model.show_image_to_label(self.ui.label_28, self.image_result_overlap_view, width)

                    if self.image_result_birds_view is not None:
                        self.model.show_image_to_label(self.ui.label_29, self.image_result_birds_view, width)
        else:
            if self.ui.radioButton_low_speed.isChecked():
                if self.image_result_birds_view is not None:
                    width = self.round_to_nearest_100(self.ui.scrollArea.width() - 20)
                    self.model.show_image_to_label(self.ui.label_25, self.image_result_birds_view, width)

                if self.ui.btn_forward.isChecked():
                    width_image_2 = self.round_to_nearest_100(self.ui.scrollArea_3.width() - 20)
                    self.model.show_image_to_label(self.ui.label_26, self.image_anypoint_dash, width_image_2)
                    self.label_add_condition_low_speed.setText("- Low speed \n- Forward View")

                elif self.ui.btn_turn_left.isChecked():
                    width_image_2 = self.round_to_nearest_100(self.ui.scrollArea_3.width() - 20)
                    self.label_add_condition_low_speed.setText("- Low speed \n- Turn Left View")
                    self.model.show_image_to_label(self.ui.label_26, self.image_anypoint_dash, width_image_2, angle=90)

                elif self.ui.btn_turn_right.isChecked():
                    width_image_2 = self.round_to_nearest_100(self.ui.scrollArea_3.width() - 20)
                    self.label_add_condition_low_speed.setText("- Low speed \n- Turn Right View")
                    self.model.show_image_to_label(self.ui.label_26, self.image_anypoint_dash, width_image_2, angle=-90)

                elif self.ui.btn_reverse.isChecked():
                    width_image_2 = self.round_to_nearest_100(self.ui.scrollArea_3.width() - 20)
                    self.label_add_condition_low_speed.setText("- Low speed \n- Reverse View")
                    self.model.show_image_to_label(self.ui.label_26, self.image_anypoint_dash, width_image_2)

            else:
                if self.ui.btn_dash_cam_front.isChecked():
                    width = self.round_to_nearest_100(self.ui.scrollArea_4.width() - 20)
                    self.label_add_condition_high_speed.setText("- High Speed \n- Forward View")
                    self.model.show_image_to_label(self.ui.label_27, self.image_dash_camera_result, width)

                elif self.ui.btn_dash_cam_driver.isChecked():
                    width = self.round_to_nearest_100(self.ui.scrollArea_4.width() - 20)
                    self.label_add_condition_high_speed.setText("- High Speed \n- Backward View")
                    self.model.show_image_to_label(self.ui.label_27, self.image_dash_camera_result,
                                                   width, angle=180)
                elif self.ui.btn_driver.isChecked():
                    self.label_add_condition_high_speed.setText("- High Speed \n- Driver View")
                    self.model.show_image_to_label(self.ui.label_27, self.image_anypoint_dash, 1000)

                elif self.ui.btn_second_driver.isChecked():
                    self.label_add_condition_high_speed.setText("- High Speed \n- Second Driver View")
                    self.model.show_image_to_label(self.ui.label_27, self.image_anypoint_dash, 1000)

    @QtCore.pyqtSlot(list)
    def show_dash_camera_info(self, info):
        if info[0] is not None:
            self.ui.lineEdit_project_name.setText(info[0])
        self.ui.lbl_info_camera_type.setText(info[1][-18:])
        if isinstance(info[2], int):
            self.ui.lbl_info_source.setText(os.path.basename(str(info[2])))

        else:
            self.ui.lbl_info_source.setText(os.path.basename(info[2][-18:]))

        self.ui.lbl_info_width_image.setText(str(info[3]))
        self.ui.lbl_info_height_image.setText(str(info[4]))
        self.ui.lbl_info_icx.setText(str(info[5]))
        self.ui.lbl_info_icy.setText(str(info[6]))

    def control_view_condition_car_moving(self):
        if self.image_dash_camera_result is not None:
            if self.ui.radioButton_low_speed.isChecked():
                self.ui.scrollArea.setMaximumWidth(640)
                self.ui.scrollArea_3.setMaximumWidth(16777215)
                self.ui.btn_forward.setChecked(True)
                self.ui.btn_forward.show()
                self.ui.btn_turn_left.show()
                self.ui.btn_turn_right.show()
                self.ui.btn_reverse.show()

                self.ui.btn_dash_cam_front.hide()
                self.ui.btn_dash_cam_driver.hide()
                self.ui.btn_driver.hide()
                self.ui.btn_second_driver.hide()
                self.ui.stackedWidget_2.setCurrentIndex(0)
                self.onclick_btn_forward()

            else:
                self.ui.btn_dash_cam_front.setChecked(True)
                self.ui.btn_forward.hide()
                self.ui.btn_turn_left.hide()
                self.ui.btn_turn_right.hide()
                self.ui.btn_reverse.hide()

                self.ui.btn_dash_cam_front.show()
                self.ui.btn_dash_cam_driver.show()
                self.ui.btn_driver.show()
                self.ui.btn_second_driver.show()

                self.ui.stackedWidget_2.setCurrentIndex(1)
                self.onclick_btn_dash_cam_front()

            self.show_result_image_to_ui()

    def set_button_state(self, btn_forward=False, btn_turn_left=False, btn_turn_right=False, btn_reverse=False,
                         btn_dash_cam_front=False, btn_dash_cam_driver=False, btn_driver=False,
                         btn_second_driver=False):
        self.ui.btn_forward.setChecked(btn_forward)
        self.ui.btn_turn_left.setChecked(btn_turn_left)
        self.ui.btn_turn_right.setChecked(btn_turn_right)
        self.ui.btn_reverse.setChecked(btn_reverse)
        self.ui.btn_dash_cam_front.setChecked(btn_dash_cam_front)
        self.ui.btn_dash_cam_driver.setChecked(btn_dash_cam_driver)
        self.ui.btn_driver.setChecked(btn_driver)
        self.ui.btn_second_driver.setChecked(btn_second_driver)

    def onclick_btn_forward(self):
        self.set_button_state(btn_forward=True)
        self.model_plugin.create_maps_front_view_anypoint()
        if self.image_dash_camera_result is not None:
            self.model_plugin.create_image_front_view_anypoint()
        self.show_result_image_to_ui()

    def onclick_btn_turn_left(self):
        self.set_button_state(btn_turn_left=True)
        self.model_plugin.create_maps_turn_left_view_anypoint()
        if self.image_dash_camera_result is not None:
            self.model_plugin.create_image_turn_left_view_anypoint()
        self.show_result_image_to_ui()

    def onclick_btn_turn_right(self):
        self.set_button_state(btn_turn_right=True)
        self.model_plugin.create_maps_turn_right_view_anypoint()
        if self.image_dash_camera_result is not None:
            self.model_plugin.create_image_turn_right_view_anypoint()
        self.show_result_image_to_ui()

    def onclick_btn_reverse(self):
        self.set_button_state(btn_reverse=True)
        self.model_plugin.create_maps_rear_view_anypoint()
        if self.image_dash_camera_result is not None:
            self.model_plugin.create_image_rear_view_anypoint()
        self.show_result_image_to_ui()

    def onclick_btn_dash_cam_front(self):
        self.set_button_state(btn_dash_cam_front=True)
        view_mode = "Dash_front_view"
        if self.image_dash_camera_result is not None:
            self.model_plugin.set_dash_image_mode = view_mode
            self.model_plugin.create_dash_image()
        self.show_result_image_to_ui()

    def onclick_btn_dash_cam_driver(self):
        self.set_button_state(btn_dash_cam_driver=True)
        view_mode = "Dash_driver_view"
        if self.image_dash_camera_result is not None:
            self.model_plugin.set_dash_image_mode = view_mode
            self.model_plugin.create_dash_image()
        self.show_result_image_to_ui()

    def onclick_btn_driver(self):
        self.set_button_state(btn_driver=True)
        self.model_plugin.set_anypoint_image_mode = "Steering View"
        if self.image_dash_camera_result is not None:
            self.model_plugin.create_anypoint_image()
        self.show_result_image_to_ui()

    def onclick_btn_second_driver(self):
        self.set_button_state(btn_second_driver=True)
        self.model_plugin.set_anypoint_image_mode = "Second Driver View"
        if self.image_dash_camera_result is not None:
            self.model_plugin.create_anypoint_image()
        self.show_result_image_to_ui()

    # change screen buttons
    def onclick_compare_panorama_anypoint(self):
        if self.ui.btn_compare_panorama_anypoint.isChecked():
            self.ui.comboBox.setCurrentIndex(0)
            self.control_setting_view()
            self.ui.scrollArea.setMaximumWidth(16777215)
            self.ui.scrollArea_3.setMaximumWidth(720)
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.stackedWidget_2.setCurrentIndex(0)
            self.model_plugin.set_dash_image_mode = "Dash_front_view"
            self.model_plugin.set_anypoint_image_mode = "For comparison View"

            if self.image_dash_camera_result is not None:
                self.model_plugin.process_to_result_image()
                self.show_result_image_to_ui()

        else:
            self.ui.scrollArea_3.setMaximumWidth(16777215)
            self.ui.stackedWidget.setCurrentIndex(1)

    def control_setting_view(self):
        self.model_plugin.set_mode_calibration(self.ui.comboBox.currentText())
        if self.ui.comboBox.currentText() == "Dash camera":
            self.ui.lineEdit_project_name.setPlaceholderText("Project name dash cam")
            self.ui.stackedWidget_setting_config.setCurrentIndex(0)
            self.ui.stackedWidget_setting_view.setCurrentIndex(0)

        else:
            self.ui.lineEdit_project_name.setPlaceholderText("Project name birds view")
            self.ui.stackedWidget_setting_config.setCurrentIndex(1)
            self.ui.stackedWidget_setting_view.setCurrentIndex(1)
            self.ui.scrollArea_6.setMaximumWidth(640)
            for i in range(1, 5):
                self.model_plugin.process_source_image(i)
                self.control_video_controller()
                self.control_config_birds_view.showing_confing_to_ui()
                self.show_result_image_to_ui()

    def change_view_config_page(self):
        if self.ui.btn_setting_configuration.isChecked():
            self.ui.frame_16.hide()
            self.ui.btn_compare_panorama_anypoint.show()
            self.ui.stackedWidget.setCurrentIndex(1)

        else:
            self.ui.frame_16.show()
            self.ui.btn_compare_panorama_anypoint.hide()
            self.ui.btn_compare_panorama_anypoint.setChecked(False)
            self.ui.stackedWidget.setCurrentIndex(0)

        self.control_view_condition_car_moving()

    def back_to_main_view(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.btn_setting_configuration.setChecked(False)

    def onclick_modify_camera_parameter(self):
        self.model.form_camera_parameter()

    def change_stylesheets(self):
        self.change_style_ui.change_stylesheets()

    # ############ Birds view start here ##############################
    def change_anypoint_birds(self, index):
        self.control_config_birds_view.change_config_anypoint_properties_bird_view(index)
        self.model_plugin.create_maps_anypoint_bird_view(index)

    def onclick_change_rotate(self, index):
        self.control_config_birds_view.change_config_anypoint_properties_bird_view(index)
        self.model_plugin.create_remap_image_anypoint_bird_view(index)

    def change_shift_properties_birds(self, index):
        self.control_config_birds_view.change_properties_shift_birds_image(index)
        self.model_plugin.create_bird_view_image()

    def change_properties_crop_birds(self, index):
        self.control_config_birds_view.change_crop_properties_image_bird_view(index)
        self.model_plugin.create_bird_view_image()

    def onclick_change_gradient_mode(self):
        if self.ui.radioButton_horizontal_blend.isChecked():
            self.model_plugin.change_gradient_mode("H")
        elif self.ui.radioButton_vertical_blend.isChecked():
            self.model_plugin.change_gradient_mode("V")
        elif self.ui.radioButton_overlap_blend.isChecked():
            self.model_plugin.change_gradient_mode("O")
        elif self.ui.radioButton_horizontal_diagonal.isChecked():
            self.model_plugin.change_gradient_mode("D")
        self.model_plugin.create_bird_view_image()

    # ############ control video start here ###########################
    def onclick_play_pause_video(self):
        if self.ui.btn_play_pause.isChecked():
            self.timer.start()
        else:
            self.timer.stop()

        media_sources = ("Video", "usb_cam", "Streaming")
        if self.model_plugin.media_source_type in media_sources:
            self.set_icon.set_icon_play_pause()

    def onclick_stop_video(self):
        self.ui.btn_play_pause.setChecked(False)
        self.ui.btn_play_pause.setIcon(self.model.icon.get_icon_play_video())
        self.model_plugin.stop_video()
        self.timer.stop()

    def onclick_rewind_video(self):
        self.model_plugin.rewind_video()

    def onclick_forward_video(self):
        self.model_plugin.forward_video()

    def onclick_slider_video(self, value):
        value_max = self.ui.slider_video.maximum()
        self.model_plugin.slider_controller(value, value_max)

    @QtCore.pyqtSlot(float)
    def set_value_slider_video(self, current_position):
        self.ui.slider_video.blockSignals(True)
        self.ui.slider_video.setValue(int(current_position))
        self.ui.slider_video.blockSignals(False)

    @QtCore.pyqtSlot(list)
    def set_time_video(self, list_video_duration):
        """
            set time of video in label
        Returns:
            None
        """
        total_minute = list_video_duration[0]
        total_second = list_video_duration[1]
        current_minute = list_video_duration[2]
        current_second = list_video_duration[3]
        self.ui.lbl_current_time.setText("%02d:%02d" % (current_minute, current_second))
        if total_minute < 0:
            self.ui.lbl_total_time.setText("--:--")

        else:
            self.ui.lbl_total_time.setText("%02d:%02d" % (total_minute, total_second))
