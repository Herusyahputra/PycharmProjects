import os
from PyQt6 import QtCore, QtGui


class IconSource(object):
    def __init__(self):
        self.__realpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        QtCore.QDir.addSearchPath("icons", CURRENT_DIRECTORY + "/icons")

    def get_icon_forward(self):
        return QtGui.QIcon(self.__realpath + "/icons/forward.png")

    def get_icon_reverse(self):
        return QtGui.QIcon(self.__realpath + "/icons/reverse.png")

    def get_icon_turn_left(self):
        return QtGui.QIcon(self.__realpath + "/icons/turn_left.png")

    def get_icon_turn_right(self):
        return QtGui.QIcon(self.__realpath + "/icons/turn_right.png")

    def driver_view(self):
        return QtGui.QIcon(self.__realpath + "/icons/driver_view.png")

    def second_driver_view(self):
        return QtGui.QIcon(self.__realpath + "/icons/second_driver_view.png")

    def get_icon_screenshot(self):
        return QtGui.QIcon(self.__realpath + "/icons/screenshot.png")

    def get_icon_setting(self):
        return QtGui.QIcon(self.__realpath + "/icons/setting.png")

    def get_icon_records(self):
        return QtGui.QIcon(self.__realpath + "/icons/rec.png")

    def get_icon_dash_front(self):
        return QtGui.QIcon(self.__realpath + "/icons/dash_front.png")

    def get_icon_dash_driver(self):
        return QtGui.QIcon(self.__realpath + "/icons/dash_driver.png")
