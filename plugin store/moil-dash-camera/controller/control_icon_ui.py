from PyQt6 import QtGui, QtCore


class ControlIconInUI:
    def __init__(self, controller):
        super(ControlIconInUI, self).__init__()
        self.controller = controller
        self.video_controller_icon()
        self.dash_controller_icon()
        self.configuration_media_control_icon()

    def video_controller_icon(self):
        self.controller.ui.btn_play_pause_dash.setIcon(self.controller.model.icon.get_icon_play_video())
        self.controller.ui.btn_rewind_dash.setIcon(self.controller.model.icon.get_icon_rewind_video())
        self.controller.ui.btn_stop_dash.setIcon(self.controller.model.icon.get_icon_resume_video())
        self.controller.ui.btn_forward_dash.setIcon(self.controller.model.icon.get_icon_forward_video())

    def dash_controller_icon(self):
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(self.model.icon.get_icon_moilapp()), QtGui.QIcon.Mode.Normal,
        #                QtGui.QIcon.State.Off)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("controllers/plugins/moil-dash-camera/controller/icon/home.png"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.ui.btn_home_dash.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("controllers/plugins/moil-dash-camera/controller/icon/page-24.png"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.ui.btn_panorama_view_dash.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("controllers/plugins/moil-dash-camera/controller/icon/page-5.png"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.ui.btn_left_window_dash.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("controllers/plugins/moil-dash-camera/controller/icon/driver_view.png"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.ui.btn_driver_view_dash.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("controllers/plugins/moil-dash-camera/controller/icon/second_driver_view.png"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.ui.btn_second_driver_view_dash.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("controllers/plugins/moil-dash-camera/controller/icon/page-6.png"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.ui.btn_right_window_dash.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("controllers/plugins/moil-dash-camera/controller/icon/original_fisheye.png"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.ui.btn_original_view_dash.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("controllers/plugins/moil-dash-camera/controller/icon/screenshot.png"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.ui.btn_screenshot_active_image_dash.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("controllers/plugins/moil-dash-camera/controller/icon/settings-solid.png"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.ui.btn_dash_setting_dash.setIcon(icon)

    def configuration_media_control_icon(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("controllers/plugins/moil-dash-camera/controller/icon/folder.png"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.ui.btn_source_config_dash.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("controllers/plugins/moil-dash-camera/controller/icon/text.svg"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.ui.btn_parameter_form_dash.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("controllers/plugins/moil-dash-camera/controller/icon/camera.png"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.ui.btn_change_camera_type_dash.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("controllers/plugins/moil-dash-camera/controller/icon/back.png"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.ui.btn_close_dash.setIcon(icon)


    def get_config_file(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/config_ui.yaml"

    def get_configuration_view_file(self):
        return "controllers/plugins/moil-dash-camera/controller/icon/configuration_view.yaml"

    def get_parameter_file(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/camera_parameters.json"

    def get_maps_x_panorama_dash(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/map_x_image_panorama_dash.npy"

    def get_maps_y_panorama_dash(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/map_y_image_panorama_dash.npy"

    def get_maps_x_panorama_x(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/map_x_panorama_x.npy"

    def get_maps_y_panorama_x(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/map_y_panorama_x.npy"

    def get_maps_x_anypoint_mode_2(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/map_x_anypoint_mode_2.npy"

    def get_maps_y_anypoint_mode_2(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/map_y_anypoint_mode_2.npy"

    def get_maps_x_anypoint_left(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/map_x_left_window.npy"

    def get_maps_y_anypoint_left(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/map_y_left_window.npy"

    def get_maps_x_anypoint_right(self):
        return ".controllers/plugins/moil-dash-camera/controller/data_config/map_x_right_window.npy"

    def get_maps_y_anypoint_right(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/map_y_right_window.npy"

    def get_maps_x_anypoint_driver(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/map_x_driver_view.npy"

    def get_maps_y_anypoint_driver(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/map_y_driver_view.npy"

    def get_maps_x_anypoint_second_driver(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/map_x_second_driver_view.npy"

    def get_maps_y_anypoint_second_driver(self):
        return "controllers/plugins/moil-dash-camera/controller/data_config/map_y_second_driver_view.npy"
