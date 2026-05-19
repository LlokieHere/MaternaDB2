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

    # ── Sidebar profile ───────────────────────────────────────────────────────
    def _inject_sidebar_profile(self):
        user = session.get()
        name = user["name"] if user else "User"
        role = user.get("role", "Admin") if user else "Admin"

        sidebar_layout = self.ui.frame.layout()
        self.ui.label_10.setParent(None)

        self.profile_avatar = QLabel("👤")
        self.profile_avatar.setFixedSize(64, 64)
        self.profile_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_avatar.setStyleSheet(
            "background-color: #ECC6DC; border-radius: 32px;"
            "font-size: 28px; border: none;"
        )
        self.profile_avatar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.profile_avatar.mousePressEvent = lambda _: self._open_profile_dialog()

        self.profile_name_lbl = QLabel(name)
        self.profile_name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_name_lbl.setWordWrap(True)
        self.profile_name_lbl.setCursor(Qt.CursorShape.PointingHandCursor)
        self.profile_name_lbl.mousePressEvent = lambda _: self._open_profile_dialog()
        self.profile_name_lbl.setStyleSheet(
            "color: white; font-size: 13px; font-weight: bold;"
            "background: transparent; border: none;"
        )

        self.profile_role_lbl = QLabel(role)
        self.profile_role_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_role_lbl.setStyleSheet(
            "color: white; font-size: 11px; border: none;"
        )

        self.profile_divider = QLabel()
        self.profile_divider.setFixedHeight(1)
        self.profile_divider.setStyleSheet(
            "background-color: rgba(255,255,255,0.2); border: none;"
        )

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

    # ── Main appointment list ─────────────────────────────────────────────────
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

    # ── Detail panel ──────────────────────────────────────────────────────────
    def load_details(self, appointment_id):
        self.current_appointment_id = appointment_id
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()

            # Fetch all appointment fields + staff name in one query.
            # Every column here corresponds to a field in one of the two dialogs:
            #   patient_name, date, time, type  → Add dialog
            #   status, staff_name, date_created → Edit dialog info panel
            #   remarks                          → both dialogs
            cursor.execute("""
                SELECT pp.first_name || ' ' || pp.last_name          AS patient_name,
                       a.appointment_date,
                       a.appointment_time,
                       a.appointment_type,
                       a.status,
                       a.remarks,
                       a.patient_id,
                       a.date_created,
                       s.first_name || ' ' || s.last_name
                           || ' (' || s.role || ')'                  AS staff_name
                FROM appointment a
                JOIN patient_profile pp ON a.patient_id = pp.patient_id
                JOIN staff           s  ON a.staff_id   = s.staff_id
                WHERE a.appointment_id = %s
            """, (appointment_id,))
            data = cursor.fetchone()

            # Purposes — one row per purpose, entered in Add dialog
            cursor.execute("""
                SELECT purpose FROM appointment_purpose
                WHERE appointment_id = %s
                ORDER BY purpose_id
            """, (appointment_id,))
            purposes = [row[0] for row in cursor.fetchall()]

            # Status history — each Edit dialog save appends one row:
            #   status     → New Status combo
            #   reason     → Reason for Status Change text
            #   updated_by → Updated By combo
            cursor.execute("""
                SELECT ash.status,
                       ash.status_date,
                       ash.reason,
                       COALESCE(s.first_name || ' ' || s.last_name, 'System') AS updated_by
                FROM appointment_status_history ash
                LEFT JOIN staff s ON ash.updated_by = s.staff_id
                WHERE ash.appointment_id = %s
                ORDER BY ash.status_date ASC, ash.status_history_id ASC
            """, (appointment_id,))
            history_rows = cursor.fetchall()

            cursor.close()
            conn.close()

            if not data:
                return

            (patient_name, appt_date, appt_time, appt_type,
             status, remarks, patient_id, date_created, staff_name) = data

            date_str    = appt_date.strftime("%B %d, %Y")    if appt_date    else "—"
            time_str    = str(appt_time)[:5]                  if appt_time    else "—"
            created_str = date_created.strftime("%B %d, %Y") if date_created else "—"

            # ── Left column ───────────────────────────────────────────────────
            self.ui.label_3.setText(f"<b>Patient:</b> {patient_name}")
            self.ui.label_4.setText(f"<b>Date:</b> {date_str}")
            self.ui.label_6.setText(f"<b>Time:</b> {time_str}")
            self.ui.label_5.setText(f"<b>Type of Visit:</b> {appt_type}")
            self.ui.label_status.setText(f"<b>Status:</b> {status}")
            self.ui.label_staff.setText(f"<b>Assigned Staff:</b> {staff_name}")
            self.ui.label_date_created.setText(f"<b>Date Created:</b> {created_str}")

            # ── Middle column ─────────────────────────────────────────────────
            self.ui.textEdit.setPlainText(
                ", ".join(purposes) if purposes else "—"
            )
            self.ui.textEdit_2.setPlainText(remarks or "—")

            # ── Right column: status history ──────────────────────────────────
            # [MMM DD, YYYY]  STATUS — reason  (by Staff Name)
            history_lines = []
            for h in history_rows:
                h_status = h[0]
                h_date   = h[1].strftime("%b %d, %Y") if h[1] else "—"
                h_reason = f"  —  {h[2]}" if h[2] else ""
                h_by     = h[3]
                history_lines.append(
                    f"[{h_date}]  {h_status}{h_reason}  (by {h_by})"
                )

            self.ui.textEdit_3.setPlainText(
                "\n".join(history_lines) if history_lines
                else "No status history recorded."
            )

            self.current_patient_id = patient_id
            self._show_details()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load details:\n{e}")

    # ── Actions ───────────────────────────────────────────────────────────────
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

    # ── Screen navigation ─────────────────────────────────────────────────────
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