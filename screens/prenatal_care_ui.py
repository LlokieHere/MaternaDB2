from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PrenatalCareScreen(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1224, 674)
        MainWindow.setStyleSheet("")

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ── Sidebar
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 60, 231, 581))
        self.frame.setStyleSheet("background-color: rgb(192, 116, 182)")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        self.pushButton = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton.setGeometry(QtCore.QRect(20, 180, 191, 41))
        self.pushButton.setStyleSheet("background-color: rgb(240, 230, 240)")
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 230, 191, 41))
        self.pushButton_2.setStyleSheet("background-color: rgb(240, 230, 240)")
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 280, 191, 41))
        self.pushButton_3.setStyleSheet("background-color: rgb(21, 23, 61); color: white;")
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 330, 191, 41))
        self.pushButton_4.setStyleSheet("background-color: rgb(240, 230, 240)")
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 500, 191, 41))
        self.pushButton_5.setObjectName("pushButton_5")

        # ── Top Navbar
        self.frame_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 1231, 61))
        self.frame_2.setStyleSheet("background-color: rgb(26, 26, 62)")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")

        self.logo = QtWidgets.QLabel(parent=self.frame_2)
        self.logo.setGeometry(QtCore.QRect(40, 10, 50, 50))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setMinimumSize(QtCore.QSize(50, 50))
        self.logo.setObjectName("logo")

        self.label_2 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(110, 20, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")

        # ── Main Content Frame
        self.frame_3 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(230, 60, 1001, 601))
        font2 = QtGui.QFont()
        font2.setFamily("Nirmala UI Semilight")
        self.frame_3.setFont(font2)
        self.frame_3.setStyleSheet("background-color: rgb(240, 230, 240)")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")

        # Page title
        self.title_label = QtWidgets.QLabel(parent=self.frame_3)
        self.title_label.setGeometry(QtCore.QRect(40, 20, 400, 61))
        font3 = QtGui.QFont()
        font3.setFamily("Arial Black")
        font3.setPointSize(30)
        self.title_label.setFont(font3)
        self.title_label.setObjectName("title_label")

        # Patient selector label
        self.patient_selector_label = QtWidgets.QLabel(parent=self.frame_3)
        self.patient_selector_label.setGeometry(QtCore.QRect(40, 88, 110, 21))
        self.patient_selector_label.setStyleSheet(
            "color: rgb(21, 23, 61); font-size: 13px; font-weight: bold;"
        )
        self.patient_selector_label.setObjectName("patient_selector_label")

        # Patient combo box
        self.patient_combo = QtWidgets.QComboBox(parent=self.frame_3)
        self.patient_combo.setGeometry(QtCore.QRect(155, 85, 320, 28))
        self.patient_combo.setStyleSheet("""
            QComboBox {
                background-color: rgb(236, 198, 220);
                border: 1px solid rgb(158, 136, 163);
                border-radius: 6px;
                padding: 3px 8px;
                color: rgb(21, 23, 61);
                font-size: 12px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background-color: rgb(240, 230, 240);
                border: 1px solid rgb(158, 136, 163);
                selection-background-color: rgb(192, 116, 182);
                color: rgb(21, 23, 61);
            }
        """)
        self.patient_combo.setObjectName("patient_combo")

        # Patient info card
        self.patient_info_frame = QtWidgets.QFrame(parent=self.frame_3)
        self.patient_info_frame.setGeometry(QtCore.QRect(40, 122, 921, 70))
        self.patient_info_frame.setStyleSheet("""
            QFrame {
                background-color: rgb(236, 198, 220);
                border-radius: 15px;
                border: 1px solid rgb(158, 136, 163);
            }
        """)
        self.patient_info_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.patient_info_frame.setObjectName("patient_info_frame")

        self.patient_name_label = QtWidgets.QLabel(parent=self.patient_info_frame)
        self.patient_name_label.setGeometry(QtCore.QRect(20, 10, 400, 28))
        self.patient_name_label.setStyleSheet(
            "color: rgb(21, 23, 61); font-size: 18px; font-weight: bold; border: none;"
        )
        self.patient_name_label.setObjectName("patient_name_label")

        self.patient_sub_label = QtWidgets.QLabel(parent=self.patient_info_frame)
        self.patient_sub_label.setGeometry(QtCore.QRect(20, 40, 500, 20))
        self.patient_sub_label.setStyleSheet(
            "color: rgb(21, 23, 61); font-size: 11px; border: none;"
        )
        self.patient_sub_label.setObjectName("patient_sub_label")

        self.btn_add_prescription = QtWidgets.QPushButton(parent=self.patient_info_frame)
        self.btn_add_prescription.setGeometry(QtCore.QRect(680, 18, 110, 32))
        self.btn_add_prescription.setStyleSheet("""
            QPushButton {
                background-color: rgb(240, 230, 240);
                color: rgb(21, 23, 61);
                border: 1px solid rgb(21, 23, 61);
                border-radius: 8px;
                font-size: 11px;
            }
            QPushButton:hover { background-color: rgb(21, 23, 61); color: white; }
        """)
        self.btn_add_prescription.setObjectName("btn_add_prescription")

        self.btn_record_visit = QtWidgets.QPushButton(parent=self.patient_info_frame)
        self.btn_record_visit.setGeometry(QtCore.QRect(800, 18, 110, 32))
        self.btn_record_visit.setStyleSheet("""
            QPushButton {
                background-color: rgb(21, 23, 61);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: rgb(192, 116, 182); }
        """)
        self.btn_record_visit.setObjectName("btn_record_visit")

        # ── Tab buttons
        self.tab_frame = QtWidgets.QFrame(parent=self.frame_3)
        self.tab_frame.setGeometry(QtCore.QRect(40, 200, 921, 40))
        self.tab_frame.setStyleSheet("background: transparent;")
        self.tab_frame.setObjectName("tab_frame")

        tab_btn_style_inactive = """
            QPushButton {
                background: transparent;
                color: rgb(21, 23, 61);
                border: none;
                border-bottom: 2px solid transparent;
                font-size: 12px;
                padding: 0 4px;
            }
            QPushButton:hover { border-bottom: 2px solid rgb(192, 116, 182); }
        """
        tab_btn_style_active = """
            QPushButton {
                background: transparent;
                color: rgb(21, 23, 61);
                border: none;
                border-bottom: 3px solid rgb(21, 23, 61);
                font-size: 12px;
                font-weight: bold;
                padding: 0 4px;
            }
        """

        self.tab_visit_history = QtWidgets.QPushButton(parent=self.tab_frame)
        self.tab_visit_history.setGeometry(QtCore.QRect(0, 0, 110, 38))
        self.tab_visit_history.setStyleSheet(tab_btn_style_inactive)
        self.tab_visit_history.setObjectName("tab_visit_history")

        self.tab_lab = QtWidgets.QPushButton(parent=self.tab_frame)
        self.tab_lab.setGeometry(QtCore.QRect(120, 0, 120, 38))
        self.tab_lab.setStyleSheet(tab_btn_style_inactive)
        self.tab_lab.setObjectName("tab_lab")

        self.tab_delivery = QtWidgets.QPushButton(parent=self.tab_frame)
        self.tab_delivery.setGeometry(QtCore.QRect(250, 0, 140, 38))
        self.tab_delivery.setStyleSheet(tab_btn_style_inactive)
        self.tab_delivery.setObjectName("tab_delivery")

        self.tab_prenatal = QtWidgets.QPushButton(parent=self.tab_frame)
        self.tab_prenatal.setGeometry(QtCore.QRect(400, 0, 110, 38))
        self.tab_prenatal.setStyleSheet(tab_btn_style_active)
        self.tab_prenatal.setObjectName("tab_prenatal")

        # Tab separator line
        self.tab_line = QtWidgets.QFrame(parent=self.frame_3)
        self.tab_line.setGeometry(QtCore.QRect(40, 238, 921, 1))
        self.tab_line.setStyleSheet("background-color: rgb(180, 150, 180);")
        self.tab_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.tab_line.setObjectName("tab_line")

        # ── Scroll area for visit cards
        self.scroll_area = QtWidgets.QScrollArea(parent=self.frame_3)
        self.scroll_area.setGeometry(QtCore.QRect(40, 245, 921, 320))
        self.scroll_area.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical {
                background: rgb(240, 230, 240);
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: rgb(178, 100, 168);
                border-radius: 3px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setObjectName("scroll_area")

        # Placeholder widget inside scroll area (cards are added at runtime)
        self.scroll_contents = QtWidgets.QWidget()
        self.scroll_contents.setStyleSheet("background: transparent;")
        self.scroll_contents.setObjectName("scroll_contents")
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_contents)
        self.scroll_layout.setContentsMargins(0, 8, 0, 16)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.addStretch()
        self.scroll_area.setWidget(self.scroll_contents)

        # Z-order
        self.frame_3.raise_()
        self.frame.raise_()
        self.frame_2.raise_()

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1224, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MaternaDB - Prenatal Care"))
        self.pushButton.setText(_translate("MainWindow", "Dashboard"))
        self.pushButton_2.setText(_translate("MainWindow", "Patient Records"))
        self.pushButton_3.setText(_translate("MainWindow", "Prenatal Care"))
        self.pushButton_4.setText(_translate("MainWindow", "Appointments"))
        self.pushButton_5.setText(_translate("MainWindow", "Log out"))
        self.label_2.setText(_translate("MainWindow", "MATERNADB"))
        self.logo.setText(_translate("MainWindow", ""))
        self.title_label.setText(_translate("MainWindow", "PRENATAL CARE"))
        self.patient_selector_label.setText(_translate("MainWindow", "Select Patient:"))
        self.patient_name_label.setText(_translate("MainWindow", "—"))
        self.patient_sub_label.setText(_translate("MainWindow", "Select a patient above to view their prenatal visits."))
        self.btn_add_prescription.setText(_translate("MainWindow", "+ Add Prescription"))
        self.btn_record_visit.setText(_translate("MainWindow", "+ Record New Visit"))
        self.tab_visit_history.setText(_translate("MainWindow", "Visit History"))
        self.tab_lab.setText(_translate("MainWindow", "Lab & Referrals"))
        self.tab_delivery.setText(_translate("MainWindow", "Delivery & Newborn"))
        self.tab_prenatal.setText(_translate("MainWindow", "Prenatal Visit"))
