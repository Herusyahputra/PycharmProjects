import os
import shutil
import sys

from PyQt6 import QtWidgets, QtGui, QtCore
from pathlib import Path
from .control_plugin_collection import PluginCollection


class PluginManager(object):
    def __init__(self, main_control):
        super().__init__()
        self.main_control = main_control
        self.plugin = PluginCollection("plugins")
        self.apps_activated = None
        self.index = None
        self.init_available_plugin()
        self.connect_to_event()

    def connect_to_event(self):
        self.main_control.ui.add_plugins_button.clicked.connect(self.install_new_plugin)
        self.main_control.ui.delete_plugins_button.clicked.connect(self.action_delete_apps)
        self.main_control.ui.close_plugin_button.clicked.connect(self.main_control.back_to_home)
        self.main_control.ui.help_plugins_button.clicked.connect(self.help_menu_plugin)

    def init_available_plugin(self):
        for i in range(self.main_control.ui.layout_application.count()):
            self.main_control.ui.layout_application.itemAt(i).widget().close()

        for i in range(len(self.plugin.name_application)):
            icon = self.plugin.get_icon_(i)
            button = self.add_btn_apps_plugin(icon, self.plugin.name_application[i])
            button.clicked.connect(self.open_plugin_apps)
            self.main_control.ui.layout_application.addWidget(button)

    def install_new_plugin(self):
        options = QtWidgets.QFileDialog.Option.DontUseNativeDialog
        dir_plugin = QtWidgets.QFileDialog.getExistingDirectory(None,
                                                                'Select Application Folder', "../plugin_store", options)
        if dir_plugin:
            original = dir_plugin
            name_plug = os.path.basename(os.path.normpath(original))
            path_file = os.path.dirname(os.path.realpath(__file__))
            target = path_file + '/plugins/'
            name_exist = Path(target + name_plug)
            if name_exist.exists():
                QtWidgets.QMessageBox.warning(None, "Warning !!", "Plugins already exist!!")
            else:
                listApp = self.plugin.name_application
                self.main_control.model.copy_directory(original, target)
                self.plugin.reload_plugins()
                newList = self.plugin.name_application
                name = [item for item in newList if item not in listApp]

                def listToString(listIn):
                    return " ".join(listIn)

                index = newList.index(listToString(name))
                icon = self.plugin.get_icon_(index)
                button = self.add_btn_apps_plugin(icon, self.plugin.name_application[index])
                button.clicked.connect(self.open_plugin_apps)
                self.main_control.ui.layout_application.addWidget(button)
                self.pop_up_message_box("Plugins was successfully added!!")

    def refresh_theme_widget(self):
        if self.index is not None:
            self.plugin.change_theme(self.index)

    def open_plugin_apps(self):
        button = self.main_control.sender()
        index = self.plugin.name_application.index(button.objectName())
        if index != self.index:
            self.index = self.plugin.name_application.index(button.objectName())
            self.main_control.ui.delete_plugins_button.show()
            self.main_control.ui.close_plugin_button.show()
            for i in range(self.main_control.ui.layout_plugin.count()):
                self.main_control.ui.layout_plugin.itemAt(i).widget().close()

            widget = self.plugin.get_widget(self.index, self.main_control.model)
            self.main_control.ui.layout_plugin.addWidget(widget)
            self.main_control.ui.widget_container_content.setCurrentIndex(1)
            self.main_control.ui.frame_btn_moilapp.hide()
            self.main_control.ui.frame_button_view.hide()
            self.apps_activated = button.objectName()

    @classmethod
    def add_btn_apps_plugin(cls, icon_, name):
        button = QtWidgets.QPushButton()
        button.setObjectName(name)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy)
        button.setMinimumSize(QtCore.QSize(40, 25))
        button.setMaximumSize(QtCore.QSize(35, 16777215))
        if icon_ is not None:
            icon = QtGui.QIcon(icon_)
            button.setIcon(icon)
        button.setIconSize(QtCore.QSize(30, 30))
        return button

    def action_delete_apps(self):
        index = self.plugin.name_application.index(self.apps_activated)
        self.delete_apps(index)

    def delete_apps(self, index):
        """
        Delete selected application from the list.

        Returns:
            None.
        """
        name = self.plugin.name_application[index]
        path = self.plugin.path_folder[index]
        path = path.split(".")[1]

        path_file = os.path.dirname(os.path.realpath(__file__))
        path = path_file + '/plugins/'+path

        reply = QtWidgets.QMessageBox.question(None, 'Message',
                                               "Are you sure want to delete \n" +
                                               name + " application ?\n",
                                               QtWidgets.QMessageBox.StandardButton.Yes |
                                               QtWidgets.QMessageBox.StandardButton.No,
                                               QtWidgets.QMessageBox.StandardButton.No)

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            shutil.rmtree(path, ignore_errors=True)
            self.plugin.reload_plugins()
            self.init_available_plugin()
            self.pop_up_message_box("Plugins was successfully deleted !!")
            self.main_control.back_to_home()

    def help_menu_plugin(self):
        if self.main_control.ui.widget_container_content.currentIndex() == 0:
            message = "Help menu plugin under development \n" \
                      "we Will inform you after finish!!\n"

        else:
            print(self.plugin.get_description(self.index))
            message = "Help menu plugin under development \n" \
                      "we Will inform you after finish!!\n\n" \
                      "Note App: " + self.plugin.get_description(self.index)
        self.pop_up_message_box(message)

    @classmethod
    def pop_up_message_box(cls, message=""):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setStyleSheet("font-family: Segoe UI; font-size:14px;")
        msg.setWindowTitle("Information")
        # setting message for Message Box
        msg.setText("Information !! \n\n" + message)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.show()

        def close_msg():
            msg.done(0)

        QtCore.QTimer.singleShot(6000, close_msg)
