from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTableWidgetItem, QPushButton, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
from screens.completed_appointments_ui import Ui_MainWindow
from database import get_connection


class CompletedAppointmentsScreen(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Completed Appointments")
        self.current_appointment_id = None
        self.current_patient_id = None  # ✅ add this

        self._hide_details()
        self.setup_navigation()
        self.load_appointments()

        self.ui.pushButton_6.clicked.connect(self.open_new_appointment)
        self.ui.pushButton_7.clicked.connect(self.go_back)
        self.ui.pushButton_8.clicked.connect(self.schedule_followup)
        self.ui.pushButton_9.clicked.connect(self.view_full_record)

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
                       a.patient_id                          -- ✅ grab patient_id
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

            self.current_patient_id = data[6]  # ✅ store it

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
        dialog = AddAppointmentDialog(
            appointment_type="Follow-up",
            parent=self
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_appointments()

    def view_full_record(self):
        if not self.current_appointment_id:
            QMessageBox.warning(self, "No Selection",
                                "Please select an appointment first.")
            return

        # ✅ Go directly to patient profile — no DB call needed, we already have the id
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