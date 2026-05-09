"""
appointments_module.py
======================
Connects all Appointments-related UI files:
  - appointments_main.py       → AppointmentsWindow  (main window)
  - completed_appointments.py  → CompletedAppointmentsWindow
  - new_appointment_dialog.py  → NewAppointmentDialog
  - date_dialog.py             → DateDialog

All windows are responsive (no fixed geometry).  Sidebar nav buttons are
wired so the caller can hook them to other modules.  Log-out is also exposed
as a signal.

Usage
-----
    from appointments_module import AppointmentsWindow

    window = AppointmentsWindow(db=your_db)
    window.nav_dashboard.connect(dashboard_window.show)
    window.nav_logout.connect(app.quit)
    window.showMaximized()

Database contract (optional)
-----------------------------
Pass any object that implements:
    .fetch_appointments(status="pending"|"completed") -> list[dict]
        dict keys: patient, date, time, status, visit_type, vital_signs, notes
    .save_appointment(patient, date, time, visit_type)
    .mark_appointment_complete(appt_dict)
"""

from __future__ import annotations

from PyQt6 import QtCore, QtGui, QtWidgets

from appointments_main      import Ui_MainWindow as _MainUI
from completed_appointments import Ui_MainWindow as _CompletedUI
from new_appointment_dialog import Ui_Dialog     as _NewApptUI
from date_dialog            import Ui_Dialog     as _DateUI


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  DateDialog                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════╝
class DateDialog(QtWidgets.QDialog):
    """Calendar picker. Access the chosen date via .selected_date (str)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_date: str = ""
        self.setWindowTitle("Select Date")
        self.setMinimumSize(341, 260)

        self.ui = _DateUI()
        self.ui.setupUi(self)

        # Replace fixed-geometry placement with a real layout
        self.ui.calendarWidget.setParent(None)
        self.ui.buttonBox.setParent(None)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        today = QtCore.QDate.currentDate()
        self.ui.calendarWidget.setMinimumDate(today)
        self.ui.calendarWidget.setSelectedDate(today)
        layout.addWidget(self.ui.calendarWidget, stretch=1)
        layout.addWidget(self.ui.buttonBox)

        self.ui.buttonBox.accepted.connect(self._on_accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def _on_accept(self):
        self.selected_date = self.ui.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        self.accept()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  NewAppointmentDialog                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════╝
class NewAppointmentDialog(QtWidgets.QDialog):
    """
    Dialog for adding a new appointment.
    Emits appointment_saved(patient, date, time, visit_type) on success.
    """

    appointment_saved = QtCore.pyqtSignal(str, str, str, str)

    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self._db = db
        self._selected_date: str = ""

        self.ui = _NewApptUI()
        self.ui.setupUi(self)
        self.setWindowTitle("New Appointment")
        self.setMinimumSize(400, 350)

        self.ui.pushButton_3.clicked.connect(self._pick_date)   # Select Date
        self.ui.pushButton.clicked.connect(self._save)          # Save
        self.ui.pushButton_2.clicked.connect(self.reject)       # Cancel

    def _pick_date(self):
        dlg = DateDialog(self)
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self._selected_date = dlg.selected_date
            self.ui.pushButton_3.setText(self._selected_date or "Select Date")

    def _save(self):
        patient    = self.ui.lineEdit.text().strip()
        date       = self._selected_date
        time       = self.ui.comboBox_2.currentText()
        visit_type = self.ui.comboBox.currentText()

        if not patient:
            QtWidgets.QMessageBox.warning(self, "Validation",
                                          "Please enter the patient's name.")
            return
        if not date:
            QtWidgets.QMessageBox.warning(self, "Validation",
                                          "Please select a date.")
            return

        if self._db is not None:
            try:
                self._db.save_appointment(patient, date, time, visit_type)
            except Exception as exc:
                QtWidgets.QMessageBox.critical(self, "Database Error", str(exc))
                return

        self.appointment_saved.emit(patient, date, time, visit_type)
        self.accept()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  CompletedAppointmentsWindow                                             ║
# ╚══════════════════════════════════════════════════════════════════════════╝
class CompletedAppointmentsWindow(QtWidgets.QMainWindow):
    """
    Full-screen window showing completed appointments with a detail panel.
    """

    nav_dashboard = QtCore.pyqtSignal()
    nav_patient_records = QtCore.pyqtSignal()
    nav_prenatal = QtCore.pyqtSignal()
    nav_appointments = QtCore.pyqtSignal()
    nav_logout = QtCore.pyqtSignal()
    request_new_appointment = QtCore.pyqtSignal()
    followup_saved = QtCore.pyqtSignal(str, str, str, str)

    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self._db = db
        self._appointments = []

        self._current_selected_row = -1
        self._details_visible = False

        self.ui = _CompletedUI()
        self.ui.setupUi(self)

        self.setWindowTitle("MaternaDB — Completed Appointments")

        # ── Table behavior ─────────────────────────────
        self.ui.left_prescription_date_and_purpose.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.ui.left_prescription_date_and_purpose.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )

        # ── SCROLL ENABLED (IMPORTANT) ─────────────────
        self.ui.left_prescription_date_and_purpose.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.ui.left_prescription_date_and_purpose.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # ── hide details initially ─────────────────────
        self._hide_details_panel()

        # ── Sidebar nav ────────────────────────────────
        self.ui.pushButton.clicked.connect(self.nav_dashboard)
        self.ui.pushButton_2.clicked.connect(self.nav_patient_records)
        self.ui.pushButton_3.clicked.connect(self.nav_prenatal)
        self.ui.pushButton_4.clicked.connect(self.nav_appointments)
        self.ui.pushButton_5.clicked.connect(self.nav_logout)

        # ── Top buttons ────────────────────────────────
        self.ui.pushButton_7.clicked.connect(self._back_to_appointments)
        self.ui.pushButton_6.clicked.connect(self.request_new_appointment)

        # ── Detail buttons ─────────────────────────────
        self.ui.pushButton_8.clicked.connect(self._schedule_followup)
        self.ui.pushButton_9.clicked.connect(self._view_full_record)

    # ───────────────────────────────────────────────
    # DATA LOADING
    # ───────────────────────────────────────────────
    def load_appointments(self):
        if self._db is not None:
            try:
                self._appointments = self._db.fetch_appointments(status="completed")
            except Exception:
                self._appointments = []
        self._populate_table()

    def _populate_table(self):
        tbl = self.ui.left_prescription_date_and_purpose
        tbl.setColumnCount(5)  # Patient, Date, Time, Status, Action
        tbl.setHorizontalHeaderLabels(["Patient", "Date", "Time", "Status", "Action"])
        tbl.setRowCount(0)

        header = tbl.horizontalHeader()

        header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )

        for row_idx, appt in enumerate(self._appointments):
            tbl.insertRow(row_idx)

            # Add data columns
            for col_idx, key in enumerate(
                    ["patient", "date", "time", "status"]
            ):
                item = QtWidgets.QTableWidgetItem(
                    str(appt.get(key, ""))
                )

                # Center alignment
                item.setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter
                )

                # Make patient name bold
                if key == "patient":
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)

                tbl.setItem(row_idx, col_idx, item)

            # Add "View" button in Action column (index 4)
            view_btn = QtWidgets.QPushButton("View")
            view_btn.setStyleSheet(
                "background-color: rgb(106, 27, 154);"
                "color: white;"
                "border-radius: 8px;"
                "padding: 4px 10px;"
                "font-weight: bold;"
            )
            view_btn.clicked.connect(lambda checked, r=row_idx: self._toggle_details(r))
            tbl.setCellWidget(row_idx, 4, view_btn)

    def _toggle_details(self, row):
        """Toggle the details panel when View button is clicked"""
        if row < 0 or row >= len(self._appointments):
            return

        # If same row is clicked and details are visible, HIDE them
        if row == self._current_selected_row and self._details_visible:
            self._hide_details_panel()
            self._current_selected_row = -1
            self._details_visible = False
            return

        # Otherwise, show details for the clicked row
        self._current_selected_row = row
        self._details_visible = True
        self._show_details_panel()

        appt = self._appointments[row]

        self.ui.label_3.setText(f"<b>Patient:</b>  {appt.get('patient', '')}")
        self.ui.label_4.setText(f"<b>Date:</b>  {appt.get('date', '')}")
        self.ui.label_5.setText(f"<b>Type of Visit:</b>  {appt.get('visit_type', '')}")
        self.ui.label_6.setText(f"<b>Time:</b>  {appt.get('time', '')}")

        self.ui.textEdit.setPlainText(appt.get("vital_signs", ""))
        self.ui.textEdit_2.setPlainText(appt.get("notes", ""))

    # ───────────────────────────────────────────────
    # PANEL VISIBILITY
    # ───────────────────────────────────────────────
    def _hide_details_panel(self):
        self.ui.groupBox.hide()
        self.ui.widget.hide()
        self.ui.widget_5.hide()

    def _show_details_panel(self):
        self.ui.groupBox.show()
        self.ui.widget.show()
        self.ui.widget_5.show()

    # ───────────────────────────────────────────────
    # NAVIGATION
    # ───────────────────────────────────────────────
    def _back_to_appointments(self):
        self.nav_appointments.emit()

    # ───────────────────────────────────────────────
    # ACTIONS
    # ───────────────────────────────────────────────
    def _schedule_followup(self):
        if self._current_selected_row < 0 or self._current_selected_row >= len(self._appointments):
            QtWidgets.QMessageBox.information(
                self, "Schedule Follow-up", "Please select an appointment first."
            )
            return

        appt = self._appointments[self._current_selected_row]

        dlg = NewAppointmentDialog(self, self._db)
        dlg.ui.lineEdit.setText(appt.get("patient", ""))

        # Connect to the dialog's appointment_saved signal
        # This signal is emitted AFTER the dialog saves to database
        dlg.appointment_saved.connect(self._on_followup_scheduled)
        dlg.exec()

    def _on_followup_scheduled(self, patient, date, time, visit_type):
        """Handle followup scheduling - the dialog has already saved to DB"""
        # Just emit the signal to update the main window's UI
        # DO NOT show popup here - let the main window handle it
        self.followup_saved.emit(patient, date, time, visit_type)
        # REMOVED the QMessageBox from here to avoid duplicate popups

    def _view_full_record(self):
        if self._current_selected_row < 0 or self._current_selected_row >= len(self._appointments):
            QtWidgets.QMessageBox.information(
                self, "View Full Record", "Please select an appointment first."
            )
            return

        appt = self._appointments[self._current_selected_row]

        QtWidgets.QMessageBox.information(
            self,
            "Full Record",
            f"Patient: {appt.get('patient', '')}\n"
            f"Date: {appt.get('date', '')}\n"
            f"Time: {appt.get('time', '')}\n"
            f"Type of Visit: {appt.get('visit_type', '')}\n"
            f"Status: {appt.get('status', '')}\n\n"
            f"Vital Signs:\n{appt.get('vital_signs', '')}\n\n"
            f"Notes:\n{appt.get('notes', '')}"
        )


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  AppointmentsWindow  — main entry point                                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝
class AppointmentsWindow(QtWidgets.QMainWindow):
    """
    Main Appointments screen.  Wire the nav_* signals to your other modules.

    Signals
    -------
    nav_dashboard, nav_patient_records, nav_prenatal
        Emitted when the corresponding sidebar button is clicked.
    nav_logout
        Emitted when Log out is clicked.
    """

    nav_dashboard = QtCore.pyqtSignal()
    nav_patient_records = QtCore.pyqtSignal()
    nav_prenatal = QtCore.pyqtSignal()
    nav_logout = QtCore.pyqtSignal()

    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self._db = db
        self._appointments: list[dict] = []

        self.ui = _MainUI()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB — Appointments")

        # ── Sidebar nav ───────────────────────────────────────────────────
        self.ui.pushButton.clicked.connect(self.nav_dashboard)
        self.ui.pushButton_2.clicked.connect(self.nav_patient_records)
        self.ui.pushButton_3.clicked.connect(self.nav_prenatal)
        self.ui.pushButton_4.clicked.connect(self._noop)  # already here
        self.ui.pushButton_5.clicked.connect(self.nav_logout)

        # ── Top-bar buttons ───────────────────────────────────────────────
        self.ui.pushButton_6.clicked.connect(self._open_new_appointment)
        self.ui.pushButton_7.clicked.connect(self._go_to_completed)

        self._completed_window = CompletedAppointmentsWindow(db=self._db)
        self._completed_window.nav_dashboard.connect(self.nav_dashboard)
        self._completed_window.nav_patient_records.connect(self.nav_patient_records)
        self._completed_window.nav_prenatal.connect(self.nav_prenatal)
        self._completed_window.nav_logout.connect(self.nav_logout)
        self._completed_window.nav_appointments.connect(self._return_from_completed)
        self._completed_window.request_new_appointment.connect(self._open_new_appointment_from_completed)
        # IMPORTANT: Connect followup_saved to add appointment
        self._completed_window.followup_saved.connect(self._on_followup_saved)

        self.load_appointments()

    # ── Public API ────────────────────────────────────────────────────────
    def load_appointments(self):
        """Fetch pending appointments from db and refresh table."""
        if self._db is not None:
            try:
                self._appointments = self._db.fetch_appointments(status="pending")
            except Exception:
                self._appointments = []
        self._populate_table()

    def add_appointment(self, patient: str, date: str, time: str, visit_type: str, save_to_db: bool = True):
        """
        Add one appointment row.

        Args:
            save_to_db: If True, save to database first (default: True)
                       If False, assume already saved (for follow-ups)
        """
        # Save to database only if requested
        if save_to_db and self._db is not None:
            try:
                self._db.save_appointment(patient, date, time, visit_type)
            except Exception as exc:
                QtWidgets.QMessageBox.critical(self, "Database Error", str(exc))
                return

        new_appt = {
            "patient": patient,
            "date": date,
            "time": time,
            "status": "Upcoming",
            "visit_type": visit_type,
            "vital_signs": "",
            "notes": ""
        }

        self._appointments.append(new_appt)

        self._populate_table()

    # ── Private ───────────────────────────────────────────────────────────
    def _populate_table(self):
        tbl = self.ui.left_prescription_date_and_purpose
        tbl.setColumnCount(5)
        tbl.setHorizontalHeaderLabels(
            ["Patient", "Date", "Time", "Status", "Action"]
        )
        tbl.setRowCount(0)

        header = tbl.horizontalHeader()

        # Make columns evenly distributed
        header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )

        # Remove duplicates
        unique_appointments = []
        seen = set()

        for appt in self._appointments:
            key = (appt['patient'], appt['date'], appt['time'])
            if key not in seen:
                seen.add(key)
                unique_appointments.append(appt)

        self._appointments = unique_appointments

        # Sort by date first, then by time — soonest appointment on top
        import datetime

        def _sort_key(appt):
            try:
                date = datetime.date.fromisoformat(appt.get("date", "9999-12-31"))
            except ValueError:
                date = datetime.date(9999, 12, 31)
            try:
                time = datetime.datetime.strptime(appt.get("time", "11:59 PM"), "%I:%M %p").time()
            except ValueError:
                time = datetime.time(23, 59)
            return (date, time)

        self._appointments.sort(key=_sort_key)

        # Populate rows
        for row_idx, appt in enumerate(self._appointments):

            tbl.insertRow(row_idx)

            for col_idx, key in enumerate(
                    ["patient", "date", "time", "status"]
            ):
                item = QtWidgets.QTableWidgetItem(
                    str(appt.get(key, ""))
                )

                # Center alignment
                item.setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter
                )

                # Make patient name bold
                if key == "patient":
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)

                tbl.setItem(row_idx, col_idx, item)

            # Action column: Edit button
            btn = QtWidgets.QPushButton("Edit")

            btn.setStyleSheet(
                "background-color: rgb(106, 27, 154);"
                "color: white;"
                "border-radius: 8px;"
                "padding: 4px 10px;"
                "font-weight: bold;"
            )

            btn.clicked.connect(
                lambda checked, r=row_idx: self._view_appointment(r)
            )

            tbl.setCellWidget(row_idx, 4, btn)

    def _noop(self):
        pass

    def _open_new_appointment(self):
        dlg = NewAppointmentDialog(self, self._db)
        dlg.appointment_saved.connect(self._on_appointment_saved)
        dlg.exec()

    def _on_appointment_saved(self, patient, date, time, visit_type):
        # New appointment from dialog - the dialog already saved to DB
        # Pass save_to_db=False to prevent double-saving
        self.add_appointment(patient, date, time, visit_type, save_to_db=False)
        QtWidgets.QMessageBox.information(
            self, "Appointment Saved",
            f"Appointment for {patient} on {date} at {time} has been saved."
        )

    def _view_appointment(self, row_idx: int):
        if row_idx < 0 or row_idx >= len(self._appointments):
            return

        appt = self._appointments[row_idx]

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Appointment Details")
        dialog.resize(400, 350)  # Keep original size
        dialog.setModal(True)

        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setSpacing(15)  # Add space between elements (was default ~5)
        layout.setContentsMargins(15, 15, 15, 15)  # Add margins

        # Show all appointment details
        info = QtWidgets.QLabel(
            f"""
            <b>Patient:</b> {appt['patient']}<br>
            <b>Date:</b> {appt['date']}<br>
            <b>Type of Visit:</b> {appt['visit_type']}<br>
            <b>Time:</b> {appt['time']}<br>
            <b>Status:</b> {appt['status']}
            """
        )
        info.setWordWrap(True)
        info.setStyleSheet("padding: 5px; font-size: 11pt; line-height: 1.6;")

        layout.addWidget(info)

        # Add some spacing
        layout.addSpacing(10)

        status_combo = QtWidgets.QComboBox()
        status_combo.addItems(["Upcoming", "Arrived", "Completed"])
        status_combo.setCurrentText(appt["status"])
        status_combo.setStyleSheet("padding: 6px;")

        layout.addWidget(status_combo)

        layout.addSpacing(10)

        save_btn = QtWidgets.QPushButton("Save")
        save_btn.setStyleSheet(
            "background-color: rgb(106, 27, 154);"
            "color: white;"
            "padding: 8px;"
            "border-radius: 5px;"
            "font-weight: bold;"
        )
        layout.addWidget(save_btn)

        def save_changes():
            new_status = status_combo.currentText()
            appt["status"] = new_status

            # Move to completed page
            if new_status == "Completed":
                if self._db is not None:
                    try:
                        self._db.mark_appointment_complete(appt)
                    except Exception as exc:
                        QtWidgets.QMessageBox.critical(
                            self, "Database Error", str(exc)
                        )
                        return

                self._appointments.pop(row_idx)
                self._completed_window.load_appointments()

            self._populate_table()
            dialog.accept()

        save_btn.clicked.connect(save_changes)

        dialog.exec()

    def _go_to_completed(self):
        self._completed_window.load_appointments()
        self._completed_window.showMaximized()
        self.hide()

    def _return_from_completed(self):
        self._completed_window.hide()
        self.load_appointments()  # Refresh to show any new follow-ups
        self.showMaximized()

    def _open_new_appointment_from_completed(self):
        dlg = NewAppointmentDialog(self._completed_window, self._db)
        dlg.appointment_saved.connect(self._on_appointment_saved)
        dlg.exec()

    def _on_followup_saved(self, patient: str, date: str, time: str, visit_type: str):
        """Handle followup from completed appointments window"""
        # The follow-up dialog already saved to DB
        # Pass save_to_db=False to prevent double-saving
        self.add_appointment(patient, date, time, visit_type, save_to_db=False)
        QtWidgets.QMessageBox.information(
            self, "Follow-up Scheduled",
            f"Follow-up for {patient} on {date} at {time} has been scheduled."
        )

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  Standalone test / demo                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝
if __name__ == "__main__":
    import sys

    class _StubDB:
        """Minimal in-memory database for quick testing."""

        _pending = [
            {"patient": "Maria Santos",   "date": "2026-05-10", "time": "9:00 AM",
             "status": "Upcoming",   "visit_type": "Prenatal Care",
             "vital_signs": "",     "notes": ""},
            {"patient": "Ana Reyes",      "date": "2026-05-11", "time": "10:00 AM",
             "status": "Upcoming",   "visit_type": "General Check-up",
             "vital_signs": "",     "notes": ""},
        ]
        _completed = [
            {"patient": "Carlos Dela Cruz", "date": "2026-05-08", "time": "9:00 AM",
             "status": "Completed", "visit_type": "Consultation",
             "vital_signs": "BP 120/80\nHR 72 bpm", "notes": "Follow-up in 2 weeks"},
        ]

        def fetch_appointments(self, status="pending"):
            return list(self._pending if status == "pending" else self._completed)

        def save_appointment(self, patient, date, time, visit_type):
            self._pending.append({
                "patient": patient, "date": date, "time": time,
                "status": "Upcoming", "visit_type": visit_type,
                "vital_signs": "", "notes": "",
            })

        def mark_appointment_complete(self, appt):
            appt["status"] = "Completed"
            if appt in self._pending:
                self._pending.remove(appt)
            self._completed.append(appt)

    app = QtWidgets.QApplication(sys.argv)

    db  = _StubDB()
    win = AppointmentsWindow(db=db)

    win.nav_dashboard.connect(lambda: print("→ Dashboard"))
    win.nav_patient_records.connect(lambda: print("→ Patient Records"))
    win.nav_prenatal.connect(lambda: print("→ Prenatal Care"))
    win.nav_logout.connect(lambda: (print("→ Log out"), app.quit()))

    win.showMaximized()
    sys.exit(app.exec())