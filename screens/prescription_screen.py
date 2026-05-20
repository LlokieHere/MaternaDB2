from PyQt6.QtWidgets import (
    QLabel, QMainWindow, QMessageBox, QTableWidgetItem, QPushButton, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
from Dialog.add_prescription_dialog import AddPrescriptionDialog
from screens.prescription_ui import Ui_MainWindow
from database import get_connection
import user_profile.session as session


class PrescriptionScreen(QMainWindow):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.patient_id = patient_id
        self._selected_date = None
        self._selected_staff_id = None
        self._selected_prescription_id = None
        self.setWindowTitle("Prescriptions")

        self.setup_navigation()
        self.load_patient_data()
        self.load_prescriptions()

        self.ui.ad_prescription.clicked.connect(self.open_add_dialog)
        self.ui.edit_prescription.clicked.connect(self.open_edit_dialog)
        self.ui.left_prescription_date_and_purpose.cellClicked.connect(
            self.on_prescription_selected)

        # ── Delete button (created in code) ───────────────────────────────────
        self.delete_btn = QPushButton("Delete Prescription", parent=self.ui.frame_3)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                border-radius: 12px;
                background-color: rgb(220, 80, 80);
                color: white;
                border: none;
                font-size: 12px;
            }
            QPushButton:hover { background-color: rgb(180, 50, 50); }
        """)
        self.delete_btn.clicked.connect(self.open_delete_dialog)
        self.delete_btn.show()

        self.load_logo()
        self._build_sidebar_profile()

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

    # ── Sidebar profile ───────────────────────────────────────────────────────
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

        for w in (self.profile_avatar, self.profile_name_lbl,
                  self.profile_role_lbl, self.profile_divider):
            w.raise_()
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

    # ── Layout helpers ────────────────────────────────────────────────────────
    def layout_sidebar(self):
        h = self.height()
        sidebar_w = 230

        self.profile_avatar.setGeometry(73, 20, 64, 64)
        self.profile_name_lbl.setGeometry(20, 95, 190, 30)
        self.profile_role_lbl.setGeometry(20, 120, 190, 20)
        self.profile_divider.setGeometry(15, 150, 200, 1)

        btn_top = 170
        btn_h   = 41
        btn_gap = 8
        btn_x   = 10
        btn_w   = sidebar_w - 20

        for i, btn in enumerate([
            self.ui.pushButton, self.ui.pushButton_2,
            self.ui.pushButton_3, self.ui.pushButton_4,
        ]):
            btn.setGeometry(btn_x, btn_top + i * (btn_h + btn_gap), btn_w, btn_h)

        self.ui.pushButton_5.setGeometry(btn_x, h - 120, btn_w, btn_h)

    def _build_patient_avatar(self, full_name: str):
        parts    = full_name.strip().split()
        initials = ""
        if len(parts) == 1:
            initials = parts[0][0].upper()
        elif len(parts) >= 2:
            initials = parts[0][0].upper() + parts[-1][0].upper()

        avatar = QLabel(initials, parent=self.ui.frame_5)
        avatar.setGeometry(0, 0, self.ui.frame_5.width(), self.ui.frame_5.height())
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            "background-color: rgb(192, 116, 182);"
            "color: white; font-size: 32px; font-weight: bold;"
            "border-radius: 6px; border: none;"
        )
        avatar.show()

    def layout_nav(self):
        w = self.width()
        h = self.height()

        sidebar_w = 230
        navbar_h  = 60

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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.width()
        h = self.height()

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

        pad     = 40
        inner_w = content_w - (pad * 2)

        self.ui.label.setGeometry(pad, 20, inner_w // 2, 61)

        header_h = 141
        self.ui.frame_4.setGeometry(pad, 80, inner_w, header_h)
        self.ui.frame_5.setGeometry(20, 20, 111, 91)
        self.ui.patient_name.setGeometry(170, 15, inner_w - 320, 30)
        self.ui.layoutWidget.setGeometry(170, 50, inner_w - 320, 80)

        tab_y = 80 + header_h + 20
        self.ui.layoutWidget1.setGeometry(pad, tab_y, inner_w, 40)

        # ── 3 action buttons in a row ─────────────────────────────────────────
        btn_y = tab_y + 50
        self.ui.edit_prescription.setGeometry(inner_w - 390, btn_y, 130, 31)
        self.ui.ad_prescription.setGeometry(inner_w - 250, btn_y, 130, 31)
        self.delete_btn.setGeometry(inner_w - 110, btn_y, 150, 31)

        panels_y = btn_y + 41
        panels_h = content_h - panels_y - pad
        left_w   = int(inner_w * 0.45)
        right_w  = inner_w - left_w - 20

        self.ui.left.setGeometry(pad, panels_y, left_w, panels_h)
        self.ui.left_prescription_date_and_purpose.setGeometry(0, 0, left_w, panels_h)
        self.ui.left_prescription_date_and_purpose.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        self.ui.right_details_prescription.setGeometry(
            pad + left_w + 20, panels_y, right_w, panels_h)
        self.ui.layoutWidget2.setGeometry(10, 10, right_w - 20, 44)
        self.ui.patient_table_3.setGeometry(10, 60, right_w - 20, panels_h - 110)
        self.ui.patient_table_3.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.ui.notes_label.setGeometry(10, panels_h - 45, 50, 18)
        self.ui.notes_placeholder.setGeometry(65, panels_h - 45, right_w - 75, 18)

        self._reposition_sidebar_profile()
        self.layout_sidebar()
        self.layout_nav()

    # ── Navigation setup ──────────────────────────────────────────────────────
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
            self.ui.pushButton_11.clicked.connect(self.go_to_appointments_tab)
        except Exception as e:
            print("Navigation error:", e)

    # ── Patient header ────────────────────────────────────────────────────────
    def load_patient_data(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT patient_id, first_name, middle_name, last_name,
                       date_registered, blood_type, philhealth_no
                FROM patient_profile
                WHERE patient_id = %s
            """, (self.patient_id,))
            data = cursor.fetchone()

            cursor.execute("""
                SELECT EXTRACT(YEAR FROM AGE(date_of_birth))
                FROM patient_profile
                WHERE patient_id = %s
            """, (self.patient_id,))
            age_result = cursor.fetchone()
            cursor.close()

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
                str(int(age_result[0])) if age_result and age_result[0] else "—"
            )
            self._build_patient_avatar(full_name)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load patient:\n{e}")
        finally:
            conn.close()

    # ── Left table ────────────────────────────────────────────────────────────
    def load_prescriptions(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT
                    p.prescription_date,
                    s.staff_id,
                    s.first_name || ' ' || s.last_name AS staff_name
                FROM prescription p
                JOIN staff s ON p.prescribed_by = s.staff_id
                WHERE p.patient_id = %s
                ORDER BY p.prescription_date DESC
            """, (self.patient_id,))
            rows = cursor.fetchall()
            cursor.close()

            tbl = self.ui.left_prescription_date_and_purpose
            tbl.setRowCount(0)
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            tbl.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

            for raw_date, staff_id, staff_name in rows:
                presc_date = raw_date.strftime("%B %d, %Y") if raw_date else ""
                row_index  = tbl.rowCount()
                tbl.insertRow(row_index)

                date_item = QTableWidgetItem(presc_date)
                date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                date_item.setData(Qt.ItemDataRole.UserRole, (raw_date, staff_id))
                tbl.setItem(row_index, 0, date_item)

                staff_item = QTableWidgetItem(staff_name)
                staff_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tbl.setItem(row_index, 1, staff_item)

                view_btn = QPushButton("View")
                view_btn.clicked.connect(
                    (lambda d, sid: lambda: self.load_prescription_medicines(d, sid))(raw_date, staff_id)
                )
                tbl.setCellWidget(row_index, 2, view_btn)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load prescriptions:\n{e}")
        finally:
            conn.close()

    def on_prescription_selected(self, row, col):
        item = self.ui.left_prescription_date_and_purpose.item(row, 0)
        if item:
            raw_date, staff_id = item.data(Qt.ItemDataRole.UserRole)
            self.load_prescription_medicines(raw_date, staff_id)

    # ── Right panel ───────────────────────────────────────────────────────────
    def load_prescription_medicines(self, presc_date, staff_id):
        self._selected_date = presc_date
        self._selected_staff_id = staff_id
        self._selected_prescription_id = None

        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    p.prescription_id,
                    s.first_name || ' ' || s.last_name AS prescriber,
                    p.prescription_date,
                    p.medicine_name,
                    p.dosage,
                    p.frequency,
                    p.duration,
                    p.route,
                    p.timing,
                    p.notes
                FROM prescription p
                JOIN staff s ON p.prescribed_by = s.staff_id
                WHERE p.patient_id       = %s
                  AND p.prescription_date = %s
                  AND p.prescribed_by     = %s
                ORDER BY p.prescription_id
            """, (self.patient_id, presc_date, staff_id))

            rows = cursor.fetchall()
            cursor.close()

            if not rows:
                return

            self.ui.prescribed_by_placeholder.setText(rows[0][1])
            date_str = rows[0][2].strftime("%B %d, %Y") if rows[0][2] else ""
            self.ui.date_prescription_date_placeholder.setText(date_str)

            notes = next((r[9] for r in rows if r[9]), "")
            self.ui.notes_placeholder.setText(notes)

            tbl = self.ui.patient_table_3
            tbl.setRowCount(0)
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            tbl.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

            for med in rows:
                row_index = tbl.rowCount()
                tbl.insertRow(row_index)
                for col, val in enumerate(med[3:9]):
                    item = QTableWidgetItem(str(val) if val else "")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if col == 0:
                        item.setData(Qt.ItemDataRole.UserRole, med[0])
                    tbl.setItem(row_index, col, item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load medicines:\n{e}")
        finally:
            conn.close()

        tbl.cellClicked.connect(self._on_medicine_row_clicked)

    def _on_medicine_row_clicked(self, row, col):
        item = self.ui.patient_table_3.item(row, 0)
        if item:
            self._selected_prescription_id = item.data(Qt.ItemDataRole.UserRole)

    # ── Add ───────────────────────────────────────────────────────────────────
    def open_add_dialog(self):
        dialog = AddPrescriptionDialog(self.patient_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_prescriptions()

    # ── Edit ──────────────────────────────────────────────────────────────────
    def open_edit_dialog(self):
        if self._selected_prescription_id is None:
            QMessageBox.warning(self, "No Selection",
                "Please click a medicine row in the right panel to select it first.")
            return

        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT prescription_id, patient_id, prescribed_by,
                       medicine_name, dosage, frequency, duration,
                       route, timing, prescription_date, notes
                FROM prescription
                WHERE prescription_id = %s
            """, (self._selected_prescription_id,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        if not row:
            return

        existing = {
            "prescription_id":   row[0],
            "patient_id":        row[1],
            "staff_id":          row[2],
            "medicine_name":     row[3],
            "dosage":            row[4],
            "frequency":         row[5],
            "duration":          row[6],
            "route":             row[7],
            "timing":            row[8],
            "prescription_date": row[9],
            "notes":             row[10],
        }

        dialog = AddPrescriptionDialog(self.patient_id, existing=existing, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            d = dialog.result_data
            conn = get_connection()
            if not conn:
                return
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE prescription SET
                        prescribed_by     = %s,
                        medicine_name     = %s,
                        dosage            = %s,
                        frequency         = %s,
                        duration          = %s,
                        route             = %s,
                        timing            = %s,
                        prescription_date = %s,
                        notes             = %s
                    WHERE prescription_id = %s
                """, (
                    d["staff_id"], d["medicine_name"], d["dosage"],
                    d["frequency"], d["duration"], d["route"], d["timing"],
                    d["prescription_date"], d["notes"],
                    self._selected_prescription_id
                ))
                conn.commit()
                conn.close()
                self.load_prescriptions()
                if self._selected_date and self._selected_staff_id:
                    self.load_prescription_medicines(
                        self._selected_date, self._selected_staff_id)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                if conn:
                    conn.close()

    # ── Delete ────────────────────────────────────────────────────────────────
    def open_delete_dialog(self):
        if self._selected_prescription_id is None:
            QMessageBox.warning(self, "No Selection",
                "Please click a medicine row in the right panel to select it first.")
            return

        # fetch medicine name for the confirm message
        medicine_name = ""
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT medicine_name FROM prescription WHERE prescription_id = %s",
                    (self._selected_prescription_id,)
                )
                row = cursor.fetchone()
                medicine_name = row[0] if row else ""
                cursor.close()
                conn.close()
            except Exception:
                if conn:
                    conn.close()

        confirm = QMessageBox.question(
            self, "Delete Prescription",
            f"Delete '{medicine_name}'? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM prescription WHERE prescription_id = %s",
                (self._selected_prescription_id,)
            )
            conn.commit()
            cursor.close()
            conn.close()

            self._selected_prescription_id = None

            # clear right panel
            self.ui.patient_table_3.setRowCount(0)
            self.ui.prescribed_by_placeholder.setText("")
            self.ui.date_prescription_date_placeholder.setText("")
            self.ui.notes_placeholder.setText("")

            self.load_prescriptions()

            # reload right panel if other medicines still exist in this group
            if self._selected_date and self._selected_staff_id:
                self.load_prescription_medicines(
                    self._selected_date, self._selected_staff_id)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete:\n{e}")
            if conn:
                conn.close()

    # ── Outer navigation ──────────────────────────────────────────────────────
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

    # ── Inner navigation ──────────────────────────────────────────────────────
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
        pass

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

    def go_to_appointments_tab(self):
        from screens.appointment_patient_record_screen import PatientAppointmentScreen
        self.new_window = PatientAppointmentScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()