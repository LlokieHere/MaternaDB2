# appointments_main.py — responsive layout version
# All fixed setGeometry() calls replaced with Qt layout managers so the UI
# scales correctly when the window is maximised / full-screened.

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1223, 674)
        MainWindow.setStyleSheet("")

        # ── Central widget ──────────────────────────────────────────────────
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Root layout: top header bar + bottom area (sidebar | content)
        root_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── Top header (frame_2) ─────────────────────────────────────────────
        self.frame_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_2.setStyleSheet("background-color: rgb(26, 26, 62);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_2.setFixedHeight(61)

        header_layout = QtWidgets.QHBoxLayout(self.frame_2)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        self.label_3 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_3.setMinimumSize(QtCore.QSize(100, 45))
        font_logo = QtGui.QFont()
        font_logo.setFamily("Segoe UI")
        font_logo.setPointSize(12)
        self.label_3.setFont(font_logo)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.label_2 = QtWidgets.QLabel(parent=self.frame_2)
        font_title = QtGui.QFont()
        font_title.setFamily("Segoe UI")
        font_title.setPointSize(12)
        self.label_2.setFont(font_title)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")

        header_layout.addWidget(self.label_3)
        header_layout.addWidget(self.label_2)
        header_layout.addStretch(1)

        root_layout.addWidget(self.frame_2)

        # ── Bottom area: sidebar + main content ──────────────────────────────
        bottom_widget = QtWidgets.QWidget(parent=self.centralwidget)
        bottom_layout = QtWidgets.QHBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)

        # ── Sidebar (frame) ──────────────────────────────────────────────────
        self.frame = QtWidgets.QFrame(parent=bottom_widget)
        self.frame.setFixedWidth(231)
        self.frame.setStyleSheet("background-color: rgb(192, 116, 182);")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        sidebar_layout = QtWidgets.QVBoxLayout(self.frame)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(10)

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

        sidebar_layout.addSpacing(90)
        sidebar_layout.addWidget(self.pushButton)
        sidebar_layout.addWidget(self.pushButton_2)
        sidebar_layout.addWidget(self.pushButton_3)
        sidebar_layout.addWidget(self.pushButton_4)
        sidebar_layout.addStretch(1)

        self.pushButton_5 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_5.setFixedHeight(41)
        self.pushButton_5.setObjectName("pushButton_5")
        sidebar_layout.addWidget(self.pushButton_5)

        # ── Main content area (frame_3) ───────────────────────────────────────
        self.frame_3 = QtWidgets.QFrame(parent=bottom_widget)
        font_main = QtGui.QFont()
        font_main.setFamily("Nirmala UI Semilight")
        self.frame_3.setFont(font_main)
        self.frame_3.setStyleSheet("background-color: rgb(240, 230, 240);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")

        content_layout = QtWidgets.QVBoxLayout(self.frame_3)
        content_layout.setContentsMargins(40, 20, 40, 20)
        content_layout.setSpacing(10)

        # -- Top row: heading + action buttons ---
        top_row = QtWidgets.QHBoxLayout()

        self.label = QtWidgets.QLabel(parent=self.frame_3)
        font_h1 = QtGui.QFont()
        font_h1.setFamily("Arial Black")
        font_h1.setPointSize(30)
        self.label.setFont(font_h1)
        self.label.setObjectName("label")

        self.pushButton_7 = QtWidgets.QPushButton(parent=self.frame_3)
        self.pushButton_7.setFixedHeight(31)
        self.pushButton_7.setStyleSheet(
            "background-color: rgb(106, 27, 154);"
            "color: rgb(255, 255, 255);"
            "padding: 6px 14px;"
            "border-radius: 10px;"
        )
        self.pushButton_7.setObjectName("pushButton_7")

        self.pushButton_6 = QtWidgets.QPushButton(parent=self.frame_3)
        self.pushButton_6.setFixedHeight(31)
        self.pushButton_6.setFixedWidth(130)
        self.pushButton_6.setStyleSheet(
            "background-color: rgb(156, 39, 176);"
            "color: rgb(255, 255, 255);"
            "border-radius: 10px;"
        )
        self.pushButton_6.setObjectName("pushButton_6")

        top_row.addWidget(self.label)
        top_row.addStretch(1)
        top_row.addWidget(self.pushButton_7)
        top_row.addWidget(self.pushButton_6)

        content_layout.addLayout(top_row)

        # -- Table (flat border, no rounded corners) ---------------------------
        self.left_prescription_date_and_purpose = QtWidgets.QTableWidget(
            parent=self.frame_3
        )
        self.left_prescription_date_and_purpose.setAutoFillBackground(True)
        self.left_prescription_date_and_purpose.setStyleSheet(
            "QTableWidget {"
            "  background-color: rgb(236,198,220);"
            "  border: 1px solid rgb(158,136,163);"
            "  border-radius: 0px;"
            "  outline: none;"
            "}"
            "QTableWidget::item {"
            "  background-color: rgb(236,198,220);"
            "  color: rgb(21,23,61);"
            "  padding: 8px;"
            "  border: none;"
            "  border-bottom: 1px solid rgb(210,177,200);"
            "}"
            "QHeaderView::section {"
            "  background-color: rgb(236,198,220);"
            "  color: rgb(21,23,61);"
            "  font-weight: bold;"
            "  font-size: 10px;"
            "  border: none;"
            "  border-bottom: 1px solid rgb(155,132,160);"
            "  padding: 5px;"
            "}"
            "QScrollBar:vertical {"
            "  background: white; width: 6px; border-radius: 3px;"
            "}"
            "QScrollBar::handle:vertical {"
            "  background: rgb(178,100,168); border-radius: 3px;"
            "}"
        )
        self.left_prescription_date_and_purpose.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.left_prescription_date_and_purpose.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.left_prescription_date_and_purpose.setAlternatingRowColors(False)
        self.left_prescription_date_and_purpose.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.left_prescription_date_and_purpose.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.left_prescription_date_and_purpose.setHorizontalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.left_prescription_date_and_purpose.setShowGrid(False)
        self.left_prescription_date_and_purpose.setColumnCount(5)
        self.left_prescription_date_and_purpose.setObjectName(
            "left_prescription_date_and_purpose"
        )
        self.left_prescription_date_and_purpose.setRowCount(1)

        item = QtWidgets.QTableWidgetItem()
        self.left_prescription_date_and_purpose.setVerticalHeaderItem(0, item)
        for col in range(5):
            item = QtWidgets.QTableWidgetItem()
            self.left_prescription_date_and_purpose.setHorizontalHeaderItem(col, item)

        hh = self.left_prescription_date_and_purpose.horizontalHeader()
        hh.setCascadingSectionResizes(False)
        hh.setDefaultSectionSize(200)
        hh.setHighlightSections(True)
        hh.setMinimumSectionSize(32)
        hh.setSortIndicatorShown(False)
        hh.setStretchLastSection(True)

        vh = self.left_prescription_date_and_purpose.verticalHeader()
        vh.setVisible(False)
        vh.setCascadingSectionResizes(False)
        vh.setDefaultSectionSize(40)

        content_layout.addWidget(self.left_prescription_date_and_purpose)

        # ── Assemble bottom area ─────────────────────────────────────────────
        bottom_layout.addWidget(self.frame)
        bottom_layout.addWidget(self.frame_3, stretch=1)

        root_layout.addWidget(bottom_widget, stretch=1)

        MainWindow.setCentralWidget(self.centralwidget)

        # ── Menu / status bar ────────────────────────────────────────────────
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setObjectName("menubar")
        self.menuAppointments = QtWidgets.QMenu(parent=self.menubar)
        self.menuAppointments.setObjectName("menuAppointments")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionMaternaDB = QtGui.QAction(parent=MainWindow)
        self.actionMaternaDB.setObjectName("actionMaternaDB")
        self.menubar.addAction(self.menuAppointments.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # ── retranslateUi ────────────────────────────────────────────────────────
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
        self.label.setText(_translate("MainWindow", "Appointments"))
        self.pushButton_6.setText(_translate("MainWindow", "+ New Appointment"))
        self.pushButton_7.setText(_translate("MainWindow", "View Completed Appointments"))

        item = self.left_prescription_date_and_purpose.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "#0001"))

        headers = ["Patient", "Date", "Time", "Status", "Action"]
        for col, text in enumerate(headers):
            item = self.left_prescription_date_and_purpose.horizontalHeaderItem(col)
            item.setText(_translate("MainWindow", text))

        self.menuAppointments.setTitle(_translate("MainWindow", "MaternaDB"))
        self.actionMaternaDB.setText(_translate("MainWindow", "MaternaDB"))