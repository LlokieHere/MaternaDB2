from PyQt6.QtWidgets import (
    QDialog, QMessageBox, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QDateEdit, QComboBox, QTableWidget, QHeaderView,
    QCompleter
)
from PyQt6.QtCore import QDate, Qt, QStringListModel
from database import get_connection


STYLE      = "border-radius: 10px; border: 1px solid rgb(26,26,62); padding: 4px;"
BTN_PINK   = """
    QPushButton {
        border-radius: 10px; border: 1px solid rgb(26,26,62);
        padding: 6px; background-color: rgb(236, 198, 220);
    }
    QPushButton:hover { background-color: rgb(220, 170, 200); }
"""
BTN_PLAIN  = "border-radius: 10px; border: 1px solid rgb(26,26,62); padding: 6px;"


class AddPrescriptionDialog(QDialog):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.medicines  = []     # staged list of dicts
        self.staff_map  = {}     # display name → staff_id

        self.setWindowTitle("Add Prescription")
        self.setMinimumWidth(540)
        self.setup_ui()
        self.load_staff()
        self.load_medicine_suggestions()

    # ─────────────────────────────────────────────
    #  UI
    # ─────────────────────────────────────────────
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Add Prescription")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; border: none;")
        layout.addWidget(title)

        # ── Row 1: Date + Prescribed By ──────────────────────────────────────
        row1 = QHBoxLayout()

        date_col = QVBoxLayout()
        date_col.addWidget(QLabel("Date"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setStyleSheet(STYLE)
        date_col.addWidget(self.date_input)
        row1.addLayout(date_col)

        prescribed_col = QVBoxLayout()
        prescribed_col.addWidget(QLabel("Prescribed By"))
        self.prescribed_combo = QComboBox()
        self.prescribed_combo.setStyleSheet(STYLE)
        prescribed_col.addWidget(self.prescribed_combo)
        row1.addLayout(prescribed_col)

        layout.addLayout(row1)

        # ── Row 2: Medicine (free text + autocomplete) + Dosage ──────────────
        row2 = QHBoxLayout()

        med_col = QVBoxLayout()
        med_col.addWidget(QLabel("Medicine"))
        self.medicine_input = QLineEdit()
        self.medicine_input.setPlaceholderText("Type medicine name…")
        self.medicine_input.setStyleSheet(STYLE)

        # Autocomplete — populated from DB suggestions, but fully editable
        self.medicine_completer = QCompleter([])
        self.medicine_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.medicine_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.medicine_input.setCompleter(self.medicine_completer)

        med_col.addWidget(self.medicine_input)
        row2.addLayout(med_col)

        dosage_col = QVBoxLayout()
        dosage_col.addWidget(QLabel("Dosage"))
        self.dosage_input = QLineEdit()
        self.dosage_input.setPlaceholderText("e.g., 500mg")
        self.dosage_input.setStyleSheet(STYLE)
        dosage_col.addWidget(self.dosage_input)
        row2.addLayout(dosage_col)

        layout.addLayout(row2)

        # ── Row 3: Frequency + Duration ───────────────────────────────────────
        row3 = QHBoxLayout()

        freq_col = QVBoxLayout()
        freq_col.addWidget(QLabel("Frequency"))
        self.frequency_input = QLineEdit()
        self.frequency_input.setPlaceholderText("e.g., Once a day")
        self.frequency_input.setStyleSheet(STYLE)
        freq_col.addWidget(self.frequency_input)
        row3.addLayout(freq_col)

        dur_col = QVBoxLayout()
        dur_col.addWidget(QLabel("Duration"))
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("e.g., 7 days")
        self.duration_input.setStyleSheet(STYLE)
        dur_col.addWidget(self.duration_input)
        row3.addLayout(dur_col)

        layout.addLayout(row3)

        # ── Row 4: Route + Timing ─────────────────────────────────────────────
        row4 = QHBoxLayout()

        route_col = QVBoxLayout()
        route_col.addWidget(QLabel("Route"))
        self.route_input = QLineEdit()
        self.route_input.setPlaceholderText("e.g., Oral")
        self.route_input.setStyleSheet(STYLE)
        route_col.addWidget(self.route_input)
        row4.addLayout(route_col)

        timing_col = QVBoxLayout()
        timing_col.addWidget(QLabel("Timing"))
        self.timing_input = QLineEdit()
        self.timing_input.setPlaceholderText("e.g., After meal")
        self.timing_input.setStyleSheet(STYLE)
        timing_col.addWidget(self.timing_input)
        row4.addLayout(timing_col)

        layout.addLayout(row4)

        # ── Notes ─────────────────────────────────────────────────────────────
        layout.addWidget(QLabel("Notes (optional)"))
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("e.g., Take with water")
        self.notes_input.setStyleSheet(STYLE)
        layout.addWidget(self.notes_input)

        # ── Add to list button ────────────────────────────────────────────────
        self.add_medicine_btn = QPushButton("+ Add Medicine to List")
        self.add_medicine_btn.setStyleSheet(BTN_PINK)
        self.add_medicine_btn.clicked.connect(self.add_medicine_to_list)
        layout.addWidget(self.add_medicine_btn)

        # ── Staged medicines table ────────────────────────────────────────────
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

        # ── Remove last / Cancel / Save ───────────────────────────────────────
        btn_row = QHBoxLayout()

        self.remove_btn = QPushButton("Remove Last")
        self.remove_btn.setStyleSheet(BTN_PLAIN)
        self.remove_btn.clicked.connect(self.remove_last_medicine)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(BTN_PLAIN)
        self.cancel_btn.clicked.connect(self.reject)

        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet(BTN_PLAIN)
        self.save_btn.clicked.connect(self.save)

        btn_row.addWidget(self.remove_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.save_btn)
        layout.addLayout(btn_row)

    # ─────────────────────────────────────────────
    #  DATA LOADING
    # ─────────────────────────────────────────────
    def load_staff(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT staff_id, first_name || ' ' || last_name
                FROM staff
                WHERE status = 'Active'
                ORDER BY last_name, first_name
            """)
            for staff_id, name in cursor.fetchall():
                self.staff_map[name] = staff_id
                self.prescribed_combo.addItem(name)
            cursor.close()
        except Exception as e:
            print(f"Staff load error: {e}")
        finally:
            conn.close()

    def load_medicine_suggestions(self):
        """
        Pull existing medicine names from the DB to power autocomplete.
        The field is still fully free-text — this just helps with common entries.
        If the medicine table is dropped, this method is safely skipped.
        """
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT medicine_name FROM medicine ORDER BY medicine_name"
            )
            names = [row[0] for row in cursor.fetchall()]
            cursor.close()

            if names:
                model = QStringListModel(names)
                self.medicine_completer.setModel(model)
        except Exception:
            # Table may not exist — autocomplete just won't suggest anything
            pass
        finally:
            conn.close()

    # ─────────────────────────────────────────────
    #  ACTIONS
    # ─────────────────────────────────────────────
    def add_medicine_to_list(self):
        medicine_name = self.medicine_input.text().strip()
        dosage        = self.dosage_input.text().strip()
        frequency     = self.frequency_input.text().strip()
        duration      = self.duration_input.text().strip()
        route         = self.route_input.text().strip()
        timing        = self.timing_input.text().strip()
        notes         = self.notes_input.text().strip()

        if not medicine_name:
            QMessageBox.warning(self, "Missing Field", "Please enter a medicine name.")
            return
        if not dosage or not frequency or not duration:
            QMessageBox.warning(self, "Missing Fields",
                                "Please fill in Dosage, Frequency, and Duration.")
            return

        self.medicines.append({
            "medicine_name": medicine_name,
            "dosage":    dosage,
            "frequency": frequency,
            "duration":  duration,
            "route":     route,
            "timing":    timing,
            "notes":     notes,
        })

        row = self.medicine_table.rowCount()
        self.medicine_table.insertRow(row)
        for col, val in enumerate([medicine_name, dosage, frequency,
                                    duration, route, timing]):
            item = QTableWidgetItem(val)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.medicine_table.setItem(row, col, item)

        # Clear fields for next entry
        self.medicine_input.clear()
        self.dosage_input.clear()
        self.frequency_input.clear()
        self.duration_input.clear()
        self.route_input.clear()
        self.timing_input.clear()
        self.notes_input.clear()
        self.medicine_input.setFocus()

    def remove_last_medicine(self):
        if not self.medicines:
            return
        self.medicines.pop()
        self.medicine_table.removeRow(self.medicine_table.rowCount() - 1)

    def save(self):
        if not self.medicines:
            QMessageBox.warning(self, "No Medicines",
                                "Please add at least one medicine.")
            return

        staff_name = self.prescribed_combo.currentText()
        staff_id   = self.staff_map.get(staff_name)
        presc_date = self.date_input.date().toPyDate()

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
                        patient_id, medicine_name, prescribed_by,
                        dosage, frequency, duration,
                        prescription_date, notes, route, timing
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    self.patient_id,
                    med["medicine_name"],
                    staff_id,
                    med["dosage"],
                    med["frequency"],
                    med["duration"],
                    presc_date,
                    med["notes"] or None,
                    med["route"]  or None,
                    med["timing"] or None,
                ))

            conn.commit()
            cursor.close()
            QMessageBox.information(self, "Success", "Prescription saved successfully!")
            self.accept()

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Failed to save:\n{e}")
        finally:
            conn.close()