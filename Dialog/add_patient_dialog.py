# screens/patient_profile_dialog_screen.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QStackedWidget, QMessageBox
from Dialog.add_patient_dialog_ui import Ui_StackedWidget
from database import get_connection


class EditPatientDialog(QDialog):
    def __init__(self, mode="add", patient_data=None, patient_id=None, parent=None):
        """
        mode        : "add" or "edit"
        patient_data: dict with existing values (edit mode only)
        patient_id  : int (edit mode only)
        """
        super().__init__(parent)

        self.mode       = mode
        self.patient_id = patient_id
        self.setWindowTitle("Add Patient" if mode == "add" else "Edit Patient Profile")
        self.setFixedSize(400, 570)

        # ── Build UI ──────────────────────────────────────────────────────────
        self.ui = Ui_StackedWidget()
        self.stack = QStackedWidget(self)
        self.ui.setupUi(self.stack)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)

        # ── Pre-fill only in edit mode ────────────────────────────────────────
        if mode == "edit" and patient_data:
            self.ui.firstName_placeholder.setText(patient_data.get("first_name", ""))
            self.ui.middleName_placeholder.setText(patient_data.get("middle_name", ""))
            self.ui.lastName_placeholder.setText(patient_data.get("last_name", ""))
            self.ui.suffix_placeholder.setText(patient_data.get("suffix", ""))
            self.ui.civilStatus_placeholder.setText(patient_data.get("civil_status", ""))
            self.ui.contactNum_placeholder.setText(patient_data.get("contact_number", ""))
            self.ui.philHealth_placeholder.setText(patient_data.get("philhealth_no", ""))
            self.ui.occupation_placeholder.setText(patient_data.get("occupation", ""))
            self.ui.religion_placeholder.setText(patient_data.get("religion", ""))
            self.ui.nationality_placeholder.setText(patient_data.get("nationality", ""))
            self.ui.religion_placeholder_2.setText(patient_data.get("blood_type", ""))  # blood type

            # Address (page 1)
            self.ui.street_placeholder.setText(patient_data.get("street", ""))
            self.ui.barangay_placeholder.setText(patient_data.get("barangay", ""))
            self.ui.city_placeholder.setText(patient_data.get("city", ""))
            self.ui.province_placeholder.setText(patient_data.get("province", ""))

            # Emergency contact (page 1)
            self.ui.EC_firstName_placeholder_2.setText(patient_data.get("ec_first_name", ""))
            self.ui.EC_last_name_placeholder_2.setText(patient_data.get("ec_last_name", ""))
            self.ui.EC_middleName_placeholder_2.setText(patient_data.get("ec_middle_name", ""))
            self.ui.emergencyNum_placeholder_2.setText(patient_data.get("ec_contact", ""))
            self.ui.relationship_placeholder_2.setText(patient_data.get("ec_relationship", ""))

            # Set DOB if available
            if patient_data.get("date_of_birth"):
                from PyQt6.QtCore import QDate
                dob = patient_data["date_of_birth"]  # expects a Python date object
                self.ui.dateOfBirth_placeholder.setDate(
                    QDate(dob.year, dob.month, dob.day)
                )

        # ── Wire up buttons ───────────────────────────────────────────────────
        # Page 0
        self.ui.pushButton.clicked.connect(self.cancel)        # Cancel
        self.ui.pushButton_2.clicked.connect(self.save)        # Save
        self.ui.pushButton_3.clicked.connect(self.go_to_page1) # Next

        # Page 1
        self.ui.back_btn_2.clicked.connect(self.go_to_page0)
        self.ui.cancel_btn_2.clicked.connect(self.cancel)
        self.ui.save_btn_2.clicked.connect(self.save)

        # Page 2
        self.ui.back_btn.clicked.connect(self.go_to_page1)
        self.ui.cancel_btn.clicked.connect(self.cancel)
        self.ui.save_btn.clicked.connect(self.save)

    # =====================================================
    # 🔁 NAVIGATION
    # =====================================================
    def go_to_page0(self): self.stack.setCurrentIndex(0)
    def go_to_page1(self): self.stack.setCurrentIndex(1)
    def go_to_page2(self): self.stack.setCurrentIndex(2)
    def cancel(self):      self.reject()

    # =====================================================
    # 💾 SAVE — branches on mode
    # =====================================================
    def save(self):
        # ── Basic validation ──────────────────────────────────────────────────
        first = self.ui.firstName_placeholder.text().strip()
        last  = self.ui.lastName_placeholder.text().strip()

        if not first or not last:
            QMessageBox.warning(self, "Validation", "First name and last name are required.")
            self.stack.setCurrentIndex(0)
            return

        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "DB Error", "Cannot connect to database")
            return

        try:
            cursor = conn.cursor()

            if self.mode == "edit":
                self._update(cursor)
            else:
                self._insert(cursor)

            conn.commit()
            cursor.close()
            conn.close()

            action = "updated" if self.mode == "edit" else "added"
            QMessageBox.information(self, "Success", f"Patient {action} successfully!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{e}")

    def _insert(self, cursor):
        vals = self._collect_values()

        # Patient Profile
        cursor.execute("""
            INSERT INTO patient_profile (
                first_name, middle_name, last_name, suffix,
                date_of_birth, civil_status, contact_number,
                philhealth_no, occupation, religion,
                nationality, blood_type
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s
            ) RETURNING patient_id
        """, vals[0:12])

        patient_id = cursor.fetchone()[0]

        # Patient Address
        cursor.execute("""
            INSERT INTO patient_address (
                patient_id, street, barangay, city, province
            ) VALUES (
                %s, %s, %s, %s, %s
            )
        """, (patient_id,) + vals[12:16])

        # Emergency Contact
        cursor.execute("""
            INSERT INTO emergency_contact (
                patient_id, contact_first_name, contact_last_name, contact_middle_name,
                contact_number, relationship
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s
            )
        """, (patient_id,) + vals[16:21])

    def _update(self, cursor):

        vals = self._collect_values()

        # ─────────────────────────────
        # PATIENT PROFILE TABLE
        # ─────────────────────────────
        cursor.execute("""
            UPDATE patient_profile SET
                first_name     = %s,
                middle_name    = %s,
                last_name      = %s,
                suffix         = %s,
                date_of_birth  = %s,
                civil_status   = %s,
                contact_number = %s,
                philhealth_no  = %s,
                occupation     = %s,
                religion       = %s,
                nationality    = %s,
                blood_type     = %s
            WHERE patient_id = %s
        """, vals[0:12] + (self.patient_id,))

        # ─────────────────────────────
        # PATIENT ADDRESS TABLE
        # ─────────────────────────────
        cursor.execute("""
            UPDATE patient_address SET
                street   = %s,
                barangay = %s,
                city     = %s,
                province = %s
            WHERE patient_id = %s
        """, vals[12:16] + (self.patient_id,))

        # ─────────────────────────────
        # EMERGENCY CONTACT TABLE
        # ─────────────────────────────
        cursor.execute("""
            UPDATE emergency_contact SET
                contact_first_name    = %s,
                contact_last_name     = %s,
                contact_middle_name   = %s,
                contact_number = %s,
                relationship  = %s
            WHERE patient_id = %s
        """, vals[16:21] + (self.patient_id,))

    def _collect_values(self):
        """Returns a tuple of all form values in column order."""
        dob = self.ui.dateOfBirth_placeholder.date().toPyDate()

        return (
            self.ui.firstName_placeholder.text().strip(),
            self.ui.middleName_placeholder.text().strip(),
            self.ui.lastName_placeholder.text().strip(),
            self.ui.suffix_placeholder.text().strip(),
            dob,
            self.ui.civilStatus_placeholder.text().strip(),
            self.ui.contactNum_placeholder.text().strip(),
            self.ui.philHealth_placeholder.text().strip(),
            self.ui.occupation_placeholder.text().strip(),
            self.ui.religion_placeholder.text().strip(),
            self.ui.nationality_placeholder.text().strip(),
            self.ui.religion_placeholder_2.text().strip(),   # blood type
            self.ui.street_placeholder.text().strip(),
            self.ui.barangay_placeholder.text().strip(),
            self.ui.city_placeholder.text().strip(),
            self.ui.province_placeholder.text().strip(),
            self.ui.EC_firstName_placeholder_2.text().strip(),
            self.ui.EC_last_name_placeholder_2.text().strip(),
            self.ui.EC_middleName_placeholder_2.text().strip(),
            self.ui.emergencyNum_placeholder_2.text().strip(),
            self.ui.relationship_placeholder_2.text().strip(),
        )