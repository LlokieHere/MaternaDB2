# Form implementation generated from reading ui file 'Ui/patient_records_.ui'
#
# Fixed: Replaced hardcoded geometries with proper Qt layouts for fullscreen support.
# Added: AGE column (col 3) and REGISTERED column (col 4), PhilHealth moved to col 5.

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PatientRecord(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1230, 700)
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

        # ── Root layout: top-bar + body ─────────────────────────────────────
        root_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── TOP BAR (frame_2) ────────────────────────────────────────────────
        self.frame_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_2.setFixedHeight(61)
        self.frame_2.setStyleSheet("background-color: rgb(26, 26, 62);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")

        topbar_layout = QtWidgets.QHBoxLayout(self.frame_2)
        topbar_layout.setContentsMargins(10, 5, 10, 5)
        topbar_layout.setSpacing(8)

        self.label_3 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_3.setMinimumSize(QtCore.QSize(100, 45))
        font_logo = QtGui.QFont()
        font_logo.setFamily("Segoe UI")
        font_logo.setPointSize(12)
        font_logo.setBold(False)
        self.label_3.setFont(font_logo)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.label_2 = QtWidgets.QLabel(parent=self.frame_2)
        font_title = QtGui.QFont()
        font_title.setFamily("Segoe UI")
        font_title.setPointSize(12)
        font_title.setBold(False)
        self.label_2.setFont(font_title)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")

        topbar_layout.addWidget(self.label_3)
        topbar_layout.addWidget(self.label_2)
        topbar_layout.addStretch()

        root_layout.addWidget(self.frame_2)

        # ── BODY: sidebar + content ──────────────────────────────────────────
        body_layout = QtWidgets.QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # ── SIDEBAR (frame) ──────────────────────────────────────────────────
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFixedWidth(231)
        self.frame.setStyleSheet("background-color: rgb(192, 116, 182);")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        sidebar_layout = QtWidgets.QVBoxLayout(self.frame)
        sidebar_layout.setContentsMargins(20, 20, 10, 20)
        sidebar_layout.setSpacing(8)

        btn_style = "background-color: rgb(240, 230, 240);"

        self.pushButton = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton.setFixedHeight(41)
        self.pushButton.setStyleSheet(btn_style)
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_2.setFixedHeight(41)
        self.pushButton_2.setStyleSheet(btn_style)
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_3.setFixedHeight(41)
        self.pushButton_3.setStyleSheet(btn_style)
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_4.setFixedHeight(41)
        self.pushButton_4.setStyleSheet(btn_style)
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_5.setFixedHeight(41)
        self.pushButton_5.setObjectName("pushButton_5")

        sidebar_layout.addSpacing(140)
        sidebar_layout.addWidget(self.pushButton)
        sidebar_layout.addWidget(self.pushButton_2)
        sidebar_layout.addWidget(self.pushButton_3)
        sidebar_layout.addWidget(self.pushButton_4)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.pushButton_5)

        body_layout.addWidget(self.frame)

        # ── CONTENT AREA (frame_3) ───────────────────────────────────────────
        self.frame_3 = QtWidgets.QFrame(parent=self.centralwidget)
        font_content = QtGui.QFont()
        font_content.setFamily("Nirmala UI Semilight")
        self.frame_3.setFont(font_content)
        self.frame_3.setStyleSheet("background-color: rgb(240, 230, 240);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")

        content_layout = QtWidgets.QVBoxLayout(self.frame_3)
        content_layout.setContentsMargins(40, 20, 40, 20)
        content_layout.setSpacing(12)

        # Title
        self.label = QtWidgets.QLabel(parent=self.frame_3)
        font_h1 = QtGui.QFont()
        font_h1.setFamily("Arial Black")
        font_h1.setPointSize(30)
        self.label.setFont(font_h1)
        self.label.setObjectName("label")
        content_layout.addWidget(self.label)

        # ── Search + Buttons row ─────────────────────────────────────────────
        toolbar_layout = QtWidgets.QHBoxLayout()
        toolbar_layout.setSpacing(10)

        self.lineEdit = QtWidgets.QLineEdit(parent=self.frame_3)
        self.lineEdit.setFixedHeight(41)
        self.lineEdit.setMinimumWidth(200)
        self.lineEdit.setMaximumWidth(340)
        self.lineEdit.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        self.lineEdit.setStyleSheet(
            "background-color: rgb(224, 188, 209);"
            "border-radius: 15px;"
            "border: 1px solid rgb(177, 152, 177);"
        )
        self.lineEdit.setObjectName("lineEdit")

        btn_action_style = (
            "border-radius: 12px;"
            "background-color: rgb(236, 198, 220);"
            "border: 1px solid rgb(210, 177, 200);"
        )

        self.add_patient_btn = QtWidgets.QPushButton(parent=self.frame_3)
        self.add_patient_btn.setFixedSize(121, 35)
        self.add_patient_btn.setStyleSheet(btn_action_style)
        self.add_patient_btn.setObjectName("add_patient_btn")

        self.remove_patient_btn = QtWidgets.QPushButton(parent=self.frame_3)
        self.remove_patient_btn.setFixedSize(121, 35)
        self.remove_patient_btn.setStyleSheet(btn_action_style)
        self.remove_patient_btn.setObjectName("remove_patient_btn")

        toolbar_layout.addWidget(self.lineEdit)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_patient_btn)
        toolbar_layout.addWidget(self.remove_patient_btn)

        content_layout.addLayout(toolbar_layout)

        # ── Patient Table ────────────────────────────────────────────────────
        self.patient_table = QtWidgets.QTableWidget(parent=self.frame_3)
        self.patient_table.setAutoFillBackground(True)
        self.patient_table.setStyleSheet(
            "QTableWidget {"
            "    background-color: rgb(236, 198, 220);"
            "    border: 1px solid rgb(158, 136, 163);"
            "    border-radius: 15px;"
            "}"
            "QTableWidget::item {"
            "    background-color: rgb(236, 198, 220);"
            "    color: rgb(21, 23, 61);"
            "    padding: 8px;"
            "    border: none;"
            "    border-bottom: 1px solid rgb(210, 177, 200);"
            "}"
            "QTableWidget::item:selected {"
            "    color: rgb(21, 23, 61);"
            "}"
            "QHeaderView::section {"
            "    background-color: rgb(236, 198, 220);"
            "    color: rgb(21, 23, 61);"
            "    font-weight: bold;"
            "    font-size: 10px;"
            "    border: none;"
            "    border-bottom: 1px solid rgb(155, 132, 160);"
            "    padding: 0px;"
            "}"
            "QScrollBar:vertical {"
            "    background: white;"
            "    width: 6px;"
            "    border-radius: 3px;"
            "}"
            "QScrollBar::handle:vertical {"
            "    background: rgb(178, 100, 168);"
            "    border-radius: 3px;"
            "}"
        )
        self.patient_table.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.patient_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.patient_table.setAlternatingRowColors(False)
        self.patient_table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.patient_table.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.patient_table.setHorizontalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.patient_table.setShowGrid(False)
        self.patient_table.setObjectName("patient_table")

        # Columns: PATIENT# | NAME | DATE OF BIRTH | AGE | REGISTERED | CONTACT
        self.patient_table.setColumnCount(6)
        self.patient_table.setRowCount(1)

        item = QtWidgets.QTableWidgetItem()
        self.patient_table.setVerticalHeaderItem(0, item)
        for i in range(6):
            self.patient_table.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())

        self.patient_table.horizontalHeader().setCascadingSectionResizes(False)
        self.patient_table.horizontalHeader().setDefaultSectionSize(150)
        self.patient_table.horizontalHeader().setHighlightSections(True)
        self.patient_table.horizontalHeader().setMinimumSectionSize(32)
        self.patient_table.horizontalHeader().setSortIndicatorShown(False)
        self.patient_table.horizontalHeader().setStretchLastSection(True)
        self.patient_table.verticalHeader().setVisible(False)
        self.patient_table.verticalHeader().setCascadingSectionResizes(False)

        content_layout.addWidget(self.patient_table)

        body_layout.addWidget(self.frame_3)
        root_layout.addLayout(body_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        # ── Menu / status bar ────────────────────────────────────────────────
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
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
        self.pushButton_4.setText(_translate("MainWindow", "Appointments        "))
        self.pushButton_5.setText(_translate("MainWindow", "Log out"))
        self.label_2.setText(_translate("MainWindow", "MATERNADB"))
        self.label_3.setText(_translate("MainWindow", "LOGO"))
        self.label.setText(_translate("MainWindow", "Patient Records"))

        item = self.patient_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "#0001"))

        headers = ["PATIENT#", "NAME", "DATE OF BIRTH", "AGE", "REGISTERED", "CONTACT"]
        for i, text in enumerate(headers):
            self.patient_table.horizontalHeaderItem(i).setText(
                _translate("MainWindow", text)
            )

        self.lineEdit.setPlaceholderText(
            _translate("MainWindow", "           Search for patient")
        )
        self.add_patient_btn.setText(_translate("MainWindow", "Add Patient"))
        self.remove_patient_btn.setText(_translate("MainWindow", "Remove Patient"))