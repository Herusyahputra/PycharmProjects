"""
This Class is to provide model for moilapp application. to make it not make confuse on the plugin class
"""
import cv2
import os
import yaml
from PyQt6.QtCore import pyqtSignal, QObject, Qt, QTimer
from PyQt6.QtWidgets import QMessageBox


class ModelApps(QObject):
    image_original = pyqtSignal(object)
    image_result = pyqtSignal(object)
    alpha_beta = pyqtSignal(list)
    slider_time_value = pyqtSignal(float)
    timer_video_info = pyqtSignal(list)
    timer_status = pyqtSignal(bool)

    def __init__(self, model):
        super().__init__()

        self.__model = model
        self.__image = None
        self.__moildev = None
        self.__media_source = None
        self.__parameter_name = None
        self.__state_view = "FisheyeView"
        self.__pano_mode = "car"
        self.__anypoint_mode = "mode_1"
        self.__angle_rotate = None
        self.__map_x_anypoint = None
        self.__map_y_anypoint = None
        self.__map_x_pano = None
        self.__map_y_pano = None
        self.__configuration_view = None
        self.__config_file = None
        self.__ratio_x, self.__ratio_y = None, None
        self.__pos_x, self.__pos_y = None, None
        self.__image_original = None
        self.__draw_polygon = True

        self.cap = None
        self.video = False
        self.fps = 25
        self.i_camera = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame_signal)

    def update_file_config(self):
        path_file = os.path.dirname(os.path.realpath(__file__))
        self.__config_file = path_file + "/cached/cache_config.yaml"
        if os.path.exists(self.__config_file):
            with open(self.__config_file, "r") as file:
                self.__configuration_view = yaml.safe_load(file)

    def set_media_source(self, cam_type, media_source, parameter_name):
        if self.__configuration_view is not None:
            self.__configuration_view["Cam_type"] = cam_type
            self.__configuration_view["Media_path"] = media_source
            self.__configuration_view["Parameter_name"] = parameter_name
            with open(self.__config_file, "w") as outfile:
                yaml.dump(self.__configuration_view, outfile, default_flow_style=False)
        self.__media_source = media_source
        self.__parameter_name = parameter_name
        self.create_moildev()
        self.create_image_original()

    def set_anypoint_mode(self, mode):
        self.__anypoint_mode = mode

    def set_state_view(self, state_view):
        self.__state_view = state_view
        self.manipulate_image()

    def set_draw_polygon(self, state):
        self.__draw_polygon = state
        self.manipulate_image()

    def mouse_move_event_label_original(self, label, event):
        if self.__image is not None:
            self.__ratio_x, self.__ratio_y = self.__model.calculate_ratio_image2label(label, self.__image)
            x = round(int(event.position().x()) * self.__ratio_x)
            y = round(int(event.position().y()) * self.__ratio_y)
            if self.__state_view == "FisheyeView":
                image = self.__model.marker.point(self.__image.copy(), (x, y))

            elif self.__state_view == "AnypointView":
                image = self.__model.marker.point(self.__image_original.copy(), (x, y))
                if self.__anypoint_mode == "mode_1":
                    alpha, beta = self.__moildev.get_alpha_beta(x, y, 1)
                else:
                    alpha, beta = self.__moildev.get_alpha_beta(x, y, 2)
                self.alpha_beta.emit([alpha, beta])

            else:
                image = self.__model.marker.point(self.__image_original.copy(), (x, y))
                alpha, beta = self.__moildev.get_alpha_beta(x, y, 1)
                self.alpha_beta.emit([alpha, beta])
            self.draw_crosshair_original_image(image)

    def mouse_leave_event_label_original(self, event):
        if self.__image is not None:
            self.calculate_alpha_beta()

    def calculate_alpha_beta(self):
        if self.__state_view == "AnypointView":
            self.draw_crosshair_original_image(self.__image_original.copy())
            if self.__anypoint_mode == "mode_1":
                if self.__configuration_view["Mode_1"]["coord"][0] is None:
                    alpha, beta = 0, 0
                else:
                    alpha, beta = self.__moildev.get_alpha_beta(
                        self.__configuration_view["Mode_1"]["coord"][0],
                        self.__configuration_view["Mode_1"]["coord"][1], 1)
            else:
                if self.__configuration_view["Mode_2"]["coord"][0] is None:
                    alpha, beta = 0, 0
                else:
                    alpha, beta = self.__moildev.get_alpha_beta(
                        self.__configuration_view["Mode_2"]["coord"][0],
                        self.__configuration_view["Mode_2"]["coord"][1], 2)
            self.alpha_beta.emit([alpha, beta])

        elif self.__state_view == "PanoramaView":
            self.draw_crosshair_original_image(self.__image_original.copy())
            if self.__pano_mode == "car":
                if self.__configuration_view["Pano_car"]["coord"][0] is None:
                    alpha, beta = 0, 0
                else:
                    alpha, beta = self.__moildev.get_alpha_beta(
                        self.__configuration_view["Pano_car"]["coord"][0],
                        self.__configuration_view["Pano_car"]["coord"][1], 1)
            else:
                alpha, beta = 0, 0

            self.alpha_beta.emit([alpha, beta])

        else:
            self.draw_crosshair_original_image(self.__image.copy())

    def mouse_press_event_label_original(self, event):
        pos_x = round(int(event.position().x()) * self.__ratio_x)
        pos_y = round(int(event.position().y()) * self.__ratio_y)
        if self.__state_view == "AnypointView":
            if self.__anypoint_mode == "mode_1":
                self.__configuration_view["Mode_1"]["coord"][0] = pos_x
                self.__configuration_view["Mode_1"]["coord"][1] = pos_y
                alpha, beta = self.__moildev.get_alpha_beta(round(pos_x), round(pos_y), 1)

                if alpha is not None:
                    self.__configuration_view["Mode_1"]["alpha"] = round(alpha, 1)
                    self.__configuration_view["Mode_1"]["beta"] = round(beta, 1)

            else:
                self.__configuration_view["Mode_2"]["coord"][0] = round(pos_x)
                self.__configuration_view["Mode_2"]["coord"][1] = round(pos_y)
                alpha, beta = self.__moildev.get_alpha_beta(round(pos_x), round(pos_y), 2)
                if alpha is not None:
                    self.__configuration_view["Mode_2"]["pitch"] = round(alpha, 1)
                    self.__configuration_view["Mode_2"]["yaw"] = round(beta, 1)

        elif self.__state_view == "PanoramaView":
            if self.__pano_mode == "car":
                self.__configuration_view["Pano_car"]["coord"][0] = round(pos_x)
                self.__configuration_view["Pano_car"]["coord"][1] = round(pos_y)

                alpha, beta = self.__moildev.get_alpha_beta(round(pos_x), round(pos_y), 1)
                if alpha is not None:
                    self.__configuration_view["Pano_car"]["alpha"] = round(alpha, 1)
                    self.__configuration_view["Pano_car"]["beta"] = round(beta, 1)

        with open(self.__config_file, "w") as outfile:
            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)
        self.draw_crosshair_original_image(self.__image_original.copy())

    def set_alpha_beta(self, alpha, beta, state=True):
        if self.__anypoint_mode == "mode_1":
            self.__configuration_view["Mode_1"]["alpha"] = alpha
            self.__configuration_view["Mode_1"]["beta"] = beta
            if any([alpha > 110, beta > 110]):
                alpha = alpha - 90
                beta = beta - 90
            self.__configuration_view["Mode_1"]["coord"][0] = round(self.__moildev.get_rho_from_alpha(alpha))
            self.__configuration_view["Mode_1"]["coord"][1] = round(self.__moildev.get_rho_from_alpha(beta))
        else:
            self.__configuration_view["Mode_2"]["pitch"] = alpha
            self.__configuration_view["Mode_2"]["yaw"] = beta
            if any([alpha > 110, beta > 110]):
                alpha = alpha - 90
                beta = beta - 90
            self.__configuration_view["Mode_2"]["coord"][0] = round(self.__moildev.get_rho_from_alpha(alpha))
            self.__configuration_view["Mode_2"]["coord"][1] = round(self.__moildev.get_rho_from_alpha(beta))

        with open(self.__config_file, "w") as outfile:
            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)
        if state:
            self.draw_crosshair_original_image(self.__image_original.copy())

    def reset_config(self):
        self.__configuration_view["Media_path"] = None
        self.__configuration_view["Cam_type"] = None
        self.__configuration_view["Parameter_name"] = None
        self.__configuration_view["Mode_1"] = {}
        self.__configuration_view["Mode_1"]["coord"] = [None, None]
        self.__configuration_view["Mode_1"]["alpha"] = 0
        self.__configuration_view["Mode_1"]["beta"] = 0
        self.__configuration_view["Mode_1"]["zoom"] = 4
        self.__configuration_view["Mode_2"] = {}
        self.__configuration_view["Mode_2"]["coord"] = [None, None]
        self.__configuration_view["Mode_2"]["pitch"] = 0
        self.__configuration_view["Mode_2"]["yaw"] = 0
        self.__configuration_view["Mode_2"]["roll"] = 0
        self.__configuration_view["Mode_2"]["zoom"] = 4
        self.__configuration_view["Pano_tube"] = {}
        self.__configuration_view["Pano_tube"]["alpha_min"] = 8
        self.__configuration_view["Pano_tube"]["alpha_max"] = 110
        self.__configuration_view["Pano_tube"]["crop_top"] = 0
        self.__configuration_view["Pano_tube"]["crop_bottom"] = 1
        self.__configuration_view["Pano_car"] = {}
        self.__configuration_view["Pano_car"]["coord"] = [None, None]
        self.__configuration_view["Pano_car"]["alpha"] = 0
        self.__configuration_view["Pano_car"]["beta"] = 0
        self.__configuration_view["Pano_car"]["crop_left"] = 0
        self.__configuration_view["Pano_car"]["crop_right"] = 1
        self.__configuration_view["Pano_car"]["crop_top"] = 0
        self.__configuration_view["Pano_car"]["crop_bottom"] = 1

        with open(self.__config_file, "w") as outfile:
            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)

    def create_image_original(self):
        if self.__configuration_view is not None:
            if self.__configuration_view["Media_path"] is not None:
                self.__media_source = self.__configuration_view["Media_path"]
                try:
                    if isinstance(self.__media_source, int) or self.__media_source.endswith('.mjpg'):
                        self.cap = self.__model.moil_camera(cam_type=self.__configuration_view["Cam_type"],
                                                            cam_id=self.__media_source, resolution=(2592, 1944))
                        self.video = False
                        self.timer.start()
                        self.timer_status.emit(self.timer.isActive())
                        print("streaming camera")

                    elif self.__media_source.endswith(tuple(['.mp4', '.MOV', '.avi'])):
                        self.cap = cv2.VideoCapture(self.__media_source)
                        self.video = True
                        self.next_frame_signal()
                        self.timer.stop()
                        self.timer_status.emit(self.timer.isActive())
                        print("video source")

                    elif self.__media_source.endswith(tuple(['.jpeg', '.JPG', '.jpg', '.png', 'TIFF'])):
                        print("image source")
                        self.cap = None
                        self.timer.stop()
                        self.__image = cv2.imread(self.__media_source)
                        print(self.__image.shape)
                        self.manipulate_image()
                        self.timer_status.emit(self.timer.isActive())

                    else:
                        print("some error")

                except:
                    QMessageBox.warning(None, "Warning", "Cant load the history, have error in media source\n"
                                                         "Please check that your camera is on plug or \n"
                                                         "the file is exist!.")
                    print("some error in media_source")

    def next_frame_signal(self):
        if self.cap is not None:
            if self.video:
                success, self.__image = self.cap.read()
                if success:
                    self.pos_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                    self.total_frame = float(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    # print(self.pos_frame, self.frame_count)
                    self.manipulate_image()
                    self.set_slider_video_time_position()
                    duration_sec = int(self.total_frame / self.fps)
                    total_minutes = duration_sec // 60
                    duration_sec %= 60
                    total_seconds = duration_sec
                    sec_pos = int(self.pos_frame / self.fps)
                    recent_minute = int(sec_pos // 60)
                    sec_pos %= 60
                    recent_sec = sec_pos
                    self.timer_video_info.emit([total_minutes, total_seconds, recent_minute, recent_sec])
                else:
                    self.timer.stop()

            else:
                self.__image = self.cap.frame()
                self.manipulate_image()
                self.timer_video_info.emit([0, 0, 0, 0])
                self.i_camera += 1

    def play_pause_video(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(1000 / self.fps)
        self.timer_status.emit(self.timer.isActive())

    def stop_video(self):
        if self.cap is not None:
            if self.video:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.timer.stop()
                self.next_frame_signal()

    def rewind_video_5_second(self):
        if self.cap is not None:
            if self.video:
                position = self.pos_frame - 5 * self.fps
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
                self.next_frame_signal()

    def forward_video_5_second(self):
        if self.cap is not None:
            if self.video:
                position = self.pos_frame + 5 * self.fps
                if position > self.total_frame:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.total_frame - 1)
                else:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)

                self.next_frame_signal()

    def slider_controller(self, value):
        if self.cap is not None:
            if self.video:
                dst_frame = self.total_frame * value / 100
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, dst_frame)
                self.next_frame_signal()

    def set_slider_video_time_position(self):
        if self.cap is not None:
            if self.video:
                dst_value = self.pos_frame * 100 / self.total_frame
                self.slider_time_value.emit(dst_value)

    def create_moildev(self):
        if self.__configuration_view is not None:
            if self.__configuration_view["Parameter_name"] is not None:
                self.__parameter_name = self.__configuration_view["Parameter_name"]
                self.__moildev = self.__model.connect_to_moildev(parameter_name=self.__parameter_name)
                self.__pos_x, self.__pos_y = self.__moildev.icx, self.__moildev.icy

    def manipulate_image(self):
        if self.__state_view == "FisheyeView":
            image_result = self.__model.rotate_image(self.__image, self.__angle_rotate)
            self.draw_crosshair_original_image(self.__image.copy())

        elif self.__state_view == "AnypointView":
            image_result = self.__model.rotate_image(self.__image, self.__angle_rotate)
            image_result = self.__model.remap_image(image_result, self.__map_x_anypoint, self.__map_y_anypoint)
            if self.__draw_polygon:
                self.__image_original = self.__model.draw_polygon(self.__image.copy(), self.__map_x_anypoint,
                                                                  self.__map_y_anypoint)
            else:
                self.__image_original = self.__image.copy()
            self.draw_crosshair_original_image(self.__image_original.copy())

        elif self.__state_view == "PanoramaView":
            image_result = self.__model.rotate_image(self.__image, self.__angle_rotate)
            image_result = self.__model.remap_image(image_result, self.__map_x_pano, self.__map_y_pano)
            image_result = self.__crop_panorama(image_result)
            if self.__draw_polygon:
                self.__image_original = self.__model.draw_polygon(self.__image.copy(),
                                                                  self.__map_x_pano,
                                                                  self.__map_y_pano)
            else:
                self.__image_original = self.__image.copy()
            self.draw_crosshair_original_image(self.__image_original.copy())

        else:
            image_result = None
        self.image_result.emit(image_result)

    def change_panorama_mode(self, mode):
        self.__pano_mode = mode

    def set_angle_rotate(self, angle_rotate):
        self.__angle_rotate = angle_rotate
        self.manipulate_image()

    def draw_crosshair_original_image(self, image):
        with open(self.__config_file, "r") as file:
            configuration_view = yaml.safe_load(file)
        if self.__state_view == "FisheyeView":
            x = self.__moildev.icx
            y = self.__moildev.icy

        elif self.__state_view == "AnypointView":
            if self.__anypoint_mode == "mode_1":
                if any([configuration_view["Mode_1"]["coord"][0] is None,
                        configuration_view["Mode_1"]["coord"][0] == 0]):
                    x = self.__moildev.icx
                    y = self.__moildev.icy
                else:
                    x = configuration_view["Mode_1"]["coord"][0]
                    y = configuration_view["Mode_1"]["coord"][1]

            else:
                if any([configuration_view["Mode_2"]["coord"][0] is None,
                        configuration_view["Mode_2"]["coord"][0] == 0]):
                    x = self.__moildev.icx
                    y = self.__moildev.icy
                else:
                    x = configuration_view["Mode_2"]["coord"][0]
                    y = configuration_view["Mode_2"]["coord"][1]
        else:
            if self.__pano_mode == "car":
                if any([configuration_view["Pano_car"]["coord"][0] is None,
                        configuration_view["Pano_car"]["coord"][0] == 0]):
                    x = self.__moildev.icx
                    y = self.__moildev.icy
                else:
                    x = configuration_view["Pano_car"]["coord"][0]
                    y = configuration_view["Pano_car"]["coord"][1]
            else:
                x = self.__moildev.icx
                y = self.__moildev.icy

        image = self.__model.marker.crosshair(image, (x, y))
        self.image_original.emit(image)

    def __crop_panorama(self, image):
        with open(self.__config_file, "r") as file:
            configuration_view = yaml.safe_load(file)
        if self.__pano_mode == "car":
            image = cv2.resize(image, (image.shape[1] * 2, image.shape[0]))
            crop_left = configuration_view["Pano_car"]["crop_left"]
            crop_right = configuration_view["Pano_car"]["crop_right"]
            crop_top = configuration_view["Pano_car"]["crop_top"]
            crop_bottom = configuration_view["Pano_car"]["crop_bottom"]
            image = self.__model.cropping_image(image, crop_left, crop_right, crop_top, crop_bottom)
        else:
            crop_top = configuration_view["Pano_tube"]["crop_top"]
            crop_bottom = configuration_view["Pano_tube"]["crop_bottom"]
            image = self.__model.cropping_image(image, 0, 1, crop_top, crop_bottom)
        return image

    def create_maps_anypoint_mode_1(self):
        if os.path.exists(self.__config_file):
            with open(self.__config_file, "r") as file:
                configuration_view = yaml.safe_load(file)
            alpha = configuration_view["Mode_1"]["alpha"]
            beta = configuration_view["Mode_1"]["beta"]
            zoom = configuration_view["Mode_1"]["zoom"]
            if self.__moildev is not None:
                self.__map_x_anypoint, self.__map_y_anypoint = self.__moildev.maps_anypoint_mode1(alpha, beta, zoom)
                self.manipulate_image()

    def create_maps_anypoint_mode_2(self):
        if os.path.exists(self.__config_file):
            with open(self.__config_file, "r") as file:
                configuration_view = yaml.safe_load(file)
            pitch = configuration_view["Mode_2"]["pitch"]
            yaw = configuration_view["Mode_2"]["yaw"]
            roll = configuration_view["Mode_2"]["roll"]
            zoom = configuration_view["Mode_2"]["zoom"]
            if self.__moildev is not None:
                self.__map_x_anypoint, self.__map_y_anypoint = self.__moildev.maps_anypoint_mode2(pitch, yaw, roll,
                                                                                                  zoom)
                self.manipulate_image()

    def create_maps_panorama_car(self):
        if os.path.exists(self.__config_file):
            with open(self.__config_file, "r") as file:
                configuration_view = yaml.safe_load(file)
            alpha = configuration_view["Pano_car"]["alpha"]
            beta = configuration_view["Pano_car"]["beta"]
            if self.__moildev is not None:
                alpha_max = self.__moildev.camera_fov / 2
                self.__map_x_pano, self.__map_y_pano = self.__moildev.maps_panorama_car(alpha_max,
                                                                                        alpha, beta, 0, 1)
                self.manipulate_image()

    def create_maps_panorama_tube(self):
        if os.path.exists(self.__config_file):
            with open(self.__config_file, "r") as file:
                configuration_view = yaml.safe_load(file)
            alpha_min = configuration_view["Pano_tube"]["alpha_min"]
            alpha_max = configuration_view["Pano_tube"]["alpha_max"]
            if self.__moildev is not None:
                self.__map_x_anypoint, self.__map_y_anypoint = self.__moildev.maps_panorama_tube(alpha_min, alpha_max)
                self.manipulate_image()
