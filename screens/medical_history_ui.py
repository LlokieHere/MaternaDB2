from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1301, 864)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ── SIDEBAR ───────────────────────────────────────────────────────────
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 60, 231, 761))
        self.frame.setStyleSheet("background-color: rgb(192, 116, 182)")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        self.pushButton = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton.setGeometry(QtCore.QRect(20, 180, 191, 41))
        self.pushButton.setStyleSheet("background-color: rgb(240, 230, 240);")
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 230, 191, 41))
        self.pushButton_2.setStyleSheet("background-color: rgb(240, 230, 240);")
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 280, 191, 41))
        self.pushButton_3.setStyleSheet("background-color: rgb(240, 230, 240);")
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 330, 191, 41))
        self.pushButton_4.setStyleSheet("background-color: rgb(240, 230, 240);")
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 500, 191, 41))
        self.pushButton_5.setObjectName("pushButton_5")

        # ── TOP BAR ───────────────────────────────────────────────────────────
        self.frame_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 1341, 61))
        self.frame_2.setStyleSheet("background-color: rgb(26, 26, 62)")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")

        self.label_2 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(130, 0, 91, 61))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(30, 10, 100, 45))
        self.label_3.setMinimumSize(QtCore.QSize(100, 45))
        font2 = QtGui.QFont()
        font2.setFamily("Segoe UI")
        font2.setPointSize(12)
        self.label_3.setFont(font2)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")

        # ── CONTENT FRAME ─────────────────────────────────────────────────────
        self.frame_3 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(230, 60, 1071, 761))
        self.frame_3.setStyleSheet("background-color: rgb(240, 230, 240)")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")

        self.label = QtWidgets.QLabel(parent=self.frame_3)
        self.label.setGeometry(QtCore.QRect(40, 20, 401, 61))
        font3 = QtGui.QFont()
        font3.setFamily("Arial Black")
        font3.setPointSize(30)
        self.label.setFont(font3)
        self.label.setObjectName("label")

        # ── PATIENT HEADER CARD ───────────────────────────────────────────────
        self.frame_4 = QtWidgets.QFrame(parent=self.frame_3)
        self.frame_4.setGeometry(QtCore.QRect(40, 80, 1001, 141))
        self.frame_4.setStyleSheet(
            "border-radius: 15px;\n"
            "background-color: rgb(26, 26, 62);"
        )
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")

        self.frame_5 = QtWidgets.QFrame(parent=self.frame_4)
        self.frame_5.setGeometry(QtCore.QRect(20, 20, 111, 91))
        self.frame_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName("frame_5")

        self.patient_name = QtWidgets.QLabel(parent=self.frame_4)
        self.patient_name.setGeometry(QtCore.QRect(170, 15, 600, 30))
        self.patient_name.setStyleSheet("color: rgb(255, 255, 255); font-size: 20px;")
        self.patient_name.setObjectName("patient_name")

        # ── HEADER INFO GRID ──────────────────────────────────────────────────
        # Row 0: Patient ID | value | Age | value | Registered | value
        # Row 1: Blood Type | value | PhilHealth# | value
        self.layoutWidget = QtWidgets.QWidget(parent=self.frame_4)
        self.layoutWidget.setGeometry(QtCore.QRect(170, 55, 660, 75))
        self.layoutWidget.setObjectName("layoutWidget")

        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setObjectName("gridLayout")

        white_style = "color: rgb(255, 255, 255); font-size: 16px;"

        # Row 0
        self.patient_id_label = QtWidgets.QLabel("Patient ID:", parent=self.layoutWidget)
        self.patient_id_label.setStyleSheet(white_style)
        self.patient_id_label.setObjectName("patient_id_label")
        self.gridLayout.addWidget(self.patient_id_label, 0, 0)

        self.placeholder_p_ID = QtWidgets.QLabel("placeholder", parent=self.layoutWidget)
        self.placeholder_p_ID.setStyleSheet(white_style)
        self.placeholder_p_ID.setObjectName("placeholder_p_ID")
        self.gridLayout.addWidget(self.placeholder_p_ID, 0, 1)

        self.age_label = QtWidgets.QLabel("Age:", parent=self.layoutWidget)
        self.age_label.setStyleSheet(white_style)
        self.age_label.setObjectName("age_label")
        self.gridLayout.addWidget(self.age_label, 0, 2)

        self.placeholder_age = QtWidgets.QLabel("—", parent=self.layoutWidget)
        self.placeholder_age.setStyleSheet(white_style)
        self.placeholder_age.setObjectName("placeholder_age")
        self.gridLayout.addWidget(self.placeholder_age, 0, 3)

        self.patient_id_label_3 = QtWidgets.QLabel("Registered:", parent=self.layoutWidget)
        self.patient_id_label_3.setStyleSheet(white_style)
        self.patient_id_label_3.setObjectName("patient_id_label_3")
        self.gridLayout.addWidget(self.patient_id_label_3, 0, 4)

        self.placeholder_register_date = QtWidgets.QLabel("MM/DD/YYYY", parent=self.layoutWidget)
        self.placeholder_register_date.setStyleSheet(white_style)
        self.placeholder_register_date.setObjectName("placeholder_register_date")
        self.gridLayout.addWidget(self.placeholder_register_date, 0, 5)

        # Row 1
        self.patient_id_label_2 = QtWidgets.QLabel("Blood Type:", parent=self.layoutWidget)
        self.patient_id_label_2.setStyleSheet(white_style)
        self.patient_id_label_2.setObjectName("patient_id_label_2")
        self.gridLayout.addWidget(self.patient_id_label_2, 1, 0)

        self.placeholder_p_bloodType = QtWidgets.QLabel("placeholder", parent=self.layoutWidget)
        self.placeholder_p_bloodType.setStyleSheet(white_style)
        self.placeholder_p_bloodType.setObjectName("placeholder_p_bloodType")
        self.gridLayout.addWidget(self.placeholder_p_bloodType, 1, 1)

        self.patient_id_label_4 = QtWidgets.QLabel("PhilHealth#:", parent=self.layoutWidget)
        self.patient_id_label_4.setStyleSheet(white_style)
        self.patient_id_label_4.setObjectName("patient_id_label_4")
        self.gridLayout.addWidget(self.patient_id_label_4, 1, 2)

        self.placeholder_philhealth_num = QtWidgets.QLabel("1234-5678-9012", parent=self.layoutWidget)
        self.placeholder_philhealth_num.setStyleSheet(white_style)
        self.placeholder_philhealth_num.setObjectName("placeholder_philhealth_num")
        self.gridLayout.addWidget(self.placeholder_philhealth_num, 1, 3)

        # ── TAB BAR ───────────────────────────────────────────────────────────
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.frame_3)
        self.layoutWidget1.setGeometry(QtCore.QRect(40, 240, 803, 40))
        self.layoutWidget1.setObjectName("layoutWidget1")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        tab_style = (
            "QPushButton { background: transparent; border: none; padding: 8px 18px;"
            "color: rgb(26, 26, 62); font-size: 14px; }"
            "QPushButton:hover { color: #000; }"
            "QPushButton:checked { color: #1a1a1a; border-bottom: 3px solid #2c2c54; }"
            "QPushButton:!checked { border-bottom: 3px solid transparent; }"
        )

        tab_active_style = (
            "QPushButton { background: transparent; border: none; padding: 8px 18px;"
            "color: rgb(26, 26, 62); font-size: 14px; font-weight: bold; }"
            "QPushButton:hover { color: #000; }"
            "QPushButton:checked { color: #1a1a1a; border-bottom: 3px solid #2c2c54; }"
            "QPushButton:!checked { border-bottom: 3px solid transparent; }"
        )

        sp_exp = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        self.pushButton_6 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_6.setSizePolicy(sp_exp)
        self.pushButton_6.setStyleSheet(tab_style)
        self.pushButton_6.setCheckable(True)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout.addWidget(self.pushButton_6)

        self.pushButton_7 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_7.setSizePolicy(sp_exp)
        self.pushButton_7.setStyleSheet(tab_style)
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout.addWidget(self.pushButton_7)

        self.pushButton_8 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_8.setSizePolicy(sp_exp)
        self.pushButton_8.setStyleSheet(tab_style)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout.addWidget(self.pushButton_8)

        # Medical History tab — active/checked
        self.pushButton_9 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_9.setSizePolicy(sp_exp)
        self.pushButton_9.setStyleSheet(tab_active_style)
        self.pushButton_9.setCheckable(True)
        self.pushButton_9.setChecked(True)
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout.addWidget(self.pushButton_9)

        self.pushButton_10 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_10.setSizePolicy(sp_exp)
        self.pushButton_10.setStyleSheet(tab_style)
        self.pushButton_10.setObjectName("pushButton_10")
        self.horizontalLayout.addWidget(self.pushButton_10)

        self.pushButton_11 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_11.setSizePolicy(sp_exp)
        self.pushButton_11.setStyleSheet(tab_style)
        self.pushButton_11.setObjectName("pushButton_11")
        self.horizontalLayout.addWidget(self.pushButton_11)

        # ── ADD CONDITION BUTTON ──────────────────────────────────────────────
        self.add_condition_btn = QtWidgets.QPushButton(parent=self.frame_3)
        self.add_condition_btn.setGeometry(QtCore.QRect(40, 300, 130, 31))
        self.add_condition_btn.setStyleSheet(
            "border-radius: 12px;"
            "background-color: rgb(192, 116, 182);"
            "color: white;"
            "border: 1px solid rgb(158, 136, 163);"
        )
        self.add_condition_btn.setObjectName("add_condition_btn")

        # ── MEDICAL HISTORY TABLE FRAME ───────────────────────────────────────
        self.left = QtWidgets.QFrame(parent=self.frame_3)
        self.left.setGeometry(QtCore.QRect(40, 340, 991, 381))
        self.left.setStyleSheet(
            "background-color: rgb(236, 198, 220);"
            "border: 1px solid rgb(158, 136, 163);"
            "border-radius: 15px;"
        )
        self.left.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.left.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.left.setObjectName("left")

        table_style = (
            "QTableWidget { background-color: rgb(236, 198, 220);"
            "border: 1px solid rgb(158, 136, 163); border-radius: 15px; }"
            "QTableWidget::item { background-color: rgb(236, 198, 220); color: rgb(21, 23, 61);"
            "padding: 8px; border: none; border-bottom: 1px solid rgb(210, 177, 200); }"
            "QTableWidget::item:selected { background-color: rgb(192, 116, 182); color: white; }"
            "QHeaderView::section { background-color: rgb(236, 198, 220); color: rgb(21, 23, 61);"
            "font-weight: bold; font-size: 10px; border: none;"
            "border-bottom: 1px solid rgb(155, 132, 160); padding: 5px; }"
            "QScrollBar:vertical { background: white; width: 6px; border-radius: 3px; }"
            "QScrollBar::handle:vertical { background: rgb(178, 100, 168); border-radius: 3px; }"
        )

        self.medical_history_table = QtWidgets.QTableWidget(parent=self.left)
        self.medical_history_table.setGeometry(QtCore.QRect(0, 0, 991, 381))
        self.medical_history_table.setAutoFillBackground(True)
        self.medical_history_table.setStyleSheet(table_style)
        self.medical_history_table.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.medical_history_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.medical_history_table.setAlternatingRowColors(False)
        self.medical_history_table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.medical_history_table.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.medical_history_table.setHorizontalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.medical_history_table.setShowGrid(False)
        self.medical_history_table.setColumnCount(4)
        self.medical_history_table.setObjectName("medical_history_table")
        self.medical_history_table.setRowCount(0)

        for i, h in enumerate(["CONDITION", "DIAGNOSED DATE", "STATUS", "NOTES"]):
            item = QtWidgets.QTableWidgetItem()
            self.medical_history_table.setHorizontalHeaderItem(i, item)

        self.medical_history_table.horizontalHeader().setCascadingSectionResizes(False)
        self.medical_history_table.horizontalHeader().setDefaultSectionSize(200)
        self.medical_history_table.horizontalHeader().setHighlightSections(True)
        self.medical_history_table.horizontalHeader().setMinimumSectionSize(32)
        self.medical_history_table.horizontalHeader().setSortIndicatorShown(False)
        self.medical_history_table.horizontalHeader().setStretchLastSection(True)
        self.medical_history_table.verticalHeader().setVisible(False)
        self.medical_history_table.verticalHeader().setCascadingSectionResizes(False)
        self.medical_history_table.verticalHeader().setDefaultSectionSize(40)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1301, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Dashboard"))
        self.pushButton_2.setText(_translate("MainWindow", "Patient Records"))
        self.pushButton_3.setText(_translate("MainWindow", "Prenatal Care"))
        self.pushButton_4.setText(_translate("MainWindow", "Appointments"))
        self.pushButton_5.setText(_translate("MainWindow", "Log out"))
        self.label_2.setText(_translate("MainWindow", "MATERNADB"))
        self.label_3.setText(_translate("MainWindow", "LOGO"))
        self.label.setText(_translate("MainWindow", "Medical History"))
        self.patient_name.setText(_translate("MainWindow", "NAME"))

        self.patient_id_label.setText(_translate("MainWindow", "Patient ID:"))
        self.placeholder_p_ID.setText(_translate("MainWindow", "placeholder"))
        self.age_label.setText(_translate("MainWindow", "Age:"))
        self.placeholder_age.setText(_translate("MainWindow", "—"))
        self.patient_id_label_3.setText(_translate("MainWindow", "Registered:"))
        self.placeholder_register_date.setText(_translate("MainWindow", "MM/DD/YYYY"))
        self.patient_id_label_2.setText(_translate("MainWindow", "Blood Type:"))
        self.placeholder_p_bloodType.setText(_translate("MainWindow", "placeholder"))
        self.patient_id_label_4.setText(_translate("MainWindow", "PhilHealth#:"))
        self.placeholder_philhealth_num.setText(_translate("MainWindow", "1234-5678-9012"))

        self.pushButton_6.setText(_translate("MainWindow", "Patient Profile"))
        self.pushButton_7.setText(_translate("MainWindow", "Past Pregnancy"))
        self.pushButton_8.setText(_translate("MainWindow", "Prescriptions"))
        self.pushButton_9.setText(_translate("MainWindow", "Medical History"))
        self.pushButton_10.setText(_translate("MainWindow", "Family Planning"))
        self.pushButton_11.setText(_translate("MainWindow", "Appointments"))

        self.add_condition_btn.setText(_translate("MainWindow", "+ Add Condition"))

        for i, col in enumerate(["CONDITION", "DIAGNOSED DATE", "STATUS", "NOTES"]):
            item = self.medical_history_table.horizontalHeaderItem(i)
            item.setText(_translate("MainWindow", col))