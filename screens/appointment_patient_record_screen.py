from PyQt6.QtWidgets import (
    QDialog, QLabel, QMainWindow, QMessageBox, QTableWidgetItem, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
from screens.appointment_patient_record_ui import Ui_MainWindow
from database import get_connection
import user_profile.session as session


class PatientAppointmentScreen(QMainWindow):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.patient_id = patient_id
        self.setWindowTitle("Appointment History")

        # ── Fix the mislabelled "Type" label → "Remarks:" ────────────────────
        # label_10 sits at grid row 4 col 0 and was showing "Type" (wrong).
        # duration_value at row 4 col 1 was receiving remarks data (correct use,
        # wrong label). Relabel both cleanly here so the .ui file stays untouched.
        self.ui.label_10.setText("Remarks:")

        # ── Add Status and Date Created rows to the grid ──────────────────────
        # The existing gridLayout_2 inside formWidget has rows 0-4.
        # We append two more rows (5 and 6) for the fields that were missing
        # vs the completed appointments screen.
        lbl_style = (
            "font: 10pt 'Segoe UI'; font-weight: bold;"
            "color: rgb(26, 26, 62); border: none;"
        )
        val_style = (
            "font: 10pt 'Segoe UI';"
            "color: rgb(26, 26, 62); border: none;"
        )

        self._status_label = QLabel("Status:")
        self._status_label.setStyleSheet(lbl_style)
        self._status_value = QLabel("")
        self._status_value.setStyleSheet(val_style)

        self._created_label = QLabel("Date Created:")
        self._created_label.setStyleSheet(lbl_style)
        self._created_value = QLabel("")
        self._created_value.setStyleSheet(val_style)

        grid = self.ui.gridLayout_2
        grid.addWidget(self._status_label,  5, 0)
        grid.addWidget(self._status_value,  5, 1)
        grid.addWidget(self._created_label, 6, 0)
        grid.addWidget(self._created_value, 6, 1)

        self.clear_details()
        self.setup_navigation()
        self.load_patient_data()
        self.load_appointments()

        self.ui.appointments_table.cellClicked.connect(self.on_row_clicked)
        self.load_logo()
        self._build_sidebar_profile()

    # ─────────────────────────────────────────────────────────────────────────
    # SIDEBAR PROFILE
    # ─────────────────────────────────────────────────────────────────────────
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
            "color: white; font-size: 11px; border: none;"
        )

        self.profile_divider = QLabel(parent=self.ui.frame)
        self.profile_divider.setFixedHeight(1)
        self.profile_divider.setStyleSheet(
            "background-color: rgba(255,255,255,0.2); border: none;"
        )

        for w in (
            self.profile_avatar,
            self.profile_name_lbl,
            self.profile_role_lbl,
            self.profile_divider,
        ):
            w.raise_()
            w.show()

    def _reposition_sidebar_profile(self):
        sidebar_w = self.ui.frame.width()
        pad, av_size = 16, 64
        av_x = (sidebar_w - av_size) // 2
        av_y = 20
        self.profile_avatar.setGeometry(av_x, av_y, av_size, av_size)
        name_y = av_y + av_size + 8
        self.profile_name_lbl.setGeometry(pad, name_y, sidebar_w - pad * 2, 36)
        role_y = name_y + 24
        self.profile_role_lbl.setGeometry(pad, role_y, sidebar_w - pad * 2, 18)
        div_y = role_y + 18
        self.profile_divider.setGeometry(pad, div_y, sidebar_w - pad * 2, 1)

    def _open_profile_dialog(self):
        from user_profile.user_profile_dialog import UserProfileDialog
        dlg = UserProfileDialog(parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            user = session.get()
            if user:
                self.profile_name_lbl.setText(user.get("name", ""))
                self.profile_role_lbl.setText(user.get("role", ""))

    # ─────────────────────────────────────────────────────────────────────────
    # RESIZE / LAYOUT
    # ─────────────────────────────────────────────────────────────────────────
    def layout_sidebar(self):
        h = self.height()
        sidebar_w = 230
        self.profile_avatar.setGeometry(73, 20, 64, 64)
        self.profile_name_lbl.setGeometry(20, 95, 190, 30)
        self.profile_role_lbl.setGeometry(20, 120, 190, 20)
        self.profile_divider.setGeometry(15, 150, 200, 1)
        btn_top, btn_h, btn_gap, btn_x = 170, 41, 8, 10
        btn_w = sidebar_w - 20
        for i, btn in enumerate([
            self.ui.pushButton, self.ui.pushButton_2,
            self.ui.pushButton_3, self.ui.pushButton_4,
        ]):
            btn.setGeometry(btn_x, btn_top + i * (btn_h + btn_gap), btn_w, btn_h)
        self.ui.pushButton_5.setGeometry(btn_x, h - 120, btn_w, btn_h)

    def layout_nav(self):
        w, h = self.width(), self.height()
        sidebar_w, navbar_h = 230, 60
        self.ui.frame_2.setGeometry(0, 0, w, navbar_h)
        self.ui.frame.setGeometry(0, navbar_h, sidebar_w, h - navbar_h)
        self.ui.frame_3.setGeometry(sidebar_w, navbar_h, w - sidebar_w, h - navbar_h)
        btn_x, btn_w, btn_h, gap = 20, 191, 41, 10
        start_y = 180
        for i, btn in enumerate([
            self.ui.pushButton, self.ui.pushButton_2,
            self.ui.pushButton_3, self.ui.pushButton_4,
        ]):
            btn.setGeometry(btn_x, start_y + i * (btn_h + gap), btn_w, btn_h)
        self.ui.pushButton_5.setGeometry(btn_x, h - navbar_h - 70, btn_w, btn_h)

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
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            self.ui.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = self.width(), self.height()

        self.ui.frame_2.setGeometry(0, 0, w, 61)
        sidebar_w = int(w * 0.19)
        self.ui.frame.setGeometry(0, 61, sidebar_w, h - 61)
        btn_x, btn_w = 20, sidebar_w - 30
        self.ui.pushButton.setGeometry(btn_x, 180, btn_w, 41)
        self.ui.pushButton_2.setGeometry(btn_x, 230, btn_w, 41)
        self.ui.pushButton_3.setGeometry(btn_x, 280, btn_w, 41)
        self.ui.pushButton_4.setGeometry(btn_x, 330, btn_w, 41)
        self.ui.pushButton_5.setGeometry(btn_x, h - 200, btn_w, 41)

        content_x = sidebar_w
        content_w = w - sidebar_w
        content_h = h - 61
        self.ui.frame_3.setGeometry(content_x, 61, content_w, content_h)

        pad = 40
        inner_w = content_w - (pad * 2)

        self.ui.label.setGeometry(pad, 20, inner_w // 2, 61)

        header_h = 141
        self.ui.frame_4.setGeometry(pad, 80, inner_w, header_h)
        self.ui.frame_5.setGeometry(20, 20, 111, 91)
        self.ui.patient_name.setGeometry(170, 15, inner_w - 320, 30)
        self.ui.next_btn.setGeometry(inner_w - 140, 45, 120, 51)
        self.ui.layoutWidget.setGeometry(170, 55, inner_w - 320, 75)

        tab_y = 80 + header_h + 20
        self.ui.layoutWidget1.setGeometry(pad, tab_y, inner_w, 40)

        section_label_y = tab_y + 50
        self.ui.label_12.setGeometry(pad, section_label_y, inner_w // 2, 40)

        panels_y = section_label_y + 50
        panels_h = content_h - panels_y - pad
        left_w  = int(inner_w * 0.44)
        right_w = inner_w - left_w - 20

        self.ui.left.setGeometry(pad, panels_y, left_w, panels_h)
        self.ui.appointments_table.setGeometry(0, 0, left_w, panels_h)
        self.ui.appointments_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        # right_details is taller now (two extra rows: Status + Date Created)
        self.ui.right_details.setGeometry(pad + left_w + 20, panels_y, right_w, panels_h)
        self.ui.label_4.setGeometry(15, 10, right_w - 20, 21)
        self.ui.formWidget.setGeometry(15, 40, right_w - 20, 280)   # was 220, now 280
        self.ui.purpose_label.setGeometry(15, 330, right_w - 20, 18)  # shifted down
        self.ui.purpose_value.setGeometry(15, 352, right_w - 20, 60)  # shifted down

        self._reposition_sidebar_profile()
        self.layout_sidebar()
        self.layout_nav()

    # ─────────────────────────────────────────────────────────────────────────
    # DETAILS PANEL
    # ─────────────────────────────────────────────────────────────────────────
    def clear_details(self):
        """Reset every value label in the detail panel to blank."""
        self.ui.date_value.setText("")
        self.ui.time_value.setText("")
        self.ui.type_value.setText("")
        self.ui.doctor_value.setText("")
        self.ui.duration_value.setText("")   # remarks
        self.ui.purpose_value.setText("")
        self._status_value.setText("")
        self._created_value.setText("")

    def load_details(self, appointment_id):
        """
        Populate the right-hand detail panel for one appointment.

        Field mapping (UI widget → DB column):
            date_value    → appointment.appointment_date
            time_value    → appointment.appointment_time
            type_value    → appointment.appointment_type
            doctor_value  → staff.first_name + last_name (+ role)
            duration_value→ appointment.remarks          ← was mislabelled "Type"
            purpose_value → appointment_purpose rows
            _status_value → appointment.status           ← NEW
            _created_value→ appointment.date_created      ← NEW
        """
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()

            # One query pulls everything from appointment + staff join
            cursor.execute("""
                SELECT a.appointment_date,
                       a.appointment_time,
                       a.appointment_type,
                       s.first_name || ' ' || s.last_name
                           || ' (' || s.role || ')' AS staff_name,
                       a.remarks,
                       a.status,
                       a.date_created
                FROM appointment a
                JOIN staff s ON a.staff_id = s.staff_id
                WHERE a.appointment_id = %s
            """, (appointment_id,))
            data = cursor.fetchone()

            cursor.execute("""
                SELECT purpose FROM appointment_purpose
                WHERE appointment_id = %s
                ORDER BY purpose_id
            """, (appointment_id,))
            purposes = [row[0] for row in cursor.fetchall()]

            cursor.close()
            conn.close()

            if not data:
                return

            (appt_date, appt_time, appt_type,
             staff_name, remarks, status, date_created) = data

            date_str    = appt_date.strftime("%B %d, %Y")    if appt_date    else "—"
            time_str    = str(appt_time)[:5]                  if appt_time    else "—"
            created_str = date_created.strftime("%B %d, %Y") if date_created else "—"

            # Bind to UI widgets
            self.ui.date_value.setText(date_str)
            self.ui.time_value.setText(time_str)
            self.ui.type_value.setText(appt_type or "—")
            self.ui.doctor_value.setText(staff_name or "—")
            self.ui.duration_value.setText(remarks or "—")   # Remarks field
            self.ui.purpose_value.setText(
                ", ".join(purposes) if purposes else "—"
            )
            self._status_value.setText(status or "—")
            self._created_value.setText(created_str)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load details:\n{e}")

    # ─────────────────────────────────────────────────────────────────────────
    # NAVIGATION SETUP
    # ─────────────────────────────────────────────────────────────────────────
    def setup_navigation(self):
        try:
            self.ui.pushButton.clicked.connect(self.go_to_dashboard)
            self.ui.pushButton_2.clicked.connect(self.go_to_patient_records)
            self.ui.pushButton_3.clicked.connect(self.go_to_prenatal_care)
            self.ui.pushButton_4.clicked.connect(self.go_to_appointments)
            self.ui.pushButton_5.clicked.connect(self.logout)

            self.ui.pushButton_6.clicked.connect(self.go_to_patient_profile)
            self.ui.pushButton_7.clicked.connect(self.go_to_past_pregnancy)
            self.ui.pushButton_8.clicked.connect(self.go_to_prescription)
            self.ui.pushButton_9.clicked.connect(self.go_to_medical_history)
            self.ui.pushButton_10.clicked.connect(self.go_to_family_planning)
            self.ui.pushButton_11.clicked.connect(self.go_to_appointment_tab)
        except Exception as e:
            print("Navigation error:", e)

    # ─────────────────────────────────────────────────────────────────────────
    # DATA LOADERS
    # ─────────────────────────────────────────────────────────────────────────
    def load_patient_data(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT patient_id, first_name, middle_name, last_name,
                       date_registered, blood_type, philhealth_no
                FROM patient_profile WHERE patient_id = %s
            """, (self.patient_id,))
            data = cursor.fetchone()

            cursor.execute("""
                SELECT EXTRACT(YEAR FROM AGE(date_of_birth))
                FROM patient_profile WHERE patient_id = %s
            """, (self.patient_id,))
            age_result = cursor.fetchone()
            cursor.close()
            conn.close()

            if not data:
                return

            full_name = " ".join(filter(None, [data[1], data[2], data[3]]))
            register  = data[4].strftime("%B %d, %Y") if data[4] else ""

            self.ui.patient_name.setText(full_name)
            self.ui.placeholder_p_ID.setText(str(data[0]))
            self.ui.placeholder_register_date.setText(register)
            self.ui.placeholder_p_bloodType.setText(data[5] or "")
            self.ui.placeholder_philhealth_num.setText(str(data[6]))
            self.ui.placeholder_age.setText(
                str(int(age_result[0])) if age_result else "N/A")

            self._build_patient_avatar(full_name)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load patient:\n{e}")

    def _build_patient_avatar(self, full_name: str):
        from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont

        # Generate initials
        parts    = full_name.strip().split()
        initials = ""
        if len(parts) == 1:
            initials = parts[0][0].upper()
        elif len(parts) >= 2:
            initials = parts[0][0].upper() + parts[-1][0].upper()

        # Create avatar label inside frame_5
        avatar = QLabel(initials, parent=self.ui.frame_5)
        avatar.setGeometry(0, 0, self.ui.frame_5.width(), self.ui.frame_5.height())
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            "background-color: rgb(192, 116, 182);"
            "color: white;"
            "font-size: 32px;"
            "font-weight: bold;"
            "border-radius: 6px;"
            "border: none;"
        )
        avatar.show()

    def load_appointments(self):
        """
        List only Completed appointments for this patient.
        These are the same records shown in CompletedAppointmentsScreen,
        filtered to the specific patient — enforcing the rule that a patient
        must exist in patient_profile before any appointment can be saved
        (FK constraint: appointment.patient_id → patient_profile.patient_id).
        """
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.appointment_id,
                       a.appointment_date,
                       a.appointment_time,
                       a.appointment_type
                FROM appointment a
                WHERE a.patient_id = %s
                  AND a.status = 'Completed'
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            """, (self.patient_id,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            tbl = self.ui.appointments_table
            tbl.setRowCount(0)
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            tbl.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

            for row_data in rows:
                appointment_id = row_data[0]
                date      = row_data[1].strftime("%B %d, %Y") if row_data[1] else ""
                time      = str(row_data[2])[:5] if row_data[2] else ""
                appt_type = row_data[3] or ""

                row_index = tbl.rowCount()
                tbl.insertRow(row_index)

                # Store appointment_id in the date cell for on_row_clicked
                date_item = QTableWidgetItem(date)
                date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                date_item.setData(Qt.ItemDataRole.UserRole, appointment_id)
                tbl.setItem(row_index, 0, date_item)

                for col, val in enumerate([time, appt_type], start=1):
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
                tbl.setCellWidget(row_index, 3, view_btn)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load appointments:\n{e}")

    def on_row_clicked(self, row, col):
        item = self.ui.appointments_table.item(row, 0)
        if item:
            appointment_id = item.data(Qt.ItemDataRole.UserRole)
            self.load_details(appointment_id)

    # ─────────────────────────────────────────────────────────────────────────
    # OUTER NAVIGATION
    # ─────────────────────────────────────────────────────────────────────────
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
        from screens.appointments_screen import AppointmentsScreen
        self.new_window = AppointmentsScreen()
        self.new_window.showMaximized()
        self.close()

    def logout(self):
        from screens.login_screen import LoginScreen
        self.new_window = LoginScreen()
        self.new_window.showMaximized()
        self.close()

    # ─────────────────────────────────────────────────────────────────────────
    # INNER (PATIENT RECORD TAB) NAVIGATION
    # ─────────────────────────────────────────────────────────────────────────
    def go_to_patient_profile(self):
        from screens.patient_profile_screen import PatientProfileScreen
        self.new_window = PatientProfileScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_past_pregnancy(self):
        from screens.past_pregnancy_screen import pastPregnancyScreen
        self.new_window = pastPregnancyScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_prescription(self):
        from screens.prescription_screen import PrescriptionScreen
        self.new_window = PrescriptionScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_medical_history(self):
        from screens.medical_history_screen import MedicalHistoryScreen
        self.new_window = MedicalHistoryScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_family_planning(self):
        from screens.family_planning_screen import FamilyPlanningScreen
        self.new_window = FamilyPlanningScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_appointment_tab(self):
        pass  # already here