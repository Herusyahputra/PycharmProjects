# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1325, 737)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_main = QtWidgets.QFrame(Form)
        self.frame_main.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_main.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_main.setObjectName("frame_main")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_main)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_button_control = QtWidgets.QFrame(self.frame_main)
        self.frame_button_control.setMaximumSize(QtCore.QSize(400, 30))
        self.frame_button_control.setObjectName("frame_button_control")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_button_control)
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton = QtWidgets.QPushButton(self.frame_button_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.label_4 = QtWidgets.QLabel(self.frame_button_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(40, 0))
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.spinBox = QtWidgets.QSpinBox(self.frame_button_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setMinimum(400)
        self.spinBox.setMaximum(4000)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_3.addWidget(self.spinBox)
        self.label_5 = QtWidgets.QLabel(self.frame_button_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(40, 0))
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.spinBox_2 = QtWidgets.QSpinBox(self.frame_button_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_2.sizePolicy().hasHeightForWidth())
        self.spinBox_2.setSizePolicy(sizePolicy)
        self.spinBox_2.setMinimum(20)
        self.spinBox_2.setMaximum(4000)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_3.addWidget(self.spinBox_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_5.addWidget(self.frame_button_control)
        self.frame = QtWidgets.QFrame(self.frame_main)
        self.frame.setMinimumSize(QtCore.QSize(400, 0))
        self.frame.setMaximumSize(QtCore.QSize(400, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMinimumSize(QtCore.QSize(0, 300))
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(0, 300))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout_5.addWidget(self.frame)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.frame_2 = QtWidgets.QFrame(self.frame_main)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setContentsMargins(5, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_control_view = QtWidgets.QFrame(self.frame_2)
        self.frame_control_view.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_control_view.setObjectName("frame_control_view")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_control_view)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBox = QtWidgets.QCheckBox(self.frame_control_view)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_4.addWidget(self.checkBox)
        self.radioButton = QtWidgets.QRadioButton(self.frame_control_view)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_4.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.frame_control_view)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_4.addWidget(self.radioButton_2)
        self.line_2 = QtWidgets.QFrame(self.frame_control_view)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_4.addWidget(self.line_2)
        self.label_6 = QtWidgets.QLabel(self.frame_control_view)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.spinBox_3 = QtWidgets.QSpinBox(self.frame_control_view)
        self.spinBox_3.setMinimumSize(QtCore.QSize(50, 0))
        self.spinBox_3.setMinimum(12)
        self.spinBox_3.setMaximum(110)
        self.spinBox_3.setObjectName("spinBox_3")
        self.horizontalLayout_4.addWidget(self.spinBox_3)
        self.label_7 = QtWidgets.QLabel(self.frame_control_view)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.spinBox_4 = QtWidgets.QSpinBox(self.frame_control_view)
        self.spinBox_4.setMinimumSize(QtCore.QSize(50, 0))
        self.spinBox_4.setMaximum(150)
        self.spinBox_4.setProperty("value", 110)
        self.spinBox_4.setObjectName("spinBox_4")
        self.horizontalLayout_4.addWidget(self.spinBox_4)
        self.label_8 = QtWidgets.QLabel(self.frame_control_view)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_4.addWidget(self.label_8)
        self.c_top = QtWidgets.QDoubleSpinBox(self.frame_control_view)
        self.c_top.setMinimumSize(QtCore.QSize(50, 0))
        self.c_top.setMaximum(1.0)
        self.c_top.setSingleStep(0.01)
        self.c_top.setObjectName("c_top")
        self.horizontalLayout_4.addWidget(self.c_top)
        self.label_9 = QtWidgets.QLabel(self.frame_control_view)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_4.addWidget(self.label_9)
        self.c_btn = QtWidgets.QDoubleSpinBox(self.frame_control_view)
        self.c_btn.setMinimumSize(QtCore.QSize(50, 0))
        self.c_btn.setMaximum(1.0)
        self.c_btn.setSingleStep(0.01)
        self.c_btn.setProperty("value", 1.0)
        self.c_btn.setObjectName("c_btn")
        self.horizontalLayout_4.addWidget(self.c_btn)
        self.label_10 = QtWidgets.QLabel(self.frame_control_view)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_4.addWidget(self.label_10)
        self.c_left = QtWidgets.QDoubleSpinBox(self.frame_control_view)
        self.c_left.setMinimumSize(QtCore.QSize(50, 0))
        self.c_left.setMaximum(1.0)
        self.c_left.setSingleStep(0.01)
        self.c_left.setObjectName("c_left")
        self.horizontalLayout_4.addWidget(self.c_left)
        self.label_11 = QtWidgets.QLabel(self.frame_control_view)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_4.addWidget(self.label_11)
        self.c_right = QtWidgets.QDoubleSpinBox(self.frame_control_view)
        self.c_right.setMinimumSize(QtCore.QSize(50, 0))
        self.c_right.setMaximum(1.0)
        self.c_right.setSingleStep(0.01)
        self.c_right.setProperty("value", 1.0)
        self.c_right.setObjectName("c_right")
        self.horizontalLayout_4.addWidget(self.c_right)
        self.pushButton_zoom_out = QtWidgets.QPushButton(self.frame_control_view)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_zoom_out.sizePolicy().hasHeightForWidth())
        self.pushButton_zoom_out.setSizePolicy(sizePolicy)
        self.pushButton_zoom_out.setMinimumSize(QtCore.QSize(30, 0))
        self.pushButton_zoom_out.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_zoom_out.setObjectName("pushButton_zoom_out")
        self.horizontalLayout_4.addWidget(self.pushButton_zoom_out)
        self.pushButton_zoom_in = QtWidgets.QPushButton(self.frame_control_view)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_zoom_in.sizePolicy().hasHeightForWidth())
        self.pushButton_zoom_in.setSizePolicy(sizePolicy)
        self.pushButton_zoom_in.setMinimumSize(QtCore.QSize(30, 0))
        self.pushButton_zoom_in.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_zoom_in.setObjectName("pushButton_zoom_in")
        self.horizontalLayout_4.addWidget(self.pushButton_zoom_in)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_3.addWidget(self.frame_control_view)
        self.scrollArea = QtWidgets.QScrollArea(self.frame_2)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 900, 683))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.horizontalLayout.addWidget(self.frame_2)
        self.verticalLayout.addWidget(self.frame_main)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Open Media"))
        self.label_4.setText(_translate("Form", "Icx:"))
        self.label_5.setText(_translate("Form", "Icy:"))
        self.checkBox.setText(_translate("Form", "Pano Car"))
        self.radioButton.setText(_translate("Form", "Yes"))
        self.radioButton_2.setText(_translate("Form", "No"))
        self.label_6.setText(_translate("Form", "Alpha min:"))
        self.label_7.setText(_translate("Form", "alpha max:"))
        self.label_8.setText(_translate("Form", "top:"))
        self.label_9.setText(_translate("Form", "buttom:"))
        self.label_10.setText(_translate("Form", "left:"))
        self.label_11.setText(_translate("Form", "right:"))
        self.pushButton_zoom_out.setText(_translate("Form", "-"))
        self.pushButton_zoom_in.setText(_translate("Form", "+"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
