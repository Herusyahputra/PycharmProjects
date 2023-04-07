# Form implementation generated from reading ui file 'ui_select_media_source.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(518, 284)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.central_widget = QtWidgets.QWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.central_widget.sizePolicy().hasHeightForWidth())
        self.central_widget.setSizePolicy(sizePolicy)
        self.central_widget.setMaximumSize(QtCore.QSize(500, 16777215))
        self.central_widget.setStyleSheet("QWidget {\n"
                                          "    color: rgb(221, 221, 221);\n"
                                          "    font: 10pt \"Segoe UI\";\n"
                                          "}\n"
                                          "\n"
                                          "#frame{\n"
                                          "    background-color: rgb(37, 41, 48);\n"
                                          "    border: 2px solid rgb(155, 125, 175);\n"
                                          "    border-radius: 10px;\n"
                                          "}\n"
                                          "\n"
                                          "#label_title{\n"
                                          "color: rgb(238,238,238);\n"
                                          "font: 14pt \"Segoe UI\";\n"
                                          "}\n"
                                          "\n"
                                          "QLineEdit {\n"
                                          "    font: 9pt \"Segoe UI\";\n"
                                          "    background-color: rgb(33, 37, 43);\n"
                                          "    border-radius: 5px;\n"
                                          "    border: 1px solid rgb(145, 125, 175);\n"
                                          "    padding-left: 10px;\n"
                                          "    selection-color: rgb(255, 255, 255);\n"
                                          "    selection-background-color: rgb(255, 121, 198);\n"
                                          "}\n"
                                          "QLineEdit:hover {\n"
                                          "    border: 2px solid rgb(64, 71, 88);\n"
                                          "}\n"
                                          "QLineEdit:focus {\n"
                                          "    border: 2px solid rgb(91, 101, 124);\n"
                                          "}\n"
                                          "\n"
                                          "QComboBox{\n"
                                          "    background-color: rgb(27, 29, 35);\n"
                                          "    border-radius: 5px;\n"
                                          "    border: 1px solid rgb(145, 125, 175);\n"
                                          "    padding: 1px;\n"
                                          "    padding-left: 15px;\n"
                                          "}\n"
                                          "#portCamera::drop-down{\n"
                                          "border:0Px;\n"
                                          "}\n"
                                          "QComboBox:hover{\n"
                                          "    border: 2px solid rgb(64, 71, 88);\n"
                                          "}\n"
                                          "QComboBox::drop-down {\n"
                                          "    subcontrol-origin: padding;\n"
                                          "    subcontrol-position: top right;\n"
                                          "    width: 25px; \n"
                                          "    border-left-width: 3px;\n"
                                          "    border-left-color: rgba(39, 44, 54, 150);\n"
                                          "    border-left-style: solid;\n"
                                          "    border-top-right-radius: 3px;\n"
                                          "    border-bottom-right-radius: 3px;    \n"
                                          "    background-position: center;\n"
                                          "    background-repeat: no-reperat;\n"
                                          "    background-image: url(icons:light/cil-arrow-bottom.png);\n"
                                          " }\n"
                                          "QComboBox QAbstractItemView {\n"
                                          "    color: rgb(255, 121, 198);    \n"
                                          "    background-color: rgb(33, 37, 43);\n"
                                          "    padding: 10px;\n"
                                          "    selection-background-color: rgb(39, 44, 54);\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton {\n"
                                          "    border: 2px solid rgb(52, 59, 72);\n"
                                          "    border-radius: 5px;    \n"
                                          "    background-color: rgb(52, 59, 72);\n"
                                          "}\n"
                                          "QPushButton:hover {\n"
                                          "    background-color: rgb(57, 65, 80);\n"
                                          "    border: 2px solid rgb(61, 70, 86);\n"
                                          "}\n"
                                          "QPushButton:pressed {    \n"
                                          "    background-color: rgb(35, 40, 49);\n"
                                          "    border: 2px solid rgb(43, 50, 61);\n"
                                          "}")
        self.central_widget.setObjectName("central_widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.central_widget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame = QtWidgets.QFrame(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_title = QtWidgets.QLabel(self.frame)
        self.label_title.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("")
        self.label_title.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.label_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.verticalLayout_3.addWidget(self.label_title)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(80, 0))
        self.label_2.setMaximumSize(QtCore.QSize(80, 35))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.label_2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.comboBox_camera_sources = QtWidgets.QComboBox(self.frame)
        self.comboBox_camera_sources.setMinimumSize(QtCore.QSize(250, 35))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.comboBox_camera_sources.setFont(font)
        self.comboBox_camera_sources.setObjectName("comboBox_camera_sources")
        self.comboBox_camera_sources.addItem("")
        self.comboBox_camera_sources.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_camera_sources)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setMinimumSize(QtCore.QSize(80, 0))
        self.label_3.setMaximumSize(QtCore.QSize(80, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.label_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.label_3.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.comboBox_type_cam = QtWidgets.QComboBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_type_cam.sizePolicy().hasHeightForWidth())
        self.comboBox_type_cam.setSizePolicy(sizePolicy)
        self.comboBox_type_cam.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_type_cam.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBox_type_cam.setObjectName("comboBox_type_cam")
        self.horizontalLayout_2.addWidget(self.comboBox_type_cam)
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setMinimumSize(QtCore.QSize(0, 0))
        self.label_5.setMaximumSize(QtCore.QSize(60, 35))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.label_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.label_5.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.comboBox_id_url_camera = QtWidgets.QComboBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_id_url_camera.sizePolicy().hasHeightForWidth())
        self.comboBox_id_url_camera.setSizePolicy(sizePolicy)
        self.comboBox_id_url_camera.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.comboBox_id_url_camera.setFont(font)
        self.comboBox_id_url_camera.setObjectName("comboBox_id_url_camera")
        self.horizontalLayout_2.addWidget(self.comboBox_id_url_camera)
        self.media_path = QtWidgets.QLineEdit(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.media_path.sizePolicy().hasHeightForWidth())
        self.media_path.setSizePolicy(sizePolicy)
        self.media_path.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.media_path.setFont(font)
        self.media_path.setInputMask("")
        self.media_path.setText("")
        self.media_path.setObjectName("media_path")
        self.horizontalLayout_2.addWidget(self.media_path)
        self.btn_load_media = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_load_media.sizePolicy().hasHeightForWidth())
        self.btn_load_media.setSizePolicy(sizePolicy)
        self.btn_load_media.setMinimumSize(QtCore.QSize(75, 30))
        self.btn_load_media.setObjectName("btn_load_media")
        self.horizontalLayout_2.addWidget(self.btn_load_media)
        self.verticalLayout.addWidget(self.frame_2)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(5)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setMinimumSize(QtCore.QSize(80, 0))
        self.label_4.setMaximumSize(QtCore.QSize(80, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.label_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.label_4.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_8.addWidget(self.label_4)
        self.comboBox_parameters = QtWidgets.QComboBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_parameters.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters.setSizePolicy(sizePolicy)
        self.comboBox_parameters.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_parameters.setObjectName("comboBox_parameters")
        self.horizontalLayout_8.addWidget(self.comboBox_parameters)
        self.btn_form_camera_params = QtWidgets.QPushButton(self.frame)
        self.btn_form_camera_params.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_form_camera_params.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_form_camera_params.setText("")
        self.btn_form_camera_params.setObjectName("btn_form_camera_params")
        self.horizontalLayout_8.addWidget(self.btn_form_camera_params)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.btn_cancel = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_cancel.sizePolicy().hasHeightForWidth())
        self.btn_cancel.setSizePolicy(sizePolicy)
        self.btn_cancel.setMinimumSize(QtCore.QSize(90, 30))
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout_6.addWidget(self.btn_cancel)
        self.btn_ok = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_ok.sizePolicy().hasHeightForWidth())
        self.btn_ok.setSizePolicy(sizePolicy)
        self.btn_ok.setMinimumSize(QtCore.QSize(55, 30))
        self.btn_ok.setObjectName("btn_ok")
        self.horizontalLayout_6.addWidget(self.btn_ok)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_3.addWidget(self.frame)
        self.verticalLayout_2.addWidget(self.central_widget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select Camera Source"))
        self.label_title.setText(_translate("Dialog", "Select Media Source"))
        self.label_2.setText(_translate("Dialog", "Source :"))
        self.comboBox_camera_sources.setItemText(0, _translate("Dialog", "Streaming Camera"))
        self.comboBox_camera_sources.setItemText(1, _translate("Dialog", "Image/Video"))
        self.label_3.setText(_translate("Dialog", "Type cam:"))
        self.label_5.setText(_translate("Dialog", "ID/URL:"))
        self.media_path.setPlaceholderText(_translate("Dialog", "Please select file"))
        self.btn_load_media.setText(_translate("Dialog", "Open File"))
        self.label_4.setText(_translate("Dialog", "Params:"))
        self.btn_cancel.setText(_translate("Dialog", "Cancel"))
        self.btn_ok.setText(_translate("Dialog", "Ok"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
