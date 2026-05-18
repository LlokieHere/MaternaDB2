from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTableWidgetItem, QPushButton, QDialog,
    QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
from screens.completed_appointments_ui import Ui_MainWindow
from database import get_connection
import user_profile.session as session


class CompletedAppointmentsScreen(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Completed Appointments")
        self.current_appointment_id = None
        self.current_patient_id = None

        self.load_logo()
        self._inject_sidebar_profile()
        self._hide_details()
        self.setup_navigation()
        self.load_appointments()

        self.ui.pushButton_6.clicked.connect(self.open_new_appointment)
        self.ui.pushButton_7.clicked.connect(self.go_back)
        self.ui.pushButton_8.clicked.connect(self.schedule_followup)
        self.ui.pushButton_9.clicked.connect(self.view_full_record)

    # ── Logo ──────────────────────────────────────────────────────────────────
    def load_logo(self):
        from PyQt6.QtGui import QPixmap
        pixmap = QPixmap("Asset/MaternaDB_logo.png")
        if not pixmap.isNull():
            # label_9 is the logo slot in the completed_appointments UI header
            self.ui.label_9.setText("")
            self.ui.label_9.setStyleSheet("")
            self.ui.label_9.setPixmap(
                pixmap.scaled(
                    40, 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
            self.ui.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # ── Sidebar profile — inserted into the sidebar's own QVBoxLayout ─────────
    def _inject_sidebar_profile(self):
        """
        The completed_appointments UI sidebar has a QVBoxLayout that starts
        with label_10 (a 'LOGO' placeholder) then the nav buttons.
        We remove label_10 and insert the real profile widgets in its place
        so the layout manager handles all positioning — no setGeometry needed.
        """
        user = session.get()
        name = user["name"] if user else "User"
        role = user.get("role", "Admin") if user else "Admin"

        sidebar_layout = self.ui.frame.layout()   # existing QVBoxLayout

        # Remove the placeholder label_10 that the UI put at index 0
        self.ui.label_10.setParent(None)

        # ── Avatar ────────────────────────────────────────────────────────────
        self.profile_avatar = QLabel("👤")
        self.profile_avatar.setFixedSize(64, 64)
        self.profile_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_avatar.setStyleSheet(
            "background-color: #ECC6DC; border-radius: 32px;"
            "font-size: 28px; border: none;"
        )
        self.profile_avatar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.profile_avatar.mousePressEvent = lambda _: self._open_profile_dialog()

        # ── Name ──────────────────────────────────────────────────────────────
        self.profile_name_lbl = QLabel(name)
        self.profile_name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_name_lbl.setWordWrap(True)
        self.profile_name_lbl.setCursor(Qt.CursorShape.PointingHandCursor)
        self.profile_name_lbl.mousePressEvent = lambda _: self._open_profile_dialog()
        self.profile_name_lbl.setStyleSheet(
            "color: white; font-size: 13px; font-weight: bold;"
            "background: transparent; border: none;"
        )

        # ── Role ──────────────────────────────────────────────────────────────
        self.profile_role_lbl = QLabel(role)
        self.profile_role_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_role_lbl.setStyleSheet(
            "color: white; font-size: 11px; border: none;"
        )

        # ── Divider ───────────────────────────────────────────────────────────
        self.profile_divider = QLabel()
        self.profile_divider.setFixedHeight(1)
        self.profile_divider.setStyleSheet(
            "background-color: rgba(255,255,255,0.2); border: none;"
        )

        # Insert at index 0 (where label_10 was), pushing buttons down
        sidebar_layout.insertWidget(0, self.profile_divider)
        sidebar_layout.insertWidget(0, self.profile_role_lbl)
        sidebar_layout.insertWidget(0, self.profile_name_lbl)
        sidebar_layout.insertWidget(0, self.profile_avatar,
                                    alignment=Qt.AlignmentFlag.AlignHCenter)

    def _open_profile_dialog(self):
        from user_profile.user_profile_dialog import UserProfileDialog
        dlg = UserProfileDialog(parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            user = session.get()
            if user:
                self.profile_name_lbl.setText(user.get("name", ""))
                self.profile_role_lbl.setText(user.get("role", ""))

    # ── No resizeEvent needed — Qt layouts handle everything ──────────────────

    # ── Navigation ────────────────────────────────────────────────────────────
    def setup_navigation(self):
        try:
            self.ui.pushButton.clicked.connect(self.go_to_dashboard)
            self.ui.pushButton_2.clicked.connect(self.go_to_patient_records)
            self.ui.pushButton_3.clicked.connect(self.go_to_prenatal_care)
            self.ui.pushButton_4.clicked.connect(self.go_back)
            self.ui.pushButton_5.clicked.connect(self.logout)
        except Exception as e:
            print("Navigation error:", e)

    def _hide_details(self):
        self.ui.groupBox.hide()
        self.ui.widget.hide()
        self.ui.widget_5.hide()

    def _show_details(self):
        self.ui.groupBox.show()
        self.ui.widget.show()
        self.ui.widget_5.show()

    def load_appointments(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.appointment_id,
                       pp.first_name || ' ' || pp.last_name AS patient_name,
                       a.appointment_date,
                       a.appointment_time,
                       a.status
                FROM appointment a
                JOIN patient_profile pp ON a.patient_id = pp.patient_id
                WHERE a.status IN ('Completed', 'Missed', 'Cancelled')
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            tbl = self.ui.left_prescription_date_and_purpose
            tbl.setRowCount(0)
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            tbl.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

            for row_data in rows:
                appointment_id = row_data[0]
                patient_name   = row_data[1]
                date           = row_data[2].strftime("%B %d, %Y") if row_data[2] else ""
                time           = str(row_data[3])[:5] if row_data[3] else ""
                status         = row_data[4] or ""

                row_index = tbl.rowCount()
                tbl.insertRow(row_index)

                for col, val in enumerate([patient_name, date, time, status]):
                    item = QTableWidgetItem(val)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    tbl.setItem(row_index, col, item)

                view_btn = QPushButton("View")
                view_btn.setStyleSheet(
                    "background-color: rgb(106,27,154); color: white;"
                    "border-radius: 8px; padding: 4px 10px; font-weight: bold;"
                )
                def make_handler(aid):
                    def handler():
                        self.load_details(aid)
                    return handler
                view_btn.clicked.connect(make_handler(appointment_id))
                tbl.setCellWidget(row_index, 4, view_btn)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load appointments:\n{e}")

    def load_details(self, appointment_id):
        self.current_appointment_id = appointment_id
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pp.first_name || ' ' || pp.last_name,
                       a.appointment_date,
                       a.appointment_time,
                       a.appointment_type,
                       a.status,
                       a.remarks,
                       a.patient_id
                FROM appointment a
                JOIN patient_profile pp ON a.patient_id = pp.patient_id
                WHERE a.appointment_id = %s
            """, (appointment_id,))
            data = cursor.fetchone()

            cursor.execute("""
                SELECT purpose FROM appointment_purpose
                WHERE appointment_id = %s
            """, (appointment_id,))
            purposes = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()

            if not data:
                return

            date = data[1].strftime("%B %d, %Y") if data[1] else ""
            time = str(data[2])[:5] if data[2] else ""

            self.ui.label_3.setText(f"<b>Patient:</b> {data[0]}")
            self.ui.label_4.setText(f"<b>Date:</b> {date}")
            self.ui.label_5.setText(f"<b>Type of Visit:</b> {data[3]}")
            self.ui.label_6.setText(f"<b>Time:</b> {time}")
            self.ui.textEdit.setPlainText(", ".join(purposes) if purposes else "")
            self.ui.textEdit_2.setPlainText(data[5] or "")

            self.current_patient_id = data[6]
            self._show_details()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load details:\n{e}")

    def open_new_appointment(self):
        from Dialog.add_appointment_dialog import AddAppointmentDialog
        dialog = AddAppointmentDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_appointments()

    def schedule_followup(self):
        if not self.current_appointment_id:
            QMessageBox.warning(self, "No Selection",
                                "Please select an appointment first.")
            return
        from Dialog.add_appointment_dialog import AddAppointmentDialog
        dialog = AddAppointmentDialog(appointment_type="Follow-up", parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_appointments()

    def view_full_record(self):
        if not self.current_appointment_id:
            QMessageBox.warning(self, "No Selection",
                                "Please select an appointment first.")
            return
        from screens.patient_profile_screen import PatientProfileScreen
        self.new_window = PatientProfileScreen(self.current_patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_back(self):
        from screens.appointments_screen import AppointmentsScreen
        self.new_window = AppointmentsScreen()
        self.new_window.showMaximized()
        self.close()

    def go_to_dashboard(self):
        from screens.dashboard_screen import DashboardScreen
        self.new_window = DashboardScreen()
        self.new_window.showMaximized()
        self.close()

    def go_to_patient_records(self):
        from screens.patient_records_screen import PatientRecordScreen
        self.new_window = PatientRecordScreen()
        self.new_window.showMaximized()
        self.close()

    def go_to_prenatal_care(self):
        from screens.prenatal_dashboard_screen import PrenatalDashboardScreen
        self.new_window = PrenatalDashboardScreen()
        self.new_window.showMaximized()
        self.close()

    def logout(self):
        from screens.login_screen import LoginScreen
        self.new_window = LoginScreen()
        self.new_window.showMaximized()
        self.close()