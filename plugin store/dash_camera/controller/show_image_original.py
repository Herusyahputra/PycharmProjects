from PyQt6.QtWidgets import QWidget
from ..view.show_image_original_bird_view import Ui_original_image


class ShowOriginalImageBirdView(QWidget):
    def __init__(self, model, list_image):
        super().__init__()
        self.ui = Ui_original_image()
        self.ui.setupUi(self)
        self.model = model
        self.list_image = list_image
        self.show_original_image()

    def show_original_image(self):
        if self.list_image[0] is not None:
            self.model.show_image_to_label(self.ui.lbl_show_original_image_1, self.list_image[0], 600)
        if self.list_image[1] is not None:
            self.model.show_image_to_label(self.ui.lbl_show_original_image_2, self.list_image[1], 600)
        if self.list_image[2] is not None:
            self.model.show_image_to_label(self.ui.lbl_show_original_image_3, self.list_image[2], 600)
        if self.list_image[3] is not None:
            self.model.show_image_to_label(self.ui.lbl_show_original_image_4, self.list_image[3], 600)
