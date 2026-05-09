from PyQt6.QtWidgets import (
    QDialog, QMessageBox, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QDateEdit, QComboBox, QTextEdit
)
from PyQt6.QtCore import QDate, Qt
from database import get_connection


class AddFamilyPlanningDialog(QDialog):
    def __init__(self, patient_id, planning_id=None, parent=None):
        super().__init__(parent)
        self.patient_id  = patient_id
        self.planning_id = planning_id  # None = add, not None = edit
        self.setWindowTitle("Edit Plan" if planning_id else "Add Family Planning")
        self.setMinimumWidth(400)
        self.setup_ui()

        if self.planning_id:
            self.load_existing_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        style = "border-radius: 10px; border: 1px solid rgb(26,26,62); padding: 4px;"

        title = QLabel("Edit Plan" if self.planning_id else "Add Family Planning")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; border: none;")
        layout.addWidget(title)

        # Method
        layout.addWidget(QLabel("Method"))
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Pills", "IUD", "Injectable", "Natural", "BTL", "None"])
        self.method_combo.setStyleSheet(style)
        layout.addWidget(self.method_combo)

        # Start Date
        layout.addWidget(QLabel("Start Date"))
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setStyleSheet(style)
        layout.addWidget(self.start_date_input)

        # End Date
        layout.addWidget(QLabel("End Date (optional)"))
        self.end_date_input = QDateEdit()
        self.end_date_input.setDate(QDate.currentDate())
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setStyleSheet(style)
        self.end_date_input.setSpecialValueText("No end date")
        layout.addWidget(self.end_date_input)

        # Status
        layout.addWidget(QLabel("Status"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Active", "Resolved"])
        self.status_combo.setStyleSheet(style)
        layout.addWidget(self.status_combo)

        # Remarks
        layout.addWidget(QLabel("Remarks / Side Effects (optional)"))
        self.remarks_input = QTextEdit()
        self.remarks_input.setPlaceholderText("e.g., Mild nausea in first month...")
        self.remarks_input.setStyleSheet(style)
        self.remarks_input.setFixedHeight(80)
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
            "background-color: rgb(192,116,182); color: white;")
        save_btn.clicked.connect(self.save)

        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def load_existing_data(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT method, start_date, end_date, status, remarks
                FROM family_planning WHERE planning_id = %s
            """, (self.planning_id,))
            data = cursor.fetchone()
            cursor.close()
            conn.close()

            if not data:
                return

            # Set method
            idx = self.method_combo.findText(data[0])
            if idx >= 0:
                self.method_combo.setCurrentIndex(idx)

            # Set dates
            if data[1]:
                self.start_date_input.setDate(
                    QDate(data[1].year, data[1].month, data[1].day))
            if data[2]:
                self.end_date_input.setDate(
                    QDate(data[2].year, data[2].month, data[2].day))

            # Set status
            idx = self.status_combo.findText(data[3])
            if idx >= 0:
                self.status_combo.setCurrentIndex(idx)

            # Set remarks
            self.remarks_input.setPlainText(data[4] or "")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data:\n{e}")

    def save(self):
        method     = self.method_combo.currentText()
        start_date = self.start_date_input.date().toPyDate()
        end_date   = self.end_date_input.date().toPyDate()
        status     = self.status_combo.currentText()
        remarks    = self.remarks_input.toPlainText().strip() or None

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            if self.planning_id:
                # ── Edit existing ─────────────────────────
                cursor.execute("""
                    UPDATE family_planning
                    SET method = %s, start_date = %s, end_date = %s,
                        status = %s, remarks = %s
                    WHERE planning_id = %s
                """, (method, start_date, end_date, status, remarks,
                      self.planning_id))
            else:
                # ── Add new ───────────────────────────────
                cursor.execute("""
                    INSERT INTO family_planning
                        (patient_id, method, start_date, end_date, status, remarks)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (self.patient_id, method, start_date, end_date,
                      status, remarks))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Success", "Family planning record saved!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{e}")