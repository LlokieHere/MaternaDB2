from PyQt6.QtWidgets import (
    QDialog, QMessageBox, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QDateEdit,
    QComboBox, QTextEdit, QFrame, QWidget
)
from PyQt6.QtCore import QDate, Qt
from database import get_connection
from datetime import date as dt_date, datetime


DIALOG_BG = """
    QDialog { background-color: #ECC6DC; }
    QLabel  { color: #15173D; font-size: 13px; border: none; }
    QLineEdit, QComboBox, QDateEdit, QTextEdit {
        border: 1px solid #15173D; border-radius: 8px;
        padding: 5px 10px; background-color: white;
        color: #15173D; font-size: 13px;
    }
"""
BTN_SAVE = (
    "QPushButton { background-color: #9C27B0; color: white; border-radius: 15px;"
    "padding: 8px 20px; font-size: 13px; font-weight: bold; border: none; }"
    "QPushButton:hover { background-color: #7B1FA2; }"
)
BTN_CANCEL = (
    "QPushButton { background-color: white; color: black; border-radius: 15px;"
    "padding: 8px 20px; font-size: 13px; border: none; }"
    "QPushButton:hover { background-color: #f0f0f0; }"
)
BTN_ADD = (
    "QPushButton { background-color: #854E6B; color: white; border-radius: 15px;"
    "padding: 4px 14px; font-size: 12px; font-weight: bold; border: none; }"
    "QPushButton:hover { background-color: #6d3d57; }"
)
BTN_REMOVE = (
    "QPushButton { background-color: #f5c2c2; color: #8b0000; border-radius: 6px;"
    "padding: 2px 8px; font-size: 11px; border: none; }"
    "QPushButton:hover { background-color: #e8a0a0; }"
)


class AddAppointmentDialog(QDialog):
    def __init__(self, appointment_type=None, parent=None):
        super().__init__(parent)
        self.preset_type    = appointment_type
        self.staff_map      = {}
        self.patient_map    = {}
        self.purpose_inputs = []

        self.setWindowTitle("New Appointment")
        self.setMinimumWidth(460)
        self.setStyleSheet(DIALOG_BG)
        self._setup_ui()
        self._load_patients()
        self._load_staff()

    def _bold(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #15173D; font-size: 13px; font-weight: bold; border: none;")
        return lbl

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(24, 20, 24, 20)

        title = QLabel("New Appointment")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #15173D; border: none;")
        layout.addWidget(title)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #b08090;"); layout.addWidget(sep)

        # Patient
        layout.addWidget(self._bold("Patient *"))
        self.patient_combo = QComboBox()
        layout.addWidget(self.patient_combo)

        # Staff
        layout.addWidget(self._bold("Staff / Doctor *"))
        self.staff_combo = QComboBox()
        layout.addWidget(self.staff_combo)

        # Date + Time (side by side)
        dt_row = QHBoxLayout()

        date_col = QVBoxLayout()
        date_col.addWidget(self._bold("Date *"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("MMMM dd, yyyy")
        date_col.addWidget(self.date_input)
        dt_row.addLayout(date_col)

        time_col = QVBoxLayout()
        time_col.addWidget(self._bold("Time *"))
        self.time_combo = QComboBox()
        self.time_combo.addItems([
            "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM",
            "11:00 AM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM"
        ])
        time_col.addWidget(self.time_combo)
        dt_row.addLayout(time_col)
        layout.addLayout(dt_row)

        # Appointment Type
        layout.addWidget(self._bold("Type of Visit *"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Scheduled", "Walk-in", "Follow-up"])
        if self.preset_type:
            idx = self.type_combo.findText(self.preset_type)
            if idx >= 0:
                self.type_combo.setCurrentIndex(idx)
        layout.addWidget(self.type_combo)

        # ── Purposes (multiple rows) ──────────────────────────────────────────
        ph_row = QHBoxLayout()
        ph_row.addWidget(self._bold("Purposes *"))
        ph_row.addStretch()
        add_btn = QPushButton("+ Add Purpose")
        add_btn.setStyleSheet(BTN_ADD)
        add_btn.setFixedHeight(26)
        add_btn.clicked.connect(lambda checked: self._add_purpose_row())
        ph_row.addWidget(add_btn)
        layout.addLayout(ph_row)

        self.purposes_widget = QWidget()
        self.purposes_widget.setStyleSheet("background: transparent;")
        self.purposes_layout = QVBoxLayout(self.purposes_widget)
        self.purposes_layout.setContentsMargins(0, 0, 0, 0)
        self.purposes_layout.setSpacing(5)
        layout.addWidget(self.purposes_widget)

        self._add_purpose_row()   # start with one row

        # ── Remarks ───────────────────────────────────────────────────────────
        layout.addWidget(self._bold("Remarks (optional)"))
        self.remarks_input = QTextEdit()
        self.remarks_input.setFixedHeight(55)
        self.remarks_input.setPlaceholderText("Any additional notes…")
        layout.addWidget(self.remarks_input)

        # ── Buttons ───────────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(BTN_SAVE)
        save_btn.setDefault(True)
        save_btn.clicked.connect(self.save)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(BTN_CANCEL)
        cancel_btn.clicked.connect(self.reject)

        btn_row.addWidget(save_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

    def _add_purpose_row(self, text="", checked=False):
        if isinstance(text, bool):
            text = ""

        row_w = QWidget()
        row_w.setStyleSheet("background: transparent;")
        row_l = QHBoxLayout(row_w)
        row_l.setContentsMargins(0, 0, 0, 0)
        row_l.setSpacing(5)

        inp = QLineEdit()
        inp.setPlaceholderText("e.g., Prenatal Check-up")
        inp.setText(text)
        self.purpose_inputs.append(inp)
        row_l.addWidget(inp)

        rem = QPushButton("✕")
        rem.setStyleSheet(BTN_REMOVE)
        rem.setFixedSize(26, 26)
        rem.clicked.connect(lambda _, rw=row_w, i=inp: self._remove_purpose_row(rw, i))
        row_l.addWidget(rem)

        self.purposes_layout.addWidget(row_w)

    def _remove_purpose_row(self, row_w, inp):
        if len(self.purpose_inputs) <= 1:
            QMessageBox.warning(self, "Warning", "At least one purpose is required.")
            return
        self.purpose_inputs.remove(inp)
        row_w.setParent(None)
        row_w.deleteLater()

    # ── DB loaders ────────────────────────────────────────────────────────────
    def _load_patients(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT patient_id,
                       first_name || ' ' || COALESCE(middle_name || ' ', '') || last_name
                FROM patient_profile
                ORDER BY last_name, first_name
            """)
            for pid, name in cur.fetchall():
                self.patient_map[name] = pid
                self.patient_combo.addItem(name)
            cur.close(); conn.close()
        except Exception as e:
            print(f"Patient load error: {e}")

    def _load_staff(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT staff_id,
                       first_name || ' ' || last_name || ' (' || role || ')'
                FROM staff
                WHERE status = 'Active'
                ORDER BY last_name, first_name
            """)
            for sid, name in cur.fetchall():
                self.staff_map[name] = sid
                self.staff_combo.addItem(name)
            cur.close(); conn.close()
        except Exception as e:
            print(f"Staff load error: {e}")

    def _parse_time(self):
        time_str = self.time_combo.currentText().strip()
        try:
            return datetime.strptime(time_str, "%I:%M %p").time()
        except ValueError:
            return datetime.strptime("9:00 AM", "%I:%M %p").time()

    # ── Save ──────────────────────────────────────────────────────────────────
    def save(self):
        patient_id = self.patient_map.get(self.patient_combo.currentText())
        staff_id   = self.staff_map.get(self.staff_combo.currentText())
        appt_date  = self.date_input.date().toPyDate()
        appt_time  = self._parse_time()
        appt_type  = self.type_combo.currentText()
        remarks    = self.remarks_input.toPlainText().strip() or None
        purposes   = [i.text().strip() for i in self.purpose_inputs if i.text().strip()]

        if not patient_id:
            QMessageBox.warning(self, "Missing", "Please select a patient."); return
        if not staff_id:
            QMessageBox.warning(self, "Missing", "Please select a staff member."); return
        if not purposes:
            QMessageBox.warning(self, "Missing", "Please enter at least one purpose."); return

        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()

            # ── appointment ───────────────────────────────────────────────────
            cur.execute("""
                INSERT INTO appointment (
                    patient_id, staff_id,
                    appointment_date, appointment_time,
                    appointment_type, status,
                    date_created, remarks
                ) VALUES (%s, %s, %s, %s, %s, 'Scheduled', %s, %s)
                RETURNING appointment_id
            """, (patient_id, staff_id, appt_date, appt_time,
                  appt_type, dt_date.today(), remarks))

            appointment_id = cur.fetchone()[0]

            # ── appointment_purpose — one row per purpose ─────────────────────
            for p in purposes:
                cur.execute("""
                    INSERT INTO appointment_purpose (appointment_id, purpose)
                    VALUES (%s, %s)
                """, (appointment_id, p))

            # ── appointment_status_history ────────────────────────────────────
            # reason = None on initial scheduling (nothing to explain yet)
            # updated_by = staff_id who is creating the appointment
            cur.execute("""
                INSERT INTO appointment_status_history
                    (appointment_id, status, status_date, reason, updated_by)
                VALUES (%s, 'Scheduled', %s, %s, %s)
            """, (appointment_id, dt_date.today(), None, staff_id))

            conn.commit()
            cur.close()
            QMessageBox.information(self, "Success", "Appointment saved!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{e}")
        finally:
            try: conn.close()
            except Exception: pass