
class SetThemeStylesheet:
    def __init__(self, ui, model):
        self.ui = ui
        self.model = model

    def change_stylesheets(self):
        self.ui.frame.setStyleSheet(self.model.style_frame_main())

        self.ui.frame_8.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_14.setStyleSheet(self.model.style_frame_object())

        self.ui.horizontalFrame_config.setStyleSheet(self.model.style_frame_object())
        self.ui.horizontalFrame_anypoint.setStyleSheet(self.model.style_frame_object())

        self.ui.frame_4.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_2.setStyleSheet(self.model.style_frame_object())

        self.ui.frame_13.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_15.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_18.setStyleSheet(self.model.style_frame_object())

        self.ui.frame_config_button_group.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_camera_info.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_10.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_11.setStyleSheet(self.model.style_frame_object())
        self.ui.horizontalFrame_2.setStyleSheet(self.model.style_frame_object())

        self.ui.btn_forward.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_second_driver.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_record.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_reverse.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_screenshoot.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_setting_configuration.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_compare_panorama_anypoint.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_turn_left.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_turn_right.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_dash_cam_driver.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_dash_cam_front.setStyleSheet(self.model.style_pushbutton())

        self.ui.btn_driver.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_play_pause.setStyleSheet(self.model.style_pushbutton_play_pause_video())
        self.ui.btn_stop.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_forward_5_second.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_backward_5_second.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_parameter_form.setStyleSheet(self.model.style_pushbutton())

        self.ui.pushButton_show_original_image_bird_view.setStyleSheet(self.model.style_pushbutton())

        self.ui.btn_load_config.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_save_config.setStyleSheet(self.model.style_pushbutton())

        self.ui.btn_zoom_in.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_zoom_out.setStyleSheet(self.model.style_pushbutton())

        self.ui.lineEdit_project_name.setStyleSheet(self.model.style_line_edit())

        self.ui.btn_parameter_form.setStyleSheet(self.model.style_pushbutton())

        self.ui.btn_open_source.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_close_config.setStyleSheet(self.model.style_pushbutton())

        self.ui.scrollArea.setStyleSheet(self.model.style_scroll_area())
        self.ui.scrollArea_3.setStyleSheet(self.model.style_scroll_area())

        self.ui.label_11.setStyleSheet(self.model.style_label())
        self.ui.label_25.setStyleSheet(self.model.style_label())
        self.ui.label_8.setStyleSheet(self.model.style_label())
        self.ui.label_14.setStyleSheet(self.model.style_label())
        self.ui.label_20.setStyleSheet(self.model.style_label())
        self.ui.label_21.setStyleSheet(self.model.style_label())
        self.ui.label_30.setStyleSheet(self.model.style_label())

        # birds view
        self.ui.label_34.setStyleSheet(self.model.style_label())
        self.ui.label_38.setStyleSheet(self.model.style_label())

        self.ui.label_26.setStyleSheet(self.model.style_label())
        self.ui.label_27.setStyleSheet(self.model.style_label())

        self.ui.label_28.setStyleSheet(self.model.style_label())
        self.ui.label_29.setStyleSheet(self.model.style_label())

        self.ui.line.setStyleSheet(self.model.style_line())
        self.ui.line_2.setStyleSheet(self.model.style_line())
        self.ui.line_3.setStyleSheet(self.model.style_line())
        self.ui.line_4.setStyleSheet(self.model.style_line())
