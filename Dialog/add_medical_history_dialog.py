from PyQt6.QtWidgets import (
    QDialog, QMessageBox, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QDateEdit, QComboBox
)
from PyQt6.QtCore import QDate, Qt
from database import get_connection


class AddMedicalHistoryDialog(QDialog):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.setWindowTitle("Add Medical Condition")
        self.setMinimumWidth(400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        style = "border-radius: 10px; border: 1px solid rgb(26,26,62); padding: 4px;"

        # Title
        title = QLabel("Add Medical Condition")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; border: none;")
        layout.addWidget(title)

        # Condition
        layout.addWidget(QLabel("Condition"))
        self.condition_input = QLineEdit()
        self.condition_input.setPlaceholderText("e.g., Hypertension")
        self.condition_input.setStyleSheet(style)
        layout.addWidget(self.condition_input)

        # Diagnosis Date
        layout.addWidget(QLabel("Diagnosis Date"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setStyleSheet(style)
        layout.addWidget(self.date_input)

        # Status
        layout.addWidget(QLabel("Status"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Active", "Resolved"])
        self.status_combo.setStyleSheet(style)
        layout.addWidget(self.status_combo)

        # Remarks
        layout.addWidget(QLabel("Remarks (optional)"))
        self.remarks_input = QLineEdit()
        self.remarks_input.setPlaceholderText("e.g., Under medication")
        self.remarks_input.setStyleSheet(style)
        layout.addWidget(self.remarks_input)

        # Buttons
        btn_row = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(
            "border-radius: 10px; border: 1px solid rgb(26,26,62); padding: 6px;")
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(
            "border-radius: 10px; border: 1px solid rgb(26,26,62); padding: 6px; background-color: rgb(192,116,182); color: white;")
        save_btn.clicked.connect(self.save)

        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def save(self):
        condition = self.condition_input.text().strip()
        date      = self.date_input.date().toPyDate()
        status    = self.status_combo.currentText()
        remarks   = self.remarks_input.text().strip() or None

        if not condition:
            QMessageBox.warning(self, "Missing Field", "Please enter a condition.")
            return

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO medical_history (
                    patient_id, condition, diagnosis_date, status, remarks
                ) VALUES (%s, %s, %s, %s, %s)
            """, (self.patient_id, condition, date, status, remarks))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Success", "Medical condition added!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{e}")