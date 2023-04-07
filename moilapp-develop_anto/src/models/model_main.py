from .moilutils import MoilUtils
from .model_apps import ModelApps
from .theme import *


class Model(MoilUtils):
    def __init__(self):
        """
        The backend that contains all the data logic.
        The model's job is to simply manage the data. Whether the data is from a database,
        API, or a JSON object, the model is responsible for managing it.

        """
        super(Model, self).__init__()
        self.theme = "dark"
        self.model_apps = ModelApps(self)

    def next_frame(self):
        print("this is next frame function")

    # change style user interface
    def theme_light_mode(self):
        self.theme = "light"
        return STYLE_LIGHT_MODE

    def theme_dark_mode(self):
        self.theme = "dark"
        return STYLE_DARK_MODE

    def pushbutton_stylesheet(self):
        if self.theme == "light":
            stylesheet = """
                            QPushButton {
                                color: rgb(0,0,0);
                                border-radius: 3px;
                                padding-left:8px;    
                                padding-right:8px;    
                                background-color:rgb(200, 200, 200);
                            }
                            QPushButton:hover {
                                background-color: rgb(255, 255, 255);
                                border: 2px solid rgb(52, 59, 72);
                            }
                            QPushButton:pressed {    
                                background-color: rgb(35, 40, 49);
                                border: 2px solid rgb(43, 50, 61);
                                color: rgb(255,255,255);
                            }
                        """
        else:
            stylesheet = """
                            QPushButton {
                                color: rgb(221,221,221);
                                border-radius: 3px;
                                padding-left:8px;
                                padding-right:8px;
                                background-color: rgb(52, 59, 72);
                            }
                            QPushButton:hover {
                                color: rgb(0,0,0);
                                background-color: rgb(200, 200, 200);
                                border: 1px solid rgb(255, 255, 255);
                            }
                            QPushButton:pressed {    
                                background-color: rgb(35, 40, 49);
                                border: 2px solid rgb(43, 50, 61);
                                color: rgb(255,255,255);
                            }
                        """
        return stylesheet

    def label_stylesheet(self):
        if self.theme == "light":
            stylesheet = """
                            QLabel { 
                                background-color: rgb(200,205,205);
                            }
                            """
        else:
            stylesheet = """
                            QLabel { 
                                background-color: #17202b;
                            }
                        """
        return stylesheet

    def combobox_stylesheet(self):
        if self.theme == "light":
            stylesheet = """
                QComboBox{
                        color: rgb(0, 0, 0);
                        background-color: rgb(238, 238, 236);
                        border-radius: 3px;
                        border: 2px solid rgb(200, 200, 200);
                        padding: 5px;
                        padding-left: 10px;
                    }

                    QComboBox:hover{
                        border: 2px solid rgb(52, 59, 72);
                    }

                    QComboBox::drop-down {
                        subcontrol-origin: padding;
                        subcontrol-position: top right;
                        width: 25px;
                        border-left-width: 3px;
                        border-left-color: rgb(200, 200, 200);
                        border-left-style: solid;
                        border-top-right-radius: 3px;
                        border-bottom-right-radius: 3px;
                        background-image: url(icons:chevron-down.svg);
                        background-position: center;
                        background-repeat: no-reperat;
                     }

                    QComboBox QAbstractItemView {
                        color: rgb(0, 0, 0);
                        background-color: rgb(255, 255, 255);
                        padding:5px;
                        selection-background-color: rgb(39, 44, 54);
                    }
                """

        else:
            stylesheet = """
                QComboBox{
                        background-color: rgb(27, 29, 35);
                        border-radius: 5px;
                        border: 2px solid rgb(52, 59, 72);
                        padding: 5px;
                        padding-left: 10px;
                    }
                QComboBox:hover{
                        border: 2px solid rgb(82, 94, 88);
                    }
                QComboBox::drop-down {
                        subcontrol-origin: padding;
                        subcontrol-position: top right;
                        width: 25px;
                        border-left-width: 3px;
                        border-left-color: rgba(39, 44, 54, 150);
                        border-left-style: solid;
                        border-top-right-radius: 3px;
                        border-bottom-right-radius: 3px;
                        background-image: url(icons:light/cil-arrow-bottom.png);
                        background-position: center;
                        background-repeat: no-reperat;
                     }
                QComboBox QAbstractItemView {
                        color: rgb(255, 121, 198);
                        background-color: rgb(33, 37, 43);
                        padding: 10px;
                        selection-background-color: rgb(39, 44, 54);
                    }
                    """
        return stylesheet

