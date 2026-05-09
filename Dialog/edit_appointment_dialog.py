from PyQt6.QtWidgets import (
    QDialog, QMessageBox, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QTextEdit
)
from PyQt6.QtCore import Qt
from database import get_connection
from datetime import date as dt_date


class EditAppointmentDialog(QDialog):
    def __init__(self, appointment_id, parent=None):
        super().__init__(parent)
        self.appointment_id = appointment_id
        self.staff_map = {}
        self.setWindowTitle("Edit Appointment")
        self.setMinimumWidth(400)
        self.setup_ui()
        self.load_staff()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        style = "border-radius: 10px; border: 1px solid rgb(26,26,62); padding: 4px;"

        title = QLabel("Edit Appointment")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; border: none;")
        layout.addWidget(title)

        # Info label (read-only)
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("border: none; color: rgb(26,26,62);")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        # Status
        layout.addWidget(QLabel("Status"))
        self.status_combo = QComboBox()
        self.status_combo.addItems([
            "Scheduled", "Completed", "Missed", "Cancelled", "Rescheduled"
        ])
        self.status_combo.setStyleSheet(style)
        layout.addWidget(self.status_combo)

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

    def load_staff(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT staff_id, first_name || ' ' || last_name FROM staff")
            for sid, name in cursor.fetchall():
                self.staff_map[sid] = name
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Staff load error: {e}")

    def load_data(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pp.first_name || ' ' || pp.last_name,
                       a.appointment_date, a.appointment_time,
                       a.appointment_type, a.status, a.remarks, a.staff_id
                FROM appointment a
                JOIN patient_profile pp ON a.patient_id = pp.patient_id
                WHERE a.appointment_id = %s
            """, (self.appointment_id,))
            data = cursor.fetchone()
            cursor.close()
            conn.close()

            if not data:
                return

            date = data[1].strftime("%B %d, %Y") if data[1] else ""
            time = str(data[2])[:5] if data[2] else ""
            staff = self.staff_map.get(data[6], "Unknown")

            self.info_label.setText(
                f"<b>Patient:</b> {data[0]}<br>"
                f"<b>Date:</b> {date} at {time}<br>"
                f"<b>Type:</b> {data[3]}<br>"
                f"<b>Staff:</b> {staff}"
            )

            idx = self.status_combo.findText(data[4])
            if idx >= 0:
                self.status_combo.setCurrentIndex(idx)

            self.remarks_input.setPlainText(data[5] or "")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load:\n{e}")

    def save(self):
        status  = self.status_combo.currentText()
        remarks = self.remarks_input.toPlainText().strip() or None

        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE appointment
                SET status = %s, remarks = %s
                WHERE appointment_id = %s
            """, (status, remarks, self.appointment_id))

            # Log status history
            cursor.execute("""
                INSERT INTO appointment_status_history
                    (appointment_id, status, status_date)
                VALUES (%s, %s, %s)
            """, (self.appointment_id, status, dt_date.today()))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Success", "Appointment updated!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{e}")