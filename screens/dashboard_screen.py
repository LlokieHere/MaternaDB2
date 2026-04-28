from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from screens.dashboard_ui import Ui_Dashboard
from database import get_connection


class DashboardScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dashboard()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB - Dashboard")

        self.ui.pushButton.clicked.connect(self.go_to_dashboard)
        self.ui.pushButton_2.clicked.connect(self.go_to_patient_records)
        self.ui.pushButton_3.clicked.connect(self.go_to_prenatal_care)
        self.ui.pushButton_4.clicked.connect(self.go_to_appointments)
        self.ui.pushButton_5.clicked.connect(self.logout)

        self.load_stats()
        self.load_recent_patients()

    def showEvent(self, event):
        super().showEvent(event)
        self.reposition_elements()
        self.load_stats()
        self.load_recent_patients()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.reposition_elements()

    def reposition_elements(self):
        w = self.width()
        h = self.height()

        self.ui.frame_2.setGeometry(0, 0, w, 61)
        self.ui.frame.setGeometry(0, 61, 231, h - 61)

        main_x = 231
        main_w = w - 231
        main_h = h - 61
        self.ui.frame_3.setGeometry(main_x, 61, main_w, main_h)
        self.ui.widget.setGeometry(40, 100, main_w - 80, 101)

        table_w = int(main_w * 0.62)
        self.ui.patient_table.setGeometry(50, 260, table_w, main_h - 320)
        self.ui.label_3.setGeometry(50, 230, 131, 21)

        appt_x = table_w + 70
        appt_w = main_w - table_w - 90
        self.ui.today_appointment.setGeometry(appt_x, 260, appt_w, main_h - 320)
        self.ui.Todays_appointment_TA.setGeometry(appt_x, 230, appt_w, 21)
        self.ui.content_container_TA.setGeometry(appt_x + 15, 280, appt_w - 30, 81)

    def load_stats(self):
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM patients")
                self.ui.total_patient_label_2.setText(str(cursor.fetchone()[0]))
                cursor.execute("SELECT COUNT(*) FROM appointments")
                self.ui.total_patient_label_3.setText(str(cursor.fetchone()[0]))
                cursor.execute("SELECT COUNT(*) FROM patients WHERE type = 'Maternal'")
                self.ui.total_patient_label_4.setText(str(cursor.fetchone()[0]))
                cursor.execute("SELECT COUNT(*) FROM patients WHERE status = 'Delivered'")
                self.ui.total_patient_label_5.setText(str(cursor.fetchone()[0]))
                conn.close()
            except Exception as e:
                print(f"Error loading stats: {e}")
                conn.close()

    def load_recent_patients(self):
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name, type, registered, status FROM patients ORDER BY registered DESC LIMIT 5"
                )
                patients = cursor.fetchall()
                conn.close()
                self.ui.patient_table.setRowCount(len(patients))
                for row, patient in enumerate(patients):
                    for col, data in enumerate(patient):
                        self.ui.patient_table.setItem(row, col, QTableWidgetItem(str(data)))
            except Exception as e:
                print(f"Error loading patients: {e}")
                conn.close()

    def go_to_dashboard(self):
        self.load_stats()
        self.load_recent_patients()

    def go_to_patient_records(self):
        print("Go to Patient Records")

    def go_to_prenatal_care(self):
        print("Go to Prenatal Care")

    def go_to_appointments(self):
        print("Go to Appointments")

    def logout(self):
        from screens.login_screen import LoginScreen
        self.login_window = LoginScreen()
        self.login_window.showMaximized()
        self.login_window.show()
        self.close()