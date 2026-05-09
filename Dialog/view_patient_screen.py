from PyQt6.QtWidgets import QDialog
from Dialog.view_pregnancy_ui import Ui_Dialog
from database import get_connection
from PyQt6.QtWidgets import QMessageBox


class PastPregnancyViewDialog(QDialog):
    def __init__(self, history_id, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Pregnancy Details")

        self.history_id = history_id
        self.load_data()

    def load_data(self):
        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "DB Error", "Cannot connect to database")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT last_delivery_date,
                       delivery_type,
                       outcome,
                       baby_weight,
                       presentation,
                       complications,
                       episiotomy
                FROM past_pregnancy
                WHERE history_id = %s
            """, (self.history_id,))

            data = cursor.fetchone()
            cursor.close()
            conn.close()

            if not data:
                QMessageBox.warning(self, "Not Found", "Pregnancy record not found")
                return

            delivery_date = data[0].strftime("%B %d, %Y") if data[0] else "N/A"
            delivery_type = data[1] or "N/A"
            outcome       = data[2] or "N/A"
            baby_weight   = f"{data[3]} g" if data[3] else "N/A"
            presentation  = data[4] or "N/A"
            complications = data[5] or "N/A"
            episiotomy    = "Yes" if data[6] else "No"

            self.ui.delivery_date_placeholder.setText(delivery_date)
            self.ui.delivery_type_placeholderr.setText(delivery_type)
            self.ui.outcome_placeholder.setText(outcome)
            self.ui.baby_weight_placeholder.setText(baby_weight)
            self.ui.presentation_placeholder.setText(presentation)
            self.ui.complications_placeholder.setText(complications)
            self.ui.episiotomy_placeholder.setText(episiotomy)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load pregnancy details:\n{e}")