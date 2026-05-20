# Patient Profile UI - Responsive Full-Screen Layout
# Uses QVBoxLayout/QHBoxLayout/QGridLayout instead of fixed geometry
# so the window fills and resizes properly like a dashboard.

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1230, 835)
        MainWindow.setMinimumSize(QtCore.QSize(900, 600))

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        MainWindow.setSizePolicy(sizePolicy)

        # ── Central widget ────────────────────────────────────────────────────
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Root vertical layout: [top-bar] / [body]
        root_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── TOP BAR (frame_2) ─────────────────────────────────────────────────
        self.frame_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_2.setObjectName("frame_2")
        self.frame_2.setFixedHeight(61)
        self.frame_2.setStyleSheet("background-color: rgb(26, 26, 62);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        topbar_layout = QtWidgets.QHBoxLayout(self.frame_2)
        topbar_layout.setContentsMargins(10, 0, 20, 0)
        topbar_layout.setSpacing(10)

        self.label_3 = QtWidgets.QLabel("LOGO", parent=self.frame_2)
        self.label_3.setObjectName("label_3")
        self.label_3.setFixedSize(100, 45)
        font_logo = QtGui.QFont("Segoe UI", 12)
        self.label_3.setFont(font_logo)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label_2 = QtWidgets.QLabel("MATERNADB", parent=self.frame_2)
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(font_logo)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        topbar_layout.addWidget(self.label_3)
        topbar_layout.addWidget(self.label_2)
        topbar_layout.addStretch()

        root_layout.addWidget(self.frame_2)

        # ── BODY: sidebar + content ───────────────────────────────────────────
        body_layout = QtWidgets.QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # ── SIDEBAR (frame) ───────────────────────────────────────────────────
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setObjectName("frame")
        self.frame.setFixedWidth(231)
        self.frame.setStyleSheet("background-color: rgb(192, 116, 182);")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        sidebar_layout = QtWidgets.QVBoxLayout(self.frame)
        sidebar_layout.setContentsMargins(20, 240, 10, 20)
        sidebar_layout.setSpacing(8)

        btn_style_nav = (
            "background-color: rgb(240, 230, 240);"
        )

        self.pushButton = QtWidgets.QPushButton("Dashboard", parent=self.frame)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setFixedHeight(41)
        self.pushButton.setStyleSheet(btn_style_nav)

        self.pushButton_2 = QtWidgets.QPushButton("Patient Records", parent=self.frame)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setFixedHeight(41)
        self.pushButton_2.setStyleSheet(btn_style_nav)

        self.pushButton_3 = QtWidgets.QPushButton("Prenatal Care", parent=self.frame)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setFixedHeight(41)
        self.pushButton_3.setStyleSheet(btn_style_nav)

        self.pushButton_4 = QtWidgets.QPushButton("Appointments", parent=self.frame)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setFixedHeight(41)
        self.pushButton_4.setStyleSheet(btn_style_nav)

        sidebar_layout.addWidget(self.pushButton)
        sidebar_layout.addWidget(self.pushButton_2)
        sidebar_layout.addWidget(self.pushButton_3)
        sidebar_layout.addWidget(self.pushButton_4)
        sidebar_layout.addStretch()

        self.pushButton_5 = QtWidgets.QPushButton("Log out", parent=self.frame)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setFixedHeight(41)
        sidebar_layout.addWidget(self.pushButton_5)

        body_layout.addWidget(self.frame)

        # ── CONTENT AREA (frame_3) ────────────────────────────────────────────
        self.frame_3 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.setStyleSheet("background-color: rgb(240, 230, 240);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        content_layout = QtWidgets.QVBoxLayout(self.frame_3)
        content_layout.setContentsMargins(40, 20, 40, 20)
        content_layout.setSpacing(10)

        # ── Page title row ────────────────────────────────────────────────────
        title_row = QtWidgets.QHBoxLayout()

        self.label = QtWidgets.QLabel("Patient Records", parent=self.frame_3)
        self.label.setObjectName("label")
        font_title = QtGui.QFont("Arial Black", 24)
        self.label.setFont(font_title)
        title_row.addWidget(self.label)
        title_row.addStretch()

        self.remove_patient_btn = QtWidgets.QPushButton(
            "Edit Patient Profile", parent=self.frame_3
        )
        self.remove_patient_btn.setObjectName("remove_patient_btn")
        self.remove_patient_btn.setFixedHeight(31)
        self.remove_patient_btn.setStyleSheet(
            "border-radius: 12px;"
            "background-color: rgb(236, 198, 220);"
            "border: 1px solid rgb(210, 177, 200);"
        )
        title_row.addWidget(self.remove_patient_btn)

        content_layout.addLayout(title_row)

        # ── Patient header card (frame_4) ─────────────────────────────────────
        self.frame_4 = QtWidgets.QFrame(parent=self.frame_3)
        self.frame_4.setObjectName("frame_4")
        self.frame_4.setFixedHeight(141)
        self.frame_4.setStyleSheet(
            "border-radius: 15px;"
            "background-color: rgb(26, 26, 62);"
        )
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        card_layout = QtWidgets.QHBoxLayout(self.frame_4)
        card_layout.setContentsMargins(20, 15, 20, 15)
        card_layout.setSpacing(15)

        # Avatar placeholder
        self.frame_5 = QtWidgets.QFrame(parent=self.frame_4)
        self.frame_5.setObjectName("frame_5")
        self.frame_5.setFixedSize(111, 91)
        self.frame_5.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 6px;")
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        card_layout.addWidget(self.frame_5)

        # Name + meta grid
        meta_widget = QtWidgets.QWidget(parent=self.frame_4)
        meta_widget.setStyleSheet("background: transparent;")
        meta_layout = QtWidgets.QVBoxLayout(meta_widget)
        meta_layout.setContentsMargins(0, 0, 0, 0)
        meta_layout.setSpacing(4)

        white_label_style = "color: rgb(255, 255, 255); font-size: 16px; background: transparent; border: none;"

        self.patient_name = QtWidgets.QLabel("NAME", parent=meta_widget)
        self.patient_name.setObjectName("patient_name")
        self.patient_name.setStyleSheet("color: rgb(255, 255, 255); font-size: 20px; background: transparent; border: none;")
        meta_layout.addWidget(self.patient_name)

        # Row 1: ID | Age | Registered
        row1_widget = QtWidgets.QWidget()
        row1_widget.setStyleSheet("background: transparent;")
        row1 = QtWidgets.QHBoxLayout(row1_widget)
        row1.setContentsMargins(0, 0, 0, 0)
        row1.setSpacing(20)

        self.patient_id_label = QtWidgets.QLabel("Patient ID:", parent=row1_widget)
        self.patient_id_label.setStyleSheet(white_label_style)
        self.patient_id_label.setObjectName("patient_id_label")

        self.placeholder_p_ID = QtWidgets.QLabel("placeholder", parent=row1_widget)
        self.placeholder_p_ID.setStyleSheet(white_label_style)
        self.placeholder_p_ID.setObjectName("placeholder_p_ID")

        self.age_label = QtWidgets.QLabel("Age:", parent=row1_widget)
        self.age_label.setStyleSheet(white_label_style)
        self.age_label.setObjectName("age_label")

        self.age_placeholder = QtWidgets.QLabel("null", parent=row1_widget)
        self.age_placeholder.setStyleSheet(white_label_style)
        self.age_placeholder.setObjectName("age_placeholder")

        self.patient_id_label_3 = QtWidgets.QLabel("Registered:", parent=row1_widget)
        self.patient_id_label_3.setStyleSheet(white_label_style)
        self.patient_id_label_3.setObjectName("patient_id_label_3")

        self.placeholder_register_date_2 = QtWidgets.QLabel("MM/DD/YYYY", parent=row1_widget)
        self.placeholder_register_date_2.setStyleSheet(white_label_style)
        self.placeholder_register_date_2.setObjectName("placeholder_register_date_2")

        for w in [
            self.patient_id_label, self.placeholder_p_ID,
            self.age_label, self.age_placeholder,
            self.patient_id_label_3, self.placeholder_register_date_2,
        ]:
            row1.addWidget(w)
        row1.addStretch()
        meta_layout.addWidget(row1_widget)

        # Row 2: Blood Type | PhilHealth
        row2_widget = QtWidgets.QWidget()
        row2_widget.setStyleSheet("background: transparent;")
        row2 = QtWidgets.QHBoxLayout(row2_widget)
        row2.setContentsMargins(0, 0, 0, 0)
        row2.setSpacing(20)

        self.blood_type_label = QtWidgets.QLabel("Blood Type:", parent=row2_widget)
        self.blood_type_label.setStyleSheet(white_label_style)
        self.blood_type_label.setObjectName("blood_type_label")

        self.placeholder_p_bloodType = QtWidgets.QLabel("placeholder", parent=row2_widget)
        self.placeholder_p_bloodType.setStyleSheet(white_label_style)
        self.placeholder_p_bloodType.setObjectName("placeholder_p_bloodType")

        self.patient_id_label_4 = QtWidgets.QLabel("PhilHealth#:", parent=row2_widget)
        self.patient_id_label_4.setStyleSheet(white_label_style)
        self.patient_id_label_4.setObjectName("patient_id_label_4")

        self.placeholder_philhealth_num = QtWidgets.QLabel("1234-5676-8907", parent=row2_widget)
        self.placeholder_philhealth_num.setStyleSheet(white_label_style)
        self.placeholder_philhealth_num.setObjectName("placeholder_philhealth_num")

        for w in [
            self.blood_type_label, self.placeholder_p_bloodType,
            self.patient_id_label_4, self.placeholder_philhealth_num,
        ]:
            row2.addWidget(w)
        row2.addStretch()
        meta_layout.addWidget(row2_widget)
        meta_layout.addStretch()

        card_layout.addWidget(meta_widget, stretch=1)

        content_layout.addWidget(self.frame_4)

        # ── Tab bar ───────────────────────────────────────────────────────────
        tab_style = (
            "QPushButton {"
            "    background: transparent;"
            "    border: none;"
            "    padding: 8px 18px;"
            "    color: rgb(26, 26, 62);"
            "    font-size: 14px;"
            "}"
            "QPushButton:hover { color: #000; }"
            "QPushButton:checked {"
            "    color: #1a1a1a;"
            "    border-bottom: 3px solid #2c2c54;"
            "    font-weight: bold;"
            "}"
            "QPushButton:!checked { border-bottom: 3px solid transparent; }"
        )

        self.layoutWidget3 = QtWidgets.QWidget(parent=self.frame_3)
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.layoutWidget3.setFixedHeight(40)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)

        tab_names = [
            ("pushButton_6",  "Patient Profile",  True),
            ("pushButton_7",  "Past Pregnancy",   False),
            ("pushButton_8",  "Prescriptions",    False),
            ("pushButton_9",  "Medical History",  False),
            ("pushButton_10", "Family Planning",  False),
            ("pushButton_11", "Appointments",     False),
        ]

        self.tab_buttons = []
        for obj_name, label, checked in tab_names:
            btn = QtWidgets.QPushButton(label, parent=self.layoutWidget3)
            btn.setObjectName(obj_name)
            btn.setCheckable(True)
            btn.setChecked(checked)
            btn.setStyleSheet(tab_style)
            sp = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Expanding,
            )
            btn.setSizePolicy(sp)
            self.horizontalLayout.addWidget(btn)
            setattr(self, obj_name, btn)
            self.tab_buttons.append(btn)

        content_layout.addWidget(self.layoutWidget3)

        # ── PERSONAL INFORMATION card ─────────────────────────────────────────
        self.personal_information_frame = QtWidgets.QFrame(parent=self.frame_3)
        self.personal_information_frame.setObjectName("personal_information_frame")
        self.personal_information_frame.setStyleSheet(
            "background-color: rgb(236, 198, 220);"
            "border-radius: 15px;"
            "border: 1px solid rgb(210, 177, 200);"
        )
        self.personal_information_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        pi_layout = QtWidgets.QVBoxLayout(self.personal_information_frame)
        pi_layout.setContentsMargins(20, 10, 20, 10)
        pi_layout.setSpacing(6)

        self.personalInformation_text = QtWidgets.QLabel(
            "PERSONAL INFORMATION", parent=self.personal_information_frame
        )
        self.personalInformation_text.setObjectName("personalInformation_text")
        self.personalInformation_text.setStyleSheet(
            "color: rgb(26, 26, 62); font-size: 20px; border: none; font-weight: bold;"
        )
        pi_layout.addWidget(self.personalInformation_text)

        label_style = "color: rgb(26, 26, 62); border: none; font-size: 16px;"
        value_style = "border: none; font-weight: bold; color: rgb(26, 26, 62); font-size: 16px;"

        self.layoutWidget = QtWidgets.QWidget(parent=self.personal_information_frame)
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(4)

        pi_fields = [
            # (row, col, obj_name, text, style)
            (0, 0, "last_name_placeholder_2", "LAST NAME",    label_style),
            (0, 1, "first_name_label",         "FIRST NAME",   label_style),
            (0, 2, "middle_name_label",         "MIDDLE NAME",  label_style),
            (1, 0, "last_name_placeholder",     "placeholder",  value_style),
            (1, 1, "first_name_placeholder",    "placeholder",  value_style),
            (1, 2, "middle_name_placeholder",   "placeholder",  value_style),
            (2, 0, "date_of_birth_placeholder", "DATE OF BIRTH",label_style),
            (2, 1, "civi_status_label",         "CIVIL STATUS", label_style),
            (2, 2, "nationality_label",         "NATIONALITY",  label_style),
            (3, 0, "bday_placeholder",          "MM/DD/YYYY",   value_style),
            (3, 1, "civil_status_placeholder",  "placeholder",  value_style),
            (3, 2, "nationality_placeholder",   "placeholder",  value_style),
            (4, 0, "religion_placeholder_2",    "RELIGION",     label_style),
            (4, 1, "occupation_label",          "OCCUPATION",   label_style),
            (4, 2, "contact_number_label",      "CONTACT#",     label_style),
            (5, 0, "religion_placeholder",      "placeholder",  value_style),
            (5, 1, "occupation_placeholder",    "placeholder",  value_style),
            (5, 2, "contact_number_placeholder","placeholder",  value_style),
        ]

        for row, col, obj_name, text, style in pi_fields:
            lbl = QtWidgets.QLabel(text, parent=self.layoutWidget)
            lbl.setObjectName(obj_name)
            lbl.setStyleSheet(style)
            self.gridLayout.addWidget(lbl, row, col)
            setattr(self, obj_name, lbl)

        pi_layout.addWidget(self.layoutWidget)
        content_layout.addWidget(self.personal_information_frame)

        # ── Bottom row: Address + Emergency Contact ───────────────────────────
        bottom_row = QtWidgets.QHBoxLayout()
        bottom_row.setSpacing(20)

        # Address card
        self.frame_7 = QtWidgets.QFrame(parent=self.frame_3)
        self.frame_7.setObjectName("frame_7")
        self.frame_7.setStyleSheet(
            "background-color: rgb(236, 198, 220);"
            "border-radius: 15px;"
            "border: 1px solid rgb(210, 177, 200);"
        )
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        addr_layout = QtWidgets.QVBoxLayout(self.frame_7)
        addr_layout.setContentsMargins(20, 10, 20, 10)
        addr_layout.setSpacing(6)

        self.Address_text = QtWidgets.QLabel("ADDRESS", parent=self.frame_7)
        self.Address_text.setObjectName("Address_text")
        self.Address_text.setStyleSheet(
            "color: rgb(26, 26, 62); font-size: 20px; border: none; font-weight: bold;"
        )
        addr_layout.addWidget(self.Address_text)

        self.layoutWidget1 = QtWidgets.QWidget(parent=self.frame_7)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(4)

        addr_fields = [
            (0, 0, "street_label",       "STREET",       label_style),
            (0, 1, "barangay_label",     "BARANGAY",     label_style),
            (1, 0, "street_placeholder", "placeholder",  value_style),
            (1, 1, "barangay_placeholder","placeholder", value_style),
            (2, 0, "city_label",         "CITY",         label_style),
            (2, 1, "province_label",     "PROVINCE",     label_style),
            (3, 0, "cit_placeholder",    "placeholder",  value_style),
            (3, 1, "province_placeholder","placeholder", value_style),
        ]

        for row, col, obj_name, text, style in addr_fields:
            lbl = QtWidgets.QLabel(text, parent=self.layoutWidget1)
            lbl.setObjectName(obj_name)
            lbl.setStyleSheet(style)
            self.gridLayout_2.addWidget(lbl, row, col)
            setattr(self, obj_name, lbl)

        addr_layout.addWidget(self.layoutWidget1)
        bottom_row.addWidget(self.frame_7)

        # Emergency contact card
        self.frame_8 = QtWidgets.QFrame(parent=self.frame_3)
        self.frame_8.setObjectName("frame_8")
        self.frame_8.setStyleSheet(
            "background-color: rgb(236, 198, 220);"
            "border-radius: 15px;"
            "border: 1px solid rgb(210, 177, 200);"
        )
        self.frame_8.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        ec_layout = QtWidgets.QVBoxLayout(self.frame_8)
        ec_layout.setContentsMargins(20, 10, 20, 10)
        ec_layout.setSpacing(6)

        self.Emergency_text = QtWidgets.QLabel("Emergency Contact", parent=self.frame_8)
        self.Emergency_text.setObjectName("Emergency_text")
        self.Emergency_text.setStyleSheet(
            "color: rgb(26, 26, 62); font-size: 20px; border: none; font-weight: bold;"
        )
        ec_layout.addWidget(self.Emergency_text)

        self.layoutWidget2 = QtWidgets.QWidget(parent=self.frame_8)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(4)

        ec_fields = [
            (0, 0, "EC_last_name_label",        "LAST NAME",    label_style),
            (0, 1, "EC_first_name_label",        "FIRST NAME",   label_style),
            (0, 2, "EC_middle_name_label",       "MIDDLE NAME",  label_style),
            (1, 0, "EC_last_name_placeholder",   "placeholder",  value_style),
            (1, 1, "EC_first_name_placeholder",  "placeholder",  value_style),
            (1, 2, "EC_middle_name_placeholder", "placeholder",  value_style),
            (2, 0, "EC_contact_label",           "CONTACT#",     label_style),
            (2, 1, "EC_relationship_label",      "RELATIONSHIP", label_style),
            (3, 0, "EC_contact_placeholder",     "placeholder",  value_style),
            (3, 1, "EC_relationship_placeholder","placeholder",  value_style),
        ]

        for row, col, obj_name, text, style in ec_fields:
            lbl = QtWidgets.QLabel(text, parent=self.layoutWidget2)
            lbl.setObjectName(obj_name)
            lbl.setStyleSheet(style)
            self.gridLayout_3.addWidget(lbl, row, col)
            setattr(self, obj_name, lbl)

        # EC relationship spans 2 columns
        self.gridLayout_3.itemAtPosition(3, 1).widget().deleteLater()
        lbl_rel = QtWidgets.QLabel("placeholder", parent=self.layoutWidget2)
        lbl_rel.setObjectName("EC_relationship_placeholder")
        lbl_rel.setStyleSheet(value_style)
        self.gridLayout_3.addWidget(lbl_rel, 3, 1, 1, 2)
        self.EC_relationship_placeholder = lbl_rel

        ec_layout.addWidget(self.layoutWidget2)
        bottom_row.addWidget(self.frame_8)

        content_layout.addLayout(bottom_row)
        content_layout.addStretch()

        body_layout.addWidget(self.frame_3, stretch=1)
        root_layout.addLayout(body_layout, stretch=1)

        MainWindow.setCentralWidget(self.centralwidget)

        # ── Menu / status bars ────────────────────────────────────────────────
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1230, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)