# Form implementation generated from reading ui file 'Ui/dashboard.ui'
# Fixed: Replaced all hardcoded geometries with proper Qt layouts
# so elements scale correctly in fullscreen / resized windows.

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DashboardScreen(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1224, 674)
        MainWindow.setStyleSheet("")

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ── Root layout: vertical stack (top-bar + body) ────────────────────
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
        topbar_layout.setSpacing(10)

        self.logo = QtWidgets.QLabel(parent=self.frame_2)
        self.logo.setFixedSize(50, 50)
        self.logo.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        self.logo.setObjectName("logo")

        self.label_2 = QtWidgets.QLabel(parent=self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")

        topbar_layout.addWidget(self.logo)
        topbar_layout.addWidget(self.label_2)
        topbar_layout.addStretch()

        root_layout.addWidget(self.frame_2)

        # ── BODY: sidebar (frame) + content (frame_3) ───────────────────────
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
        font3 = QtGui.QFont()
        font3.setFamily("Nirmala UI Semilight")
        self.frame_3.setFont(font3)
        self.frame_3.setStyleSheet("background-color: rgb(240, 230, 240);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")

        content_layout = QtWidgets.QVBoxLayout(self.frame_3)
        content_layout.setContentsMargins(40, 20, 40, 20)
        content_layout.setSpacing(16)

        # Title label
        self.label = QtWidgets.QLabel(parent=self.frame_3)
        font_title = QtGui.QFont()
        font_title.setFamily("Arial Black")
        font_title.setPointSize(30)
        self.label.setFont(font_title)
        self.label.setObjectName("label")
        content_layout.addWidget(self.label)

        # ── STAT CARDS row ───────────────────────────────────────────────────
        self.layoutWidget = QtWidgets.QWidget(parent=self.frame_3)
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)

        card_min = QtCore.QSize(200, 99)
        card_max = QtCore.QSize(16777215, 130)   # allow horizontal growth
        expanding = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        def make_stat_card(parent, bg_style, label_text, label_color):
            card = QtWidgets.QFrame(parent=parent)
            card.setSizePolicy(expanding)
            card.setMinimumSize(card_min)
            card.setMaximumSize(card_max)
            card.setStyleSheet(bg_style)
            card.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            card.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

            vl = QtWidgets.QVBoxLayout(card)
            vl.setContentsMargins(10, 8, 10, 8)
            vl.setSpacing(4)

            lbl_title = QtWidgets.QLabel(parent=card)
            lbl_title.setStyleSheet(
                f"color: {label_color}; font-size: 15px; font-weight: bold; border: none;"
            )
            lbl_title.setText(label_text)

            lbl_count = QtWidgets.QLabel(parent=card)
            lbl_count.setStyleSheet(
                f"color: {label_color}; font-size: 40px; border: none;"
            )
            lbl_count.setText("0")

            vl.addWidget(lbl_title)
            vl.addWidget(lbl_count)
            return card, lbl_title, lbl_count

        dark_bg = "background-color: rgb(21, 23, 61); border-radius: 15px;"
        light_bg = (
            "background-color: rgb(236, 198, 220); border-radius: 15px;"
            "border: 1px solid rgb(150, 128, 156);"
        )
        dark_color  = "rgb(241, 233, 233)"
        light_color = "#15173D"

        self.total_patient, self.total_patient_label, self.total_patient_label_2 = \
            make_stat_card(self.layoutWidget, dark_bg,  "Total Patients",        dark_color)
        self.upcomingApp,   self.upcoming_app_label,   self.total_patient_label_3 = \
            make_stat_card(self.layoutWidget, light_bg, "Upcoming Appointments", light_color)
        self.prenatalVisit, self.prenatal_visit_label, self.total_patient_label_4 = \
            make_stat_card(self.layoutWidget, light_bg, "Prenatal Visits",       light_color)
        self.Deliveries,    self.delivery_label,       self.total_patient_label_5 = \
            make_stat_card(self.layoutWidget, light_bg, "Deliveries",            light_color)

        self.total_patient_label.setObjectName("total_patient_label")
        self.total_patient_label_2.setObjectName("total_patient_label_2")
        self.upcoming_app_label.setObjectName("upcoming_app_label")
        self.total_patient_label_3.setObjectName("total_patient_label_3")
        self.prenatal_visit_label.setObjectName("prenatal_visit_label")
        self.total_patient_label_4.setObjectName("total_patient_label_4")
        self.delivery_label.setObjectName("delivery_label")
        self.total_patient_label_5.setObjectName("total_patient_label_5")

        self.gridLayout.addWidget(self.total_patient,  0, 0)
        self.gridLayout.addWidget(self.upcomingApp,    0, 1)
        self.gridLayout.addWidget(self.prenatalVisit,  0, 2)
        self.gridLayout.addWidget(self.Deliveries,     0, 3)

        content_layout.addWidget(self.layoutWidget)

        # ── LOWER SECTION: patient table + today's appointment ───────────────
        lower_layout = QtWidgets.QHBoxLayout()
        lower_layout.setSpacing(20)

        # Left column: Recent Patients table
        left_col = QtWidgets.QVBoxLayout()
        left_col.setSpacing(6)

        self.label_3 = QtWidgets.QLabel(parent=self.frame_3)
        self.label_3.setStyleSheet(
            "QLabel { font-size: 16px; font-weight: bold; color: rgb(21, 23, 61);"
            "border: none; background: transparent; }"
        )
        self.label_3.setObjectName("label_3")
        left_col.addWidget(self.label_3)

        self.patient_table = QtWidgets.QTableWidget(parent=self.frame_3)
        self.patient_table.setMinimumSize(QtCore.QSize(400, 191))
        self.patient_table.setAutoFillBackground(True)
        self.patient_table.setStyleSheet(
            "QTableWidget { background-color:rgb(236, 198, 220);"
            "border: 1px solid rgb(158, 136, 163); border-radius: 15px; }"
            "QTableWidget::item { background-color: rgb(236, 198, 220); color: rgb(21, 23, 61);"
            "padding: 8px; border: none; border-bottom: 1px solid rgb(210, 177, 200); }"
            "QTableWidget::item:selected { background-color: rgb(240, 210, 230); color: rgb(21, 23, 61); }"
            "QHeaderView::section { background-color: rgb(236, 198, 220); color: rgb(21, 23, 61);"
            "font-weight: bold; font-size: 10px; border: none;"
            "border-bottom: 1px solid rgb(155, 132, 160); padding: 5px; }"
            "QScrollBar:vertical { background: white; width: 6px; border-radius: 3px; }"
            "QScrollBar::handle:vertical { background: rgb(178, 100, 168); border-radius: 3px; }"
        )
        self.patient_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.patient_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.patient_table.setAlternatingRowColors(False)
        self.patient_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.patient_table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.patient_table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.patient_table.setShowGrid(False)
        self.patient_table.setObjectName("patient_table")
        self.patient_table.setColumnCount(3)
        self.patient_table.setRowCount(1)

        item = QtWidgets.QTableWidgetItem()
        self.patient_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.patient_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.patient_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.patient_table.setHorizontalHeaderItem(2, item)

        self.patient_table.horizontalHeader().setCascadingSectionResizes(False)
        self.patient_table.horizontalHeader().setDefaultSectionSize(170)
        self.patient_table.horizontalHeader().setHighlightSections(True)
        self.patient_table.horizontalHeader().setMinimumSectionSize(32)
        self.patient_table.horizontalHeader().setSortIndicatorShown(True)
        self.patient_table.horizontalHeader().setStretchLastSection(True)
        self.patient_table.verticalHeader().setVisible(False)
        self.patient_table.verticalHeader().setCascadingSectionResizes(False)

        left_col.addWidget(self.patient_table)
        lower_layout.addLayout(left_col, stretch=2)

        # Right column: Today's Appointments
        right_col = QtWidgets.QVBoxLayout()
        right_col.setSpacing(6)

        self.Todays_appointment_TA = QtWidgets.QLabel(parent=self.frame_3)
        self.Todays_appointment_TA.setStyleSheet(
            "QLabel { font-size: 16px; font-weight: bold; color: rgb(21, 23, 61);"
            "border: none; background: transparent; }"
        )
        self.Todays_appointment_TA.setObjectName("Todays_appointment_TA")
        right_col.addWidget(self.Todays_appointment_TA)

        # Appointment card
        self.content_container_TA = QtWidgets.QFrame(parent=self.frame_3)
        self.content_container_TA.setMinimumSize(QtCore.QSize(260, 78))
        self.content_container_TA.setStyleSheet(
            "border-radius: 15px; border: 1px solid rgb(162, 139, 166);"
            "background-color: rgb(236, 198, 220);"
        )
        self.content_container_TA.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.content_container_TA.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.content_container_TA.setObjectName("content_container_TA")

        card_hl = QtWidgets.QHBoxLayout(self.content_container_TA)
        card_hl.setContentsMargins(10, 10, 10, 10)
        card_hl.setSpacing(10)

        # Date box
        self.date_TA = QtWidgets.QFrame(parent=self.content_container_TA)
        self.date_TA.setFixedSize(71, 61)
        self.date_TA.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.date_TA.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.date_TA.setObjectName("date_TA")

        date_vl = QtWidgets.QVBoxLayout(self.date_TA)
        date_vl.setContentsMargins(0, 0, 0, 0)
        date_vl.setSpacing(2)

        self.day = QtWidgets.QLabel(parent=self.date_TA)
        self.day.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.day.setStyleSheet("border: none; font-size: 22px;")
        self.day.setObjectName("day")

        self.day_2 = QtWidgets.QLabel(parent=self.date_TA)
        self.day_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.day_2.setStyleSheet("border: none; font-size: 20px;")
        self.day_2.setObjectName("day_2")

        date_vl.addWidget(self.day)
        date_vl.addWidget(self.day_2)
        card_hl.addWidget(self.date_TA)

        # Patient info
        info_vl = QtWidgets.QVBoxLayout()
        info_vl.setSpacing(4)

        self.patient_name_TA = QtWidgets.QLabel(parent=self.content_container_TA)
        self.patient_name_TA.setStyleSheet(
            "color: #15173D; font-size: 14px; font-weight: bold; border: none;"
        )
        self.patient_name_TA.setObjectName("patient_name_TA")
        self.patient_name_TA.setWordWrap(True)

        appt_hl = QtWidgets.QHBoxLayout()
        self.time_TA = QtWidgets.QLabel(parent=self.content_container_TA)
        self.time_TA.setStyleSheet("color: #15173D; font-size: 12px; border: none;")
        self.time_TA.setObjectName("time_TA")

        self.purpose_TA = QtWidgets.QLabel(parent=self.content_container_TA)
        self.purpose_TA.setStyleSheet("color: #15173D; font-size: 12px; border: none;")
        self.purpose_TA.setObjectName("purpose_TA")

        appt_hl.addWidget(self.time_TA)
        appt_hl.addWidget(self.purpose_TA)
        appt_hl.addStretch()

        info_vl.addWidget(self.patient_name_TA)
        info_vl.addLayout(appt_hl)
        card_hl.addLayout(info_vl)

        right_col.addWidget(self.content_container_TA)

        # Keep the QTableView placeholder too
        self.today_appointment = QtWidgets.QTableView(parent=self.frame_3)
        self.today_appointment.setStyleSheet(
            "background-color: rgb(235, 197, 219); border-radius: 15px;"
            "border: 1px solid rgb(158, 136, 163);"
        )
        self.today_appointment.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.today_appointment.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.today_appointment.setObjectName("today_appointment")
        right_col.addWidget(self.today_appointment)

        lower_layout.addLayout(right_col, stretch=1)
        content_layout.addLayout(lower_layout)

        body_layout.addWidget(self.frame_3)
        root_layout.addLayout(body_layout)

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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Dashboard"))
        self.pushButton_2.setText(_translate("MainWindow", "Patient Records"))
        self.pushButton_3.setText(_translate("MainWindow", "Prenatal Care"))
        self.pushButton_4.setText(_translate("MainWindow", "Appointments"))
        self.pushButton_5.setText(_translate("MainWindow", "Log out"))
        self.label_2.setText(_translate("MainWindow", "MATERNADB"))
        self.logo.setText(_translate("MainWindow", ""))
        self.label.setText(_translate("MainWindow", "DASHBOARD"))

        item = self.patient_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.patient_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "NAME"))
        item = self.patient_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "PHILHEALTH"))
        item = self.patient_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "REGISTERED"))

        self.label_3.setText(_translate("MainWindow", "Recent Patients"))
        self.Todays_appointment_TA.setText(_translate("MainWindow", "Today's Appointments"))
        self.day.setText(_translate("MainWindow", "5"))
        self.day_2.setText(_translate("MainWindow", "Jun"))
        self.patient_name_TA.setText(_translate("MainWindow", "Kaleil Jay O. Batumbakal"))
        self.time_TA.setText(_translate("MainWindow", "9:00AM"))
        self.purpose_TA.setText(_translate("MainWindow", "Prenatal Checkup"))

        self.total_patient_label.setText(_translate("MainWindow", "Total Patients"))
        self.total_patient_label_2.setText(_translate("MainWindow", "0"))
        self.upcoming_app_label.setText(_translate("MainWindow", "Upcoming Appointments"))
        self.total_patient_label_3.setText(_translate("MainWindow", "0"))
        self.prenatal_visit_label.setText(_translate("MainWindow", "Prenatal Visits"))
        self.total_patient_label_4.setText(_translate("MainWindow", "0"))
        self.delivery_label.setText(_translate("MainWindow", "Deliveries"))
        self.total_patient_label_5.setText(_translate("MainWindow", "0"))

        self.menuAppointments.setTitle(_translate("MainWindow", "MaternaDB"))
        self.actionMaternaDB.setText(_translate("MainWindow", "MaternaDB"))