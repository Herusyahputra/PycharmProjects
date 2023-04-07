# import necessary library you used here
import os
import webbrowser
from PyQt6 import QtCore, QtGui, QtWidgets
from .control_main_ui_apps import ControlApps
from .control_setup_icon import SetIconsUI
from .control_plugin_manager import PluginManager
from .control_result_image import ControlResultImage
from .control_anypoint import AnypointConfig
from .control_panorama import PanoramaConfig
from .control_config_file import ConfigFileApps


class Controller(QtWidgets.QMainWindow):
    def __init__(self, ui, model, *args, **kwargs):
        """
        The controllers class is The bridge of the application that controls how data is displayed.

        Args:
            model: The backend that contains all the data logic
        """
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.ui = ui
        self.ui.setupUi(self)
        self.model = model
        self.__state_view = "FisheyeView"

        self.ctrl_apps = ControlApps(self.ui)
        self.ctrl_icon = SetIconsUI(self.ui)
        self.ctrl_plugin = PluginManager(self)
        self.ctrl_config = ConfigFileApps(self.ui)
        self.model.model_apps.update_file_config()
        self.ctrl_result_image = ControlResultImage()
        self.anypoint_config = AnypointConfig(self.ui)
        self.panorama_config = PanoramaConfig(self.ui)

        self.__width_image_result = 1080
        self.__angle_image_result = 0
        self.__image_result = None

        self.ui.label_logo.mousePressEvent = self.mouse_event_in_moil_logo
        self.ui.delete_plugins_button.hide()
        self.ui.close_plugin_button.hide()

        self.ui.widget_container_content.setCurrentIndex(0)
        self.ui.widget_mode_view.hide()
        self.ui.frame_recenter_image.hide()
        self.ui.frame_pointer_anypoint.hide()

        self.onclick_change_theme_apps()

        # property anypoint mode 1
        self.ui.label_6.hide()
        self.ui.doubleSpinBox_roll.hide()

        # property panorama tube
        self.ui.frame_panorama_tube_config.hide()

        # show maximized window
        self.showMaximized()

        self.model.model_apps.image_original.connect(self.show_image_original)
        self.model.model_apps.image_result.connect(self.get_image_result)
        self.model.model_apps.alpha_beta.connect(self.alpha_beta_from_coordinate)
        self.model.model_apps.slider_time_value.connect(self.set_slider_position)
        self.model.model_apps.timer_video_info.connect(self.show_timer_video_info)
        self.model.model_apps.timer_status.connect(self.onclick_play_pause_video)
        self.model.model_apps.create_moildev()
        self.model.model_apps.create_image_original()

        if self.__image_result is not None:
            self.ui.btn_fisheye_view.setStyleSheet(self.set_style_selected_menu())

        # connect event to button
        self.connect_event()

    def connect_event(self):
        shortcut = QtGui.QShortcut(QtCore.Qt.Key.Key_Escape, self)
        shortcut.activated.connect(self.escape_event)

        self.ui.label_image_original.mouseMoveEvent = self.original_mouse_event
        self.ui.label_image_original.mousePressEvent = self.original_press_event
        self.ui.label_image_original.leaveEvent = self.original_leave_event

        self.ui.btn_change_theme.clicked.connect(self.onclick_change_theme_apps)
        self.ui.btn_togle_menu.clicked.connect(self.onclick_button_menu)
        self.ui.btn_setting.clicked.connect(self.onclick_button_setting_menu)
        self.ui.btn_about_us.clicked.connect(self.onclick_button_about_us)
        self.ui.btn_open_media.clicked.connect(self.onclick_btn_open_media)
        self.ui.btn_form_params.clicked.connect(self.model.form_camera_parameter)
        self.ui.btn_fisheye_view.clicked.connect(self.onclick_btn_fisheye)
        self.ui.btn_anypoint_view.clicked.connect(self.onclick_btn_anypoint)
        self.ui.btn_panorama_view.clicked.connect(self.onclick_btn_panorama)
        self.ui.btn_clear_ui.clicked.connect(self.onclick_reset_button)
        self.ui.github_button.clicked.connect(self.onclick_btn_github)
        self.ui.check_draw_poligon.stateChanged.connect(self.change_polygon_state)

        self.ui.zoom_in_button.clicked.connect(lambda: self.show_image_result("zoom_in"))
        self.ui.zoom_out_button.clicked.connect(lambda: self.show_image_result("zoom_out"))
        self.ui.rotate_left_button.clicked.connect(self.rotate_left)
        self.ui.rotate_right_button.clicked.connect(self.rotate_right)

        self.ui.radio_mode_1.toggled.connect(self.change_mode_anypoint)
        self.ui.radio_mode_2.toggled.connect(self.change_mode_anypoint)

        self.ui.doubleSpinBox_alpha.valueChanged.connect(self.change_properties_anypoint)
        self.ui.doubleSpinBox_beta.valueChanged.connect(self.change_properties_anypoint)
        self.ui.doubleSpinBox_roll.valueChanged.connect(self.change_properties_anypoint)
        self.ui.doubleSpinBox_zoom.valueChanged.connect(self.change_properties_anypoint)

        self.ui.radioButton_car.toggled.connect(self.change_mode_panorama)
        self.ui.radioButton_tube.toggled.connect(self.change_mode_panorama)

        self.ui.spinBox_pano_car_alpha.valueChanged.connect(self.change_properties_panorama)
        self.ui.spinBox_pano_car_beta.valueChanged.connect(self.change_properties_panorama)

        self.ui.doubleSpinBox_pano_car_crop_left.valueChanged.connect(self.change_properties_crop_panorama)
        self.ui.doubleSpinBox_pano_car_crop_right.valueChanged.connect(self.change_properties_crop_panorama)
        self.ui.doubleSpinBox_pano_car_crop_top.valueChanged.connect(self.change_properties_crop_panorama)
        self.ui.doubleSpinBox_pano_car_crop_bottom.valueChanged.connect(self.change_properties_crop_panorama)

        self.ui.spinBox_pano_tube_alpha_min.valueChanged.connect(self.change_properties_panorama)
        self.ui.spinBox_pano_tube_alpha_max.valueChanged.connect(self.change_properties_panorama)

        self.ui.doubleSpinBox_pano_tube_crop_top.valueChanged.connect(self.change_properties_crop_panorama)
        self.ui.doubleSpinBox_pano_tube_crop_buttom.valueChanged.connect(self.change_properties_crop_panorama)

        self.ui.pushButton_any_up.clicked.connect(self.onclick_anypoint)
        self.ui.pushButton_any_left.clicked.connect(self.onclick_anypoint)
        self.ui.pushButton_any_center.clicked.connect(self.onclick_anypoint)
        self.ui.pushButton_any_bottom.clicked.connect(self.onclick_anypoint)
        self.ui.pushButton_any_right.clicked.connect(self.onclick_anypoint)

        self.ui.play_pause_button.clicked.connect(self.model.model_apps.play_pause_video)
        self.ui.stop_button.clicked.connect(self.model.model_apps.stop_video)
        self.ui.rewind_button.clicked.connect(self.model.model_apps.rewind_video_5_second)
        self.ui.forward_button.clicked.connect(self.model.model_apps.forward_video_5_second)
        self.ui.slider_video_time.valueChanged.connect(self.model.model_apps.slider_controller)

    def onclick_play_pause_video(self, status):
        if status:
            self.ui.play_pause_button.setIcon(QtGui.QIcon("icons:pause.svg"))
        else:
            self.ui.play_pause_button.setIcon(QtGui.QIcon("icons:play.svg"))

    def change_polygon_state(self):
        if self.ui.check_draw_poligon.isChecked():
            self.model.model_apps.set_draw_polygon(True)
        else:
            self.model.model_apps.set_draw_polygon(False)

    def original_leave_event(self, event):
        self.model.model_apps.mouse_leave_event_label_original(event)

    def original_press_event(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.__state_view == "AnypointView":
                self.model.model_apps.mouse_press_event_label_original(event)
                if self.ui.radio_mode_1.isChecked():
                    self.anypoint_config.showing_config_mode_1()
                    self.model.model_apps.create_maps_anypoint_mode_1()
                else:
                    self.anypoint_config.showing_config_mode_2()
                    self.model.model_apps.create_maps_anypoint_mode_2()
            elif self.__state_view == "PanoramaView":
                self.model.model_apps.mouse_press_event_label_original(event)
                if self.ui.radioButton_car.isChecked():
                    self.panorama_config.showing_config_panorama_car()
                    self.model.model_apps.create_maps_panorama_car()

        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            print("open image")

    def original_mouse_event(self, event):
        self.model.model_apps.mouse_move_event_label_original(self.ui.label_image_original, event)

    def change_properties_panorama(self):
        if self.__image_result is not None:
            if self.ui.radioButton_car.isChecked():
                self.panorama_config.change_properties_panorama_car()
                self.model.model_apps.create_maps_panorama_car()

            else:
                self.panorama_config.change_properties_panorama_tube()
                self.model.model_apps.create_maps_panorama_tube()

    def change_properties_crop_panorama(self):
        if self.__image_result is not None:
            if self.ui.radioButton_car.isChecked():
                self.panorama_config.change_properties_panorama_car()
            else:
                self.panorama_config.change_properties_panorama_tube()
            self.model.model_apps.manipulate_image()

    def change_mode_panorama(self):
        if self.ui.radioButton_car.isChecked():
            self.ui.frame_panorama_tube_config.hide()
            self.ui.frame_panorama_car_config.show()
            self.panorama_config.showing_config_panorama_car()
            self.model.model_apps.change_panorama_mode("car")
            self.model.model_apps.create_maps_panorama_car()

        else:
            self.ui.frame_panorama_car_config.hide()
            self.ui.frame_panorama_tube_config.show()
            self.panorama_config.showing_config_panorama_tube()
            self.model.model_apps.change_panorama_mode("tube")
            self.model.model_apps.create_maps_panorama_tube()

    def change_mode_anypoint(self):
        if self.ui.radio_mode_1.isChecked():
            self.ui.label_6.hide()
            self.ui.doubleSpinBox_roll.hide()
            self.ui.label.setText("Alpha:")
            self.ui.label_28.setText("Beta:")
            self.anypoint_config.showing_config_mode_1()
            self.model.model_apps.set_anypoint_mode("mode_1")
            self.model.model_apps.create_maps_anypoint_mode_1()
        else:
            self.ui.label_6.show()
            self.ui.doubleSpinBox_roll.show()
            self.ui.label.setText("Pitch:")
            self.ui.label_28.setText("Yaw:")
            self.anypoint_config.showing_config_mode_2()
            self.model.model_apps.set_anypoint_mode("mode_2")
            self.model.model_apps.create_maps_anypoint_mode_2()

    def change_properties_anypoint(self):
        if self.__image_result is not None:
            if self.ui.radio_mode_1.isChecked():
                self.anypoint_config.change_properties_mode_1()
                self.model.model_apps.create_maps_anypoint_mode_1()
            else:
                self.anypoint_config.change_properties_mode_2()
                self.model.model_apps.create_maps_anypoint_mode_2()

    def onclick_anypoint(self):
        if self.ui.radio_mode_1.isChecked():
            if self.sender().objectName() == "pushButton_any_up":
                self.model.model_apps.set_alpha_beta(90, 0)
            elif self.sender().objectName() == "pushButton_any_bottom":
                self.model.model_apps.set_alpha_beta(90, 180)
            elif self.sender().objectName() == "pushButton_any_center":
                self.model.model_apps.set_alpha_beta(0, 0)
            elif self.sender().objectName() == "pushButton_any_left":
                self.model.model_apps.set_alpha_beta(90, -90)
            elif self.sender().objectName() == "pushButton_any_right":
                self.model.model_apps.set_alpha_beta(90, 90)
            self.anypoint_config.showing_config_mode_1()
            self.model.model_apps.create_maps_anypoint_mode_1()

        else:
            if self.sender().objectName() == "pushButton_any_up":
                self.model.model_apps.set_alpha_beta(90, 0)
            elif self.sender().objectName() == "pushButton_any_bottom":
                self.model.model_apps.set_alpha_beta(-90, 0)
            elif self.sender().objectName() == "pushButton_any_center":
                self.model.model_apps.set_alpha_beta(0, 0)
            elif self.sender().objectName() == "pushButton_any_left":
                self.model.model_apps.set_alpha_beta(0, -90)
            elif self.sender().objectName() == "pushButton_any_right":
                self.model.model_apps.set_alpha_beta(0, 90)
            self.anypoint_config.showing_config_mode_2()
            self.model.model_apps.create_maps_anypoint_mode_2()

    @classmethod
    def onclick_btn_github(cls):
        webbrowser.open('https://github.com/McutOIL', new=2)

    def onclick_button_menu(self):
        self.ctrl_apps.button_menu(220, True)

    def onclick_button_about_us(self):
        self.ctrl_apps.button_about_us(True, self.model.theme)

    def onclick_button_setting_menu(self):
        self.ctrl_apps.setting_menu(True, self.model.theme)

    def onclick_btn_open_media(self):
        cam_type, source_media, parameter_name = self.model.select_media_source()
        if source_media != '':
            self.model.model_apps.set_media_source(cam_type, source_media, parameter_name)
            self.resetStyle(self.ui.btn_anypoint_view)
            self.resetStyle(self.ui.btn_panorama_view)
            self.ui.btn_fisheye_view.setStyleSheet(self.set_style_selected_menu())
        else:
            QtWidgets.QMessageBox.information(None, "Information!", "You not select any file !!")

    @QtCore.pyqtSlot(float)
    def set_slider_position(self, value):
        self.ui.slider_video_time.blockSignals(True)
        self.ui.slider_video_time.setValue(value)
        self.ui.slider_video_time.blockSignals(False)

    @QtCore.pyqtSlot(list)
    def show_timer_video_info(self, list_timer):
        self.ui.label_curent_time.setText("%02d:%02d" % (list_timer[2], list_timer[3]))
        self.ui.label_total_time.setText("%02d:%02d" % (list_timer[0], list_timer[1]))

    @QtCore.pyqtSlot(list)
    def alpha_beta_from_coordinate(self, alpha_beta):
        if any(elem is None for elem in alpha_beta):
            self.ui.label_status_alpha.setText(str(0))
            self.ui.label_status_beta.setText(str(0))
        else:
            self.ui.label_status_alpha.setText(str(round(alpha_beta[0], 1)))
            self.ui.label_status_beta.setText(str(round(alpha_beta[1], 1)))

    @QtCore.pyqtSlot(object)
    def show_image_original(self, image):
        self.model.show_image_to_label(self.ui.label_image_original, image, 320)

    @QtCore.pyqtSlot(object)
    def get_image_result(self, image):
        self.__image_result = image
        self.show_image_result()

    def show_image_result(self, operation=None):
        if operation == "zoom_in":
            self.__width_image_result = self.ctrl_result_image.zoom_in(self.__width_image_result)
        elif operation == "zoom_out":
            self.__width_image_result = self.ctrl_result_image.zoom_out(self.__width_image_result)
        self.model.show_image_to_label(self.ui.label_result,
                                       self.__image_result,
                                       self.__width_image_result)

    def rotate_left(self):
        self.__angle_image_result = self.ctrl_result_image.rotate_left(self.__angle_image_result)
        self.model.model_apps.set_angle_rotate(self.__angle_image_result)

    def rotate_right(self):
        self.__angle_image_result = self.ctrl_result_image.rotate_right(self.__angle_image_result)
        self.model.model_apps.set_angle_rotate(self.__angle_image_result)

    def onclick_btn_fisheye(self):
        self.__state_view = "FisheyeView"
        self.change_stylesheet_selected_menu()
        if self.__image_result is not None:
            self.model.model_apps.set_state_view(self.__state_view)
            self.ui.widget_mode_view.hide()
            self.ui.frame_pointer_anypoint.hide()

    def onclick_btn_anypoint(self):
        self.__state_view = "AnypointView"
        self.change_stylesheet_selected_menu()
        if self.__image_result is not None:
            self.change_mode_anypoint()
            self.model.model_apps.set_state_view(self.__state_view)
            self.model.model_apps.calculate_alpha_beta()
            self.ui.widget_mode_view.show()
            self.ui.frame_pointer_anypoint.show()
            self.ui.widget_mode_view.setCurrentIndex(0)

    def onclick_btn_panorama(self):
        self.__state_view = "PanoramaView"
        self.change_stylesheet_selected_menu()
        if self.__image_result is not None:
            self.change_mode_panorama()
            self.model.model_apps.set_state_view(self.__state_view)
            self.ui.widget_mode_view.show()
            self.ui.frame_pointer_anypoint.show()
            self.ui.widget_mode_view.setCurrentIndex(1)

    # controller standard application user interface
    def onclick_reset_button(self):
        self.onclick_btn_fisheye()
        self.__image_result = None
        self.ui.label_result.setMinimumSize(QtCore.QSize(0, 0))
        self.ui.label_result.setMaximumSize(QtCore.QSize(700, 170))
        self.ui.label_result.setPixmap(QtGui.QPixmap("icons:moilapp.png"))
        self.ui.label_result.setScaledContents(True)
        self.ui.label_image_original.setMinimumSize(QtCore.QSize(0, 0))
        self.ui.label_image_original.setMaximumSize(QtCore.QSize(200, 50))
        self.ui.label_image_original.setPixmap(QtGui.QPixmap("icons:moilapp.png"))
        self.ui.label_image_original.setScaledContents(True)
        self.resetStyle(self.ui.btn_fisheye_view)
        self.resetStyle(self.ui.btn_anypoint_view)
        self.resetStyle(self.ui.btn_panorama_view)
        self.model.model_apps.reset_config()

    def escape_event(self):
        """
        Escape button keyboard event. Will return to the default state of application.

        Returns:

        """
        self.ctrl_apps.button_menu(70, True)
        width = self.ui.frame_additional_right.width()
        if width != 0:
            self.ctrl_apps.button_about_us(True, self.model.theme)
        width = self.ui.frame_additional_left.width()
        if width != 0:
            self.ctrl_apps.setting_menu(True, self.model.theme)

    def mouse_event_in_moil_logo(self, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.back_to_home()

    def back_to_home(self):
        self.ui.widget_container_content.setCurrentIndex(0)
        self.ui.frame_btn_moilapp.show()
        self.ui.frame_button_view.show()
        self.ui.delete_plugins_button.hide()
        self.ui.close_plugin_button.hide()
        self.ctrl_plugin.index = None

    def onclick_change_theme_apps(self):
        icon = QtGui.QIcon()
        if self.model.theme == "dark":
            color = "background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);"
            self.ui.statusBar.setStyleSheet(color)
            self.setStyleSheet(self.model.theme_light_mode())
            icon.addPixmap(QtGui.QPixmap("icons:sun.svg"), QtGui.QIcon.Mode.Normal,
                           QtGui.QIcon.State.Off)
            self.ui.btn_change_theme.setIcon(icon)

        elif self.model.theme == "light":
            color = "background-color: rgb(44, 49, 58); color: rgb(255, 255, 255);"
            self.ui.statusBar.setStyleSheet(color)
            self.setStyleSheet(self.model.theme_dark_mode())
            icon.addPixmap(QtGui.QPixmap("icons:light/moon.png"), QtGui.QIcon.Mode.Normal,
                           QtGui.QIcon.State.Off)
            self.ui.btn_change_theme.setIcon(icon)
        self.ctrl_plugin.refresh_theme_widget()

        if self.__image_result is not None:
            if self.__state_view == "FisheyeView":
                self.resetStyle(self.ui.btn_fisheye_view)
                self.ui.btn_fisheye_view.setStyleSheet(self.set_style_selected_menu())

            elif self.__state_view == "AnypointView":
                self.resetStyle(self.ui.btn_anypoint_view)
                self.ui.btn_anypoint_view.setStyleSheet(self.set_style_selected_menu())

            elif self.__state_view == "PanoramaView":
                self.resetStyle(self.ui.btn_panorama_view)
                self.ui.btn_panorama_view.setStyleSheet(self.set_style_selected_menu())

            else:
                self.resetStyle(self.ui.btn_setting)
                self.ui.btn_setting.setStyleSheet(self.set_style_selected_menu())

        width_left = self.ui.frame_additional_left.width()
        style = self.ui.btn_setting.styleSheet()
        color = "background-color: rgb(238, 238, 236);"
        color_dark = "background-color: rgb(33, 37, 43);"
        color_show = "background-color: rgb(255, 255, 255);"
        color_dark_show = "background-color: rgb(44, 49, 58);"

        if width_left == 0:
            self.ui.btn_setting.setStyleSheet(style + color)
            if self.model.theme == "dark":
                self.ui.btn_setting.setStyleSheet(style + color_dark)
        else:
            self.ui.btn_setting.setStyleSheet(style + color_show)
            if self.model.theme == "dark":
                self.ui.btn_setting.setStyleSheet(style + color_dark_show)

    def change_stylesheet_selected_menu(self):
        if self.__image_result is not None:
            btn = self.sender()
            self.resetStyle(btn.objectName())
            btn.setStyleSheet(self.set_style_selected_menu())

    # selected menu button
    def set_style_selected_menu(self):
        select = self.stylesheet_selected_menu_light_theme()
        if self.model.theme == "dark":
            select = self.stylesheet_selected_menu_dark_theme()
        return select

    # deselected menu button
    def set_style_deselect_menu(self, getStyle):
        deselect = getStyle.replace(self.stylesheet_selected_menu_light_theme(), "")
        if self.model.theme == "dark":
            deselect = getStyle.replace(self.stylesheet_selected_menu_dark_theme(), "")
        return deselect

    # reset selection button
    def resetStyle(self, widget):
        for w in self.ui.frame_button_view.findChildren(QtWidgets.QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(self.set_style_deselect_menu(w.styleSheet()))

    @classmethod
    def stylesheet_selected_menu_dark_theme(cls):
        stylesheet = """
            border-left: 22px solid 
            qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), 
            stop:0.5 rgba(85, 170, 255, 0));
            background-color: rgb(45, 49, 55);
        """
        return stylesheet

    @classmethod
    def stylesheet_selected_menu_light_theme(cls):
        stylesheet = """
            border-left: 22px solid 
            qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(47, 55, 58, 255), 
            stop:0.5 rgba(85, 170, 255, 0));
            background-color: rgb(248, 248, 248);
        """
        return stylesheet
