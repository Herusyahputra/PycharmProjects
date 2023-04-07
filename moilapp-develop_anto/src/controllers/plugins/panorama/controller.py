from src.plugin_interface import PluginInterface
from PyQt6.QtWidgets import QWidget
from .ui_main import Ui_Form
import cv2


class Controller(QWidget):
    def __init__(self, model):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.model = model

        self.icx = None
        self.icy = None

        self.change_stylesheet()
        self.ui.pushButton.clicked.connect(self.open_image)
        self.ui.spinBox.valueChanged.connect(self.change_value_center_x)
        self.ui.spinBox_2.valueChanged.connect(self.change_value_center_y)
        self.ui.c_top.valueChanged.connect(self.show_panorama)
        self.ui.c_left.valueChanged.connect(self.show_panorama)
        self.ui.c_right.valueChanged.connect(self.show_panorama)
        self.ui.c_btn.valueChanged.connect(self.show_panorama)

    def change_stylesheet(self):
        self.ui.pushButton.setStyleSheet(self.model.pushbutton_stylesheet())
        self.setStyleSheet(self.model.label_stylesheet())

    def open_image(self):
        media_path, parameter_name = self.model.select_media_source()
        if media_path:
            self.image = cv2.imread(media_path)
            self.moildev = self.model.connect_to_moildev(parameter_name=parameter_name)
            self.icx = self.moildev.icx
            self.icy = self.moildev.icy
            self.ui.spinBox.setValue(self.icx)
            self.ui.spinBox_2.setValue(self.icy)
            self.show_image_ori()
            self.show_recenter_image(self.image)
            self.panorama_tube()

    def show_image_ori(self):
        image = self.model.marker.point(self.image.copy(), (self.icx, self.icy))
        self.model.show_image_to_label(self.ui.label, image, 400)

    def panorama_tube(self):
        self.pano_image = self.moildev.panorama_tube(self.image_rec, 12, 110)
        self.show_panorama()

    def show_panorama(self):
        image = self.model.cropping_image(self.pano_image, self.ui.c_right.value(), self.ui.c_btn.value(),
                                          self.ui.c_left.value(), self.ui.c_top.value())
        self.model.show_image_to_label(self.ui.label_3, image, 1000)

    def change_value_center_x(self):
        self.icx = self.ui.spinBox.value()
        alpha, beta = self.moildev.get_alpha_beta(self.icx, self.icy)
        print(alpha, beta)
        self.image_rec = self.moildev.recenter(self.image, 110, alpha, beta)
        self.show_recenter_image(self.image_rec)
        self.show_image_ori()
        self.panorama_tube()

    def change_value_center_y(self):
        self.icy = self.ui.spinBox_2.value()
        alpha, beta = self.moildev.get_alpha_beta(self.icx, self.icy)
        self.image_rec = self.moildev.recenter(self.image, 110, alpha, beta)
        self.show_recenter_image(self.image_rec)
        self.show_image_ori()
        self.panorama_tube()

    def show_recenter_image(self, image):
        image = self.model.marker.crosshair(image.copy(), (self.moildev.icx, self.moildev.icy))
        self.model.show_image_to_label(self.ui.label_2, image, 400)


class PanoramaTest(PluginInterface):
    def __init__(self):
        super().__init__()
        self.widget = None

    def set_plugin_widget(self, model):
        self.widget = Controller(model)
        return self.widget

    def set_icon_apps(self):
        return None

    def change_stylesheet(self):
        self.widget.change_stylesheet()
