from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1301, 864)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

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

        self.next_btn = QtWidgets.QPushButton(parent=self.frame_4)
        self.next_btn.setGeometry(QtCore.QRect(850, 50, 111, 51))
        self.next_btn.setStyleSheet(
            "background-color: rgb(240, 230, 240); border-radius: 15px;"
        )
        self.next_btn.setObjectName("next_btn")

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

        self.placeholder_philhealth_num = QtWidgets.QLabel("1234-5676-8907", parent=self.layoutWidget)
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
        tab_bold_style = (
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
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout.addWidget(self.pushButton_6)

        self.pushButton_7 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_7.setSizePolicy(sp_exp)
        self.pushButton_7.setStyleSheet(tab_style)
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout.addWidget(self.pushButton_7)

        self.pushButton_8 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_8.setSizePolicy(sp_exp)
        self.pushButton_8.setStyleSheet(tab_bold_style)
        self.pushButton_8.setCheckable(True)
        self.pushButton_8.setChecked(True)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.setStyleSheet("QPushButton {\n"
        "    background: transparent;\n"
        "    border: none;\n"
        "    padding: 8px 18px;\n"
        "    color: rgb(26, 26, 62);\n"
        "    font-size: 14px;\n"
        "    font-weight: bold;\n"
        "}\n"
        "\n"
        "QPushButton:hover {\n"
        "    color: #000;\n"
        "}\n"
        "\n"
        "QPushButton:checked {\n"
        "    color: #1a1a1a;\n"
        "    border-bottom: 3px solid #2c2c54;\n"
        "}\n"
        "\n"
        "QPushButton:!checked {\n"
        "    border-bottom: 3px solid transparent;\n"
        "}")
        self.horizontalLayout.addWidget(self.pushButton_8)

        self.pushButton_9 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_9.setSizePolicy(sp_exp)
        self.pushButton_9.setStyleSheet(tab_style)
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

        # ── TABLE STYLE (shared) ──────────────────────────────────────────────
        table_style = (
            "QTableWidget { background-color: rgb(236, 198, 220);"
            "border: 1px solid rgb(158, 136, 163); border-radius: 15px; }"
            "QTableWidget::item { background-color: rgb(236, 198, 220); color: rgb(21, 23, 61);"
            "padding: 8px; border: none; border-bottom: 1px solid rgb(210, 177, 200); }"
            "QTableWidget::item:selected { background-color: black; color: rgb(21, 23, 61); }"
            "QHeaderView::section { background-color: rgb(236, 198, 220); color: rgb(21, 23, 61);"
            "font-weight: bold; font-size: 10px; border: none;"
            "border-bottom: 1px solid rgb(155, 132, 160); padding: 5px; }"
            "QScrollBar:vertical { background: white; width: 6px; border-radius: 3px; }"
            "QScrollBar::handle:vertical { background: rgb(178, 100, 168); border-radius: 3px; }"
        )

        # ── LEFT PANEL ────────────────────────────────────────────────────────
        self.left = QtWidgets.QFrame(parent=self.frame_3)
        self.left.setGeometry(QtCore.QRect(60, 340, 471, 381))
        self.left.setStyleSheet(
            "background-color: rgb(236, 198, 220);"
            "border: 1px solid rgb(158, 136, 163); border-radius: 15px;"
        )
        self.left.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.left.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.left.setObjectName("left")

        self.left_prescription_date_and_purpose = QtWidgets.QTableWidget(parent=self.left)
        self.left_prescription_date_and_purpose.setGeometry(QtCore.QRect(0, 0, 471, 381))
        self.left_prescription_date_and_purpose.setAutoFillBackground(True)
        self.left_prescription_date_and_purpose.setStyleSheet(table_style)
        self.left_prescription_date_and_purpose.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.left_prescription_date_and_purpose.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.left_prescription_date_and_purpose.setAlternatingRowColors(False)
        self.left_prescription_date_and_purpose.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.left_prescription_date_and_purpose.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.left_prescription_date_and_purpose.setHorizontalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.left_prescription_date_and_purpose.setShowGrid(False)
        self.left_prescription_date_and_purpose.setColumnCount(3)
        self.left_prescription_date_and_purpose.setObjectName("left_prescription_date_and_purpose")
        self.left_prescription_date_and_purpose.setRowCount(1)

        item = QtWidgets.QTableWidgetItem()
        self.left_prescription_date_and_purpose.setVerticalHeaderItem(0, item)
        for i, h in enumerate(["PRESCRIPTION DATE", "STAFF", "ACTION"]):
            item = QtWidgets.QTableWidgetItem()
            self.left_prescription_date_and_purpose.setHorizontalHeaderItem(i, item)

        self.left_prescription_date_and_purpose.horizontalHeader().setCascadingSectionResizes(False)
        self.left_prescription_date_and_purpose.horizontalHeader().setDefaultSectionSize(150)
        self.left_prescription_date_and_purpose.horizontalHeader().setHighlightSections(True)
        self.left_prescription_date_and_purpose.horizontalHeader().setMinimumSectionSize(32)
        self.left_prescription_date_and_purpose.horizontalHeader().setSortIndicatorShown(False)
        self.left_prescription_date_and_purpose.horizontalHeader().setStretchLastSection(True)
        self.left_prescription_date_and_purpose.verticalHeader().setVisible(False)
        self.left_prescription_date_and_purpose.verticalHeader().setCascadingSectionResizes(False)
        self.left_prescription_date_and_purpose.verticalHeader().setDefaultSectionSize(40)

        # ── RIGHT PANEL ───────────────────────────────────────────────────────
        self.right_details_prescription = QtWidgets.QFrame(parent=self.frame_3)
        self.right_details_prescription.setGeometry(QtCore.QRect(540, 340, 501, 381))
        self.right_details_prescription.setStyleSheet(
            "background-color: rgb(236, 198, 220);"
            "border: 1px solid rgb(158, 136, 163); border-radius: 15px;"
        )
        self.right_details_prescription.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.right_details_prescription.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.right_details_prescription.setObjectName("right_details_prescription")

        self.patient_table_3 = QtWidgets.QTableWidget(parent=self.right_details_prescription)
        self.patient_table_3.setGeometry(QtCore.QRect(10, 58, 481, 251))
        self.patient_table_3.setAutoFillBackground(True)
        self.patient_table_3.setStyleSheet(table_style)
        self.patient_table_3.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.patient_table_3.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.patient_table_3.setAlternatingRowColors(False)
        self.patient_table_3.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.patient_table_3.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.patient_table_3.setHorizontalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.patient_table_3.setShowGrid(False)
        self.patient_table_3.setColumnCount(6)
        self.patient_table_3.setObjectName("patient_table_3")
        self.patient_table_3.setRowCount(1)

        item = QtWidgets.QTableWidgetItem()
        self.patient_table_3.setVerticalHeaderItem(0, item)
        for i, h in enumerate(["MEDICATION", "DOSE", "FREQUENCY", "DURATION", "ROUTE", "TIMING"]):
            item = QtWidgets.QTableWidgetItem()
            self.patient_table_3.setHorizontalHeaderItem(i, item)

        self.patient_table_3.horizontalHeader().setCascadingSectionResizes(False)
        self.patient_table_3.horizontalHeader().setDefaultSectionSize(110)
        self.patient_table_3.horizontalHeader().setHighlightSections(True)
        self.patient_table_3.horizontalHeader().setMinimumSectionSize(25)
        self.patient_table_3.horizontalHeader().setSortIndicatorShown(False)
        self.patient_table_3.horizontalHeader().setStretchLastSection(True)
        self.patient_table_3.verticalHeader().setVisible(False)
        self.patient_table_3.verticalHeader().setCascadingSectionResizes(False)
        self.patient_table_3.verticalHeader().setDefaultSectionSize(40)

        detail_style = "font: 10pt \"Segoe UI\"; border: none;"

        self.notes_label = QtWidgets.QLabel(parent=self.right_details_prescription)
        self.notes_label.setGeometry(QtCore.QRect(10, 330, 37, 18))
        self.notes_label.setStyleSheet(detail_style)
        self.notes_label.setObjectName("notes_label")

        self.notes_placeholder = QtWidgets.QLabel(parent=self.right_details_prescription)
        self.notes_placeholder.setGeometry(QtCore.QRect(60, 330, 67, 18))
        self.notes_placeholder.setStyleSheet(detail_style)
        self.notes_placeholder.setObjectName("notes_placeholder")

        self.layoutWidget2 = QtWidgets.QWidget(parent=self.right_details_prescription)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 10, 229, 44))
        self.layoutWidget2.setObjectName("layoutWidget2")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.prescribed_by = QtWidgets.QLabel(parent=self.layoutWidget2)
        self.prescribed_by.setStyleSheet(detail_style)
        self.prescribed_by.setObjectName("prescribed_by")
        self.gridLayout_2.addWidget(self.prescribed_by, 0, 0)

        self.prescribed_by_placeholder = QtWidgets.QLabel(parent=self.layoutWidget2)
        self.prescribed_by_placeholder.setStyleSheet(detail_style)
        self.prescribed_by_placeholder.setObjectName("prescribed_by_placeholder")
        self.gridLayout_2.addWidget(self.prescribed_by_placeholder, 0, 1)

        self.date_label = QtWidgets.QLabel(parent=self.layoutWidget2)
        self.date_label.setStyleSheet(detail_style)
        self.date_label.setObjectName("date_label")
        self.gridLayout_2.addWidget(self.date_label, 1, 0)

        self.date_prescription_date_placeholder = QtWidgets.QLabel(parent=self.layoutWidget2)
        self.date_prescription_date_placeholder.setStyleSheet(detail_style)
        self.date_prescription_date_placeholder.setObjectName("date_prescription_date_placeholder")
        self.gridLayout_2.addWidget(self.date_prescription_date_placeholder, 1, 1)

        # ── ACTION BUTTONS ────────────────────────────────────────────────────
        btn_style = (
            "border-radius: 12px;"
            "background-color: rgb(236, 198, 220);"
            "border: 1px solid rgb(210, 177, 200);"
        )

        self.edit_prescription = QtWidgets.QPushButton(parent=self.frame_3)
        self.edit_prescription.setGeometry(QtCore.QRect(790, 300, 121, 31))
        self.edit_prescription.setStyleSheet(btn_style)
        self.edit_prescription.setObjectName("edit_prescription")

        self.ad_prescription = QtWidgets.QPushButton(parent=self.frame_3)
        self.ad_prescription.setGeometry(QtCore.QRect(920, 300, 121, 31))
        self.ad_prescription.setStyleSheet(btn_style)
        self.ad_prescription.setObjectName("ad_prescription")

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
        self.label.setText(_translate("MainWindow", "Patient Records"))
        self.patient_name.setText(_translate("MainWindow", "NAME"))
        self.next_btn.setText(_translate("MainWindow", "Next"))
        self.patient_id_label.setText(_translate("MainWindow", "Patient ID:"))
        self.placeholder_p_ID.setText(_translate("MainWindow", "placeholder"))
        self.age_label.setText(_translate("MainWindow", "Age:"))
        self.placeholder_age.setText(_translate("MainWindow", "—"))
        self.patient_id_label_3.setText(_translate("MainWindow", "Registered:"))
        self.placeholder_register_date.setText(_translate("MainWindow", "MM/DD/YYYY"))
        self.patient_id_label_2.setText(_translate("MainWindow", "Blood Type:"))
        self.placeholder_p_bloodType.setText(_translate("MainWindow", "placeholder"))
        self.patient_id_label_4.setText(_translate("MainWindow", "PhilHealth#:"))
        self.placeholder_philhealth_num.setText(_translate("MainWindow", "1234-5676-8907"))

        self.pushButton_6.setText(_translate("MainWindow", "Patient Profile"))
        self.pushButton_7.setText(_translate("MainWindow", "Past Pregnancy"))
        self.pushButton_8.setText(_translate("MainWindow", "Prescriptions"))
        self.pushButton_9.setText(_translate("MainWindow", "Medical History"))
        self.pushButton_10.setText(_translate("MainWindow", "Family Planning"))
        self.pushButton_11.setText(_translate("MainWindow", "Appointments"))

        item = self.left_prescription_date_and_purpose.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "#0001"))
        item = self.left_prescription_date_and_purpose.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "PRESCRIPTION DATE"))
        item = self.left_prescription_date_and_purpose.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "STAFF"))
        item = self.left_prescription_date_and_purpose.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "ACTION"))

        item = self.patient_table_3.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "#0001"))
        for i, col in enumerate(["MEDICATION", "DOSE", "FREQUENCY", "DURATION", "ROUTE", "TIMING"]):
            item = self.patient_table_3.horizontalHeaderItem(i)
            item.setText(_translate("MainWindow", col))

        self.notes_label.setText(_translate("MainWindow", "Notes:"))
        self.notes_placeholder.setText(_translate("MainWindow", "Placeholder"))
        self.date_label.setText(_translate("MainWindow", "Date:"))
        self.date_prescription_date_placeholder.setText(_translate("MainWindow", "Placeholder"))
        self.prescribed_by.setText(_translate("MainWindow", "Prescribed by:"))
        self.prescribed_by_placeholder.setText(_translate("MainWindow", "Placeholder"))
        self.ad_prescription.setText(_translate("MainWindow", "Add Prescription"))
        self.edit_prescription.setText(_translate("MainWindow", "Edit Prescription"))