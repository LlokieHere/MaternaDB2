from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import QDate
from Dialog.past_pregnancy_add_dialog_ui import Ui_Dialog
from database import get_connection


class AddPastPregnancyDialog(QDialog):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Add Past Pregnancy")

        self.patient_id = patient_id

        # Set default date to today
        self.ui.delivery_dat_placeholder.setDate(QDate.currentDate())

        # Connect buttons
        self.ui.save_btn_2.clicked.connect(self.save)
        self.ui.cancel_btn_2.clicked.connect(self.reject)

    def save(self):
        # ── Gather values ─────────────────────────────────────
        delivery_date  = self.ui.delivery_dat_placeholder.date().toPyDate()
        delivery_type  = self.ui.delivery_date_placeholder.text().strip()  # delivery type field
        presentation   = self.ui.presentation_placeholder.text().strip()
        complications  = self.ui.complication_placeholder.text().strip()
        baby_weight    = self.ui.baby_weight_placeholder.text().strip()
        outcome        = self.ui.comboBox.currentText()
        episiotomy     = self.ui.Episiotomy_placeholder.currentText() == "Yes"

        # ── Validate required fields ──────────────────────────
        if not delivery_type:
            QMessageBox.warning(self, "Missing Field", "Please enter the delivery type.")
            return

        if baby_weight and not baby_weight.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Baby weight must be a number (grams).")
            return

        baby_weight_val = int(baby_weight) if baby_weight else None

        # ── Calculate GPAL from existing records + this new one ──
        gravida, para, abortion, living = self.calculate_gpal_with_new(outcome)

        # ── Insert into DB ────────────────────────────────────
        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "DB Error", "Cannot connect to database.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO past_pregnancy (
                    patient_id,
                    gravida,
                    para,
                    abortion,
                    living_children,
                    last_delivery_date,
                    delivery_type,
                    presentation,
                    episiotomy,
                    complications,
                    baby_weight,
                    outcome
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                self.patient_id,
                gravida,
                para,
                abortion,
                living,
                delivery_date,
                delivery_type,
                presentation,
                episiotomy,
                complications,
                baby_weight_val,
                outcome
            ))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Success", "Pregnancy record added successfully!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save record:\n{e}")

    def calculate_gpal_with_new(self, new_outcome):
        """
        Calculate GPAL from all existing records for this patient
        plus the new outcome being added right now.
        """
        conn = get_connection()
        if not conn:
            return 1, 0, 0, 0

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT outcome
                FROM past_pregnancy
                WHERE patient_id = %s
            """, (self.patient_id,))

            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            # Start with existing records
            all_outcomes = [row[0] for row in rows]

            # Add the new one being saved now
            all_outcomes.append(new_outcome)

            gravida  = len(all_outcomes)
            para     = 0
            abortion = 0
            living   = 0

            for outcome in all_outcomes:
                outcome = (outcome or "").strip().lower()
                if outcome in ("full term", "preterm"):
                    para    += 1
                    living  += 1
                elif outcome in ("miscarriage", "abortion"):
                    abortion += 1

            return gravida, para, abortion, living

        except Exception as e:
            print(f"GPAL calculation error: {e}")
            return 1, 0, 0, 0