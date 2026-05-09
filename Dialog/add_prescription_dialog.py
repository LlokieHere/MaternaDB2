from PyQt6.QtWidgets import (
    QDialog, QMessageBox, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QDateEdit, QComboBox, QTableWidget, QHeaderView
)
from PyQt6.QtCore import QDate, Qt
from database import get_connection


class AddPrescriptionDialog(QDialog):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.medicines   = []   # staged list of dicts
        self.staff_map   = {}   # name → staff_id
        self.medicine_map = {}  # name → medicine_id
        self.setWindowTitle("Add Prescription")
        self.setMinimumWidth(520)
        self.setup_ui()
        self.load_staff()
        self.load_medicines()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        style = "border-radius: 10px; border: 1px solid rgb(26,26,62); padding: 4px;"

        # Title
        title = QLabel("Add Prescription")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; border: none;")
        layout.addWidget(title)

        # Date + Prescribed By
        row1 = QHBoxLayout()

        date_col = QVBoxLayout()
        date_col.addWidget(QLabel("Date"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setStyleSheet(style)
        date_col.addWidget(self.date_input)
        row1.addLayout(date_col)

        prescribed_col = QVBoxLayout()
        prescribed_col.addWidget(QLabel("Prescribed By"))
        self.prescribed_combo = QComboBox()
        self.prescribed_combo.setStyleSheet(style)
        prescribed_col.addWidget(self.prescribed_combo)
        row1.addLayout(prescribed_col)

        layout.addLayout(row1)

        # Medicine + Dosage
        row2 = QHBoxLayout()

        med_col = QVBoxLayout()
        med_col.addWidget(QLabel("Medicine"))
        self.medicine_combo = QComboBox()
        self.medicine_combo.setStyleSheet(style)
        med_col.addWidget(self.medicine_combo)
        row2.addLayout(med_col)

        dosage_col = QVBoxLayout()
        dosage_col.addWidget(QLabel("Dosage"))
        self.dosage_input = QLineEdit()
        self.dosage_input.setPlaceholderText("e.g., 500mg")
        self.dosage_input.setStyleSheet(style)
        dosage_col.addWidget(self.dosage_input)
        row2.addLayout(dosage_col)

        layout.addLayout(row2)

        # Frequency + Duration
        row3 = QHBoxLayout()

        freq_col = QVBoxLayout()
        freq_col.addWidget(QLabel("Frequency"))
        self.frequency_input = QLineEdit()
        self.frequency_input.setPlaceholderText("e.g., Once a day")
        self.frequency_input.setStyleSheet(style)
        freq_col.addWidget(self.frequency_input)
        row3.addLayout(freq_col)

        dur_col = QVBoxLayout()
        dur_col.addWidget(QLabel("Duration"))
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("e.g., 7 days")
        self.duration_input.setStyleSheet(style)
        dur_col.addWidget(self.duration_input)
        row3.addLayout(dur_col)

        layout.addLayout(row3)

        # Route + Timing
        row4 = QHBoxLayout()

        route_col = QVBoxLayout()
        route_col.addWidget(QLabel("Route"))
        self.route_input = QLineEdit()
        self.route_input.setPlaceholderText("e.g., Oral")
        self.route_input.setStyleSheet(style)
        route_col.addWidget(self.route_input)
        row4.addLayout(route_col)

        timing_col = QVBoxLayout()
        timing_col.addWidget(QLabel("Timing"))
        self.timing_input = QLineEdit()
        self.timing_input.setPlaceholderText("e.g., After meal")
        self.timing_input.setStyleSheet(style)
        timing_col.addWidget(self.timing_input)
        row4.addLayout(timing_col)

        layout.addLayout(row4)

        # Notes
        layout.addWidget(QLabel("Notes (optional)"))
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("e.g., Take with water")
        self.notes_input.setStyleSheet(style)
        layout.addWidget(self.notes_input)

        # Add Medicine button
        self.add_medicine_btn = QPushButton("+ Add Medicine to List")
        self.add_medicine_btn.setStyleSheet("""
            QPushButton {
                border-radius: 10px; border: 1px solid rgb(26,26,62);
                padding: 6px; background-color: rgb(236, 198, 220);
            }
            QPushButton:hover { background-color: rgb(220, 170, 200); }
        """)
        self.add_medicine_btn.clicked.connect(self.add_medicine_to_list)
        layout.addWidget(self.add_medicine_btn)

        # Staged medicines table
        self.medicine_table = QTableWidget()
        self.medicine_table.setColumnCount(6)
        self.medicine_table.setHorizontalHeaderLabels([
            "Medicine", "Dosage", "Frequency", "Duration", "Route", "Timing"
        ])
        self.medicine_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.medicine_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers)
        self.medicine_table.verticalHeader().setVisible(False)
        self.medicine_table.setFixedHeight(120)
        self.medicine_table.setStyleSheet("""
            QTableWidget { border-radius: 8px; background-color: rgb(236,198,220);
                           border: 1px solid rgb(210,177,200); }
            QHeaderView::section { background-color: rgb(236,198,220);
                                   font-weight: bold; border: none; }
            QTableWidget::item { border: none; }
        """)
        layout.addWidget(self.medicine_table)

        # Cancel / Save
        btn_row = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(
            "border-radius: 10px; border: 1px solid rgb(26,26,62); padding: 6px;")
        self.cancel_btn.clicked.connect(self.reject)

        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet(
            "border-radius: 10px; border: 1px solid rgb(26,26,62); padding: 6px;")
        self.save_btn.clicked.connect(self.save)

        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.save_btn)
        layout.addLayout(btn_row)

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
            for staff_id, name in cursor.fetchall():
                self.staff_map[name] = staff_id
                self.prescribed_combo.addItem(name)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Staff load error: {e}")

    def load_medicines(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT medicine_id, medicine_name FROM medicine ORDER BY medicine_name")
            for medicine_id, name in cursor.fetchall():
                self.medicine_map[name] = medicine_id
                self.medicine_combo.addItem(name)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Medicine load error: {e}")

    def add_medicine_to_list(self):
        medicine_name = self.medicine_combo.currentText()
        dosage        = self.dosage_input.text().strip()
        frequency     = self.frequency_input.text().strip()
        duration      = self.duration_input.text().strip()
        route         = self.route_input.text().strip()
        timing        = self.timing_input.text().strip()
        notes         = self.notes_input.text().strip()

        if not dosage or not frequency or not duration:
            QMessageBox.warning(self, "Missing Fields",
                                "Please fill in Dosage, Frequency, and Duration.")
            return

        self.medicines.append({
            "medicine_id": self.medicine_map[medicine_name],
            "medicine_name": medicine_name,
            "dosage": dosage, "frequency": frequency,
            "duration": duration, "route": route,
            "timing": timing, "notes": notes
        })

        row = self.medicine_table.rowCount()
        self.medicine_table.insertRow(row)
        for col, val in enumerate([medicine_name, dosage, frequency,
                                    duration, route, timing]):
            item = QTableWidgetItem(val)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.medicine_table.setItem(row, col, item)

        # Clear for next entry
        self.dosage_input.clear()
        self.frequency_input.clear()
        self.duration_input.clear()
        self.route_input.clear()
        self.timing_input.clear()
        self.notes_input.clear()

    def save(self):
        if not self.medicines:
            QMessageBox.warning(self, "No Medicines",
                                "Please add at least one medicine.")
            return

        staff_name  = self.prescribed_combo.currentText()
        staff_id    = self.staff_map.get(staff_name)
        presc_date  = self.date_input.date().toPyDate()

        if not staff_id:
            QMessageBox.warning(self, "Missing", "Please select who prescribed.")
            return

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            for med in self.medicines:
                cursor.execute("""
                    INSERT INTO prescription (
                        patient_id, medicine_id, prescribed_by,
                        dosage, frequency, duration,
                        prescription_date, notes, route, timing
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    self.patient_id,
                    med["medicine_id"],
                    staff_id,
                    med["dosage"],
                    med["frequency"],
                    med["duration"],
                    presc_date,
                    med["notes"] or None,
                    med["route"] or None,
                    med["timing"] or None,
                ))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Success",
                                    "Prescription saved successfully!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{e}")