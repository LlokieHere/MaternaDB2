from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTableWidgetItem, QWidget,
    QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QHeaderView
from screens.past_pregnancy_ui import Ui_MainWindow
from Dialog.view_patient_screen import PastPregnancyViewDialog
from database import get_connection
from PyQt6.QtWidgets import QDialog


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

        self.ui.add_btn.clicked.connect(self.open_add_dialog)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.width()
        h = self.height()

        # ── Top navbar ───────────────────────────────────────────
        self.ui.frame_2.setGeometry(0, 0, w, 61)

        # ── Left sidebar ─────────────────────────────────────────
        sidebar_w = int(w * 0.19)
        self.ui.frame.setGeometry(0, 61, sidebar_w, h - 61)

        # Sidebar buttons
        btn_x = 20
        btn_w = sidebar_w - 30
        self.ui.pushButton.setGeometry(btn_x, 180, btn_w, 41)
        self.ui.pushButton_2.setGeometry(btn_x, 230, btn_w, 41)
        self.ui.pushButton_3.setGeometry(btn_x, 280, btn_w, 41)
        self.ui.pushButton_4.setGeometry(btn_x, 330, btn_w, 41)
        self.ui.pushButton_5.setGeometry(btn_x, h - 200, btn_w, 41)

        # ── Main content area ─────────────────────────────────────
        content_x = sidebar_w
        content_w = w - sidebar_w
        content_h = h - 61
        self.ui.frame_3.setGeometry(content_x, 61, content_w, content_h)

        # Padding inside frame_3
        pad = 40
        inner_w = content_w - (pad * 2)

        # Title label
        self.ui.label.setGeometry(pad, 20, inner_w // 2, 61)

        # ── Patient header card ───────────────────────────────────
        header_h = 141
        self.ui.frame_4.setGeometry(pad, 80, inner_w, header_h)

        # Photo box
        self.ui.frame_5.setGeometry(20, 20, 111, 91)

        # Patient name
        self.ui.patient_name.setGeometry(170, 15, inner_w - 320, 30)

        # Next button
        self.ui.next_btn.setGeometry(inner_w - 140, 50, 120, 41)

        # Info grid (Patient ID, Age, Registered, Blood Type, PhilHealth)
        info_w = inner_w - 320
        self.ui.layoutWidget_2.setGeometry(170, 55, info_w, 75)

        # ── Tab bar ───────────────────────────────────────────────
        tab_y = 80 + header_h + 20
        self.ui.layoutWidget.setGeometry(pad, tab_y, inner_w, 40)

        # ── GPAL row ──────────────────────────────────────────────
        gpal_y = tab_y + 50
        self.ui.layoutWidget1.setGeometry(pad, gpal_y, 100, 24)
        self.ui.layoutWidget2.setGeometry(pad + 110, gpal_y, 80, 24)
        self.ui.layoutWidget3.setGeometry(pad + 200, gpal_y, 110, 24)
        self.ui.layoutWidget4.setGeometry(pad + 320, gpal_y, 160, 24)

        # Add / Remove buttons (right-aligned)
        self.ui.remove_btn.setGeometry(inner_w - 120, gpal_y, 120, 24)
        self.ui.add_btn.setGeometry(inner_w - 250, gpal_y, 120, 24)

        # ── Table ─────────────────────────────────────────────────
        table_y = gpal_y + 34
        table_h = content_h - table_y - pad
        self.ui.patient_table.setGeometry(pad, table_y, inner_w, table_h)


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

            self.ui.remove_btn.clicked.connect(self.remove_pregnancy)


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

            # ── Table setup (do this ONCE, outside the loop) ──────────────────
            self.ui.patient_table.setRowCount(0)

            # Stretch all columns evenly — remove setColumnWidth calls entirely
            self.ui.patient_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            # Center-align header text
            self.ui.patient_table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

            # ── Table rows ────────────────────────────────
            for row_data in rows:
                history_id = row_data[0]  # ← already there
                delivery_date = row_data[5].strftime("%B %d, %Y") if row_data[5] else ""
                delivery_type = row_data[6] or ""
                baby_weight = f"{row_data[7]} g" if row_data[7] else ""
                outcome = row_data[8] or ""

                row_index = self.ui.patient_table.rowCount()
                self.ui.patient_table.insertRow(row_index)

                for col, value in enumerate([delivery_date, outcome, delivery_type, baby_weight]):
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.ui.patient_table.setItem(row_index, col, item)

                # ── Replace the old view_btn block with this ──────────
                view_btn = QPushButton("View")
                view_btn.setEnabled(True)

                def make_view_handler(hid):
                    def handler():
                        self.open_view_dialog(hid)

                    return handler

                view_btn.clicked.connect(make_view_handler(history_id))
                self.ui.patient_table.setCellWidget(row_index, 4, view_btn)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load past pregnancies:\n{e}")

    def open_view_dialog(self, history_id):
        from Dialog.view_patient_screen import PastPregnancyViewDialog
        dialog = PastPregnancyViewDialog(history_id, parent=self)
        dialog.exec()

    def open_add_dialog(self):
        from Dialog.add_pregnancy_dialog import AddPastPregnancyDialog
        dialog = AddPastPregnancyDialog(self.patient_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_past_pregnancy_data()  # refresh table + GPAL after saving

    def remove_pregnancy(self):
        # ── Check if a row is selected ────────────────────────
        selected = self.ui.patient_table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "No Selection", "Please select a pregnancy record to remove.")
            return

        # ── Confirm deletion ──────────────────────────────────
        confirm = QMessageBox.question(
            self, "Remove Pregnancy",
            "Are you sure you want to remove this pregnancy record?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        # ── Get history_id from selected row ──────────────────
        # We stored it via the view button handler, so re-fetch from DB by matching row data
        delivery_date_item = self.ui.patient_table.item(selected, 0)
        outcome_item = self.ui.patient_table.item(selected, 1)

        if not delivery_date_item:
            return

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            # ── Get the outcome of the record being deleted ───
            cursor.execute("""
                SELECT history_id, outcome
                FROM past_pregnancy
                WHERE patient_id = %s
                ORDER BY last_delivery_date DESC
                LIMIT 1 OFFSET %s
            """, (self.patient_id, selected))

            row = cursor.fetchone()
            if not row:
                QMessageBox.warning(self, "Error", "Could not find the selected record.")
                cursor.close()
                conn.close()
                return

            history_id = row[0]

            # ── Delete the record ─────────────────────────────
            cursor.execute("""
                DELETE FROM past_pregnancy
                WHERE history_id = %s
            """, (history_id,))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Success", "Pregnancy record removed successfully!")

            # ── Refresh table + GPAL ──────────────────────────
            self.load_past_pregnancy_data()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to remove record:\n{e}")

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

    def go_to_appointments(self):
        from screens.appointments_screen import AppointmentsScreen
        self.new_window = AppointmentsScreen()
        self.new_window.showMaximized()
        self.close()

    # ✅ Correct
    def go_to_prescription(self):
        from screens.prescription_screen import PrescriptionScreen  # ✅ add "screens."
        self.new_window = PrescriptionScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_medicalHistory(self):
        from screens.medical_history_screen import MedicalHistoryScreen
        self.new_window = MedicalHistoryScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_family_planning(self):
        from screens.family_planning_screen import FamilyPlanningScreen
        self.new_window = FamilyPlanningScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_appointment(self):
        from screens.appointment_patient_record_screen import PatientAppointmentScreen
        self.new_window = PatientAppointmentScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()