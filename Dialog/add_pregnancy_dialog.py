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

        self.ui.delivery_dat_placeholder.setDate(QDate.currentDate())

        self.ui.save_btn_2.clicked.connect(self.save)
        self.ui.cancel_btn_2.clicked.connect(self.reject)

    def save(self):
        delivery_date = self.ui.delivery_dat_placeholder.date().toPyDate()
        delivery_type = self.ui.delivery_date_placeholder.currentText().strip()
        presentation  = self.ui.presentation_placeholder.text().strip()
        complications = self.ui.complication_placeholder.text().strip()
        baby_weight   = self.ui.baby_weight_placeholder.text().strip()
        outcome       = self.ui.comboBox.currentText().strip()
        episiotomy    = self.ui.Episiotomy_placeholder.currentText() == "Yes"

        # Validate outcome matches DB constraint exactly
        valid_outcomes = ["Full Term", "Preterm", "Miscarriage", "Abortion"]
        if outcome not in valid_outcomes:
            QMessageBox.warning(self, "Invalid Input",
                f"Outcome must be one of: {', '.join(valid_outcomes)}")
            return

        # baby_weight is INTEGER in DB (store as grams)
        if baby_weight:
            try:
                baby_weight_val = int(baby_weight)
            except ValueError:
                QMessageBox.warning(self, "Invalid Input",
                    "Baby weight must be a whole number in grams (e.g. 3200).")
                return
        else:
            baby_weight_val = None

        gravida, para, abortion, living = self.calculate_gpal_with_new(outcome)

        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "DB Error", "Cannot connect to database.")
            return

        try:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO past_pregnancy (
                    patient_id, gravida, para, abortion, living_children,
                    last_delivery_date, delivery_type, presentation,
                    episiotomy, complications, baby_weight, outcome
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                self.patient_id, gravida, para, abortion, living,
                delivery_date, delivery_type or None,
                presentation or None, episiotomy,
                complications or None, baby_weight_val, outcome
            ))

            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Pregnancy record added successfully!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save record:\n{e}")

    def calculate_gpal_with_new(self, new_outcome):
        conn = get_connection()
        if not conn:
            return 1, 0, 0, 0

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT outcome FROM past_pregnancy WHERE patient_id = %s
            """, (self.patient_id,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            # All existing + the one being added now
            all_outcomes = [row[0] for row in rows] + [new_outcome]

            gravida  = len(all_outcomes)
            para     = 0
            abortion = 0
            living   = 0

            for o in all_outcomes:
                o_lower = (o or "").strip().lower()
                if o_lower in ("full term", "preterm"):
                    para   += 1
                    living += 1
                elif o_lower in ("miscarriage", "abortion"):
                    abortion += 1

            return gravida, para, abortion, living

        except Exception as e:
            print(f"GPAL calculation error: {e}")
            return 1, 0, 0, 0
        