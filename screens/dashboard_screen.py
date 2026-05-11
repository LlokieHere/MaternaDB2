from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from screens.dashboard_ui import Ui_DashboardScreen
from database import get_connection


class DashboardScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DashboardScreen()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB - Dashboard")

        self._initialized = False

        # Navigation
        self.ui.pushButton.clicked.connect(self.refresh_dashboard)
        self.ui.pushButton_2.clicked.connect(self.go_to_patient_records)
        self.ui.pushButton_3.clicked.connect(self.go_to_prenatal_care)
        self.ui.pushButton_4.clicked.connect(self.go_to_appointments)
        self.ui.pushButton_5.clicked.connect(self.logout)

    # -------------------------
    # EVENTS
    # -------------------------
    def showEvent(self, event):
        super().showEvent(event)
        if not self._initialized:
            self._initialized = True
            self.setup_ui()
            self.refresh_dashboard()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.layout_dashboard()

    # -------------------------
    # UI SETUP
    # -------------------------
    def setup_ui(self):
        self.load_logo()
        self.layout_dashboard()

        # Table styling improvement
        self.ui.patient_table.setAlternatingRowColors(True)
        self.ui.patient_table.setShowGrid(False)

        header = self.ui.patient_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

    def load_logo(self):
        pixmap = QPixmap("Asset/MaternaDB_logo.png")
        if not pixmap.isNull():
            self.ui.logo.setPixmap(
                pixmap.scaled(
                    40, 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
            self.ui.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # -------------------------
    # LAYOUT ENGINE (FIXED)
    # -------------------------
    def layout_dashboard(self):
        w = self.width()
        h = self.height()

        sidebar_w = 230
        navbar_h = 60
        padding = 30

        # Navbar
        self.ui.frame_2.setGeometry(0, 0, w, navbar_h)

        # Sidebar
        self.ui.frame.setGeometry(0, navbar_h, sidebar_w, h - navbar_h)

        # Main content
        main_x = sidebar_w
        main_w = w - sidebar_w
        main_h = h - navbar_h

        self.ui.frame_3.setGeometry(main_x, navbar_h, main_w, main_h)

        # Title
        self.ui.label.setGeometry(padding, 20, 400, 60)

        # STAT CARDS
        card_area_y = 100
        card_height = 110
        card_spacing = 20

        card_width = int((main_w - (padding * 2) - (card_spacing * 3)) / 4)

        self.ui.layoutWidget.setGeometry(
            padding,
            card_area_y,
            main_w - (padding * 2),
            card_height
        )

        # TABLE + APPOINTMENTS SECTION
        content_y = card_area_y + card_height + 40
        content_height = main_h - content_y - padding

        table_width = int(main_w * 0.65)
        right_width = main_w - table_width - (padding * 3)

        # Recent Patients
        self.ui.label_3.setGeometry(padding, content_y - 25, 200, 25)
        self.ui.patient_table.setGeometry(
            padding,
            content_y,
            table_width,
            content_height
        )

        # Appointments Panel
        right_x = padding + table_width + padding

        self.ui.Todays_appointment_TA.setGeometry(
            right_x,
            content_y - 25,
            right_width,
            25
        )

        self.ui.today_appointment.setGeometry(
            right_x,
            content_y,
            right_width,
            content_height
        )

        self.ui.content_container_TA.setGeometry(
            right_x + 10,
            content_y + 10,
            right_width - 20,
            90
        )

    # -------------------------
    # DATA LOADING
    # -------------------------
    def refresh_dashboard(self):
        self.load_stats()
        self.load_recent_patients()

    def load_stats(self):
        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM patient_profile")
            self.ui.total_patient_label_2.setText(str(cursor.fetchone()[0]))

            cursor.execute("SELECT COUNT(*) FROM appointment WHERE ")
            self.ui.total_patient_label_3.setText(str(cursor.fetchone()[0]))

            cursor.execute("SELECT COUNT(*) FROM patient_profile WHERE patient_type = 'Maternal'")
            self.ui.total_patient_label_4.setText(str(cursor.fetchone()[0]))

            cursor.execute("SELECT COUNT(*) FROM newborn")
            self.ui.total_patient_label_5.setText(str(cursor.fetchone()[0]))

        except Exception as e:
            print("Stats error:", e)

        finally:
            conn.close()

    def load_recent_patients(self):
        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    CONCAT(last_name, ', ', first_name, ' ', COALESCE(middle_name, '')),
                    philhealth_no,
                    date_registered
                FROM patient_profile
                ORDER BY date_registered DESC
                LIMIT 5
            """)

            patients = cursor.fetchall()

            self.ui.patient_table.setRowCount(len(patients))

            for row, patient in enumerate(patients):
                for col, value in enumerate(patient):
                    self.ui.patient_table.setItem(
                        row, col, QTableWidgetItem(str(value))
                    )

        except Exception as e:
            print("Patient load error:", e)

        finally:
            conn.close()

    # -------------------------
    # NAVIGATION
    # -------------------------
    def go_to_patient_records(self):
        from screens.patient_records_screen import PatientRecordScreen
        self.window = PatientRecordScreen()
        self.window.showMaximized()
        self.close()

    def go_to_prenatal_care(self):
        from screens.prenatal_dashboard_screen import PrenatalDashboardScreen
        self.window = PrenatalDashboardScreen()
        self.window.showMaximized()
        self.close()

    def go_to_appointments(self):
        print("Appointments screen not connected yet")

    def logout(self):
        from screens.login_screen import LoginScreen
        self.window = LoginScreen()
        self.window.showMaximized()
        self.close()