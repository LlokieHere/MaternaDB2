from PyQt6.QtWidgets import QMainWindow, QMessageBox
from screens.patient_profile_ui import Ui_MainWindow
from Dialog.add_patient_dialog import EditPatientDialog
from PyQt6.QtWidgets import QDialog
from database import get_connection


class PatientProfileScreen(QMainWindow):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.patient_id = patient_id

        self.setWindowTitle("Patient Profile")

        # Inner Navigation
        self.ui.pushButton_7.clicked.connect(self.go_to_pastPregnancy)
        self.ui.pushButton_8.clicked.connect(self.go_to_prescription)
        self.ui.pushButton_9.clicked.connect(self.go_to_medicalHistory)
        self.ui.pushButton_10.clicked.connect(self.go_to_family_planning)
        self.ui.pushButton_11.clicked.connect(self.go_to_appointment)

        self.setup_navigation()
        self.load_patient_data()

    # =====================================================
    # 🔁 NAVIGATION
    # =====================================================
    def setup_navigation(self):
        self.ui.pushButton.clicked.connect(self.got_to_dashboard)
        self.ui.pushButton_2.clicked.connect(self.go_to_patient_records)
        self.ui.pushButton_3.clicked.connect(self.go_to_prenatal_care)
        self.ui.pushButton_4.clicked.connect(self.go_to_appointments)
        self.ui.pushButton_5.clicked.connect(self.logout)

        self.ui.remove_patient_btn.clicked.connect(self.open_edit_dialog)


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

            # calculate age
            query = """
            SELECT EXTRACT(YEAR FROM AGE(date_of_birth)) AS age
            FROM patient_profile
            WHERE patient_id = %s;
            """

            cursor.execute(query, (self.patient_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                age = result[0]  # extract value from tuple
                self.ui.age_placeholder.setText(str(age))
            else:
                self.ui.age_placeholder.setText("N/A")
            conn.close()

            self.ui.first_name_placeholder.setText(data[1])
            self.ui.middle_name_placeholder.setText(data[2] or "")
            self.ui.last_name_placeholder.setText(data[3])

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load profile:\n{e}")

    def open_edit_dialog(self):
        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            # ───────── PROFILE ─────────
            cursor.execute("""
                SELECT first_name, middle_name, last_name, suffix,
                       date_of_birth, civil_status, contact_number,
                       philhealth_no, occupation, religion,
                       nationality, blood_type
                FROM patient_profile
                WHERE patient_id = %s
            """, (self.patient_id,))
            profile = cursor.fetchone()

            # ───────── ADDRESS ─────────
            cursor.execute("""
                SELECT street, barangay, city, province
                FROM patient_address
                WHERE patient_id = %s
            """, (self.patient_id,))
            address = cursor.fetchone()

            # ───────── EMERGENCY ─────────
            cursor.execute("""
                SELECT contact_first_name, contact_last_name, contact_middle_name,
                        contact_number, relationship
                FROM emergency_contact
                WHERE patient_id = %s
            """, (self.patient_id,))
            emergency = cursor.fetchone()

            cursor.close()
            conn.close()

            if not profile:
                return

            patient_data = {
                # profile
                "first_name": profile[0],
                "middle_name": profile[1],
                "last_name": profile[2],
                "suffix": profile[3],
                "date_of_birth": profile[4],
                "civil_status": profile[5],
                "contact_number": profile[6],
                "philhealth_no": profile[7],
                "occupation": profile[8],
                "religion": profile[9],
                "nationality": profile[10],
                "blood_type": profile[11],

                # address
                "street": address[0] if address else "",
                "barangay": address[1] if address else "",
                "city": address[2] if address else "",
                "province": address[3] if address else "",

                # emergency
                "ec_first_name": emergency[0] if emergency else "",
                "ec_last_name": emergency[1] if emergency else "",
                "ec_middle_name": emergency[2] if emergency else "",
                "ec_contact": emergency[3] if emergency else "",
                "ec_relationship": emergency[4] if emergency else "",
            }

            self.dialog = EditPatientDialog(
                mode="edit",
                patient_data=patient_data,
                patient_id=self.patient_id,
                parent=self
            )

            if self.dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_patient_data()

        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Could not load patient data:\n{e}")

    #navigation

    def go_to_patient_records(self):
        from screens.patient_records_screen import PatientRecordScreen
        self.window = PatientRecordScreen()
        self.window.showMaximized()
        self.close()

    def go_to_prenatal_care(self):
        from screens.prenatal_dashboard_screen import PrenatalDashboardScreen
        self.window = PrenatalDashboardScreen()
        self.window.showMaximized()
        self.close()

    def got_to_dashboard(self):
        from screens.dashboard_screen import DashboardScreen
        self.window = DashboardScreen()
        self.window.showMaximized()
        self.close()

    def go_to_appointments(self):
        print("Appointments screen not connected yet")

    def logout(self):
        from screens.login_screen import LoginScreen
        self.window = LoginScreen()
        self.window.showMaximized()
        self.close()

    def go_to_pastPregnancy(self):
        from screens.past_pregnancy_screen import pastPregnancyScreen
        self.new_window = pastPregnancyScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_medicalHistory(self):
        print("medical history screen clicked!")

    def go_to_prescription(self):
        print("Prescription screen clicked!")

    def go_to_family_planning(self):
        print("Family Planning screen clicked!")

    def go_to_appointment(self):
        print("Appointment screen clicked!")