import json
import os
from .form_crud_parameters import CameraParametersForm
from moil_camera import MoilCam

try:
    from PyQt6 import QtWidgets, QtCore, QtGui
    from .ui_select_media_source_pyqt6 import Ui_Dialog
    pyqt_version = "pyqt6"

except:
    from PyQt5 import QtWidgets, QtCore, QtGui
    from .ui_select_media_source_pyqt5 import Ui_Dialog
    pyqt_version = "pyqt5"


class CameraSource(Ui_Dialog):
    def __init__(self, RecentWindow):
        """
        Create class controllers open camera with inheritance from Ui Dialog Class.

        Args:
            RecentWindow ():
        """
        super(CameraSource, self).__init__()
        self.recent_win = RecentWindow
        self.setupUi(self.recent_win)

        # self.central_widget.setStyleSheet(style_appearance)
        self.recent_win.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.recent_win.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.frame.mousePressEvent = self.mousePressEvent
        self.frame.mouseMoveEvent = self.moveWindow

        type_camera = MoilCam.supported_cam_type()
        self.comboBox_type_cam.addItems(type_camera)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.database_camera_parameters = dir_path + "/camera_parameters.json"
        with open(self.database_camera_parameters) as f:
            self.data = json.load(f)

        self.camera_source = None
        self.parameter_selected = None
        self.cam_type = None
        self.comboBox_id_url_camera.addItem('http://<ip-address-cam>:8000/stream.mjpg')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons:text.svg"), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.btn_form_camera_params.setIconSize(QtCore.QSize(40, 40))
        self.btn_form_camera_params.setIcon(icon)

        self.handle_activated_comboBox_camera_source()
        self.handle_activate_type_camera()
        self.add_list_camera_to_combobox()
        self.comboBox_camera_sources.activated.connect(self.handle_activated_comboBox_camera_source)
        self.comboBox_type_cam.activated.connect(self.handle_activate_type_camera)
        self.btn_form_camera_params.clicked.connect(self.open_camera_parameters_form)
        self.btn_load_media.clicked.connect(self.open_media_path)
        self.btn_cancel.clicked.connect(self.onclick_comboBox_cancel)
        self.btn_ok.clicked.connect(self.onclick_comboBox_oke)

    def add_list_camera_to_combobox(self):
        self.comboBox_parameters.blockSignals(True)
        self.comboBox_parameters.clear()
        parameter_list = []

        for key in self.data.keys():
            parameter_list.append(key)
        self.comboBox_parameters.addItems(parameter_list)
        self.comboBox_parameters.blockSignals(False)

    def moveWindow(self, event):
        if pyqt_version == "pyqt6":
            if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
                self.recent_win.move(self.recent_win.pos() + event.globalPosition().toPoint() - self.dragPos)
                self.dragPos = event.globalPosition().toPoint()
                event.accept()

        else:
            if event.buttons() == QtCore.Qt.LeftButton:
                delta = QtCore.QPoint(event.globalPos() - self.dragPos)
                self.recent_win.move(self.recent_win.x() + delta.x(), self.recent_win.y() + delta.y())
                self.dragPos = event.globalPos()
                event.accept()

    def mousePressEvent(self, event):
        if pyqt_version == "pyqt6":
            self.dragPos = event.globalPosition().toPoint()
        else:
            self.dragPos = event.globalPos()

    def refresh_camera_parameter_list(self):
        """
        When editing the camera parameter, this will show the list of the camera parameter in uptodate
        Returns:
            None
        """
        self.comboBox_parameters.clear()
        new_list = []
        with open(self.database_camera_parameters) as f:
            data_parameter = json.load(f)
        for key in data_parameter.keys():
            new_list.append(key)
        self.comboBox_parameters.addItems(new_list)

    def open_camera_parameters_form(self):
        open_cam_params = QtWidgets.QDialog()
        CameraParametersForm(open_cam_params, self.database_camera_parameters)
        open_cam_params.exec()
        self.refresh_camera_parameter_list()

    def handle_activate_type_camera(self):
        if self.comboBox_type_cam.currentText() == "opencv_usb_cam":
            self.label_5.setText("ID :")
            self.comboBox_id_url_camera.clear()
            camera = [str(x) for x in MoilCam.scan_id("opencv_usb_cam")]
            self.comboBox_id_url_camera.addItems(camera)
        elif self.comboBox_type_cam.currentText() == "raspberry_pi4_ip_cam":
            self.label_5.setText("URL :")
            self.comboBox_id_url_camera.clear()
            camera = [str(x) for x in MoilCam.scan_id("raspberry_pi4_ip_cam")]
            self.comboBox_id_url_camera.addItems(camera)

        else:
            self.label_5.setText("URL :")

    def handle_activated_comboBox_camera_source(self):
        """
        Handle the selection from comboBox of source camera.

        Returns:

        """
        if self.comboBox_camera_sources.currentText() == "Streaming Camera":
            self.media_path.hide()
            self.btn_load_media.hide()
            self.comboBox_type_cam.show()
            self.comboBox_id_url_camera.show()
            self.label_5.show()
            self.label_3.setText("Type cam :")

        else:
            self.label_3.setText("Media Path :")
            self.comboBox_type_cam.hide()
            self.comboBox_id_url_camera.hide()
            self.media_path.show()
            self.btn_load_media.show()
            self.label_5.hide()

    def open_media_path(self):
        if pyqt_version == "pyqt6":
            option = QtWidgets.QFileDialog.Option.DontUseNativeDialog
            file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Load Media", "../",
                                                                 "Files format (*.jpeg *.jpg *.png *.gif *.bmg *.avi *.mp4)",
                                                                 options=option)
        else:
            options = QtWidgets.QFileDialog.DontUseNativeDialog
            file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Load Media", "../",
                                                                 "Files format (*.jpeg *.jpg *.png *.gif *.bmg *.avi *.mp4)",
                                                                 options=options)
        self.media_path.setText(file_path)

    def camera_source_used(self):
        """
        This function will return the source of camera used depend on what the camera use.

        Returns:
            camera source
        """
        if self.comboBox_camera_sources.currentText() == "Streaming Camera":
            if self.comboBox_id_url_camera.currentText() != "":
                if self.comboBox_id_url_camera.currentText().endswith('.mjpg'):
                    self.camera_source = self.comboBox_id_url_camera.currentText()
                else:
                    self.camera_source = int(self.comboBox_id_url_camera.currentText())

        else:
            if self.media_path.text() != "":
                self.camera_source = self.media_path.text()

            else:
                self.camera_source = None

        self.cam_type = self.comboBox_type_cam.currentText()
        self.parameter_selected = self.comboBox_parameters.currentText()

    def onclick_comboBox_oke(self):
        """
        Open the camera following the parent function and close the dialog window.

        Returns:

        """
        self.camera_source_used()
        self.recent_win.close()

    def onclick_comboBox_cancel(self):
        """
        close the window when you click the buttonBox cancel.

        Returns:

        """
        self.recent_win.close()


style_appearance = """
    QWidget {
        color: rgb(221, 221, 221);
        font: 10pt "Segoe UI";
    }
    
    #frame{
        background-color: rgb(37, 41, 48);
        border: 2px solid rgb(155, 125, 175);
        border-radius: 10px;
    }
    
    #label_title{
    color: rgb(238,238,238);
    font: 14pt "Segoe UI";
    }
    
    QLineEdit {
        font: 9pt "Segoe UI";
        background-color: rgb(33, 37, 43);
        border-radius: 5px;
        border: 1px solid rgb(145, 125, 175);
        padding-left: 10px;
        selection-color: rgb(255, 255, 255);
        selection-background-color: rgb(255, 121, 198);
    }
    QLineEdit:hover {
        border: 2px solid rgb(64, 71, 88);
    }
    QLineEdit:focus {
        border: 2px solid rgb(91, 101, 124);
    }
    
    QComboBox{
        background-color: rgb(27, 29, 35);
        border-radius: 5px;
        border: 1px solid rgb(145, 125, 175);
        padding: 5px;
        padding-left: 10px;
    }

    QComboBox:hover{
        border: 2px solid rgb(64, 71, 88);
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
        background-position: center;
        background-image: url(icons:light/cil-arrow-bottom.png);
        background-repeat: no-reperat;
     }
    QComboBox QAbstractItemView {
        color: rgb(255, 121, 198);	
        background-color: rgb(33, 37, 43);
        padding: 10px;
        selection-background-color: rgb(39, 44, 54);
    }
    
    QPushButton {
        border: 2px solid rgb(52, 59, 72);
        border-radius: 5px;	
        background-color: rgb(52, 59, 72);
    }
    QPushButton:hover {
        background-color: rgb(57, 65, 80);
        border: 2px solid rgb(61, 70, 86);
    }
    QPushButton:pressed {	
        background-color: rgb(35, 40, 49);
        border: 2px solid rgb(43, 50, 61);
    }
"""
