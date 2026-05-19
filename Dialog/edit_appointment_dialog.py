from PyQt6.QtWidgets import (
    QDialog, QMessageBox, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QTextEdit, QFrame
)
from PyQt6.QtCore import Qt
from database import get_connection
from datetime import date as dt_date


DIALOG_BG = """
    QDialog { background-color: #ECC6DC; }
    QLabel  { color: #15173D; font-size: 13px; border: none; }
    QComboBox, QTextEdit {
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


class EditAppointmentDialog(QDialog):
    def __init__(self, appointment_id, parent=None):
        super().__init__(parent)
        self.appointment_id = appointment_id
        self.staff_map      = {}   # staff_id → display name
        self.staff_id_map   = {}   # display name → staff_id  (for updated_by)
        self.current_staff_id = None

        self.setWindowTitle("Edit Appointment")
        self.setMinimumWidth(440)
        self.setStyleSheet(DIALOG_BG)
        self._setup_ui()
        self._load_staff()
        self._load_data()

    def _bold(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #15173D; font-size: 13px; font-weight: bold; border: none;")
        return lbl

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(24, 20, 24, 20)

        title = QLabel("Edit Appointment")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #15173D; border: none;")
        layout.addWidget(title)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #b08090;"); layout.addWidget(sep)

        # Read-only appointment info
        self.info_label = QLabel("")
        self.info_label.setStyleSheet(
            "border: 1px solid #c9a0ba; border-radius: 8px;"
            "padding: 8px; background: white; color: #15173D; font-size: 13px;"
        )
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        # Purposes (read-only display)
        self.purposes_label = QLabel("")
        self.purposes_label.setStyleSheet(
            "border: 1px solid #c9a0ba; border-radius: 8px;"
            "padding: 6px; background: white; color: #15173D; font-size: 12px;"
        )
        self.purposes_label.setWordWrap(True)
        layout.addWidget(self.purposes_label)

        sep2 = QFrame(); sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("color: #b08090;"); layout.addWidget(sep2)

        # ── Status ────────────────────────────────────────────────────────────
        layout.addWidget(self._bold("New Status *"))
        self.status_combo = QComboBox()
        self.status_combo.addItems([
            "Scheduled", "Completed", "Missed", "Cancelled", "Rescheduled"
        ])
        layout.addWidget(self.status_combo)

        # ── Reason for status change ──────────────────────────────────────────
        # This fills appointment_status_history.reason
        layout.addWidget(self._bold("Reason for Status Change"))
        self.reason_input = QTextEdit()
        self.reason_input.setFixedHeight(55)
        self.reason_input.setPlaceholderText(
            "e.g., Patient requested reschedule, No-show, etc. (optional)"
        )
        layout.addWidget(self.reason_input)

        # ── Updated by (which staff is making this change) ────────────────────
        # This fills appointment_status_history.updated_by
        layout.addWidget(self._bold("Updated By *"))
        self.updated_by_combo = QComboBox()
        layout.addWidget(self.updated_by_combo)

        # ── Remarks on appointment ────────────────────────────────────────────
        layout.addWidget(self._bold("Remarks (optional)"))
        self.remarks_input = QTextEdit()
        self.remarks_input.setFixedHeight(55)
        self.remarks_input.setPlaceholderText("General appointment notes…")
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

    # ── Loaders ───────────────────────────────────────────────────────────────
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
                self.staff_map[sid]   = name
                self.staff_id_map[name] = sid
                self.updated_by_combo.addItem(name)
            cur.close(); conn.close()
        except Exception as e:
            print(f"Staff load error: {e}")

    def _load_data(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()

            # Appointment + patient + staff info
            cur.execute("""
                SELECT pp.first_name || ' ' || pp.last_name,
                       a.appointment_date,
                       a.appointment_time,
                       a.appointment_type,
                       a.status,
                       a.remarks,
                       a.staff_id,
                       a.date_created
                FROM appointment a
                JOIN patient_profile pp ON a.patient_id = pp.patient_id
                WHERE a.appointment_id = %s
            """, (self.appointment_id,))
            data = cur.fetchone()

            # All purposes for this appointment
            cur.execute("""
                SELECT purpose FROM appointment_purpose
                WHERE appointment_id = %s
                ORDER BY purpose_id
            """, (self.appointment_id,))
            purposes = [r[0] for r in cur.fetchall()]

            cur.close(); conn.close()

            if not data:
                return

            date_str    = data[1].strftime("%B %d, %Y") if data[1] else ""
            time_str    = str(data[2])[:5] if data[2] else ""
            created_str = data[7].strftime("%B %d, %Y") if data[7] else ""
            staff_name  = self.staff_map.get(data[6], "Unknown")
            self.current_staff_id = data[6]

            self.info_label.setText(
                f"<b>Patient:</b> {data[0]}<br>"
                f"<b>Date:</b> {date_str} at {time_str}<br>"
                f"<b>Type:</b> {data[3]}&nbsp;&nbsp;"
                f"<b>Created:</b> {created_str}<br>"
                f"<b>Assigned Staff:</b> {staff_name}"
            )

            self.purposes_label.setText(
                "<b>Purposes:</b> " + (", ".join(purposes) if purposes else "—")
            )

            # Pre-select current status
            idx = self.status_combo.findText(data[4])
            if idx >= 0:
                self.status_combo.setCurrentIndex(idx)

            # Pre-fill remarks
            self.remarks_input.setPlainText(data[5] or "")

            # Default "Updated By" to the assigned staff if in the list
            assigned_display = self.staff_map.get(data[6])
            if assigned_display:
                idx2 = self.updated_by_combo.findText(assigned_display)
                if idx2 >= 0:
                    self.updated_by_combo.setCurrentIndex(idx2)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load:\n{e}")

    # ── Save ──────────────────────────────────────────────────────────────────
    def save(self):
        status       = self.status_combo.currentText()
        reason       = self.reason_input.toPlainText().strip() or None
        remarks      = self.remarks_input.toPlainText().strip() or None
        updated_by   = self.staff_id_map.get(self.updated_by_combo.currentText())

        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()

            # ── Update appointment ─────────────────────────────────────────────
            cur.execute("""
                UPDATE appointment
                SET status  = %s,
                    remarks = %s
                WHERE appointment_id = %s
            """, (status, remarks, self.appointment_id))

            # ── Log status change ──────────────────────────────────────────────
            # reason  → why the status changed (e.g. "Patient no-show")
            # updated_by → which staff member made this change
            cur.execute("""
                INSERT INTO appointment_status_history
                    (appointment_id, status, status_date, reason, updated_by)
                VALUES (%s, %s, %s, %s, %s)
            """, (self.appointment_id, status, dt_date.today(), reason, updated_by))

            conn.commit()
            cur.close()
            QMessageBox.information(self, "Success", "Appointment updated!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{e}")
        finally:
            try: conn.close()
            except Exception: pass