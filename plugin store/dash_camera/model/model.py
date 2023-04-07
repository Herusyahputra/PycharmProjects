import os
import yaml
from PyQt6.QtCore import pyqtSignal, QObject
import cv2
from .model_multithreading import Multithreading
from .file_maps import FileMaps
import numpy as np
from .model_birds_view import ModelBirdView
from .process_bird_view_4_cam_center_clicked import merge_image_4_camera_center_clicked
from .process_bird_view_4_cam_center_config import merge_image_4_camera_center_config


class ModelPlugin(QObject):
    original_image_dash_cam = pyqtSignal(object)
    original_image_bird_view = pyqtSignal(list)
    dash_camera_info = pyqtSignal(list)
    result_dash_image = pyqtSignal(object)
    result_bird_view = pyqtSignal(object)
    result_bird_view_overlap = pyqtSignal(object)
    result_anypoint_dash_cam = pyqtSignal(object)
    signal_video_duration = pyqtSignal(list)
    signal_video_slider_position = pyqtSignal(float)
    signal_show_config_to_ui = pyqtSignal(bool)

    def __init__(self, model):
        super().__init__()
        self.model_moil = model
        self.map_y_dash_front = None
        self.map_x_dash_front = None
        self.cap = None
        self.image = None
        self.media_source_type = None
        # self.__width_result_image = 1000

        # Birds view
        self.model_bird_view = ModelBirdView()

        # video properties
        self.pos_frame = 0
        self.frame_count = 0
        self.total_minute = 0
        self.total_second = 0
        self.current_minute = 0
        self.current_second = 0

        self.__dash_image_mode = "Dash_front_view"
        self.__anypoint_image_mode = "Left Window"

        self.file_maps = FileMaps()
        self.mode_calibration = None
        path_file = os.path.dirname(os.path.realpath(__file__))
        self.cached_file = path_file + "/cached/cache_config.yaml"

    def set_mode_calibration(self, mode):
        self.mode_calibration = mode

    def set_load_config_file(self, path):
        self.cached_file = path
        path_list = path.split(os.sep)
        self.file_maps.change_folder_config("/".join(path_list[-3:-1]))

    def draw_fov_in_original_image(self, status):
        images = [None] * 4
        for i, image in enumerate(self.model_bird_view.image):
            if status and image is not None:
                maps_x, maps_y = self.model_bird_view.moildev[i].maps_panorama_tube(10, 90)
                image = self.model_moil.draw_polygon(image.copy(), maps_x, maps_y)
                images[i] = image
            else:
                images[i] = image.copy()
        self.original_image_bird_view.emit(images)

    # def create_maps_turn_left(self):

    # @property
    # def width_result_image(self):
    #     return self.__width_result_image
    #
    # @width_result_image.setter
    # def width_result_image(self, width):
    #     self.__width_result_image = width

    @property
    def set_dash_image_mode(self):
        return self.__dash_image_mode

    @set_dash_image_mode.setter
    def set_dash_image_mode(self, mode):
        self.__dash_image_mode = mode

    @property
    def set_anypoint_image_mode(self):
        return self.__anypoint_image_mode

    @set_anypoint_image_mode.setter
    def set_anypoint_image_mode(self, mode):
        self.__anypoint_image_mode = mode

    @classmethod
    def control_contrast(cls, img, brightness=255, contrast=127):
        brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
        contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))
        if brightness != 0:

            if brightness > 0:
                shadow = brightness
                max = 255

            else:
                shadow = 0
                max = 255 + brightness

            al_pha = (max - shadow) / 255
            ga_mma = shadow

            # The function addWeighted calculates
            # the weighted sum of two arrays
            cal = cv2.addWeighted(img, al_pha, img, 0, ga_mma)

        else:
            cal = img

        if contrast != 0:
            Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
            Gamma = 127 * (1 - Alpha)

            # The function addWeighted calculates
            # the weighted sum of two arrays
            cal = cv2.addWeighted(cal, Alpha, cal, 0, Gamma)

        return cal

    def add_image_path_to_config_file(self, path, parameter, image_index=None):
        with open(self.cached_file, "r") as file:
            confi_view = yaml.safe_load(file)

        if self.mode_calibration == "Dash camera":
            confi_view["Dash_Camera"]["Source"] = path
            confi_view["Dash_Camera"]["Parameter_name"] = parameter
        else:
            confi_view["Bird_View"]["Image"][f'Image_{image_index}']["Source"] = path
            confi_view["Bird_View"]["Image"][f'Image_{image_index}']["Parameter_name"] = parameter

        with open(self.cached_file, "w") as outfile:
            yaml.dump(confi_view, outfile, default_flow_style=False)

    def process_source_image(self, image_index=None, new_parameter=False):
        with open(self.cached_file, "r") as file:
            confi_view = yaml.safe_load(file)
        if self.mode_calibration == "Dash camera":
            media_source = confi_view["Dash_Camera"]["Source"]
            if isinstance(media_source, int) or media_source.endswith('.mjpg'):
                self.media_source_type = "Streaming"
                self.cap = Multithreading(media_source)

            elif media_source.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmg")):
                self.media_source_type = "Image"
                self.image = cv2.imread(media_source)
                self.cap = None

            elif media_source.endswith((".avi", ".mp4")):
                self.media_source_type = "Video"
                self.cap = cv2.VideoCapture(media_source)

            else:
                print("Have error in opening media source")
                self.cap = None

            self.information_dash_camera()
            if new_parameter:
                self.create_initial_maps_dash_camera()
            else:
                self.load_maps_dash_camera_from_cached()

        else:
            print("Now is birds view")
            if confi_view["Bird_View"]["Image"][f'Image_{image_index}']["Source"] is not None:
                parameter_name = confi_view["Bird_View"]["Image"][f'Image_{image_index}']["Parameter_name"]
                self.model_bird_view.moildev[image_index - 1] = self.model_moil.connect_to_moildev(parameter_name)
                media_source = confi_view["Bird_View"]["Image"][f'Image_{image_index}']["Source"]
                if isinstance(media_source, int) or media_source.endswith('.mjpg'):
                    self.model_bird_view.media_source_type = "Streaming"
                    self.model_bird_view.cap[image_index - 1] = Multithreading(media_source)

                elif media_source.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmg")):
                    self.model_bird_view.media_source_type = "Image"
                    self.model_bird_view.image[image_index - 1] = cv2.imread(media_source)

                elif media_source.endswith((".avi", ".mp4")):
                    self.model_bird_view.media_source_type = "Video"
                    self.model_bird_view.cap[image_index] = cv2.VideoCapture(media_source)

                self.create_maps_anypoint_bird_view(image_index)

        self.next_frame_process()

    # control video here
    def next_frame_process(self):
        if self.mode_calibration == "Dash camera":
            if self.media_source_type == "Image":
                if self.image is not None:
                    self.process_to_result_image()

            else:
                if self.cap is None:
                    return

                if self.media_source_type in ("Video", "usb_cam"):
                    success, self.image = self.cap.read()
                    if success:
                        self.process_to_result_image()

                        if self.media_source_type == "Video":
                            self.video_duration()

                else:
                    self.image = self.cap.get_frame()
                    if self.image is not None:
                        self.process_to_result_image()

        else:
            if self.model_bird_view.media_source_type == "Image":
                if self.image is not None:
                    self.process_to_result_image()

    def process_to_result_image(self):
        if self.mode_calibration == "Dash camera":
            self.original_image_dash_cam.emit(self.image)
            self.create_dash_image()
            self.create_anypoint_image()
        else:
            self.original_image_bird_view.emit(self.model_bird_view.image)

    def video_duration(self):
        """
            This function is for get time of video
        Returns:
            None
        """
        try:
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.pos_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration_sec = int(self.frame_count / fps)

            self.total_minute = int(duration_sec // 60)
            duration_sec %= 60
            self.total_second = duration_sec
            sec_pos = int(self.pos_frame / fps)
            self.current_minute = int(sec_pos // 60)
            sec_pos %= 60
            self.current_second = sec_pos
            list_vid_duration = [self.total_minute, self.total_second,
                                 self.current_minute, self.current_second]
            dst = self.pos_frame * 100 / self.frame_count
            self.signal_video_slider_position.emit(dst)
            self.signal_video_duration.emit(list_vid_duration)

        except:
            print("error in video source")

    def reset_total_video_time(self):
        """
            This function is for set properties video total length is 0
        Returns:
            None
        """
        self.total_minute = 0
        self.total_second = 0

    def stop_video(self):
        """
            This function is set video in to frame 0
        Returns:
            None
        """
        if self.image is not None:
            if self.cap is not None:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.next_frame_process()

    def forward_video(self):
        """
            This function is for forward video frame for 5 seconds
        Returns:
            None
        """
        if self.image is not None:
            if self.cap is not None:
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                position = self.pos_frame + 5 * fps
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
                self.next_frame_process()

    def rewind_video(self):
        """
            This function is for rewind video frame for 5 seconds
        Returns:
            None
        """
        if self.image is not None:
            if self.cap is not None:
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                position = self.pos_frame - 5 * fps
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
                self.next_frame_process()

    def slider_controller(self, value, slider_maximum):
        """
            This function is for change video position base on input slider
        Args:
            value: current slider position
            slider_maximum: value maximum slider video
        Returns:
            None
        """
        if self.image is not None:
            if self.cap is not None:
                dst = self.frame_count * value / slider_maximum
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, dst - 1)
                self.next_frame_process()

    def get_value_slider_video(self, value):
        """
            This function is for get current position slider time base on position slider maximum
        Args:
            value: value slider maximum
        Returns:
            None
        """
        return self.pos_frame * (value + 1) / self.frame_count

    # ######### Birds View #########
    def change_gradient_mode(self, mode):
        with open(self.cached_file, "r") as file:
            config = yaml.safe_load(file)
            config["Bird_View"]["Gradient_mode"] = mode
        with open(self.cached_file, "w") as outfile:
            yaml.dump(config, outfile, default_flow_style=False)

    def create_maps_anypoint_bird_view(self, image_index):
        print(f'{image_index}')
        with open(self.cached_file, "r") as file:
            config = yaml.safe_load(file)

        rotate = config["Bird_View"]["Image"][f'Image_{image_index}']["rotate"]
        zoom = config["Bird_View"]["Image"][f'Image_{image_index}']["zoom"]
        alpha = config["Bird_View"]["Image"][f'Image_{image_index}']["alpha"]
        beta = config["Bird_View"]["Image"][f'Image_{image_index}']["beta"]
        if self.model_bird_view.image[image_index - 1] is not None:
            map_x_anypoint, map_y_anypoint = self.model_bird_view.moildev[image_index - 1].maps_anypoint_mode2(alpha,
                                                                                                               beta,
                                                                                                               0, zoom)
            path_map_x_anypoint, path_map_y_anypoint = self.get_path_maps_image(f'Image_{image_index}')
            np.save(path_map_x_anypoint, map_x_anypoint)
            np.save(path_map_y_anypoint, map_y_anypoint)
        self.create_remap_image_anypoint_bird_view(image_index)

    def get_path_maps_image(self, key):
        if key == "Image_1":
            path_map_x_anypoint = self.file_maps.get_maps_x_anypoint_image_1_bird_view()
            path_map_y_anypoint = self.file_maps.get_maps_y_anypoint_image_1_bird_view()
        elif key == "Image_2":
            path_map_x_anypoint = self.file_maps.get_maps_x_anypoint_image_2_bird_view()
            path_map_y_anypoint = self.file_maps.get_maps_y_anypoint_image_2_bird_view()
        elif key == "Image_3":
            path_map_x_anypoint = self.file_maps.get_maps_x_anypoint_image_3_bird_view()
            path_map_y_anypoint = self.file_maps.get_maps_y_anypoint_image_3_bird_view()
        elif key == "Image_4":
            path_map_x_anypoint = self.file_maps.get_maps_x_anypoint_image_4_bird_view()
            path_map_y_anypoint = self.file_maps.get_maps_y_anypoint_image_4_bird_view()
        else:
            path_map_x_anypoint = None
            path_map_y_anypoint = None

        return path_map_x_anypoint, path_map_y_anypoint

    def create_remap_image_anypoint_bird_view(self, index):
        with open(self.cached_file, "r") as file:
            config = yaml.safe_load(file)

        rotate = config["Bird_View"]["Image"][f'Image_{index}']["rotate"]
        path_map_x_anypoint, path_map_y_anypoint = self.get_path_maps_image(f'Image_{index}')
        if self.model_bird_view.image[index - 1] is not None and path_map_x_anypoint is not None:
            map_x = np.load(path_map_x_anypoint)
            map_y = np.load(path_map_y_anypoint)
            image = self.model_moil.rotate_image(self.model_bird_view.image[index - 1].copy(), rotate)
            self.model_bird_view.anypoint[index - 1] = self.model_moil.remap_image(image, map_x, map_y)

        self.create_bird_view_image()

    def create_bird_view_image(self):
        with open(self.cached_file, "r") as file:
            config = yaml.safe_load(file)
        image = self.model_bird_view.anypoint
        if all(x is not None for x in image):
            keys = list(config["Bird_View"]["Image"])
            shift_x = [config["Bird_View"]["Image"][keys[0]]["x_axis"],
                       config["Bird_View"]["Image"][keys[1]]["x_axis"],
                       config["Bird_View"]["Image"][keys[2]]["x_axis"],
                       config["Bird_View"]["Image"][keys[3]]["x_axis"]]
            shift_y = [config["Bird_View"]["Image"][keys[0]]["y_axis"],
                       config["Bird_View"]["Image"][keys[1]]["y_axis"],
                       config["Bird_View"]["Image"][keys[2]]["y_axis"],
                       config["Bird_View"]["Image"][keys[3]]["y_axis"]]
            image_crop = [self.cropping_anypoint_image(image[0], 0)]

            image_1 = cv2.rotate(image[1], cv2.ROTATE_90_COUNTERCLOCKWISE)
            image_crop.append(self.cropping_anypoint_image(image_1, 1))
            image_2 = cv2.rotate(image[2], cv2.ROTATE_90_CLOCKWISE)
            image_crop.append(self.cropping_anypoint_image(image_2, 2))
            image_3 = cv2.rotate(image[3], cv2.ROTATE_180)
            image_crop.append(self.cropping_anypoint_image(image_3, 3))

            if config["Bird_View"]["Mode_calib"] == "Point":
                merge_image_canvas, bird_view = merge_image_4_camera_center_clicked(image_crop,
                                                                                    config["Bird_View"]["Image"],
                                                                                    config["Bird_View"][
                                                                                        "Gradient_mode"])
            else:
                merge_image_canvas, bird_view = merge_image_4_camera_center_config(image_crop,
                                                                                   config["Bird_View"]["Image"],
                                                                                   shift_x, shift_y,
                                                                                   config["Bird_View"]["Gradient_mode"])
            self.result_bird_view_overlap.emit(merge_image_canvas)
            self.result_bird_view.emit(bird_view)

    def cropping_anypoint_image(self, image, i):
        with open(self.cached_file, "r") as file:
            config = yaml.safe_load(file)
        keys = list(config["Bird_View"]["Image"])
        top = config["Bird_View"]["Image"][keys[i]]["crop_top"]
        bottom = config["Bird_View"]["Image"][keys[i]]["crop_bottom"]
        left = config["Bird_View"]["Image"][keys[i]]["crop_left"]
        right = config["Bird_View"]["Image"][keys[i]]["crop_right"]
        return image[top:image.shape[0] - bottom, left: image.shape[1] - right]

    def create_maps_turn_left_view_anypoint(self):
        self.maps_x_turn_left, self.maps_y_turn_left = self.model_bird_view.moildev[1].maps_anypoint_mode1(20, -90, 2)

    def create_image_turn_left_view_anypoint(self):
        image = self.model_moil.remap_image(self.model_bird_view.image[1], self.maps_x_turn_left, self.maps_y_turn_left)
        image = image[200:image.shape[0] - 200, 520: image.shape[1] - 520]
        self.result_anypoint_dash_cam.emit(image)

    def create_maps_turn_right_view_anypoint(self):
        self.maps_x_turn_right, self.maps_y_turn_right = self.model_bird_view.moildev[2].maps_anypoint_mode1(40, 90, 2)

    def create_image_turn_right_view_anypoint(self):
        image = self.model_moil.remap_image(self.model_bird_view.image[2], self.maps_x_turn_right,
                                            self.maps_y_turn_right)
        image = image[200:image.shape[0] - 200, 520: image.shape[1] - 520]
        self.result_anypoint_dash_cam.emit(image)

    def create_maps_front_view_anypoint(self):
        self.maps_x_front, self.maps_y_front = self.model_bird_view.moildev[0].maps_anypoint_mode2(0, 0, 0, 2)

    def create_image_front_view_anypoint(self):
        image = self.model_moil.remap_image(self.model_bird_view.image[0], self.maps_x_front, self.maps_y_front)
        self.result_anypoint_dash_cam.emit(image)

    def create_maps_rear_view_anypoint(self):
        self.maps_x_rear, self.maps_y_rear = self.model_bird_view.moildev[3].maps_anypoint_mode2(0, 0, 0, 2)

    def create_image_rear_view_anypoint(self):
        image = self.model_moil.remap_image(self.model_bird_view.image[3], self.maps_x_rear, self.maps_y_rear)
        self.result_anypoint_dash_cam.emit(image)

    # ######### dash camera ##################
    def create_dash_image(self):
        with open(self.cached_file, "r") as file:
            confi_view = yaml.safe_load(file)
        left = confi_view["Dash_Camera"]["View"][self.set_dash_image_mode]["crop_left"]
        right = confi_view["Dash_Camera"]["View"][self.set_dash_image_mode]["crop_right"]
        top = confi_view["Dash_Camera"]["View"][self.set_dash_image_mode]["crop_top"]
        bottom = confi_view["Dash_Camera"]["View"][self.set_dash_image_mode]["crop_bottom"]
        rotate = confi_view["Dash_Camera"]["Rotate"]
        image = self.model_moil.rotate_image(self.image.copy(), rotate)
        if self.set_dash_image_mode == "Dash_front_view":
            image = cv2.resize(
                cv2.remap(image, self.map_x_dash_front, self.map_y_dash_front, cv2.INTER_CUBIC),
                (self.image.shape[1] * 2, self.image.shape[0]))
        else:
            image = cv2.resize(
                cv2.remap(image, self.map_x_dash_driver, self.map_y_dash_driver, cv2.INTER_CUBIC),
                (self.image.shape[1] * 2, self.image.shape[0]))
        image = image[round(image.shape[0] * (top + 0.3)):
                      round(image.shape[0] * (top + 0.3)) + round(image.shape[0] * (bottom - 0.3)),
                round(image.shape[1] * left): round(image.shape[1] * left) + round(image.shape[1] * (right - left))]
        self.result_dash_image.emit(image)

    def create_anypoint_image(self):
        with open(self.cached_file, "r") as file:
            confi_view = yaml.safe_load(file)
        rotate = confi_view["Dash_Camera"]["Rotate"]
        image = self.model_moil.rotate_image(self.image.copy(), rotate)
        angle = confi_view["Dash_Camera"]["View"][self.set_anypoint_image_mode]["roll"]
        map_x, map_y = self.get_map_data_for_view(self.set_anypoint_image_mode)

        if map_x is not None and map_y is not None:
            image = self.model_moil.remap_image(image, map_x, map_y)
            image = self.croping_rotate_image(image, angle)

            self.result_anypoint_dash_cam.emit(image)
        else:
            self.result_anypoint_dash_cam.emit(None)

    def croping_rotate_image(self, image, angle):
        # Rotate the image by the given angle
        rows, cols, _ = image.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
        img_rotated = cv2.warpAffine(image, M, (cols, rows))

        # Convert the image to grayscale
        gray = cv2.cvtColor(img_rotated, cv2.COLOR_BGR2GRAY)

        # Threshold the image to create a mask of the black area
        ret, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

        # Find the contours of the mask
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the bounding box of the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Crop the image to the bounding box
        return img_rotated[y:y + h, x:x + w]

    def rotate_original_image(self):
        with open(self.cached_file, "r") as file:
            confi_view = yaml.safe_load(file)
        rotate = confi_view["Dash_Camera"]["Rotate"]
        image = self.model_moil.rotate_image(self.image.copy(), rotate)
        self.original_image_dash_cam.emit(image)

    def get_map_data_for_view(self, view):
        if view == "Left Window":
            return self.map_x_left_window, self.map_y_left_window
        elif view == "Right Window":
            return self.map_x_right_window, self.map_y_right_window
        elif view == "Steering View":
            return self.map_x_driver_view, self.map_y_driver_view
        elif view == "Second Driver View":
            return self.map_x_second_driver_view, self.map_y_second_driver_view
        elif view == "For comparison View":
            return self.map_x_compare_view, self.map_y_compare_view
        else:
            return None, None

    def create_initial_maps_dash_camera(self):
        with open(self.cached_file, "r") as file:
            confi_view = yaml.safe_load(file)
        view = confi_view["Dash_Camera"]["View"]
        for view in view.keys():
            if view == "Dash_front_view":
                self.create_maps_image_dash_view(view)
                print("create new maps")

            elif view == "Dash_driver_view":
                self.create_maps_image_dash_view(view)

            else:
                self.create_maps_anypoint_view(view)

    def load_maps_dash_camera_from_cached(self):
        with open(self.cached_file, "r") as file:
            confi_view = yaml.safe_load(file)
        view = confi_view["Dash_Camera"]["View"]
        for view in view.keys():
            if view == "Dash_front_view":
                # if str(np.load(self.file_maps.get_maps_x_dash_front_view(), allow_pickle=True)) == "None":
                #     self.create_maps_image_dash_view(view)
                #     print("create new maps")
                #
                # else:
                #     print("load data maps")
                self.map_x_dash_front = np.load(self.file_maps.get_maps_x_dash_front_view())
                self.map_y_dash_front = np.load(self.file_maps.get_maps_y_dash_front_view())
                self.signal_show_config_to_ui.emit(True)

            elif view == "Dash_driver_view":
                # if str(np.load(self.file_maps.get_maps_x_dash_driver_view(), allow_pickle=True)) == "None":
                #     self.create_maps_image_dash_view(view)
                #
                # else:
                self.map_x_dash_driver = np.load(self.file_maps.get_maps_x_dash_driver_view())
                self.map_y_dash_driver = np.load(self.file_maps.get_maps_y_dash_driver_view())

            else:
                # if str(np.load(self.file_maps.get_maps_x_left_window_view(), allow_pickle=True)) == "None" or \
                #         str(np.load(self.file_maps.get_maps_x_right_window_view(), allow_pickle=True)) == "None" or \
                #         str(np.load(self.file_maps.get_maps_x_driver_window_view(), allow_pickle=True)) == "None" or \
                #         str(np.load(self.file_maps.get_maps_x_second_driver_window_view(),
                #                     allow_pickle=True)) == "None":
                #     self.create_maps_anypoint_view(view)
                #
                # else:
                self.map_x_left_window = np.load(self.file_maps.get_maps_x_left_window_view())
                self.map_y_left_window = np.load(self.file_maps.get_maps_y_left_window_view())

                self.map_x_right_window = np.load(self.file_maps.get_maps_x_right_window_view())
                self.map_y_right_window = np.load(self.file_maps.get_maps_y_right_window_view())

                self.map_x_driver_view = np.load(self.file_maps.get_maps_x_driver_window_view())
                self.map_y_driver_view = np.load(self.file_maps.get_maps_y_driver_window_view())

                self.map_x_second_driver_view = np.load(self.file_maps.get_maps_x_second_driver_window_view())
                self.map_y_second_driver_view = np.load(self.file_maps.get_maps_y_second_driver_window_view())

                self.map_x_compare_view = np.load(self.file_maps.get_maps_x_compare_view())
                self.map_y_compare_view = np.load(self.file_maps.get_maps_y_compare_view())

    def create_maps_image_dash_view(self, view):
        with open(self.cached_file, "r") as file:
            confi_view = yaml.safe_load(file)
        parameter_name = confi_view["Dash_Camera"]["Parameter_name"]
        alpha_max = confi_view["Dash_Camera"]["View"][view]["alpha_max"]
        alpha = confi_view["Dash_Camera"]["View"][view]["alpha"]
        beta = confi_view["Dash_Camera"]["View"][view]["beta"]
        alpha_from = 0
        alpha_end = 1
        if view == "Dash_front_view":
            moildev = self.model_moil.connect_to_moildev(parameter_name)

            self.map_x_dash_front, self.map_y_dash_front = moildev.maps_panorama_car(alpha_max, alpha, beta, alpha_from,
                                                                                     alpha_end)
            # saving the Maps to the system
            np.save(self.file_maps.get_maps_x_dash_front_view(), self.map_x_dash_front)
            np.save(self.file_maps.get_maps_y_dash_front_view(), self.map_y_dash_front)
        else:
            moildev = self.model_moil.connect_to_moildev(parameter_name)
            self.map_x_dash_driver, self.map_y_dash_driver = moildev.maps_panorama_car(alpha_max, alpha, beta,
                                                                                       alpha_from,
                                                                                       alpha_end)
            # saving the Maps to the system
            np.save(self.file_maps.get_maps_x_dash_driver_view(), self.map_x_dash_driver)
            np.save(self.file_maps.get_maps_y_dash_driver_view(), self.map_y_dash_driver)

    def create_maps_anypoint_view(self, view):
        with open(self.cached_file, "r") as file:
            confi_view = yaml.safe_load(file)
        parameter_name = confi_view["Dash_Camera"]["Parameter_name"]
        alpha = confi_view["Dash_Camera"]["View"][view]["alpha"]
        beta = confi_view["Dash_Camera"]["View"][view]["beta"]
        roll = confi_view["Dash_Camera"]["View"][view]["roll"]
        zoom = confi_view["Dash_Camera"]["View"][view]["zoom"]

        if view == "Left Window":
            moildev = self.model_moil.connect_to_moildev(parameter_name)
            self.map_x_left_window, self.map_y_left_window = moildev.maps_anypoint_mode2(alpha, beta, roll, zoom)

            # saving the Maps to the system
            np.save(self.file_maps.get_maps_x_left_window_view(), self.map_x_left_window)
            np.save(self.file_maps.get_maps_y_left_window_view(), self.map_y_left_window)

        elif view == "Right Window":
            moildev = self.model_moil.connect_to_moildev(parameter_name)
            self.map_x_right_window, self.map_y_right_window = moildev.maps_anypoint_mode2(alpha, beta, roll, zoom)

            # saving the Maps to the system
            np.save(self.file_maps.get_maps_x_right_window_view(), self.map_x_right_window)
            np.save(self.file_maps.get_maps_y_right_window_view(), self.map_y_right_window)

        elif view == "Steering View":
            moildev = self.model_moil.connect_to_moildev(parameter_name)
            self.map_x_driver_view, self.map_y_driver_view = moildev.maps_anypoint_mode2(alpha, beta, roll, zoom)

            # saving the Maps to the system
            np.save(self.file_maps.get_maps_x_driver_window_view(), self.map_x_driver_view)
            np.save(self.file_maps.get_maps_y_driver_window_view(), self.map_y_driver_view)

        elif view == "Second Driver View":
            moildev = self.model_moil.connect_to_moildev(parameter_name)
            self.map_x_second_driver_view, self.map_y_second_driver_view = moildev.maps_anypoint_mode2(alpha, beta,
                                                                                                       roll, zoom)

            # saving the Maps to the system
            np.save(self.file_maps.get_maps_x_second_driver_window_view(), self.map_x_second_driver_view)
            np.save(self.file_maps.get_maps_y_second_driver_window_view(), self.map_y_second_driver_view)

        elif view == "For comparison View":
            moildev = self.model_moil.connect_to_moildev(parameter_name)
            self.map_x_compare_view, self.map_y_compare_view = moildev.maps_anypoint_mode2(alpha, beta, roll, zoom)

            # saving the Maps to the system
            np.save(self.file_maps.get_maps_x_compare_view(), self.map_x_compare_view)
            np.save(self.file_maps.get_maps_y_compare_view(), self.map_y_compare_view)

    def information_dash_camera(self):
        with open(self.cached_file, "r") as file:
            config_view = yaml.safe_load(file)
        parameter_name = config_view["Dash_Camera"]["Parameter_name"]
        moildev = self.model_moil.connect_to_moildev(parameter_name)
        info = [config_view["Project_name"],
                config_view["Dash_Camera"]["Parameter_name"],
                config_view["Dash_Camera"]["Source"],
                moildev.image_width,
                moildev.image_height,
                moildev.icx,
                moildev.icy]
        self.dash_camera_info.emit(info)

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
