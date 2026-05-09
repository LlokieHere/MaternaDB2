from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTableWidgetItem, QPushButton, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
from screens.appointments_main_ui import Ui_MainWindow
from database import get_connection


class AppointmentsScreen(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Appointments")

        self.setup_navigation()
        self.load_appointments()

        self.ui.pushButton_6.clicked.connect(self.open_new_appointment)
        self.ui.pushButton_7.clicked.connect(self.go_to_completed)

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
                appt_type      = row_data[4] or ""
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

    # ── Navigation ────────────────────────────────────────────
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
        pass

    def logout(self):
        from screens.login_screen import LoginScreen
        self.new_window = LoginScreen()
        self.new_window.showMaximized()
        self.close()