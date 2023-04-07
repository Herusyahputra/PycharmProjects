from PyQt6 import QtGui, QtCore, QtWidgets


class SetIconsUI:
    def __init__(self, main_ui):
        super().__init__()
        self.ui = main_ui

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons:github.svg"), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.ui.github_button.setIcon(icon)

        label = QtWidgets.QLabel()
        label.setText("  MoilApp v3.0 (c) 2023  ")
        self.ui.statusBar.addPermanentWidget(label)

        self.ui.label_logo.setPixmap(QtGui.QPixmap("icons:moil.png"))
        self.ui.label_logo.setScaledContents(True)

        self.ui.label_10.setPixmap(QtGui.QPixmap("icons:mouse-pointer.png"))
        self.ui.label_10.setScaledContents(True)

        self.ui.rotate_left_button.setIcon(QtGui.QIcon("icons:rotate-ccw.svg"))
        self.ui.rotate_right_button.setIcon(QtGui.QIcon("icons:rotate-cw.svg"))
        self.ui.zoom_out_button.setIcon(QtGui.QIcon("icons:minus.svg"))
        self.ui.zoom_in_button.setIcon(QtGui.QIcon("icons:plus.svg"))

        self.ui.reset_view_button.setIcon(QtGui.QIcon("icons:reset.png"))
        self.ui.close_plugin_button.setIcon(QtGui.QIcon("icons:logout.png"))

        self.ui.btn_about_us.setIcon(QtGui.QIcon("icons:user.svg"))

        self.ui.add_plugins_button.setIcon(QtGui.QIcon("icons:plugins.png"))
        self.ui.delete_plugins_button.setIcon(QtGui.QIcon("icons:trash.svg"))
        self.ui.help_plugins_button.setIcon(QtGui.QIcon("icons:info.svg"))

        self.ui.label_result.setPixmap(QtGui.QPixmap("icons:moilapp.png"))
        self.ui.label_image_original.setPixmap(QtGui.QPixmap("icons:moilapp.png"))

        self.ui.play_pause_button.setIcon(QtGui.QIcon("icons:play.svg"))
        self.ui.rewind_button.setIcon(QtGui.QIcon("icons:rewind.svg"))
        self.ui.stop_button.setIcon(QtGui.QIcon("icons:square.svg"))
        self.ui.forward_button.setIcon(QtGui.QIcon("icons:fast-forward.svg"))
        self.ui.screenshoot_button.setIcon(QtGui.QIcon("icons:maximize.svg"))
        self.ui.record_button.setIcon(QtGui.QIcon("icons:video.svg"))



