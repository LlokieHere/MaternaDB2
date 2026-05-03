from PyQt6.QtWidgets import QMainWindow, QMessageBox
from screens.patient_profile_ui import Ui_MainWindow
from database import get_connection


class PatientProfileScreen(QMainWindow):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.patient_id = patient_id
        self.parent_window = parent  # reference to go back

        self.setWindowTitle("Patient Profile")

        self.setup_navigation()
        self.load_patient_data()

    # =====================================================
    # 🔁 NAVIGATION
    # =====================================================
    def setup_navigation(self):
        # 👉 Replace 'back_btn' with your actual button name in UI
        # Example: pushButton_2 (your sidebar button)
        try:
            self.ui.pushButton_2.clicked.connect(self.go_back)
        except:
            pass  # prevents crash if button name is different

    def go_back(self):
        if self.parent_window:
            self.parent_window.show()
        else:
            # fallback if no parent was passed
            from screens.patient_records_screen import PatientRecordScreen
            self.records = PatientRecordScreen()
            self.records.show()

        self.close()

    # =====================================================
    # 📥 LOAD DATA
    # =====================================================
    def load_patient_data(self):
        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "DB Error", "Cannot connect to database")
            return

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT patient_id,
                       first_name,
                       middle_name,
                       last_name,
                       date_of_birth,
                       contact_number
                FROM patient_profile
                WHERE patient_id = %s
            """, (self.patient_id,))

            data = cursor.fetchone()
            conn.close()

            if not data:
                QMessageBox.warning(self, "Not Found", "Patient not found")
                return

            # ✅ Clean full name (no extra spaces)
            full_name = " ".join(filter(None, [data[1], data[2], data[3]]))

            # ✅ Safe date formatting
            dob = data[4].strftime("%B %d, %Y") if data[4] else ""

            # =====================================================
            # 🎯 SET UI VALUES
            # =====================================================
            self.ui.patient_name.setText(full_name)
            self.ui.placeholder_p_ID.setText(str(data[0]))
            self.ui.bday_placeholder.setText(dob)
            self.ui.contact_number_placeholder.setText(str(data[5]))

            self.ui.first_name_placeholder.setText(data[1])
            self.ui.middle_name_placeholder.setText(data[2] or "")
            self.ui.last_name_placeholder.setText(data[3])

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load profile:\n{e}")