from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from screens.dashboard_ui import Ui_DashboardScreen
from database import get_connection


class DashboardScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DashboardScreen()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB - Dashboard")
        self._initialized = False

        self.ui.pushButton.clicked.connect(self.go_to_dashboard)
        self.ui.pushButton_2.clicked.connect(self.go_to_patient_records)
        self.ui.pushButton_3.clicked.connect(self.go_to_prenatal_care)
        self.ui.pushButton_4.clicked.connect(self.go_to_appointments)
        self.ui.pushButton_5.clicked.connect(self.logout)

    def showEvent(self, event):
        super().showEvent(event)
        if not self._initialized:
            self._initialized = True
            self.reposition_elements()
            self.load_logo()  # ← add this
            self.load_stats()
            self.load_recent_patients()

    def load_logo(self):
        from PyQt6.QtGui import QPixmap
        from PyQt6.QtCore import Qt
        pixmap = QPixmap("Asset/MaternaDB_logo.png")
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                self.ui.logo.width(),
                self.ui.logo.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.ui.logo.setPixmap(scaled)
            self.ui.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            print("Logo not found! Check Asset/MaternaDB_logo.png")

    def resizeEvent(self, event):  # ← this was missing!
        super().resizeEvent(event)
        self.reposition_elements()

    def reposition_elements(self):
        w = self.width()
        h = self.height()

        # Navbar
        self.ui.frame_2.setGeometry(0, 0, w, 61)

        # Sidebar
        self.ui.frame.setGeometry(0, 61, 231, h - 61)

        # Main content area
        main_x = 231
        main_w = w - 231
        main_h = h - 61
        self.ui.frame_3.setGeometry(main_x, 61, main_w, main_h)

        # Stat cards row
        self.ui.layoutWidget.setGeometry(40, 100, main_w - 80, 101)

        # Recent patients label and table
        table_w = int(main_w * 0.62)
        self.ui.label_3.setGeometry(50, 230, 131, 21)
        self.ui.patient_table.setGeometry(50, 260, table_w, main_h - 320)

        # Today's appointments
        appt_x = table_w + 70
        appt_w = main_w - table_w - 90
        self.ui.Todays_appointment_TA.setGeometry(appt_x, 230, appt_w, 21)
        self.ui.today_appointment.setGeometry(appt_x, 260, appt_w, main_h - 320)
        self.ui.content_container_TA.setGeometry(appt_x + 15, 280, appt_w - 30, 81)

    def load_stats(self):
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()

                cursor.execute("SELECT COUNT(*) FROM patient_profile")
                result = cursor.fetchone()
                self.ui.total_patient_label_2.setText(str(result[0]) if result else "0")

                cursor.execute("SELECT COUNT(*) FROM appointment")
                result = cursor.fetchone()
                self.ui.total_patient_label_3.setText(str(result[0]) if result else "0")

                cursor.execute("SELECT COUNT(*) FROM patient_profile WHERE patient_type = 'Maternal'")
                result = cursor.fetchone()
                self.ui.total_patient_label_4.setText(str(result[0]) if result else "0")

                cursor.execute("SELECT COUNT(*) FROM newborn")
                result = cursor.fetchone()
                self.ui.total_patient_label_5.setText(str(result[0]) if result else "0")

                conn.close()
            except Exception as e:
                print(f"Error loading stats: {e}")
                self.ui.total_patient_label_2.setText("0")
                self.ui.total_patient_label_3.setText("0")
                self.ui.total_patient_label_4.setText("0")
                self.ui.total_patient_label_5.setText("0")
                conn.close()

    def load_recent_patients(self):
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT
                        CONCAT(last_name, ', ', first_name, ' ', COALESCE(middle_name, '')),
                        patient_type,
                        date_registered
                    FROM patient_profile
                    ORDER BY date_registered DESC
                    LIMIT 5
                """)
                patients = cursor.fetchall()
                conn.close()

                if not patients:
                    self.ui.patient_table.setRowCount(0)
                    return

                self.ui.patient_table.setRowCount(len(patients))
                for row, patient in enumerate(patients):
                    for col, data in enumerate(patient):
                        self.ui.patient_table.setItem(
                            row, col, QTableWidgetItem(str(data) if data else "")
                        )

                # Fix column widths
                from PyQt6.QtWidgets import QHeaderView
                header = self.ui.patient_table.horizontalHeader()
                header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
                header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
                header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

            except Exception as e:
                print(f"Error loading patients: {e}")
                self.ui.patient_table.setRowCount(0)
                conn.close()

    def go_to_dashboard(self):
        self.load_stats()
        self.load_recent_patients()

    def go_to_patient_records(self):
        print("Go to Patient Records")

    def go_to_prenatal_care(self):
        from screens.prenatal_dashboard_screen import PrenatalDashboardScreen
        self.prenatal_window = PrenatalDashboardScreen()
        self.prenatal_window.showMaximized()
        self.close()

    def go_to_appointments(self):
        print("Go to Appointments")

    def logout(self):
        from screens.login_screen import LoginScreen
        self.login_window = LoginScreen()
        self.login_window.showMaximized()
        self.close()