from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTableWidgetItem, QPushButton, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
from screens.family_planning_ui import Ui_MainWindow
from database import get_connection


class FamilyPlanningScreen(QMainWindow):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.patient_id = patient_id
        self.current_planning_id = None
        self.setWindowTitle("Family Planning")

        # Hide unused fields
        self.ui.prescribed_by_value.setVisible(False)
        self.ui.next_followup_value.setVisible(False)
        self.ui.label_9.setVisible(False)
        self.ui.label_10.setVisible(False)

        self.setup_navigation()
        self.load_patient_data()
        self.load_family_planning()

        self.ui.add_plan_btn.clicked.connect(self.open_add_dialog)
        self.ui.edit_plan_btn.clicked.connect(self.open_edit_dialog)
        self.ui.discontinue_btn.clicked.connect(self.discontinue_plan)
        self.ui.family_planning_table.cellClicked.connect(self.on_row_selected)

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

        btn_y = tab_y + 50
        self.ui.add_plan_btn.setGeometry(inner_w - 120, btn_y, 120, 31)

        panels_y = btn_y + 41
        panels_h = content_h - panels_y - pad
        left_w = int(inner_w * 0.45)
        right_w = inner_w - left_w - 20

        self.ui.left.setGeometry(pad, panels_y, left_w, panels_h)
        self.ui.family_planning_table.setGeometry(0, 0, left_w, panels_h)
        self.ui.family_planning_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        self.ui.right_details.setGeometry(pad + left_w + 20, panels_y, right_w, panels_h)
        self.ui.label_4.setGeometry(15, 10, right_w - 20, 21)
        self.ui.formWidget.setGeometry(15, 40, right_w - 20, 251)
        self.ui.side_effects_label.setGeometry(15, 300, right_w - 20, 18)
        self.ui.side_effects_value.setGeometry(15, 320, right_w - 20, 50)
        self.ui.discontinue_btn.setGeometry(right_w - 260, panels_h - 50, 120, 31)
        self.ui.edit_plan_btn.setGeometry(right_w - 130, panels_h - 50, 120, 31)

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
            self.ui.pushButton_11.clicked.connect(self.go_to_appointment)
        except Exception as e:
            print("Navigation error:", e)

    def load_patient_data(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT patient_id, first_name, middle_name, last_name,
                       date_registered, blood_type, philhealth_no,
                       EXTRACT(YEAR FROM AGE(date_of_birth)) AS age
                FROM patient_profile WHERE patient_id = %s
            """, (self.patient_id,))
            data = cursor.fetchone()
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
            self.ui.placeholder_age.setText(str(int(data[7])) if data[7] else "N/A")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load patient:\n{e}")

    def clear_right_panel(self):
        self.ui.method_value.setText("")
        self.ui.start_date_value.setText("")
        self.ui.end_date_value.setText("")
        self.ui.status_value.setText("")
        self.ui.side_effects_value.setText("")

    def load_family_planning(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT planning_id, method, status
                FROM family_planning
                WHERE patient_id = %s
                ORDER BY start_date DESC
            """, (self.patient_id,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            tbl = self.ui.family_planning_table
            tbl.setRowCount(0)
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            tbl.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

            for row_data in rows:
                planning_id = row_data[0]
                method      = row_data[1] or ""
                status      = row_data[2] or ""

                row_index = tbl.rowCount()
                tbl.insertRow(row_index)

                method_item = QTableWidgetItem(method)
                method_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                method_item.setData(Qt.ItemDataRole.UserRole, planning_id)
                tbl.setItem(row_index, 0, method_item)

                status_item = QTableWidgetItem(status)
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tbl.setItem(row_index, 1, status_item)

                def make_handler(pid):
                    def handler():
                        self.load_plan_details(pid)
                    return handler

                view_btn = QPushButton("View")
                view_btn.clicked.connect(make_handler(planning_id))
                tbl.setCellWidget(row_index, 2, view_btn)

            # Always start with a blank right panel
            self.clear_right_panel()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load family planning:\n{e}")

    def on_row_selected(self, row, col):
        item = self.ui.family_planning_table.item(row, 0)
        if item:
            planning_id = item.data(Qt.ItemDataRole.UserRole)
            self.load_plan_details(planning_id)

    def load_plan_details(self, planning_id):
        self.current_planning_id = planning_id
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT method, start_date, end_date, status, remarks
                FROM family_planning
                WHERE planning_id = %s
            """, (planning_id,))
            data = cursor.fetchone()
            cursor.close()
            conn.close()

            if not data:
                return

            self.ui.method_value.setText(data[0] or "")
            self.ui.start_date_value.setText(
                data[1].strftime("%B %d, %Y") if data[1] else "")
            self.ui.end_date_value.setText(
                data[2].strftime("%B %d, %Y") if data[2] else "Ongoing")
            self.ui.status_value.setText(data[3] or "")
            self.ui.side_effects_value.setText(data[4] or "")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load plan details:\n{e}")

    def open_add_dialog(self):
        from Dialog.add_family_planning_dialog import AddFamilyPlanningDialog
        dialog = AddFamilyPlanningDialog(self.patient_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_family_planning()

    def open_edit_dialog(self):
        if not self.current_planning_id:
            QMessageBox.warning(self, "No Selection", "Please select a plan to edit.")
            return
        from Dialog.add_family_planning_dialog import AddFamilyPlanningDialog
        dialog = AddFamilyPlanningDialog(
            self.patient_id,
            planning_id=self.current_planning_id,
            parent=self
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_family_planning()
            self.load_plan_details(self.current_planning_id)

    def discontinue_plan(self):
        if not self.current_planning_id:
            QMessageBox.warning(self, "No Selection", "Please select a plan to discontinue.")
            return

        confirm = QMessageBox.question(
            self, "Discontinue Plan",
            "Are you sure you want to mark this plan as Resolved?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE family_planning SET status = 'Resolved'
                WHERE planning_id = %s
            """, (self.current_planning_id,))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Plan marked as Resolved.")
            self.load_family_planning()
            self.load_plan_details(self.current_planning_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to discontinue:\n{e}")

    # ── Outer navigation ──────────────────────────────────────
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

    # ── Inner navigation ──────────────────────────────────────
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
        pass

    def go_to_appointment(self):
        from screens.appointment_patient_record_screen import PatientAppointmentScreen
        self.new_window = PatientAppointmentScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()