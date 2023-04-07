from PyQt6 import QtGui, QtCore, QtWidgets


class SetIconsUIDashCamera:
    def __init__(self, main_controller):
        """Initialize the MoilApp object with the given main_ui object.

        Args:
            main_ui: A reference to the main user interface object of the application.

        Returns:
            None.
        """
        super().__init__()
        self.main_ctr = main_controller

        self.set_icon_button()

    def set_icon_button(self):
        self.main_ctr.ui.btn_forward.setIcon(self.main_ctr.icon.get_icon_forward())
        self.main_ctr.ui.btn_reverse.setIcon(self.main_ctr.icon.get_icon_reverse())
        self.main_ctr.ui.btn_turn_left.setIcon(self.main_ctr.icon.get_icon_turn_left())
        self.main_ctr.ui.btn_turn_right.setIcon(self.main_ctr.icon.get_icon_turn_right())
        self.main_ctr.ui.btn_driver.setIcon(self.main_ctr.icon.driver_view())
        self.main_ctr.ui.btn_second_driver.setIcon(self.main_ctr.icon.second_driver_view())
        self.main_ctr.ui.btn_dash_cam_front.setIcon(self.main_ctr.icon.get_icon_dash_front())
        self.main_ctr.ui.btn_dash_cam_driver.setIcon(self.main_ctr.icon.get_icon_dash_driver())

        self.main_ctr.ui.btn_record.setIcon(self.main_ctr.icon.get_icon_records())
        self.main_ctr.ui.btn_screenshoot.setIcon(self.main_ctr.icon.get_icon_screenshot())
        self.main_ctr.ui.btn_setting_configuration.setIcon(self.main_ctr.icon.get_icon_setting())

        self.main_ctr.ui.btn_play_pause.setIcon(self.main_ctr.model.icon.get_icon_play_video())
        self.main_ctr.ui.btn_backward_5_second.setIcon(self.main_ctr.model.icon.get_icon_rewind_video())
        self.main_ctr.ui.btn_stop.setIcon(self.main_ctr.model.icon.get_icon_square())
        self.main_ctr.ui.btn_forward_5_second.setIcon(self.main_ctr.model.icon.get_icon_forward_video())

    def set_icon_play_pause(self):
        if self.main_ctr.ui.btn_play_pause.isChecked():
            self.main_ctr.ui.btn_play_pause.setIcon(self.main_ctr.model.icon.get_icon_pause_video())
        else:
            self.main_ctr.ui.btn_play_pause.setIcon(self.main_ctr.model.icon.get_icon_resume_video())

