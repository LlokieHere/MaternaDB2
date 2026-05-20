from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QLabel, QDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
from screens.dashboard_ui import Ui_DashboardScreen
from database import get_connection
import user_profile.session as session

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

        # ── NEW: Manage Staff button ──────────────────────────────────────
        self.ui.manage_staff_btn.clicked.connect(self._open_staff_management)

        # Auto-refresh every 30 seconds
        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(30_000)
        self.refresh_timer.timeout.connect(self.refresh_dashboard)

        self._build_sidebar_profile()

    # -------------------------
    # SIDEBAR PROFILE
    # -------------------------
    def _build_sidebar_profile(self):
        user = session.get()
        name = user["name"] if user else "User"
        role = user.get("role", "Admin") if user else "Admin"

        self.profile_avatar = QLabel("👤", parent=self.ui.frame)
        self.profile_avatar.setFixedSize(64, 64)
        self.profile_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_avatar.setStyleSheet(
            "background-color: #ECC6DC; border-radius: 32px;"
            "font-size: 28px; border: none;"
        )
        self.profile_avatar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.profile_avatar.mousePressEvent = lambda _: self._open_profile_dialog()

        self.profile_name_lbl = QLabel(name, parent=self.ui.frame)
        self.profile_name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_name_lbl.setWordWrap(True)
        self.profile_name_lbl.setCursor(Qt.CursorShape.PointingHandCursor)
        self.profile_name_lbl.mousePressEvent = lambda _: self._open_profile_dialog()
        self.profile_name_lbl.setStyleSheet(
            "color: white; font-size: 13px; font-weight: bold;"
            "background: transparent; border: none;"
        )

        self.profile_role_lbl = QLabel(role, parent=self.ui.frame)
        self.profile_role_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_role_lbl.setStyleSheet(
            "color: rgba(255,255,255,0.65); font-size: 11px;"
            "background: transparent; border: none;"
        )

        self.profile_divider = QLabel(parent=self.ui.frame)
        self.profile_divider.setFixedHeight(1)
        self.profile_divider.setStyleSheet(
            "background-color: rgba(255,255,255,0.2); border: none;"
        )

        for w in (self.profile_avatar, self.profile_name_lbl,
                  self.profile_role_lbl, self.profile_divider):
            w.show()

    def _reposition_sidebar_profile(self):
        sidebar_w = self.ui.frame.width()
        pad     = 16
        av_size = 64

        av_x = (sidebar_w - av_size) // 2
        av_y = 20
        self.profile_avatar.setGeometry(av_x, av_y, av_size, av_size)

        name_y = av_y + av_size + 8
        self.profile_name_lbl.setGeometry(pad, name_y, sidebar_w - pad * 2, 36)

        role_y = name_y + 38
        self.profile_role_lbl.setGeometry(pad, role_y, sidebar_w - pad * 2, 18)

        div_y = role_y + 26
        self.profile_divider.setGeometry(pad, div_y, sidebar_w - pad * 2, 1)

    def _open_profile_dialog(self):
        from user_profile.user_profile_dialog import UserProfileDialog
        dlg = UserProfileDialog(parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            user = session.get()
            if user:
                self.profile_name_lbl.setText(user.get("name", ""))
                self.profile_role_lbl.setText(user.get("role", ""))

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
        self._reposition_sidebar_profile()

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
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.ui.patient_table.setColumnWidth(2, 120)

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

        # Nav buttons
        btn_top = 190
        btn_h   = 41
        btn_gap = 5
        btn_x   = 10
        btn_w   = sidebar_w - 20

        for i, btn in enumerate([
            self.ui.pushButton,
            self.ui.pushButton_2,
            self.ui.pushButton_3,
            self.ui.pushButton_4,
        ]):
            btn.setGeometry(btn_x, btn_top + i * (btn_h + btn_gap), btn_w, btn_h)

        self.ui.pushButton_5.setGeometry(btn_x, h - navbar_h - 60, btn_w, btn_h)

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

            # count prenatal visits under ongoing pregnancies
            cursor.execute("""
                SELECT COUNT(*)
                FROM prenatal_visit pv
                JOIN pregnancy p ON pv.pregnancy_id = p.pregnancy_id
                WHERE p.status = 'Ongoing'
            """)
            self.ui.total_patient_label_4.setText(str(cursor.fetchone()[0]))

            # count deliveries (completed pregnancies)
            cursor.execute("""
                SELECT COUNT(*)
                FROM delivery_record dr
                JOIN pregnancy p ON dr.pregnancy_id = p.pregnancy_id
                WHERE p.status = 'Completed'
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
                    TO_CHAR(date_registered, 'Mon DD, YYYY')
                FROM patient_profile
                ORDER BY date_registered DESC
                LIMIT 5
            """)
            patients = cursor.fetchall()
            self.ui.patient_table.setRowCount(len(patients))
            for row, patient in enumerate(patients):
                for col, value in enumerate(patient):
                    item = QTableWidgetItem(str(value))
                    if col == 2:
                        item.setTextAlignment(
                            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                        )
                    self.ui.patient_table.setItem(row, col, item)
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
                    p.first_name || ' ' || p.last_name AS patient_name,
                    a.appointment_time,
                    STRING_AGG(ap.purpose, ', ')        AS purposes,
                    a.appointment_date
                FROM appointment a
                JOIN patient_profile p ON a.patient_id = p.patient_id
                JOIN appointment_purpose ap ON a.appointment_id = ap.appointment_id
                WHERE a.appointment_date = CURRENT_DATE
                AND   a.status = 'Scheduled'
                GROUP BY p.first_name, p.last_name, a.appointment_time, a.appointment_date
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
        self.refresh_timer.stop()
        from screens.appointments_screen import AppointmentsScreen
        self.new_window = AppointmentsScreen()
        self.new_window.showMaximized()
        self.close()

    def logout(self):
        self.refresh_timer.stop()
        session.clear()
        from screens.login_screen import LoginScreen
        self.new_window = LoginScreen()
        self.new_window.showMaximized()
        self.close()

    # ── NEW ──────────────────────────────────────────────────────────────────
    def _open_staff_management(self):
        from staff_management.staff_management_dialog import StaffManagementDialog
        dlg = StaffManagementDialog(parent=self)
        dlg.exec()   # opens as dialog; user stays on dashboard when closed