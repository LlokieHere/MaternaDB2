from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
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

        # Auto-refresh every 30 seconds
        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(30_000)
        self.refresh_timer.timeout.connect(self.refresh_dashboard)

    # -------------------------
    # EVENTS
    # -------------------------
    def showEvent(self, event):
        super().showEvent(event)
        if not self._initialized:
            self._initialized = True
            self.setup_ui()

        self.refresh_dashboard()
        self.refresh_timer.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.layout_dashboard()

    # -------------------------
    # UI SETUP
    # -------------------------
    def setup_ui(self):
        self.load_logo()
        self.layout_dashboard()

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
    # LAYOUT ENGINE
    # -------------------------
    def layout_dashboard(self):
        w = self.width()
        h = self.height()

        sidebar_w = 230
        navbar_h  = 60
        padding   = 30

        self.ui.frame_2.setGeometry(0, 0, w, navbar_h)
        self.ui.frame.setGeometry(0, navbar_h, sidebar_w, h - navbar_h)

        main_x = sidebar_w
        main_w = w - sidebar_w
        main_h = h - navbar_h

        self.ui.frame_3.setGeometry(main_x, navbar_h, main_w, main_h)
        self.ui.label.setGeometry(padding, 20, 400, 60)

        card_area_y = 100
        card_height = 110

        self.ui.layoutWidget.setGeometry(
            padding,
            card_area_y,
            main_w - (padding * 2),
            card_height
        )

        content_y      = card_area_y + card_height + 40
        content_height = main_h - content_y - padding
        table_width    = int(main_w * 0.65)
        right_width    = main_w - table_width - (padding * 3)
        right_x        = padding + table_width + padding

        self.ui.label_3.setGeometry(padding, content_y - 25, 200, 25)
        self.ui.patient_table.setGeometry(padding, content_y, table_width, content_height)

        self.ui.Todays_appointment_TA.setGeometry(right_x, content_y - 25, right_width, 25)
        self.ui.today_appointment.setGeometry(right_x, content_y, right_width, content_height)
        self.ui.content_container_TA.setGeometry(right_x + 10, content_y + 10, right_width - 20, 90)

    # -------------------------
    # DATA LOADING
    # -------------------------
    def refresh_dashboard(self):
        self.load_stats()
        self.load_recent_patients()
        self.load_todays_appointments()

    def load_stats(self):
        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM patient_profile")
            self.ui.total_patient_label_2.setText(str(cursor.fetchone()[0]))

            cursor.execute("""
                SELECT COUNT(*) FROM appointment
                WHERE status = 'Scheduled'
                AND appointment_date >= CURRENT_DATE
            """)
            self.ui.total_patient_label_3.setText(str(cursor.fetchone()[0]))

            cursor.execute("""
                SELECT COUNT(*)
                FROM appointment a
                JOIN appointment_purpose ap ON a.appointment_id = ap.appointment_id
                WHERE a.status = 'Completed'
                AND ap.purpose ILIKE '%prenatal%'
            """)
            self.ui.total_patient_label_4.setText(str(cursor.fetchone()[0]))

            cursor.execute("""
                SELECT COUNT(*)
                FROM appointment a
                JOIN appointment_purpose ap ON a.appointment_id = ap.appointment_id
                WHERE a.status = 'Completed'
                AND ap.purpose ILIKE '%deliver%'
            """)
            self.ui.total_patient_label_5.setText(str(cursor.fetchone()[0]))

            cursor.close()

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

            cursor.close()

        except Exception as e:
            print("Patient load error:", e)

        finally:
            conn.close()

    def load_todays_appointments(self):
        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    p.first_name || ' ' || p.last_name  AS patient_name,
                    a.appointment_time,
                    STRING_AGG(ap.purpose, ', ')         AS purposes,
                    a.appointment_date
                FROM appointment a
                JOIN patient_profile p
                    ON a.patient_id = p.patient_id
                JOIN appointment_purpose ap
                    ON a.appointment_id = ap.appointment_id
                WHERE a.appointment_date = CURRENT_DATE
                AND   a.status = 'Scheduled'
                GROUP BY p.first_name, p.last_name,
                         a.appointment_time, a.appointment_date
                ORDER BY a.appointment_time
                LIMIT 1
            """)

            row = cursor.fetchone()
            cursor.close()

            if row:
                patient_name, appt_time, purposes, appt_date = row

                time_str = appt_time.strftime("%I:%M %p") if appt_time else ""

                self.ui.day.setText(str(appt_date.day))
                self.ui.day_2.setText(appt_date.strftime("%b"))
                self.ui.patient_name_TA.setText(patient_name)
                self.ui.time_TA.setText(time_str)
                self.ui.purpose_TA.setText(purposes or "")
            else:
                self.ui.day.setText("—")
                self.ui.day_2.setText("")
                self.ui.patient_name_TA.setText("No appointments today")
                self.ui.time_TA.setText("")
                self.ui.purpose_TA.setText("")

        except Exception as e:
            print("Today's appointment error:", e)

        finally:
            conn.close()

    # -------------------------
    # NAVIGATION
    # -------------------------
    def go_to_patient_records(self):
        self.refresh_timer.stop()
        from screens.patient_records_screen import PatientRecordScreen
        self.new_window = PatientRecordScreen()
        self.new_window.showMaximized()
        self.close()

    def go_to_prenatal_care(self):
        self.refresh_timer.stop()
        from screens.prenatal_dashboard_screen import PrenatalDashboardScreen
        self.new_window = PrenatalDashboardScreen()
        self.new_window.showMaximized()
        self.close()

    def go_to_appointments(self):
        print("Appointments screen not connected yet")

    def logout(self):
        self.refresh_timer.stop()
        from screens.login_screen import LoginScreen
        self.new_window = LoginScreen()
        self.new_window.showMaximized()
        self.close()