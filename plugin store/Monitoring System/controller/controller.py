import cv2
import time
import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from ..views.main_apps import Ui_Form

class Controller(QWidget):
    def __init__(self, model):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_to_ui)
        self.model = model
        self.point_z1 = []
        self.point_z2 = []
        self.click_z1 = None
        self.click_z2 = None
        self.set_stylesheet()
        self.connect_to_button()

    def set_stylesheet(self):
        self.setStyleSheet(self.model.style_label())
        self.setStyleSheet(self.model.style_pushbutton())

    def connect_to_button(self):
        self.ui.pushButton.clicked.connect(self.onclick_open_media)
        self.ui.pushButton_2.clicked.connect(self.cam_parameter)

        self.ui.label.mousePressEvent = self.mouse_event_image
        self.ui.label_58.mousePressEvent = self.mouse_point_z1
        self.ui.label_17.mousePressEvent = self.mouse_point_z2

        self.ui.zoom_fisheye.valueChanged.connect(self.fisheye_image)

        self.ui.pitch_z1.valueChanged.connect(self.anypoint_maps_z1)
        self.ui.yaw_z1.valueChanged.connect(self.anypoint_maps_z1)
        self.ui.roll_z1.valueChanged.connect(self.anypoint_maps_z1)
        self.ui.zoom_z1.valueChanged.connect(self.anypoint_maps_z1)

        self.ui.pitch_Z2.valueChanged.connect(self.anypoint_maps_z2)
        self.ui.yaw_z2.valueChanged.connect(self.anypoint_maps_z2)
        self.ui.roll_z2.valueChanged.connect(self.anypoint_maps_z2)
        self.ui.zoom_z2.valueChanged.connect(self.anypoint_maps_z2)

        self.ui.rotate_ori.valueChanged.connect(self.show_to_ui)
        self.ui.rotate_z1.valueChanged.connect(self.anypoint_maps_z1)
        self.ui.rotate_z2.valueChanged.connect(self.anypoint_maps_z2)

    def onclick_open_media(self):
        # path, parameter_name = self.model.select_media_source()
        cam_type, media_source, params_name = self.model.select_media_source()
        if cam_type:
            if params_name:
                self.moildev = self.model.connect_to_moildev(parameter_name=params_name)
            self.image = cv2.imread(media_source)
            self.image_copy = self.image.copy()
            self.show_to_ui()
            self.anypoint_maps_z1()
            self.anypoint_maps_z2()

    def cam_parameter(self):
        self.model.form_camera_parameter()

    def show_to_ui(self):
        start = time.time()
        self.timer.start()
        self.fisheye = self.image
        self.fisheye = self.rotate_value_ori(self.fisheye)
        mapx, mapy = self.moildev.maps_anypoint_mode2(0, 0, 0, 4)
        draw_img = self.model.draw_polygon(self.fisheye, mapx, mapy)
        self.model.show_image_to_label(self.ui.label, draw_img, 600)
        print("Processing Image")
        end = time.time()
        seconds = end - start
        print("Image Mode, time:{}".format(seconds))

    def fisheye_image(self):
        alpha = 0
        beta = 0
        zoom = self.ui.zoom_fisheye.value()

        self.mapx, self.mapy = self.moildev.maps_anypoint_mode1(alpha, beta, zoom)
        self.remap = self.model.remap_image(self.image, self.mapx, self.mapy)
        self.model.show_image_to_label(self.ui.label, self.remap, 600)

    def anypoint_maps_z1(self):
        pitch = self.ui.pitch_z1.value()
        yaw = self.ui.yaw_z1.value()
        roll = self.ui.roll_z1.value()
        zoom = self.ui.zoom_z1.value()

        self.mapx, self.mapy = self.moildev.maps_anypoint_mode2(pitch, yaw, roll, zoom)
        self.remap = self.model.remap_image(self.image_copy, self.mapx, self.mapy)
        self.remap_z1 = self.rotate_value_z1(self.remap)
        self.model.show_image_to_label(self.ui.label_58, self.remap_z1, 600)

    def anypoint_maps_z2(self):
        pitch = self.ui.pitch_Z2.value()
        yaw = self.ui.yaw_z2.value()
        roll = self.ui.roll_z2.value()
        zoom = self.ui.zoom_z2.value()

        self.mapx, self.mapy = self.moildev.maps_anypoint_mode2(pitch, yaw, roll, zoom)
        self.remap = self.model.remap_image(self.image_copy, self.mapx, self.mapy)
        self.remap_z2 = self.rotate_value_z2(self.remap)
        self.model.show_image_to_label(self.ui.label_17, self.remap_z2, 600)

    def rotate_value_ori(self, image):
        rotate = self.ui.rotate_ori.value()
        height, width = image.shape[:2]
        center = (width / 2, height / 2)
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=rotate, scale=1)

        return cv2.warpAffine(src=image, M=rotate_matrix, dsize=(width, height))

    def mouse_event_image(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            pos_x = round(e.position().x())
            pos_y = round(e.position().y())
            if self.image is None:
                print("Not found Image")
            else:
                ratio_x, ratio_y = self.model.calculate_ratio_image2label(self.ui.label, self.image)
                icx_front = round(pos_x * ratio_x)
                icy_font = round(pos_y * ratio_y)

                if self.ui.radioButton_2.isChecked():
                    x, y = self.moildev.get_alpha_beta(icx_front, icy_font, mode=2)
                    self.blockSignals()
                    self.unblockSignals()
                    self.ui.pitch_z1.setValue(x)
                    self.ui.yaw_z1.setValue(y)
                    self.anypoint_maps_z1()
                    self.anypoint_maps_z2()
                    self.show_to_ui()

                if self.ui.radioButton.isChecked():
                    x, y = self.moildev.get_alpha_beta(icx_front, icy_font, mode=2)
                    self.blockSignals()
                    self.unblockSignals()
                    self.ui.pitch_Z2.setValue(x)
                    self.ui.yaw_z2.setValue(y)
                    self.anypoint_maps_z1()
                    self.anypoint_maps_z2()
                    self.show_to_ui()

        elif e.button() == Qt.MouseButton.RightButton:
            if self.image is not None:
                menu = QWidget.QMenu
                save = menu.addAction("Open Image")
                info = menu.addAction("Show Info")
                save.triggered.connect()
                info.triggered.connect(info)
                menu.exec(e.globalPos())

    def mouse_point_z1(self, e):
        print("point zone 1")
        if e.button() == Qt.MouseButton.LeftButton:
            pos_x = round(e.position().x())
            pos_y = round(e.position().y())
            if self.image is None:
                print("Not found image")
            else:
                ratio_x, ratio_y = self.model.calculate_ratio_image2label(self.ui.label_58, self.remap_z1)
                icx_front = round(pos_x * ratio_x)
                icy_front = round(pos_y * ratio_y)
                coordinate = [icx_front, icy_front]

                if len(self.point_z1) <4:
                    self.point_z1.append(coordinate)

                for i, value in enumerate(self.point_z1):
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    org = self.point_z1[i]
                    fontScale = 2
                    color = (255, 0, 0)
                    thickness = 5
                    self.remap_z1 = cv2.putText(self.remap_z1, str(i + 1), (org[0], org[1]), font, fontScale,
                                                        color, thickness, cv2.LINE_AA)
                    cv2.circle(self.remap_z1, (org[0], org[1]), 15, (0, 0, 255), -1)

                if len(self.point_z1) == 4:
                    self.click_z1 = self.perspective_img_z1(self.remap_z1)
                    cv2.imwrite("image_z1.jpg", self.click_z1)

                if len(self.point_z1) > 4:
                    self.point_z1 = []
                    self.image_copy = self.anypoint_maps_z1()

                self.show_image_point_z1()

    def mouse_point_z2(self, e):
        print("point zone 2")
        if e.button() == Qt.MouseButton.LeftButton:
            pos_x = round(e.position().x())
            pos_y = round(e.position().y())
            if self.image is None:
                print("Not found image")
            else:
                ratio_x, ratio_y = self.model.calculate_ratio_image2label(self.ui.label_17, self.remap_z2)
                icx_front = round(pos_x * ratio_x)
                icy_front = round(pos_y * ratio_y)
                coordinate = [icx_front, icy_front]

                if len(self.point_z2) <4:
                    self.point_z2.append(coordinate)

                for i, value in enumerate(self.point_z2):
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    org = self.point_z2[i]
                    fontScale = 2
                    color = (255, 0, 0)
                    thickness = 5
                    self.remap_z2 = cv2.putText(self.remap_z2, str(i + 1), (org[0], org[1]), font, fontScale,
                                                        color, thickness, cv2.LINE_AA)
                    cv2.circle(self.remap_z2, (org[0], org[1]), 15, (0, 0, 255), -1)

                if len(self.point_z2) == 4:
                    self.click_z2 = self.perspective_img_z2(self.remap_z2)
                    # cv2.imwrite("image_z1.jpg", self.click_z2)

                if len(self.point_z2) > 4:
                    self.point_z2 = []
                    self.image_copy = self.anypoint_maps_z2()

                self.show_image_point_z2()

    def show_image_point_z1(self):
        self.model.show_image_to_label(self.ui.label_58, self.remap_z1, 600)
        if self.click_z1 is not None:
            self.model.show_image_to_label(self.ui.label_63, self.click_z1, 300)

    def show_image_point_z2(self):
        self.model.show_image_to_label(self.ui.label_17, self.remap_z2, 600)
        if self.click_z2 is not None:
            self.model.show_image_to_label(self.ui.label_65, self.click_z2, 300)

    def rotate_value_z1(self, image):
        rotate = self.ui.rotate_z1.value()
        height, width = image.shape[:2]
        center = (width / 2, height / 2)
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=rotate, scale=1)

        return cv2.warpAffine(src=image, M=rotate_matrix, dsize=(width, height))

    def rotate_value_z2(self, image):
        rotate = self.ui.rotate_z2.value()
        height, width = image.shape[:2]
        center = (width / 2, height / 2)
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=rotate, scale=1)

        return cv2.warpAffine(src=image, M=rotate_matrix, dsize=(width, height))

    def perspective_img_z1(self, image):
        pts1 = np.float32(self.point_z1)
        pts2 = np.float32([[0, 0], [200, 0], [0, 100], [200, 100]])
        transform = cv2.getPerspectiveTransform(pts1, pts2)

        return cv2.warpPerspective(image, transform, (200, 100))

    def perspective_img_z2(self, image):
        pts1 = np.float32(self.point_z2)
        pts2 = np.float32([[0, 0], [200, 0], [0, 100], [200, 100]])
        transform = cv2.getPerspectiveTransform(pts1, pts2)
        return cv2.warpPerspective(image, transform, (200, 100))

    def blockSignals(self):
        self.ui.rotate_ori.blockSignals(True)
        self.ui.zoom_fisheye.blockSignals(True)
        self.ui.pitch_z1.blockSignals(True)
        self.ui.yaw_z1.blockSignals(True)
        self.ui.roll_z1.blockSignals(True)
        self.ui.rotate_z1.blockSignals(True)
        self.ui.pitch_Z2.blockSignals(True)
        self.ui.yaw_z2.blockSignals(True)
        self.ui.roll_z2.blockSignals(True)
        self.ui.rotate_z2.blockSignals(True)

    def unblockSignals(self):
        self.ui.rotate_ori.blockSignals(False)
        self.ui.pitch_z1.blockSignals(False)
        self.ui.yaw_z1.blockSignals(False)
        self.ui.roll_z1.blockSignals(False)
        self.ui.rotate_z1.blockSignals(False)
        self.ui.pitch_Z2.blockSignals(False)
        self.ui.yaw_z2.blockSignals(False)
        self.ui.roll_z2.blockSignals(False)
        self.ui.rotate_z2.blockSignals(False)
