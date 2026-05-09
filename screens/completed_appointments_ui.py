# completed_appointments.py — responsive layout version

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1231, 719)

        # ── Central widget ──────────────────────────────────────────────────
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        root_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── Top header (frame_2) ─────────────────────────────────────────────
        self.frame_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_2.setFixedHeight(61)
        self.frame_2.setStyleSheet("background-color: rgb(26, 26, 62);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")

        header_layout = QtWidgets.QHBoxLayout(self.frame_2)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        font_ui = QtGui.QFont()
        font_ui.setFamily("Segoe UI")
        font_ui.setPointSize(12)

        self.label_9 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_9.setMinimumSize(QtCore.QSize(100, 45))
        self.label_9.setFont(font_ui)
        self.label_9.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_9.setObjectName("label_9")

        self.label_2 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_2.setFont(font_ui)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")

        header_layout.addWidget(self.label_9)
        header_layout.addWidget(self.label_2)
        header_layout.addStretch(1)

        root_layout.addWidget(self.frame_2)

        # ── Bottom area: sidebar + content ───────────────────────────────────
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

        self.label_10 = QtWidgets.QLabel(parent=self.frame)
        self.label_10.setMinimumSize(QtCore.QSize(100, 45))
        self.label_10.setFont(font_ui)
        self.label_10.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_10.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_10.setObjectName("label_10")

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

        sidebar_layout.addWidget(self.label_10)
        sidebar_layout.addSpacing(40)
        sidebar_layout.addWidget(self.pushButton)
        sidebar_layout.addWidget(self.pushButton_2)
        sidebar_layout.addWidget(self.pushButton_3)
        sidebar_layout.addWidget(self.pushButton_4)
        sidebar_layout.addStretch(1)
        sidebar_layout.addWidget(self.pushButton_5)

        # ── Main content area (frame_3) ──────────────────────────────────────
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

        # -- Top row: heading + action buttons --------------------------------
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
        self.pushButton_6.setFixedWidth(140)
        self.pushButton_6.setStyleSheet(
            "background-color: rgb(156, 39, 176);"
            "color: rgb(255, 255, 255);"
            "border-radius: 10px;"
        )
        self.pushButton_6.setObjectName("pushButton_6")

        top_row.addWidget(self.label)
        top_row.addStretch(1)
        top_row.addWidget(self.pushButton_7)
        top_row.addSpacing(8)
        top_row.addWidget(self.pushButton_6)
        content_layout.addLayout(top_row)

        # -- Table (flat border, no rounded corners) --------------------------
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
            self.left_prescription_date_and_purpose.setHorizontalHeaderItem(
                col, QtWidgets.QTableWidgetItem()
            )

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

        content_layout.addWidget(self.left_prescription_date_and_purpose, stretch=1)

        # -- Details panel ----------------------------------------------------
        self.widget = QtWidgets.QWidget(parent=self.frame_3)
        self.widget.setStyleSheet(
            "background-color: rgb(236, 198, 220);"
            "border-radius: 10px;"
        )
        self.widget.setObjectName("widget")

        # FIX: top margin increased to 20 so the groupBox title is not clipped
        widget_layout = QtWidgets.QVBoxLayout(self.widget)
        widget_layout.setContentsMargins(10, 20, 10, 10)
        widget_layout.setSpacing(8)

        # GroupBox
        self.groupBox = QtWidgets.QGroupBox(parent=self.widget)
        font_bold = QtGui.QFont()
        font_bold.setBold(True)
        self.groupBox.setFont(font_bold)
        self.groupBox.setStyleSheet("background-color: rgb(236, 198, 220);")
        self.groupBox.setObjectName("groupBox")

        # FIX: top margin increased to 20 so the groupBox title text clears the border
        groupbox_layout = QtWidgets.QHBoxLayout(self.groupBox)
        groupbox_layout.setContentsMargins(9, 20, 9, 9)
        groupbox_layout.setSpacing(12)

        # Left column: Patient / Date / Time / Status labels
        self.widget_2 = QtWidgets.QWidget(parent=self.groupBox)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_3 = QtWidgets.QLabel(parent=self.widget_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)

        self.frame_4 = QtWidgets.QFrame(parent=self.widget_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2.addWidget(self.frame_4)

        self.label_4 = QtWidgets.QLabel(parent=self.widget_2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)

        self.frame_5 = QtWidgets.QFrame(parent=self.widget_2)
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_2.addWidget(self.frame_5)

        self.label_5 = QtWidgets.QLabel(parent=self.widget_2)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)

        self.frame_6 = QtWidgets.QFrame(parent=self.widget_2)
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_2.addWidget(self.frame_6)

        self.label_6 = QtWidgets.QLabel(parent=self.widget_2)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)

        self.frame_7 = QtWidgets.QFrame(parent=self.widget_2)
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_2.addWidget(self.frame_7)

        # Middle column: Vital Signs
        self.widget_3 = QtWidgets.QWidget(parent=self.groupBox)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.label_7 = QtWidgets.QLabel(parent=self.widget_3)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)

        self.textEdit = QtWidgets.QTextEdit(parent=self.widget_3)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_3.addWidget(self.textEdit)

        # Right column: Notes
        self.widget_4 = QtWidgets.QWidget(parent=self.groupBox)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.label_8 = QtWidgets.QLabel(parent=self.widget_4)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_4.addWidget(self.label_8)

        self.textEdit_2 = QtWidgets.QTextEdit(parent=self.widget_4)
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout_4.addWidget(self.textEdit_2)

        groupbox_layout.addWidget(self.widget_2, stretch=3)
        groupbox_layout.addWidget(self.widget_3, stretch=2)
        groupbox_layout.addWidget(self.widget_4, stretch=2)

        widget_layout.addWidget(self.groupBox, stretch=1)

        # Button row below the groupBox
        self.widget_5 = QtWidgets.QWidget(parent=self.widget)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton_8 = QtWidgets.QPushButton(parent=self.widget_5)
        self.pushButton_8.setStyleSheet(
            "background-color: rgb(156, 39, 176);"
            "color: white;"
            "border: none;"
            "padding: 8px 16px;"
            "font-weight: bold;"
            "border-radius: 12px;"
        )
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout.addWidget(self.pushButton_8)

        self.pushButton_9 = QtWidgets.QPushButton(parent=self.widget_5)
        self.pushButton_9.setStyleSheet(
            "background-color: #98719D;"
            "color: black;"
            "border: none;"
            "padding: 8px 16px;"
            "font-weight: bold;"
            "border-radius: 12px;"
        )
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout.addWidget(self.pushButton_9)
        self.horizontalLayout.addStretch(1)

        widget_layout.addWidget(self.widget_5)

        content_layout.addWidget(self.widget, stretch=2)

        # ── Assemble bottom area ─────────────────────────────────────────────
        bottom_layout.addWidget(self.frame)
        bottom_layout.addWidget(self.frame_3, stretch=1)

        root_layout.addWidget(bottom_widget, stretch=1)

        MainWindow.setCentralWidget(self.centralwidget)

        # ── Menu / status bar ────────────────────────────────────────────────
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setObjectName("menubar")
        self.menuMaternaDB = QtWidgets.QMenu(parent=self.menubar)
        self.menuMaternaDB.setObjectName("menuMaternaDB")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuMaternaDB.menuAction())

        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # ── retranslateUi ────────────────────────────────────────────────────────
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuMaternaDB.setTitle(_translate("MainWindow", "MaternaDB"))
        self.pushButton.setText(_translate("MainWindow", "Dashboard"))
        self.pushButton_2.setText(_translate("MainWindow", "Patient Records"))
        self.pushButton_3.setText(_translate("MainWindow", "Prenatal Care"))
        self.pushButton_4.setText(_translate("MainWindow", "Appointments"))
        self.pushButton_5.setText(_translate("MainWindow", "Log out"))
        self.label_10.setText(_translate("MainWindow", "LOGO"))
        self.label_2.setText(_translate("MainWindow", "MATERNADB"))
        self.label_9.setText(_translate("MainWindow", "LOGO"))
        self.label.setText(_translate("MainWindow", "Completed Appointments"))
        self.pushButton_6.setText(_translate("MainWindow", "+ New Appointment"))
        self.pushButton_7.setText(_translate("MainWindow", "<-- Back to Appointments"))

        item = self.left_prescription_date_and_purpose.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "#0001"))

        headers = ["Patient", "Date", "Time", "Status", "Action"]
        for col, text in enumerate(headers):
            item = self.left_prescription_date_and_purpose.horizontalHeaderItem(col)
            item.setText(_translate("MainWindow", text))

        self.groupBox.setTitle(_translate("MainWindow", "Appointment Details"))
        self.label_3.setText(_translate("MainWindow", "<b>Patient:</b>"))
        self.label_4.setText(_translate("MainWindow", "<b>Date:</b>"))
        self.label_5.setText(_translate("MainWindow", "<b>Time:</b>"))
        self.label_6.setText(_translate("MainWindow", "<b>Status:</b>"))
        self.label_7.setText(_translate(
            "MainWindow",
            "<html><head/><body><p><span style=\" font-weight:700;\">Vital Signs:</span></p></body></html>"
        ))
        self.label_8.setText(_translate("MainWindow", "<b>Notes:</b>"))
        self.pushButton_8.setText(_translate("MainWindow", "Schedule Follow-up"))
        self.pushButton_9.setText(_translate("MainWindow", "View Full Record"))