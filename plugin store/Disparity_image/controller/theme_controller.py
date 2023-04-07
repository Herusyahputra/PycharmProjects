class Themes(object):
    def __init__(self, main_controller):
        self.controller = main_controller
        self.change_stylesheets()

    def change_stylesheets(self):
        self.set_icon_video_player()
        self.set_stylesheet_button()
        self.set_stylesheet_label()
        self.set_stylesheet_frame()
        self.set_stylesheet_line()
        self.set_stylesheet_radio_button()
        self.set_stylesheet_check_box()
        self.set_stylesheet_double_spin_box()

    def set_icon_video_player(self):
        self.controller.ui.btn_play_pause.setIcon(self.controller.model.icon.get_icon_play_video())
        self.controller.ui.btn_rewind.setIcon(self.controller.model.icon.get_icon_rewind_video())
        self.controller.ui.btn_forward.setIcon(self.controller.model.icon.get_icon_forward_video())
        self.controller.ui.btn_stop.setIcon(self.controller.model.icon.get_icon_square())

    def set_stylesheet_frame(self):
        self.controller.ui.main_frame.setStyleSheet(self.controller.model.style_frame_main())
        self.controller.ui.frame_image_output.setStyleSheet(self.controller.model.style_frame_main())
        self.controller.ui.frame_feature_point.setStyleSheet(self.controller.model.style_frame_main())
        self.controller.ui.frame_feature_matching.setStyleSheet(self.controller.model.style_frame_main())
        self.controller.ui.frame_optical_flow.setStyleSheet(self.controller.model.style_frame_main())
        self.controller.ui.frame_disparity_image.setStyleSheet(self.controller.model.style_frame_main())
        self.controller.ui.frame_video_player.setStyleSheet(self.controller.model.style_frame_object())

        self.controller.ui.frame_anypoint_panorama_option.setStyleSheet(self.controller.model.frame_transparent())
        self.controller.ui.frame_view.setStyleSheet(self.controller.model.frame_transparent())
        self.controller.ui.frame_config_anypoint.setStyleSheet(self.controller.model.frame_transparent())
        self.controller.ui.frame_config_optical_flow.setStyleSheet(self.controller.model.frame_transparent())
        self.controller.ui.frame_config_recenter.setStyleSheet(self.controller.model.frame_transparent())
        self.controller.ui.frame_window_image.setStyleSheet(self.controller.model.style_frame_main())

        self.controller.zoom_button.frame_image_stereo.setStyleSheet(self.controller.model.frame_transparent())
        self.controller.zoom_button.frame_zoom_feature_point.setStyleSheet(self.controller.model.frame_transparent())
        self.controller.zoom_button.frame_zoom_feature_mathing.setStyleSheet(self.controller.model.frame_transparent())
        self.controller.zoom_button.frame_zoom_disparity.setStyleSheet(self.controller.model.frame_transparent())
        self.controller.zoom_button.frame_zoom_optical_flow.setStyleSheet(self.controller.model.frame_transparent())

    def set_stylesheet_button(self):
        self.controller.ui.btn_open_media.setStyleSheet(self.controller.model.style_pushbutton())
        self.controller.ui.btn_start_disparity.setStyleSheet(self.controller.model.style_pushbutton())
        self.controller.ui.btn_go_calculate_line.setStyleSheet(self.controller.model.style_pushbutton())
        self.controller.ui.btn_reset_recenter.setStyleSheet(self.controller.model.style_pushbutton())

        self.controller.zoom_button.btn_zoom_in_stereo.setStyleSheet(self.controller.model.style_pushbutton())
        self.controller.zoom_button.btn_zoom_out_stereo.setStyleSheet(self.controller.model.style_pushbutton())

        self.controller.zoom_button.btn_zoom_in_feature_point.setStyleSheet(self.controller.model.style_pushbutton())
        self.controller.zoom_button.btn_zoom_out_feature_point.setStyleSheet(self.controller.model.style_pushbutton())

        self.controller.zoom_button.btn_zoom_in_feature_matching.setStyleSheet(self.controller.model.style_pushbutton())
        self.controller.zoom_button.btn_zoom_out_feature_matching.setStyleSheet(self.controller.model.style_pushbutton())

        self.controller.zoom_button.btn_zoom_in_disparity.setStyleSheet(self.controller.model.style_pushbutton())
        self.controller.zoom_button.btn_zoom_out_disparity.setStyleSheet(self.controller.model.style_pushbutton())

        self.controller.zoom_button.btn_zoom_in_optical_flow.setStyleSheet(self.controller.model.style_pushbutton())
        self.controller.zoom_button.btn_zoom_out_optical_flow.setStyleSheet(self.controller.model.style_pushbutton())

        self.controller.ui.btn_play_pause.setStyleSheet(self.controller.model.style_pushbutton())
        self.controller.ui.btn_rewind.setStyleSheet(self.controller.model.style_pushbutton())
        self.controller.ui.btn_forward.setStyleSheet(self.controller.model.style_pushbutton())
        self.controller.ui.btn_stop.setStyleSheet(self.controller.model.style_pushbutton())

    def set_stylesheet_label(self):
        self.controller.ui.lbl_image_sources.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.lbl_anypoint_image_1.setStyleSheet(self.controller.model.style_transparent_label())
        self.controller.ui.lbl_anypoint_image_2.setStyleSheet(self.controller.model.style_transparent_label())

        self.controller.ui.lbl_anypoint_point_1.setStyleSheet(self.controller.model.style_transparent_label())
        self.controller.ui.lbl_anypoint_point_2.setStyleSheet(self.controller.model.style_transparent_label())

        self.controller.ui.lbl_feature_matching.setStyleSheet(self.controller.model.style_transparent_label())

        self.controller.ui.lbl_optical_flow1.setStyleSheet(self.controller.model.style_transparent_label())
        self.controller.ui.lbl_optical_flow2.setStyleSheet(self.controller.model.style_transparent_label())

        self.controller.ui.lbl_disparity_2.setStyleSheet(self.controller.model.style_transparent_label())
        self.controller.ui.lbl_disparity.setStyleSheet(self.controller.model.style_transparent_label())

        self.controller.ui.label_recenter.setStyleSheet(self.controller.model.style_label())

        self.controller.ui.label_2.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_6.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_7.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_4.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_5.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_34.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_8.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_38.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_configuration.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_configuration_2.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_cropimage.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_optical_flow.setStyleSheet(self.controller.model.style_label())

        self.controller.ui.label_43.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_12.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_13.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_40.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_27.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_28.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_77.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_42.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_30.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_31.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.label_14.setStyleSheet(self.controller.model.style_label())

        self.controller.ui.lbl_image_recenter1.setStyleSheet(self.controller.model.style_label())
        self.controller.ui.lbl_image_recenter2.setStyleSheet(self.controller.model.style_label())

        self.controller.ui.scrollArea_config.setStyleSheet(self.controller.model.style_scroll_area())
        self.controller.ui.scrollArea_image.setStyleSheet(self.controller.model.style_scroll_area())
        self.controller.ui.scrollArea_anypoint1.setStyleSheet(self.controller.model.style_scroll_area())
        self.controller.ui.scrollArea_anypoint2.setStyleSheet(self.controller.model.style_scroll_area())
        self.controller.ui.scrollArea_anypoint1_point_1.setStyleSheet(self.controller.model.style_scroll_area())
        self.controller.ui.scrollArea_anypoint2_point_2.setStyleSheet(self.controller.model.style_scroll_area())
        self.controller.ui.scrollArea_feature_matching.setStyleSheet(self.controller.model.style_scroll_area())
        self.controller.ui.scrollArea_optical_low1.setStyleSheet(self.controller.model.style_scroll_area())
        self.controller.ui.scrollArea_optical_low2.setStyleSheet(self.controller.model.style_scroll_area())
        self.controller.ui.scrollArea_disparity_1.setStyleSheet(self.controller.model.style_scroll_area())
        self.controller.ui.scrollArea_disparity_2.setStyleSheet(self.controller.model.style_scroll_area())

    def set_stylesheet_line(self):
        self.controller.ui.line_6.setStyleSheet(self.controller.model.style_line())
        self.controller.ui.line_29.setStyleSheet(self.controller.model.style_line())
        self.controller.ui.line_30.setStyleSheet(self.controller.model.style_line())
        self.controller.ui.line.setStyleSheet(self.controller.model.style_line())
        self.controller.ui.line_5.setStyleSheet(self.controller.model.style_line())
        self.controller.ui.line_11.setStyleSheet(self.controller.model.style_line())
        self.controller.ui.line_2.setStyleSheet(self.controller.model.style_line())

    def set_stylesheet_radio_button(self):
        self.controller.ui.radioButton_anypoint.setStyleSheet(self.controller.model.style_radio_button())
        self.controller.ui.radioButton_panorama.setStyleSheet(self.controller.model.style_radio_button())
        self.controller.ui.radioButton_show_all_line.setStyleSheet(self.controller.model.style_radio_button())
        self.controller.ui.radioButton_random_line.setStyleSheet(self.controller.model.style_radio_button())

    def set_stylesheet_check_box(self):
        self.controller.ui.checkBox_view_recenter.setStyleSheet(self.controller.model.style_checkbox())
        self.controller.ui.checkBox_view_anypoint_panorama.setStyleSheet(self.controller.model.style_checkbox())
        self.controller.ui.checkBox_view_feature_point.setStyleSheet(self.controller.model.style_checkbox())
        self.controller.ui.checkBox_view_feature_matching.setStyleSheet(self.controller.model.style_checkbox())
        self.controller.ui.checkBox_view_optical_flow.setStyleSheet(self.controller.model.style_checkbox())
        self.controller.ui.checkBox_view_disparity.setStyleSheet(self.controller.model.style_checkbox())

    def set_stylesheet_double_spin_box(self):
        self.controller.ui.doubleSpinBox_alpha_recenter_image1.setStyleSheet(self.controller.model.style_double_spin_box())
        self.controller.ui.doubleSpinBox_beta_recenter_image1.setStyleSheet(self.controller.model.style_double_spin_box())

        self.controller.ui.doubleSpinBox_alpha_recenter_image2.setStyleSheet(self.controller.model.style_double_spin_box())
        self.controller.ui.doubleSpinBox_beta_recenter_image2.setStyleSheet(self.controller.model.style_double_spin_box())

        self.controller.ui.doubleSpinBox_pitch_image1.setStyleSheet(self.controller.model.style_double_spin_box())
        self.controller.ui.doubleSpinBox_yaw_image1.setStyleSheet(self.controller.model.style_double_spin_box())
        self.controller.ui.doubleSpinBox_roll_image1.setStyleSheet(self.controller.model.style_double_spin_box())
        self.controller.ui.doubleSpinBox_zoom_image1.setStyleSheet(self.controller.model.style_double_spin_box())

        self.controller.ui.doubleSpinBox_pitch_image2.setStyleSheet(self.controller.model.style_double_spin_box())
        self.controller.ui.doubleSpinBox_yaw_image2.setStyleSheet(self.controller.model.style_double_spin_box())
        self.controller.ui.doubleSpinBox_roll_image2.setStyleSheet(self.controller.model.style_double_spin_box())
        self.controller.ui.doubleSpinBox_zoom_image2.setStyleSheet(self.controller.model.style_double_spin_box())

        self.controller.ui.spinBox_alpha_min_image1.setStyleSheet(self.controller.model.style_double_spin_box())
        self.controller.ui.spinBox_alpha_max_image1.setStyleSheet(self.controller.model.style_double_spin_box())
        self.controller.ui.spinBox_alpha_min_image2.setStyleSheet(self.controller.model.style_double_spin_box())
        self.controller.ui.spinBox_alpha_max_image2.setStyleSheet(self.controller.model.style_double_spin_box())

        self.controller.ui.doubleSpinBox_crop_top.setStyleSheet(self.controller.model.style_double_spin_box())
        self.controller.ui.doubleSpinBox_crop_left.setStyleSheet(self.controller.model.style_double_spin_box())
        self.controller.ui.doubleSpinBox_crop_bottom.setStyleSheet(self.controller.model.style_double_spin_box())
        self.controller.ui.doubleSpinBox_crop_right.setStyleSheet(self.controller.model.style_double_spin_box())

        self.controller.ui.doubleSpinBox_total_random_line.setStyleSheet(self.controller.model.style_double_spin_box())

    def change_icon_play_pause(self):
        if self.controller.ui.btn_play_pause.isChecked():
            self.controller.ui.btn_play_pause.setIcon(self.controller.model.icon.get_icon_pause_video())
        else:
            self.controller.ui.btn_play_pause.setIcon(self.controller.model.icon.get_icon_play_video())
