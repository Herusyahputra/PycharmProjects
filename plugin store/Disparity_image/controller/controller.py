from PyQt6 import QtCore
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QWidget, QMessageBox
from ..view.main_ui import Ui_Form
from .add_zoom_button import ZoomButton
from .theme_controller import Themes


class Controller(QWidget):
    def __init__(self, model, ModelPlugin):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.model = model
        self.model_plugin = ModelPlugin
        self.zoom_button = ZoomButton(self)
        self.themes = Themes(self)
        self.hide_show_mode()

        self.zoom_anypoint1_value = 0
        self.zoom_feature_point_value = 0
        self.zoom_feature_matching_value = 0
        self.zoom_optical_flow_value = 0
        self.zoom_disparity_value = 0

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_to_user_interface)
        self.ui.checkBox_view_feature_point.setChecked(False)
        self.ui.checkBox_view_anypoint_panorama.setChecked(True)
        self.ui.checkBox_view_disparity.setChecked(True)
        self.change_view()
        self.update_config_data_to_model()
        self.ui.frame_video_player.show()
        self.connect_action()

    def connect_action(self):
        self.ui.btn_open_media.clicked.connect(self.open_media)
        self.ui.radioButton_anypoint.toggled.connect(lambda: self.change_mode_option("Anypoint"))
        self.ui.radioButton_panorama.toggled.connect(lambda: self.change_mode_option("Panorama"))

        self.ui.doubleSpinBox_pitch_image1.valueChanged.connect(self.update_config_anypoint_image_1)
        self.ui.doubleSpinBox_yaw_image1.valueChanged.connect(self.update_config_anypoint_image_1)
        self.ui.doubleSpinBox_roll_image1.valueChanged.connect(self.update_config_anypoint_image_1)
        self.ui.doubleSpinBox_zoom_image1.valueChanged.connect(self.update_config_anypoint_image_1)

        self.ui.doubleSpinBox_pitch_image2.valueChanged.connect(self.update_config_anypoint_image_2)
        self.ui.doubleSpinBox_yaw_image2.valueChanged.connect(self.update_config_anypoint_image_2)
        self.ui.doubleSpinBox_roll_image2.valueChanged.connect(self.update_config_anypoint_image_2)
        self.ui.doubleSpinBox_zoom_image2.valueChanged.connect(self.update_config_anypoint_image_2)

        self.ui.spinBox_alpha_min_image1.valueChanged.connect(self.update_config_panorama_image_1)
        self.ui.spinBox_alpha_max_image1.valueChanged.connect(self.update_config_panorama_image_1)
        self.ui.spinBox_alpha_max_image2.valueChanged.connect(self.update_config_panorama_image_2)
        self.ui.spinBox_alpha_min_image2.valueChanged.connect(self.update_config_panorama_image_2)

        self.ui.doubleSpinBox_crop_top.valueChanged.connect(self.change_properties_cropping_panorama)
        self.ui.doubleSpinBox_crop_left.valueChanged.connect(self.change_properties_cropping_panorama)
        self.ui.doubleSpinBox_crop_right.valueChanged.connect(self.change_properties_cropping_panorama)
        self.ui.doubleSpinBox_crop_bottom.valueChanged.connect(self.change_properties_cropping_panorama)

        self.zoom_button.btn_zoom_in_stereo.clicked.connect(lambda: self.change_zoom_anypoint_1("zoom_in"))
        self.zoom_button.btn_zoom_out_stereo.clicked.connect(lambda: self.change_zoom_anypoint_1("zoom_out"))

        self.zoom_button.btn_zoom_in_feature_point.clicked.connect(lambda: self.change_zoom_feature_point("zoom_in"))
        self.zoom_button.btn_zoom_out_feature_point.clicked.connect(lambda: self.change_zoom_feature_point("zoom_out"))

        self.zoom_button.btn_zoom_in_feature_matching.clicked.connect(
            lambda: self.change_zoom_feature_matching("zoom_in"))
        self.zoom_button.btn_zoom_out_feature_matching.clicked.connect(
            lambda: self.change_zoom_feature_matching("zoom_out"))

        self.zoom_button.btn_zoom_in_disparity.clicked.connect(lambda: self.change_zoom_disparity("zoom_in"))
        self.zoom_button.btn_zoom_out_disparity.clicked.connect(lambda: self.change_zoom_disparity("zoom_out"))

        self.ui.doubleSpinBox_alpha_recenter_image1.valueChanged.connect(self.update_config_recenter_image_1)
        self.ui.doubleSpinBox_beta_recenter_image1.valueChanged.connect(self.update_config_recenter_image_1)
        self.ui.doubleSpinBox_alpha_recenter_image2.valueChanged.connect(self.update_config_recenter_image_2)
        self.ui.doubleSpinBox_beta_recenter_image2.valueChanged.connect(self.update_config_recenter_image_2)
        self.ui.btn_reset_recenter.clicked.connect(self.reset_config_recenter_image)

        self.ui.btn_play_pause.clicked.connect(self.play_pause_video)
        self.ui.btn_stop.clicked.connect(self.stop_video)

        self.ui.btn_start_disparity.clicked.connect(self.process_disparity_image)

        self.ui.checkBox_view_recenter.toggled.connect(self.change_view)
        self.ui.checkBox_view_anypoint_panorama.toggled.connect(self.change_view)
        self.ui.checkBox_view_feature_matching.toggled.connect(self.change_view)
        self.ui.checkBox_view_feature_point.toggled.connect(self.change_view)
        self.ui.checkBox_view_disparity.toggled.connect(self.change_view)
        self.ui.checkBox_view_optical_flow.toggled.connect(self.change_view)

        self.ui.radioButton_show_all_line.toggled.connect(self.update_config_optical_flow)
        self.ui.radioButton_random_line.toggled.connect(self.update_config_optical_flow)
        self.ui.btn_go_calculate_line.clicked.connect(self.update_config_optical_flow)

        self.zoom_button.btn_zoom_in_optical_flow.clicked.connect(
            lambda: self.change_zoom_optical_flow_value("zoom_in"))
        self.zoom_button.btn_zoom_out_optical_flow.clicked.connect(
            lambda: self.change_zoom_optical_flow_value("zoom_out"))

    def change_view(self):
        if self.ui.checkBox_view_recenter.isChecked():
            self.ui.frame_config_recenter.show()
            self.model_plugin.mode_recenter = True
            self.model_plugin.process_image()
            self.show_image_to_ui()
        else:
            self.model_plugin.mode_recenter = False
            self.ui.frame_config_recenter.hide()
            self.model_plugin.process_image()
            self.show_image_to_ui()

        if self.ui.checkBox_view_anypoint_panorama.isChecked():
            self.ui.frame_image_output.show()
        else:
            self.ui.frame_image_output.hide()

        if self.ui.checkBox_view_feature_point.isChecked():
            self.ui.frame_feature_point.show()
        else:
            self.ui.frame_feature_point.hide()

        if self.ui.checkBox_view_feature_matching.isChecked():
            self.ui.frame_feature_matching.show()
        else:
            self.ui.frame_feature_matching.hide()

        if self.ui.checkBox_view_disparity.isChecked():
            self.ui.frame_disparity_image.show()
        else:
            self.ui.frame_disparity_image.hide()

        if self.ui.checkBox_view_optical_flow.isChecked():
            self.ui.frame_optical_flow.show()
        else:
            self.ui.frame_optical_flow.hide()

    def process_disparity_image(self):
        if self.model_plugin.image_source is not None:
            self.model_plugin.disparity_image_test_algorithm()
            self.model_plugin.draw_point_matching()
            self.model_plugin.calculate_deference_point()
            self.show_image_to_ui()

    def open_media(self):
        cam_type, media_source, params_name = self.model.select_media_source()
        print(cam_type)
        print(media_source)
        print(params_name)
        if media_source is not None:
            self.model_plugin.read_media_sources(media_source, params_name)
            self.add_icx_and_icy_recenter()
            self.show_image_to_ui()

    def change_properties_cropping_panorama(self):
        self.model_plugin.crop_panorama["left"] = self.ui.doubleSpinBox_crop_left.value()
        if self.ui.doubleSpinBox_crop_right.value() > self.ui.doubleSpinBox_crop_left.value() + 0.2:
            self.model_plugin.crop_panorama["right"] = self.ui.doubleSpinBox_crop_right.value()
        self.model_plugin.crop_panorama["top"] = self.ui.doubleSpinBox_crop_top.value()
        if self.ui.doubleSpinBox_crop_bottom.value() > self.ui.doubleSpinBox_crop_top.value() + 0.2:
            self.model_plugin.crop_panorama["bottom"] = self.ui.doubleSpinBox_crop_bottom.value()
        if self.model_plugin.image_source is not None:
            self.model_plugin.crop_panorama_image()
            self.show_image_to_ui()

    def play_pause_video(self):
        if self.model_plugin.image_source is not None:
            if self.ui.btn_play_pause.isChecked():
                self.timer.start()
            else:
                self.timer.stop()
            self.themes.change_icon_play_pause()

    def stop_video(self):
        self.timer.stop()
        self.ui.btn_play_pause.setChecked(False)
        self.themes.change_icon_play_pause()

    def update_config_data_to_model(self):
        self.update_config_anypoint_image_1()
        self.update_config_anypoint_image_2()
        self.update_config_panorama_image_1()
        self.update_config_panorama_image_2()
        self.update_config_recenter_image_1()
        self.update_config_recenter_image_2()
        self.change_properties_cropping_panorama()
        self.update_config_optical_flow()

    def add_icx_and_icy_recenter(self):
        self.ui.doubleSpinBox_alpha_recenter_image1.blockSignals(True)
        self.ui.doubleSpinBox_beta_recenter_image1.blockSignals(True)
        self.ui.doubleSpinBox_alpha_recenter_image2.blockSignals(True)
        self.ui.doubleSpinBox_beta_recenter_image2.blockSignals(True)

        self.ui.doubleSpinBox_alpha_recenter_image1.setValue(self.model_plugin.moildev[0].icx)
        self.ui.doubleSpinBox_beta_recenter_image1.setValue(self.model_plugin.moildev[0].icy)
        self.ui.doubleSpinBox_alpha_recenter_image2.setValue(self.model_plugin.moildev[1].icx)
        self.ui.doubleSpinBox_beta_recenter_image2.setValue(self.model_plugin.moildev[1].icy)

        self.ui.doubleSpinBox_alpha_recenter_image1.blockSignals(False)
        self.ui.doubleSpinBox_beta_recenter_image1.blockSignals(False)
        self.ui.doubleSpinBox_alpha_recenter_image2.blockSignals(False)
        self.ui.doubleSpinBox_beta_recenter_image2.blockSignals(False)

    def reset_config_recenter_image(self):
        if self.model_plugin.image_source is not None:
            self.add_icx_and_icy_recenter()
            self.update_config_recenter_image_1()
            self.update_config_recenter_image_2()

    def update_config_recenter_image_1(self):
        self.model_plugin.config_recenter[0]["icx"] = self.ui.doubleSpinBox_alpha_recenter_image1.value()
        self.model_plugin.config_recenter[0]["icy"] = self.ui.doubleSpinBox_beta_recenter_image1.value()
        if self.model_plugin.image_source is not None:
            self.model_plugin.get_alpha_and_beta(0)
            self.model_plugin.create_maps_recenter_image(0)
            self.model_plugin.remap_recenter_image(0)
            self.model_plugin.remap_image_output(0)
            self.show_image_to_ui()

    def update_config_recenter_image_2(self):
        self.model_plugin.config_recenter[1]["icx"] = self.ui.doubleSpinBox_alpha_recenter_image2.value()
        self.model_plugin.config_recenter[1]["icy"] = self.ui.doubleSpinBox_beta_recenter_image2.value()
        if self.model_plugin.image_source is not None:
            self.model_plugin.get_alpha_and_beta(1)
            self.model_plugin.create_maps_recenter_image(1)
            self.model_plugin.remap_recenter_image(1)
            self.model_plugin.remap_image_output(1)
            # self.model_plugin.disparity_image()
            self.show_image_to_ui()

    def update_config_optical_flow(self):
        if self.ui.radioButton_show_all_line.isChecked():
            self.model_plugin.config_line["status"] = "all"
        elif self.ui.radioButton_random_line.isChecked():
            self.model_plugin.config_line["status"] = "random"
        self.model_plugin.config_line["total_point"] = self.ui.doubleSpinBox_total_random_line.value()
        if self.model_plugin.image_source is not None and self.model_plugin.key_points[0] is not None:
            self.model_plugin.calculate_deference_point()
            self.show_image_to_ui()

    def update_config_anypoint_image_1(self):
        self.model_plugin.config_anypoint[0]["pitch"] = self.ui.doubleSpinBox_pitch_image1.value()
        self.model_plugin.config_anypoint[0]["yaw"] = self.ui.doubleSpinBox_yaw_image1.value()
        self.model_plugin.config_anypoint[0]["roll"] = self.ui.doubleSpinBox_roll_image1.value()
        self.model_plugin.config_anypoint[0]["zoom"] = self.ui.doubleSpinBox_zoom_image1.value()
        if self.model_plugin.image_source is not None:
            self.model_plugin.create_maps_anypoint(0)
            self.model_plugin.remap_image_output(0)
            # self.model_plugin.disparity_image()
            self.show_image_to_ui()

    def update_config_anypoint_image_2(self):
        self.model_plugin.config_anypoint[1]["pitch"] = self.ui.doubleSpinBox_pitch_image2.value()
        self.model_plugin.config_anypoint[1]["yaw"] = self.ui.doubleSpinBox_yaw_image2.value()
        self.model_plugin.config_anypoint[1]["roll"] = self.ui.doubleSpinBox_roll_image2.value()
        self.model_plugin.config_anypoint[1]["zoom"] = self.ui.doubleSpinBox_zoom_image2.value()
        if self.model_plugin.image_source is not None:
            self.model_plugin.create_maps_anypoint(1)
            self.model_plugin.remap_image_output(1)
            # self.model_plugin.disparity_image()
            self.show_image_to_ui()

    def update_config_panorama_image_1(self):
        self.model_plugin.config_panorama[0]["alpha_min"] = self.ui.spinBox_alpha_min_image1.value()
        self.model_plugin.config_panorama[0]["alpha_max"] = self.ui.spinBox_alpha_max_image1.value()
        if self.model_plugin.image_source is not None:
            self.model_plugin.create_maps_panorama(0)
            self.model_plugin.remap_image_output(0)
            # self.model_plugin.disparity_image()
            self.show_image_to_ui()

    def update_config_panorama_image_2(self):
        self.model_plugin.config_panorama[1]["alpha_min"] = self.ui.spinBox_alpha_min_image2.value()
        self.model_plugin.config_panorama[1]["alpha_max"] = self.ui.spinBox_alpha_max_image2.value()
        if self.model_plugin.image_source is not None:
            self.model_plugin.create_maps_panorama(1)
            self.model_plugin.remap_image_output(1)
            # self.model_plugin.disparity_image()
            self.show_image_to_ui()

    def change_zoom_anypoint_1(self, status):
        if status == "zoom_in":
            self.zoom_anypoint1_value += 100
        else:
            self.zoom_anypoint1_value -= 100
            if self.zoom_anypoint1_value == - 400:
                self.zoom_anypoint1_value = 0
        self.show_image_to_ui()

    def change_zoom_feature_point(self, status):
        if status == "zoom_in":
            self.zoom_feature_point_value += 100
        else:
            self.zoom_feature_point_value -= 100
            if self.zoom_feature_point_value == - 400:
                self.zoom_feature_point_value = 0
        self.show_image_to_ui()

    def change_zoom_feature_matching(self, status):
        if status == "zoom_in":
            self.zoom_feature_matching_value += 100
        else:
            self.zoom_feature_matching_value -= 100
            if self.zoom_feature_matching_value == - 400:
                self.zoom_feature_matching_value = 0
        self.show_image_to_ui()

    def change_zoom_optical_flow_value(self, status):
        if status == "zoom_in":
            self.zoom_optical_flow_value += 100
        else:
            self.zoom_optical_flow_value -= 100
            if self.zoom_optical_flow_value == - 400:
                self.zoom_optical_flow_value = 0
        self.show_image_to_ui()

    def change_zoom_disparity(self, status):
        if status == "zoom_in":
            self.zoom_disparity_value += 100
        else:
            self.zoom_disparity_value -= 100
            if self.zoom_disparity_value == - 400:
                self.zoom_disparity_value = 0
        self.show_image_to_ui()

    def update_to_user_interface(self):
        self.model_plugin.next_frame()
        self.show_image_to_ui()

    def show_image_to_ui(self):
        self.disable_video_player()
        if self.model_plugin.image_source is not None:
            image = self.model_plugin.draw_cross_in_image(self.model_plugin.image_source.copy(),
                                                          self.model_plugin.moildev[0].icx,
                                                          self.model_plugin.moildev[0].icy)
            self.model.show_image_to_label(self.ui.lbl_image_sources, image, 400)

            image = self.model_plugin.draw_cross_in_image(self.model_plugin.image_output[0].copy(),
                                                          int(self.model_plugin.image_output[0].shape[1]/2),
                                                          int(self.model_plugin.image_output[0].shape[0]/2))
            self.model.show_image_to_label(self.ui.lbl_anypoint_image_1, image, 460 +
                                           self.zoom_anypoint1_value)
            image = self.model_plugin.draw_cross_in_image(self.model_plugin.image_output[1].copy(),
                                                          int(self.model_plugin.image_output[1].shape[1]/2),
                                                          int(self.model_plugin.image_output[1].shape[0]/2))
            self.model.show_image_to_label(self.ui.lbl_anypoint_image_2, image, 460 +
                                           self.zoom_anypoint1_value)

            print("show image")
            if self.model_plugin.image_feature_point[0] is not None:
                self.model.show_image_to_label(self.ui.lbl_anypoint_point_1, self.model_plugin.image_feature_point[0],
                                               460 + self.zoom_feature_point_value)
            if self.model_plugin.image_feature_point[1] is not None:
                self.model.show_image_to_label(self.ui.lbl_anypoint_point_2, self.model_plugin.image_feature_point[1],
                                               460 + self.zoom_feature_point_value)
            if self.model_plugin.image_feature_matching is not None:
                self.model.show_image_to_label(self.ui.lbl_feature_matching, self.model_plugin.image_feature_matching,
                                               600 + self.zoom_feature_matching_value)

            if self.model_plugin.image_optical_flow[0] is not None:
                self.model.show_image_to_label(self.ui.lbl_optical_flow1, self.model_plugin.image_optical_flow[0], 460 +
                                               self.zoom_optical_flow_value)
            if self.model_plugin.image_optical_flow[1] is not None:
                self.model.show_image_to_label(self.ui.lbl_optical_flow2, self.model_plugin.image_optical_flow[1], 460 +
                                               self.zoom_optical_flow_value)

            if self.model_plugin.image_disparity[1] is not None:
                self.model.show_image_to_label(self.ui.lbl_disparity, self.model_plugin.image_disparity[1], 460 +
                                               self.zoom_disparity_value)
            if self.model_plugin.image_disparity[0] is not None:
                self.model.show_image_to_label(self.ui.lbl_disparity_2, self.model_plugin.image_disparity[0], 460 +
                                               self.zoom_disparity_value)

            # try:
            #     import cv2
            #     cv2.imwrite("image_source.png", self.model_plugin.image_source)
            #     cv2.imwrite("image_output1.png", self.model_plugin.image_output[0])
            #     cv2.imwrite("image_output2.png", self.model_plugin.image_output[1])
            #     cv2.imwrite("img_draw_L.png", self.model_plugin.image_feature_point[0])
            #     cv2.imwrite("img_draw_R.png", self.model_plugin.image_feature_point[1])
            #     cv2.imwrite("img_Keypoint_matches.png", self.model_plugin.image_feature_matching)
            #     cv2.imwrite("image_optical_flow_l.png", self.model_plugin.image_optical_flow[0])
            #     cv2.imwrite("image_optical_flow_r.png", self.model_plugin.image_optical_flow[1])
            #     cv2.imwrite("image_disparity1.png", self.model_plugin.image_disparity[0])
            #     cv2.imwrite("image_disparity2.png", self.model_plugin.image_disparity[1])
            # except:
            #     pass

            for image in self.model_plugin.image_recenter:
                if image is not None:
                    image1 = self.model_plugin.draw_cross_in_image(self.model_plugin.image_recenter[0].copy(),
                                                                   int(self.model_plugin.config_recenter[0]["icx"]),
                                                                   int(self.model_plugin.config_recenter[0]["icy"]))
                    self.model.show_image_to_label(self.ui.lbl_image_recenter1, image1, 180)
                    image2 = self.model_plugin.draw_cross_in_image(self.model_plugin.image_recenter[1].copy(),
                                                                   int(self.model_plugin.config_recenter[1]["icx"]),
                                                                   int(self.model_plugin.config_recenter[1]["icy"]))
                    self.model.show_image_to_label(self.ui.lbl_image_recenter2, image2, 180)

    def change_mode_option(self, mode_option):
        self.model_plugin.mode_option = mode_option
        self.model_plugin.create_maps_image_output()
        self.model_plugin.process_image()
        self.hide_show_mode()
        self.show_image_to_ui()

    def hide_show_mode(self):
        if self.model_plugin.mode_option == "Anypoint":
            self.ui.frame_config_anypoint.show()
            self.ui.frame_config_panorama.hide()
            self.ui.frame_anypoint_panorama_option.show()
            # self.ui.frame_ouput_panorama.hide()
        else:
            self.ui.frame_config_anypoint.hide()
            self.ui.frame_config_panorama.show()
            # self.ui.frame_anypoint_panorama_option.hide()
            # self.ui.frame_ouput_panorama.show()

    def disable_video_player(self):
        if self.model_plugin.properties_video["video"]:
            self.ui.frame_video_player.show()
            self.ui.btn_rewind.setEnabled(True)
            self.ui.btn_forward.setEnabled(True)
            if self.model_plugin.properties_video["streaming"]:
                self.ui.btn_rewind.setEnabled(False)
                self.ui.btn_forward.setEnabled(False)
        else:
            self.timer.stop()
            self.ui.frame_video_player.hide()
