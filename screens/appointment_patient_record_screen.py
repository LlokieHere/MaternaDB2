from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTableWidgetItem, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
from screens.appointment_patient_record_ui import Ui_MainWindow
from database import get_connection


class PatientAppointmentScreen(QMainWindow):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.patient_id = patient_id
        self.setWindowTitle("Appointment History")

        self.clear_details()
        self.setup_navigation()
        self.load_patient_data()
        self.load_appointments()

        self.ui.appointments_table.cellClicked.connect(self.on_row_clicked)
        self.load_logo()


    def load_logo(self):
        from PyQt6.QtGui import QPixmap
        from PyQt6.QtCore import Qt
        pixmap = QPixmap("Asset/MaternaDB_logo.png")
        if not pixmap.isNull():
            self.ui.label_3.setText("")
            self.ui.label_3.setStyleSheet("")  # ✅ clear the stylesheet
            self.ui.label_3.setPixmap(
                pixmap.scaled(
                    40, 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
            self.ui.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        self.ui.right_details.setGeometry(pad + left_w + 20, panels_y, right_w, panels_h)
        self.ui.label_4.setGeometry(15, 10, right_w - 20, 21)
        self.ui.formWidget.setGeometry(15, 40, right_w - 20, 220)
        self.ui.purpose_label.setGeometry(15, 270, right_w - 20, 18)
        self.ui.purpose_value.setGeometry(15, 292, right_w - 20, 60)

    def clear_details(self):
        self.ui.date_value.setText("")
        self.ui.time_value.setText("")
        self.ui.type_value.setText("")
        self.ui.doctor_value.setText("")
        self.ui.duration_value.setText("")
        self.ui.purpose_value.setText("")

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

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load patient:\n{e}")

    def load_appointments(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.appointment_id,
                       a.appointment_date,
                       a.appointment_time,
                       a.appointment_type,
                       s.first_name || ' ' || s.last_name AS staff_name,
                       a.remarks
                FROM appointment a
                JOIN staff s ON a.staff_id = s.staff_id
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
                date           = row_data[1].strftime("%B %d, %Y") if row_data[1] else ""
                time           = str(row_data[2])[:5] if row_data[2] else ""
                appt_type      = row_data[3] or ""

                row_index = tbl.rowCount()
                tbl.insertRow(row_index)

                # Store appointment_id in the date item for later retrieval
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

    def load_details(self, appointment_id):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.appointment_date,
                       a.appointment_time,
                       a.appointment_type,
                       s.first_name || ' ' || s.last_name,
                       a.remarks
                FROM appointment a
                JOIN staff s ON a.staff_id = s.staff_id
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

            date    = data[0].strftime("%B %d, %Y") if data[0] else ""
            time    = str(data[1])[:5] if data[1] else ""
            remarks = data[4] or ""

            self.ui.date_value.setText(date)
            self.ui.time_value.setText(time)
            self.ui.type_value.setText(data[2] or "")
            self.ui.doctor_value.setText(data[3] or "")
            self.ui.duration_value.setText(remarks)
            self.ui.purpose_value.setText(
                ", ".join(purposes) if purposes else "—")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load details:\n{e}")

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
        from screens.family_planning_screen import FamilyPlanningScreen
        self.new_window = FamilyPlanningScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_appointment_tab(self):
        pass  # already here