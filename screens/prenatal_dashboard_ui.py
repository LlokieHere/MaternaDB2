# Prenatal Dashboard UI
# Middle screen: Patient → Pregnancies list → (click) → Prenatal Care

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PrenatalDashboardScreen(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1224, 674)
        MainWindow.setStyleSheet("")

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ── Sidebar ────────────────────────────────────────────────────────
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

        # Prenatal Care is the active button — dark highlight
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 280, 191, 41))
        self.pushButton_3.setStyleSheet(
            "background-color: rgb(21, 23, 61); color: white;"
        )
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 330, 191, 41))
        self.pushButton_4.setStyleSheet("background-color: rgb(240, 230, 240)")
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 500, 191, 41))
        self.pushButton_5.setObjectName("pushButton_5")

        # ── Navbar ─────────────────────────────────────────────────────────
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

        # ── Main content area ──────────────────────────────────────────────
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
        self.title_label.setGeometry(QtCore.QRect(40, 20, 500, 61))
        font3 = QtGui.QFont()
        font3.setFamily("Arial Black")
        font3.setPointSize(30)
        self.title_label.setFont(font3)
        self.title_label.setObjectName("title_label")

        # Patient selector label
        self.patient_selector_label = QtWidgets.QLabel(parent=self.frame_3)
        self.patient_selector_label.setGeometry(QtCore.QRect(40, 92, 110, 21))
        self.patient_selector_label.setStyleSheet(
            "color: rgb(21, 23, 61); font-size: 13px; font-weight: bold;"
        )
        self.patient_selector_label.setObjectName("patient_selector_label")

        # Patient combo box
        self.patient_combo = QtWidgets.QComboBox(parent=self.frame_3)
        self.patient_combo.setGeometry(QtCore.QRect(155, 89, 320, 28))
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

        # Section label "Pregnancies"
        self.pregnancies_label = QtWidgets.QLabel(parent=self.frame_3)
        self.pregnancies_label.setGeometry(QtCore.QRect(40, 132, 200, 24))
        self.pregnancies_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: rgb(21, 23, 61);
                border: none;
                background: transparent;
            }
        """)
        self.pregnancies_label.setObjectName("pregnancies_label")

        # Add New Pregnancy button
        self.btn_add_pregnancy = QtWidgets.QPushButton(parent=self.frame_3)
        self.btn_add_pregnancy.setGeometry(QtCore.QRect(800, 128, 160, 32))
        self.btn_add_pregnancy.setStyleSheet("""
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
        self.btn_add_pregnancy.setObjectName("btn_add_pregnancy")

        # Separator line
        self.sep_line = QtWidgets.QFrame(parent=self.frame_3)
        self.sep_line.setGeometry(QtCore.QRect(40, 162, 921, 1))
        self.sep_line.setStyleSheet("background-color: rgb(180, 150, 180);")
        self.sep_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.sep_line.setObjectName("sep_line")

        # Scroll area — pregnancy cards go here
        self.scroll_area = QtWidgets.QScrollArea(parent=self.frame_3)
        self.scroll_area.setGeometry(QtCore.QRect(40, 170, 921, 390))
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
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical { height: 0px; }
        """)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setObjectName("scroll_area")

        self.scroll_contents = QtWidgets.QWidget()
        self.scroll_contents.setStyleSheet("background: transparent;")
        self.scroll_contents.setObjectName("scroll_contents")
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_contents)
        self.scroll_layout.setContentsMargins(0, 8, 0, 16)
        self.scroll_layout.setSpacing(12)
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
        MainWindow.setWindowTitle(
            _translate("MainWindow", "MaternaDB - Prenatal Care")
        )
        self.pushButton.setText(_translate("MainWindow", "Dashboard"))
        self.pushButton_2.setText(_translate("MainWindow", "Patient Records"))
        self.pushButton_3.setText(_translate("MainWindow", "Prenatal Care"))
        self.pushButton_4.setText(_translate("MainWindow", "Appointments"))
        self.pushButton_5.setText(_translate("MainWindow", "Log out"))
        self.label_2.setText(_translate("MainWindow", "MATERNADB"))
        self.logo.setText(_translate("MainWindow", ""))
        self.title_label.setText(_translate("MainWindow", "PRENATAL CARE"))
        self.patient_selector_label.setText(_translate("MainWindow", "Select Patient:"))
        self.pregnancies_label.setText(_translate("MainWindow", "Pregnancies"))
        self.btn_add_pregnancy.setText(_translate("MainWindow", "+ New Pregnancy"))
