from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTableWidgetItem, QPushButton, QDialog,
    QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
from screens.appointments_main_ui import Ui_MainWindow
from database import get_connection
import user_profile.session as session


class AppointmentsScreen(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Appointments")

        self.load_logo()
        self._inject_sidebar_profile()
        self.setup_navigation()
        self.load_appointments()

        self.ui.pushButton_6.clicked.connect(self.open_new_appointment)
        self.ui.pushButton_7.clicked.connect(self.go_to_completed)

    # ── Logo ──────────────────────────────────────────────────────────────────
    def load_logo(self):
        from PyQt6.QtGui import QPixmap
        pixmap = QPixmap("Asset/MaternaDB_logo.png")
        if not pixmap.isNull():
            self.ui.label_3.setText("")
            self.ui.label_3.setStyleSheet("")
            self.ui.label_3.setPixmap(
                pixmap.scaled(
                    40, 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
            self.ui.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # ── Sidebar profile — inserted into the sidebar's own QVBoxLayout ─────────
    def _inject_sidebar_profile(self):
        """
        The UI's sidebar already has a QVBoxLayout managing the buttons.
        We insert the profile widgets at the TOP of that layout so they
        sit above the nav buttons naturally, with no setGeometry conflicts.
        """
        user = session.get()
        name = user["name"] if user else "User"
        role = user.get("role", "Admin") if user else "Admin"

        sidebar_layout = self.ui.frame.layout()   # the existing QVBoxLayout

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

        # Insert at the top of the sidebar layout, above the existing spacing
        # and buttons.  Index 0 = very first slot.
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
            self.ui.pushButton_4.clicked.connect(self.go_to_appointments)
            self.ui.pushButton_5.clicked.connect(self.logout)
        except Exception as e:
            print("Navigation error:", e)

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
                       a.appointment_type,
                       a.status
                FROM appointment a
                JOIN patient_profile pp ON a.patient_id = pp.patient_id
                WHERE a.status IN ('Scheduled', 'Rescheduled')
                ORDER BY a.appointment_date ASC, a.appointment_time ASC
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
                status         = row_data[5] or ""

                row_index = tbl.rowCount()
                tbl.insertRow(row_index)

                for col, val in enumerate([patient_name, date, time, status]):
                    item = QTableWidgetItem(val)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    tbl.setItem(row_index, col, item)

                edit_btn = QPushButton("Edit")
                edit_btn.setStyleSheet(
                    "background-color: rgb(106,27,154); color: white;"
                    "border-radius: 8px; padding: 4px 10px; font-weight: bold;"
                )
                def make_handler(aid):
                    def handler():
                        self.open_edit_dialog(aid)
                    return handler
                edit_btn.clicked.connect(make_handler(appointment_id))
                tbl.setCellWidget(row_index, 4, edit_btn)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load appointments:\n{e}")

    def open_new_appointment(self):
        from Dialog.add_appointment_dialog import AddAppointmentDialog
        dialog = AddAppointmentDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_appointments()

    def open_edit_dialog(self, appointment_id):
        from Dialog.edit_appointment_dialog import EditAppointmentDialog
        dialog = EditAppointmentDialog(appointment_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_appointments()

    def go_to_completed(self):
        from screens.completed_appointments_screen import CompletedAppointmentsScreen
        self.new_window = CompletedAppointmentsScreen()
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

    def go_to_appointments(self):
        pass  # already here

    def logout(self):
        from screens.login_screen import LoginScreen
        self.new_window = LoginScreen()
        self.new_window.showMaximized()
        self.close()