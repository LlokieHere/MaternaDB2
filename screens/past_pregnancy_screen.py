from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTableWidgetItem, QWidget,
    QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from screens.past_pregnancy_ui import Ui_MainWindow
from database import get_connection


class pastPregnancyScreen(QMainWindow):
    def __init__(self, patient_id, parent=None):
        super().__init__()
        self.new_window = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.patient_id = patient_id
        self.setWindowTitle("Past Pregnancy")

        # ── Load everything ───────────────────────────────────────────────────
        self.setup_navigation()
        self.load_patient_data()
        self.load_past_pregnancy_data()


    def setup_navigation(self):
        try:
            # Navigation
            self.ui.pushButton.clicked.connect(self.go_to_dashboard)
            self.ui.pushButton_2.clicked.connect(self.go_to_patient_records)
            self.ui.pushButton_3.clicked.connect(self.go_to_prenatal_care)
            self.ui.pushButton_4.clicked.connect(self.go_to_appointments)
            self.ui.pushButton_5.clicked.connect(self.logout)

            # Inner Navigation
            self.ui.pushButton_7.clicked.connect(self.go_to_pastPregnancy)
            self.ui.pushButton_8.clicked.connect(self.go_to_prescription)
            self.ui.pushButton_9.clicked.connect(self.go_to_medicalHistory)
            self.ui.pushButton_10.clicked.connect(self.go_to_family_planning)
            self.ui.pushButton_11.clicked.connect(self.go_to_appointment_tab)


        except Exception as e:
            print("Navigation Error:", e)  # prevents crash if button name is different

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
                                   date_registered,
                                   blood_type,
                                   date_of_birth,
                                   philhealth_no
                            FROM patient_profile
                            WHERE patient_id = %s
                        """, (self.patient_id,)) #7

            data = cursor.fetchone()

            if not data:
                QMessageBox.warning(self, "Not Found", "Patient not found")
                return

            # ✅ Clean full name (no extra spaces)
            full_name = " ".join(filter(None, [data[1], data[2], data[3]]))

            # ✅ Safe date formatting
            register = data[4].strftime("%B %d, %Y") if data[4] else ""

            self.ui.placeholder_p_bloodType.setText(data[5])
            self.ui.patient_name.setText(full_name)
            self.ui.placeholder_p_ID.setText(str(data[0]))
            self.ui.registered_data_data.setText(register)
            self.ui.philhealth_placeholder.setText(str(data[7]))

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
            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load profile:\n{e}")

    def load_past_pregnancy_data(self):
        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "DB Error", "Cannot connect to database")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT history_id,
                       gravida,
                       para,
                       abortion,
                       living_children,
                       last_delivery_date,
                       delivery_type,
                       baby_weight,
                       outcome
                FROM past_pregnancy
                WHERE patient_id = %s
                ORDER BY last_delivery_date DESC
            """, (self.patient_id,))

            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            # ── GPAL labels ──────────────────────────────
            if rows:
                # take from the latest row
                latest = rows[0]
                self.ui.gravida_placeholer.setText(str(latest[1]))
                self.ui.para_placeholder.setText(str(latest[2]))
                self.ui.abortion_placeholder.setText(str(latest[3]))
                self.ui.living_children_placeholder.setText(str(latest[4]))
            else:
                self.ui.gravida_placeholer.setText("0")
                self.ui.para_placeholder.setText("0")
                self.ui.abortion_placeholder.setText("0")
                self.ui.living_children_placeholder.setText("0")

            # ── Table rows ───────────────────────────────
            self.ui.patient_table.setRowCount(0)  # 🔁 replace tableWidget with your actual name

            for row_data in rows:
                history_id = row_data[0]
                delivery_date = row_data[5].strftime("%B %d, %Y") if row_data[5] else ""
                delivery_type = row_data[6] or ""
                baby_weight = f"{row_data[7]} g" if row_data[7] else ""
                outcome = row_data[8] or ""

                row_index = self.ui.patient_table.rowCount()
                self.ui.patient_table.insertRow(row_index)

                self.ui.patient_table.setItem(row_index, 0, QTableWidgetItem(delivery_date))
                self.ui.patient_table.setItem(row_index, 1, QTableWidgetItem(outcome))
                self.ui.patient_table.setItem(row_index, 2, QTableWidgetItem(delivery_type))
                self.ui.patient_table.setItem(row_index, 3, QTableWidgetItem(baby_weight))

                # ── Action button (placeholder) ──────────
                view_btn = QPushButton("View")
                view_btn.setEnabled(False)  # not yet implemented
                self.ui.patient_table.setCellWidget(row_index, 4, view_btn)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load past pregnancies:\n{e}")

    #outer navigation
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

    def go_to_dashboard(self):  # FIXED NAME (important)
        from screens.dashboard_screen import DashboardScreen
        self.new_window = DashboardScreen()
        self.new_window.showMaximized()
        self.close()

    def go_to_appointments(self):
        print("Appointments screen not connected yet")

    def logout(self):
        from screens.login_screen import LoginScreen
        self.new_window = LoginScreen()
        self.new_window.showMaximized()
        self.close()

    #inner navigation
    def go_to_patient_profile(self):
        from screens.patient_profile_screen import PatientProfileScreen
        self.new_window = PatientProfileScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_pastPregnancy(self):
        pass

    def go_to_prescription(self):
        print("Prescriptions tab not connected yet")

    def go_to_medicalHistory(self):
        print("Medical History tab not connected yet")

    def go_to_family_planning(self):
        print("Family Planning tab not connected yet")

    def go_to_appointment_tab(self):
        print("Appointments tab not connected yet")