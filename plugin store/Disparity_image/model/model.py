import numpy as np
from .sources_maps import SourceFile
from .algorithm import algorithm
import cv2
from PyQt6.QtCore import QTimer
from random import randint
import math


class ModelPlugin:
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.source_file = SourceFile()
        self.image_source = None
        self.mode_recenter = False
        self.mode_option = "Anypoint"
        self.image_output = [None, None]
        self.image_recenter = [None, None]
        self.image_feature_point = [None, None]
        self.image_optical_flow = [None, None]
        self.image_feature_matching = None
        self.image_disparity = [None, None]
        self.moildev = [None, None]
        self.key_points = [None, None]
        self.cam = None
        self.dis_x = []
        self.dis_y = []

        self.properties_video = {"video": False, "streaming": False, "pos_frame": 0, "frame_count": 0,
                                 "total_minute": 0, "total_second": 0, "current_minute": 0, "current_second": 0}
        self.config_anypoint = {0: {"pitch": 0, "yaw": 0, "roll": 0, "zoom": 0},
                                1: {"pitch": 0, "yaw": 0, "roll": 0, "zoom": 0}}
        self.config_panorama = {0: {"alpha_max": 0, "alpha_min": 0},
                                1: {"alpha_max": 0, "alpha_min": 0}}
        self.config_recenter = {0: {"icx": 0, "icy": 0, "alpha": 0, "beta": 0},
                                1: {"icx": 0, "icy": 0, "alpha": 0, "beta": 0}}
        self.crop_panorama = {"front": 0, "bottom": 0, "left": 0, "right": 0}

        self.config_line = {"status": 'all', "total_point": 0}

    @classmethod
    def draw_point_in_image(cls, img, point_x, point_y, color):
        return cv2.circle(img, (point_x, point_y), 10, color, -1)

    @classmethod
    def draw_arrow_line_in_image(cls, img, point1_x, point1_y, point2_x, point2_y, color):
        return cv2.arrowedLine(img, (int(point1_x), int(point1_y)), (int(point2_x), int(point2_y)), color, 10)

    @classmethod
    def write_word_in_image(cls, img, point_x, point_y, color):
        org = (point_x, point_y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 2
        thickness = 8
        return cv2.putText(img, "(" + str(point_x) + "," + str(point_y) + ")", org, font,
                           fontScale, color, thickness, cv2.LINE_AA)
    
    def draw_cross_in_image(self, image, coor1, coor2):
        return self.model.marker.crosshair(image, (coor1, coor2))
        
    @classmethod
    def write_word_distance_in_image(cls, img, point_x, point_y, dis_x, dis_y, color):
        org = (point_x, point_y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 2
        thickness = 8
        return cv2.putText(img, "d=(" + str(dis_x) + "," + str(dis_y) + ")", org, font,
                           fontScale, color, thickness, cv2.LINE_AA)

    def read_media_sources(self, media_source, param_name):
        if type(media_source) == str:
            if media_source.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.properties_video["video"] = False
                self.read_image_source(media_source, param_name)
            elif media_source.lower().endswith('.avi'):
                self.properties_video["video"] = True
                self.properties_video["streaming"] = False
                self.read_video_source(media_source, param_name)
            elif media_source.lower().endswith('.mjpg'):
                self.properties_video["video"] = True
                self.properties_video["streaming"] = True
                self.read_video_source(media_source, param_name)
        elif type(media_source) == int:
            self.properties_video["video"] = True
            self.properties_video["streaming"] = True
            self.read_video_source(media_source, param_name)

    def read_image_source(self, media_source, param_name):
        self.image_source = cv2.imread(media_source)
        self.create_moildev_object(param_name)
        self.create_maps_image_output()
        self.process_image()

    def read_video_source(self, media_source, param_name):
        self.cam = cv2.VideoCapture(media_source)
        self.create_moildev_object(param_name)
        self.create_maps_image_output()
        self.next_frame()
        self.process_image()

    def next_frame(self):
        _, self.image_source = self.cam.read()
        self.process_image()
        self.video_duration()

    def create_moildev_object(self, param_name):
        for i in range(len(self.moildev)):
            self.moildev[i] = self.model.connect_to_moildev(param_name)

    def create_maps_image_output(self):
        for i, moildev in enumerate(self.moildev):
            if moildev is not None:
                self.get_alpha_and_beta(i)
                self.create_maps_recenter_image(i)
                if self.mode_option == "Anypoint":
                    self.create_maps_anypoint(i)
                elif self.mode_option == "Panorama":
                    self.create_maps_panorama(i)

    def process_image(self):
        if self.image_source is not None:
            for i in range(len(self.moildev)):
                if self.mode_recenter:
                    print("recenter " + str(self.mode_recenter))
                    self.remap_recenter_image(i)
                self.remap_image_output(i)
            # self.disparity_image()

    def get_alpha_and_beta(self, image_number,):
        if self.config_recenter[image_number]["icx"] == 0 or self.config_recenter[image_number]["icy"] == 0:
            self.config_recenter[image_number]["icx"] = self.moildev[image_number].icx
            self.config_recenter[image_number]["icy"] = self.moildev[image_number].icy
        alpha, beta = self.moildev[image_number].get_alpha_beta(self.config_recenter[image_number]["icx"],
                                                                self.config_recenter[image_number]["icy"])
        self.config_recenter[image_number]["alpha"] = alpha
        self.config_recenter[image_number]["beta"] = beta

    def create_maps_recenter_image(self, image_number):
        print(self.config_recenter)
        maps_x, maps_y = self.moildev[image_number].maps_panorama_rt(110,
                                                                     self.config_recenter[image_number]["alpha"],
                                                                     self.config_recenter[image_number]["beta"])

        # saving the Maps to the system
        np.save(self.source_file.path_maps_x_panorama_rt(image_number), maps_x)
        np.save(self.source_file.path_maps_y_panorama_rt(image_number), maps_y)

        maps_x, maps_y = self.moildev[image_number].maps_recenter(110,
                                                                  self.config_recenter[image_number]["beta"])

        # saving the Maps to the system
        np.save(self.source_file.path_maps_x_rev_panorama(image_number), maps_x)
        np.save(self.source_file.path_maps_y_rev_panorama(image_number), maps_y)

    def remap_recenter_image(self, image_number):
        maps_x = np.load(self.source_file.path_maps_x_panorama_rt(image_number))
        maps_y = np.load(self.source_file.path_maps_y_panorama_rt(image_number))

        self.image_recenter[image_number] = self.model.remap_image(self.image_source.copy(), maps_x,
                                                                   maps_y)

        maps_x = np.load(self.source_file.path_maps_x_rev_panorama(image_number))
        maps_y = np.load(self.source_file.path_maps_y_rev_panorama(image_number))

        self.image_recenter[image_number] = self.model.remap_image(self.image_recenter[image_number].copy(), maps_x,
                                                                   maps_y)
        
    def create_maps_anypoint(self, image_number):
        maps_x, maps_y = self.moildev[image_number].maps_anypoint_mode2(self.config_anypoint[image_number]["pitch"],
                                                                        self.config_anypoint[image_number]["yaw"],
                                                                        self.config_anypoint[image_number]["roll"],
                                                                        self.config_anypoint[image_number]["zoom"])
        # saving the Maps to the system
        np.save(self.source_file.path_maps_x_image(image_number), maps_x)
        np.save(self.source_file.path_maps_y_image(image_number), maps_y)

    def create_maps_panorama(self, image_number):
        maps_x, maps_y = self.moildev[image_number].maps_panorama_tube(self.config_panorama[image_number]["alpha_min"],
                                                                       self.config_panorama[image_number]["alpha_max"])
        # saving the Maps to the system
        np.save(self.source_file.path_maps_x_image(image_number), maps_x)
        np.save(self.source_file.path_maps_y_image(image_number), maps_y)

    def remap_image_output(self, image_number):
        maps_x = np.load(self.source_file.path_maps_x_image(image_number))
        maps_y = np.load(self.source_file.path_maps_y_image(image_number))

        if self.mode_recenter:
            self.image_output[image_number] = self.model.remap_image(self.image_recenter[image_number].copy(), maps_x,
                                                                     maps_y)
        else:
            self.image_output[image_number] = self.model.remap_image(self.image_source.copy(), maps_x, maps_y)
        if self.mode_option == "Panorama":
            print(self.mode_option)
            self.image_output[image_number] = cv2.resize(self.image_output[image_number].copy(),
                                                         (self.image_output[image_number].shape[0] * 2,
                                                          self.image_output[image_number].shape[1]))

    def crop_panorama_image(self):
        left = self.crop_panorama["left"]
        right = self.crop_panorama["right"]
        top = self.crop_panorama["top"]
        bottom = self.crop_panorama["bottom"]

        for i in range(len(self.image_output)):
            self.remap_image_output(i),

            self.image_output[i] = self.image_output[i][round(self.image_output[i].shape[0] * (top + 0.3)):round(
                self.image_output[i].shape[0] * (top + 0.3)) + round(self.image_output[i].shape[0] * (bottom - 0.3)),
                                   round(self.image_output[i].shape[1] * left):
                                   round(self.image_output[i].shape[1] * left) + round(
                                       self.image_output[i].shape[1] * (right - left))]

    def disparity_image_test_algorithm(self):
        self.key_points[0], self.key_points[1], matches, self.image_feature_point[0], self.image_feature_point[1], \
            self.image_feature_matching = algorithm(self.image_output[0], self.image_output[1], "SIFT")

    def calculate_deference_point(self):
        """
        Selected view image point
        """
        kps1 = self.key_points[0]
        kps2 = self.key_points[1]
        self.image_optical_flow[0] = self.image_output[0].copy()
        self.image_optical_flow[1] = self.image_output[1].copy()
        if self.config_line["status"] == "all":
            point = kps1
        elif self.config_line["status"] == "random":
            randoms = []
            kps1_mod = []
            kps2_mod = []
            for i in range(int(self.config_line["total_point"])):
                randoms.append((randint(0, len(kps1))))

            for random in randoms:
                kps1_mod.append(kps1[random])
                kps2_mod.append(kps2[random])

            kps1 = kps1_mod
            kps2 = kps2_mod
            point = kps1

        for i in range(len(point)):
            color = np.random.randint(0, 255, size=(3,))
            color = (int(color[0]), int(color[1]), int(color[2]))
            self.image_optical_flow[1] = self.draw_arrow_line_in_image(self.image_optical_flow[1], kps1[i][0], kps1[i][1],
                                                                 kps2[i][0], kps2[i][1], color)
            self.image_optical_flow[0] = self.draw_point_in_image(self.image_optical_flow[0],
                                                                  int(kps1[i][0]), int(kps1[i][1]),
                                                                  color)
            self.image_optical_flow[1] = self.draw_point_in_image(self.image_optical_flow[1],
                                                                  int(kps2[i][0]), int(kps2[i][1]),
                                                                  color)
            if self.config_line["status"] == "random":
                self.image_optical_flow[0] = self.write_word_in_image(self.image_optical_flow[0], int(kps1[i][0]),
                                                                      int(kps1[i][1]), color)
                self.image_optical_flow[1] = self.write_word_in_image(self.image_optical_flow[1], int(kps2[i][0]),
                                                                      int(kps2[i][1]), color)
                dis_x = (int(kps2[i][0] - kps1[i][0]))
                dis_y = (int(kps2[i][1] - kps1[i][1]))
                self.image_optical_flow[1] = self.write_word_distance_in_image(self.image_optical_flow[1],
                                                                               int(kps1[i][0]),
                                                                               int(kps1[i][1]), dis_x, dis_y, color)
        self.calculate_distance()

    def calculate_distance(self):
        if self.config_anypoint[1]["pitch"] > self.config_anypoint[0]["pitch"]:
            kps1 = self.key_points[0]
            kps2 = self.key_points[1]
        else:
            kps2 = self.key_points[0]
            kps1 = self.key_points[1]
        self.dis_x = []
        self.dis_y = []
        try:
            for i in range(len(kps1)):
                dis_x = int(kps2[i][0] - kps1[i][0])
                dis_y = int(kps2[i][1] - kps1[i][1])
                self.dis_x.append(dis_x)
                self.dis_y.append(dis_y)

            # dis_y = math.sqrt()

            mask = np.zeros_like(self.image_source)
            pixel = []
            for i in range(len(self.dis_y)):
                pixel.append(int(int(255 * self.dis_y[i]) / max(self.dis_y)))
            for i, coor in enumerate(kps1):
                try:
                    cv2.rectangle(mask, (int(coor[0] - 15), int(coor[1] - 15)), (int(coor[0] + 15), int(coor[1] + 15)),
                                  (pixel[i], pixel[i], pixel[i]), -1)
                except:
                    cv2.circle(mask, (int(coor[0]), int(coor[1])), 20, (pixel[i], pixel[i], pixel[i]), -1)
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            # mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            mask1 = cv2.applyColorMap(mask, cv2.COLORMAP_JET)
            self.image_disparity[1] = mask1
            self.image_disparity[0] = mask
        except:
            print("No have change value")

    def calculate_deference_point_selected(self):
        kps1 = self.key_points[0]
        kps2 = self.key_points[1]
        self.image_optical_flow[0] = self.image_output[0].copy()
        self.image_optical_flow[1] = self.image_output[1].copy()

        for i in range(len(kps1)):
            color = np.random.randint(0, 255, size=(3,))
            color = (int(color[0]), int(color[1]), int(color[2]))
            self.image_optical_flow[1] = self.draw_arrow_line_in_image(self.image_optical_flow[1], kps1[i][0], kps1[i][1],
                                                                 kps2[i][0], kps2[i][1], color)
            self.image_optical_flow[0] = self.draw_point_in_image(self.image_optical_flow[0],
                                                                  int(kps1[i][0]), int(kps1[i][1]),
                                                                  color)
            self.image_optical_flow[1] = self.draw_point_in_image(self.image_optical_flow[1],
                                                                  int(kps2[i][0]), int(kps2[i][1]),
                                                                  color)

    def draw_point_matching(self):
        kps1 = self.key_points[0]
        kps2 = self.key_points[1]
        for i in range(len(kps1)):
            color = np.random.randint(0, 255, size=(3,))
            color = (int(color[0]), int(color[1]), int(color[2]))
            self.image_feature_matching = self.draw_point_in_image(
                self.image_feature_matching,
                int(kps1[i][0]), int(kps1[i][1]),
                color)
            self.image_feature_matching = self.draw_point_in_image(
                self.image_feature_matching,
                self.image_output[0].shape[1] +
                int(kps2[i][0]), int(kps2[i][1]),
                color)

    def video_duration(self):
        """
            This function is for get time of video

        Returns:

        """
        if self.cam is not None:
            fps = self.cam.get(cv2.CAP_PROP_FPS)
            self.properties_video["pos_frame"] = self.cam.get(cv2.CAP_PROP_POS_FRAMES)
            self.properties_video["frame_count"] = float(self.cam.get(cv2.CAP_PROP_FRAME_COUNT))
            duration_sec = int(self.properties_video["frame_count"] / fps)

            self.properties_video["total_minute"] = int(duration_sec // 60)
            duration_sec %= 60
            self.properties_video["total_second"] = duration_sec
            sec_pos = int(self.properties_video["pos_frame"] / fps)
            self.properties_video["current_minute"] = int(sec_pos // 60)
            sec_pos %= 60
            self.properties_video["current_second"] = sec_pos

    def slider_controller(self, value, slider_maximum):
        """
        This function id for controller slider of video

        Args:
            value: position selected from user interface
            slider_maximum: position maximum of slider

        Returns:
            image will play with selected position
        """
        dst = self.properties_video["frame_count"] * value / slider_maximum
        if self.cam is not None:
            self.cam.set(cv2.CAP_PROP_POS_FRAMES, dst)
        self.next_frame()

    def get_value_slider_video(self, value):
        """
        This function is for show position of slider according to video player

        Args:
            value: maximum position of slider (time)

        Returns:
            position of current slider
        """
        if self.cam is not None:
            if self.properties_video["frame_count"] == 0:
                current_position = 0
            else:
                current_position = self.properties_video["pos_frame"] * (value + 1) / \
                                   self.properties_video["frame_count"]
            return current_position

    def forward_video(self):
        """
        This function is move video 5 seconds forward

        Returns:

        """
        for i in range(len(self.cam)):
            if self.cam is not None:
                try:
                    fps = self.cam.get(cv2.CAP_PROP_FPS)
                    position = self.properties_video["pos_frame"] + 5 * fps
                    self.cam.set(cv2.CAP_PROP_POS_FRAMES, position)
                except:
                    pass
                self.next_frame()

    def rewind_video(self):
        """
        This function is move video 5 seconds backward

        Returns:

        """
        for i in range(len(self.cam)):
            if self.cam is not None:
                try:
                    fps = self.cam.get(cv2.CAP_PROP_FPS)
                    position = self.properties_video["pos_frame"] - 5 * fps
                    self.cam.set(cv2.CAP_PROP_POS_FRAMES, position)
                except:
                    pass
                self.next_frame()

    def stop_video(self):
        """
        This function is for stop video

        Returns:

        """
        for i in range(len(self.cam)):
            if self.cam is not None:
                try:
                    self.cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
                except:
                    pass
            self.next_frame()
