from PyQt6.QtWidgets import (
    QDialog, QMessageBox, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QDateEdit,
    QComboBox, QTimeEdit, QTextEdit
)
from PyQt6.QtCore import QDate, QTime, Qt
from database import get_connection


class AddAppointmentDialog(QDialog):
    def __init__(self, appointment_type=None, parent=None):
        super().__init__(parent)
        self.preset_type = appointment_type
        self.staff_map   = {}
        self.patient_map = {}
        self.setWindowTitle("New Appointment")
        self.setMinimumWidth(420)
        self.setup_ui()
        self.load_patients()
        self.load_staff()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        style = "border-radius: 10px; border: 1px solid rgb(26,26,62); padding: 4px;"

        title = QLabel("New Appointment")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; border: none;")
        layout.addWidget(title)

        # Patient
        layout.addWidget(QLabel("Patient"))
        self.patient_combo = QComboBox()
        self.patient_combo.setStyleSheet(style)
        layout.addWidget(self.patient_combo)

        # Staff
        layout.addWidget(QLabel("Staff / Doctor"))
        self.staff_combo = QComboBox()
        self.staff_combo.setStyleSheet(style)
        layout.addWidget(self.staff_combo)

        # Date + Time
        row1 = QHBoxLayout()
        date_col = QVBoxLayout()
        date_col.addWidget(QLabel("Date"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setStyleSheet(style)
        date_col.addWidget(self.date_input)
        row1.addLayout(date_col)

        time_col = QVBoxLayout()
        time_col.addWidget(QLabel("Time"))
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime(8, 0))
        self.time_input.setStyleSheet(style)
        time_col.addWidget(self.time_input)
        row1.addLayout(time_col)
        layout.addLayout(row1)

        # Appointment Type
        layout.addWidget(QLabel("Appointment Type"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Scheduled", "Walk-in", "Follow-up"])
        if self.preset_type:
            idx = self.type_combo.findText(self.preset_type)
            if idx >= 0:
                self.type_combo.setCurrentIndex(idx)
        self.type_combo.setStyleSheet(style)
        layout.addWidget(self.type_combo)

        # Purpose
        layout.addWidget(QLabel("Purpose"))
        self.purpose_input = QLineEdit()
        self.purpose_input.setPlaceholderText("e.g., Prenatal Check-up")
        self.purpose_input.setStyleSheet(style)
        layout.addWidget(self.purpose_input)

        # Remarks
        layout.addWidget(QLabel("Remarks (optional)"))
        self.remarks_input = QTextEdit()
        self.remarks_input.setFixedHeight(70)
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
            "border-radius: 10px; border: 1px solid rgb(26,26,62); padding: 6px;"
            "background-color: rgb(106,27,154); color: white;")
        save_btn.clicked.connect(self.save)

        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def load_patients(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT patient_id, first_name || ' ' || last_name
                FROM patient_profile ORDER BY first_name
            """)
            for pid, name in cursor.fetchall():
                self.patient_map[name] = pid
                self.patient_combo.addItem(name)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Patient load error: {e}")

    def load_staff(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT staff_id, first_name || ' ' || last_name
                FROM staff ORDER BY first_name
            """)
            for sid, name in cursor.fetchall():
                self.staff_map[name] = sid
                self.staff_combo.addItem(name)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Staff load error: {e}")

    def save(self):
        patient_name = self.patient_combo.currentText()
        staff_name   = self.staff_combo.currentText()
        patient_id   = self.patient_map.get(patient_name)
        staff_id     = self.staff_map.get(staff_name)
        date         = self.date_input.date().toPyDate()
        time         = self.time_input.time().toPyTime()
        appt_type    = self.type_combo.currentText()
        purpose      = self.purpose_input.text().strip()
        remarks      = self.remarks_input.toPlainText().strip() or None

        if not patient_id or not staff_id:
            QMessageBox.warning(self, "Missing", "Please select a patient and staff.")
            return
        if not purpose:
            QMessageBox.warning(self, "Missing", "Please enter a purpose.")
            return

        conn = get_connection()
        if not conn:
            return
        try:
            from datetime import date as dt_date
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO appointment (
                    patient_id, staff_id, appointment_date, appointment_time,
                    appointment_type, status, date_created, remarks
                ) VALUES (%s, %s, %s, %s, %s, 'Scheduled', %s, %s)
                RETURNING appointment_id
            """, (patient_id, staff_id, date, time,
                  appt_type, dt_date.today(), remarks))

            appointment_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO appointment_purpose (appointment_id, purpose)
                VALUES (%s, %s)
            """, (appointment_id, purpose))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Success", "Appointment saved!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{e}")