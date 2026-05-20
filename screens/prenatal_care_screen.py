from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTimeEdit, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame, QDialog, QFormLayout, QLineEdit,
    QComboBox, QDateEdit, QSizePolicy, QTableWidget, QTableWidgetItem,
    QHeaderView, QTextEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QPainter, QColor, QBrush, QPen, QFont

from screens.prenatal_care_ui import Ui_PrenatalCareScreen
from database import get_connection
import user_profile.session as session


# shared field/button styles so every dialog looks the same
FIELD_STYLE = """
    border: 1px solid rgb(158, 136, 163);
    border-radius: 6px;
    padding: 5px 8px;
    background-color: rgb(247, 247, 247);
    color: rgb(21, 23, 61);
    font-size: 12px;
"""
COMBO_STYLE = """
    QComboBox {
        background-color: rgb(247,247,247);
        border: 1px solid rgb(158,136,163);
        border-radius: 6px;
        padding: 5px 8px;
        color: rgb(21,23,61);
        font-size: 12px;
    }
    QComboBox QAbstractItemView {
        background-color: rgb(247,247,247);
        color: rgb(21,23,61);
        selection-background-color: rgb(192,116,182);
    }
"""
BTN_PRIMARY = """
    QPushButton {
        background-color: rgb(21,23,61); color: white;
        border: none; border-radius: 8px;
        padding: 7px 18px; font-size: 12px; font-weight: bold;
    }
    QPushButton:hover { background-color: rgb(192,116,182); }
"""
BTN_SECONDARY = """
    QPushButton {
        background-color: rgb(240,230,240); color: rgb(21,23,61);
        border: 1px solid rgb(158,136,163); border-radius: 8px;
        padding: 7px 18px; font-size: 12px;
    }
    QPushButton:hover { background-color: rgb(220,200,220); }
"""
BTN_DANGER = """
    QPushButton {
        background-color: rgb(200,50,50); color: white;
        border: none; border-radius: 8px;
        padding: 7px 18px; font-size: 12px;
    }
    QPushButton:hover { background-color: rgb(170,30,30); }
"""
LBL_STYLE = "color: rgb(21,23,61); font-size: 12px;"
CARD_STYLE = """
    QFrame {
        background-color: rgb(236,198,220);
        border-radius: 12px;
        border: 1px solid rgb(210,177,200);
    }
"""


def fmt_date(d):
    try:
        if hasattr(d, "strftime"):
            return d.strftime("%B %d, %Y")
        from datetime import datetime
        return datetime.strptime(str(d), "%Y-%m-%d").strftime("%B %d, %Y")
    except Exception:
        return str(d) if d else "—"


# circle badge for prenatal visit cards
class CircleBadge(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self._text = text
        self.setFixedSize(50, 50)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QBrush(QColor(178, 100, 168)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(0, 0, 50, 50)
        p.setPen(QPen(QColor(255, 255, 255)))
        f = QFont("Segoe UI", 12)
        f.setBold(True)
        p.setFont(f)
        p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._text)


def ordinal(n):
    try:
        n = int(n)
        return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")
    except Exception:
        return str(n)


# ── shared base for all three add/edit dialogs ──────────────────────────────
class _BaseDialog(QDialog):
    def __init__(self, title_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title_text)
        self.setMinimumWidth(420)
        self.setStyleSheet("QDialog { background-color: rgb(240,230,240); }")

        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(22, 22, 22, 22)
        self.root.setSpacing(14)

        title = QLabel(title_text)
        title.setStyleSheet(
            "color: rgb(21,23,61); font-size: 15px;"
            "font-weight: bold; font-family: 'Arial Black';"
        )
        self.root.addWidget(title)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: rgb(210,180,210); max-height: 1px;")
        self.root.addWidget(sep)

        self.form = QFormLayout()
        self.form.setSpacing(10)
        self.root.addLayout(self.form)

    def _add_buttons(self, on_save):
        row = QHBoxLayout()
        row.addStretch()
        btn_c = QPushButton("Cancel")
        btn_c.setStyleSheet(BTN_SECONDARY)
        btn_c.clicked.connect(self.reject)
        btn_s = QPushButton("Save")
        btn_s.setStyleSheet(BTN_PRIMARY)
        btn_s.clicked.connect(on_save)
        row.addWidget(btn_c)
        row.addWidget(btn_s)
        self.root.addLayout(row)

    def _field(self, placeholder=""):
        w = QLineEdit()
        w.setPlaceholderText(placeholder)
        w.setStyleSheet(FIELD_STYLE)
        return w

    def _combo(self, items):
        w = QComboBox()
        w.addItems(items)
        w.setStyleSheet(COMBO_STYLE)
        return w

    def _date(self, default=None):
        w = QDateEdit()
        w.setCalendarPopup(True)
        w.setDate(default or QDate.currentDate())
        w.setStyleSheet(FIELD_STYLE)
        return w
    def _row(self, label, widget):
        lbl = QLabel(label)
        lbl.setStyleSheet(LBL_STYLE)
        self.form.addRow(lbl, widget)

    def _time(self, default=None):
        from PyQt6.QtCore import QTime
        w = QTimeEdit()
        w.setDisplayFormat("hh:mm AP")
        w.setTime(default or QTime.currentTime())
        w.setStyleSheet(FIELD_STYLE)
        return w


# ═══════════════════════════════════════════════════════════════════════════
# PRENATAL VISIT DIALOGS
# ═══════════════════════════════════════════════════════════════════════════

class PrenatalVisitDialog(_BaseDialog):
    PRESENTATIONS = ["Cephalic", "Breech", "Transverse"]  # removed Oblique
    RISKS = ["Low Risk", "Moderate Risk", "High Risk"]

    def __init__(self, pregnancy_id, next_num, existing=None, parent=None):
        verb = "Edit" if existing else "Record"
        super().__init__(f"{verb} Visit #{next_num if not existing else existing.get('visit_num', '?')}", parent)
        self.pregnancy_id = pregnancy_id
        self.next_num = next_num
        self.existing = existing
        self.staff_map = {}

        self.f_date  = self._date()
        self.f_aog   = self._field("e.g. 28")

        # ── staff dropdown (replaces the old free-text field) ──────────────
        self._staff_map = {}                  # "First Last (Role)" -> staff_id
        self.f_staff = self._combo([])        # start empty, fill below
        conn = get_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("""
                    SELECT staff_id,
                        CONCAT(first_name, ' ', last_name, ' (', role, ')')
                    FROM staff
                    WHERE status = 'Active'
                    ORDER BY last_name, first_name
                """)
                for sid, name in cur.fetchall():
                    self._staff_map[name] = sid
                    self.f_staff.addItem(name)
                conn.close()
            except Exception as e:
                print(f"staff load error: {e}")
                if conn: conn.close()
        # ───────────────────────────────────────────────────────────────────

        self.f_bp    = self._field("e.g. 120/80")
        self.f_wt    = self._field("e.g. 62.5")
        self.f_fht   = self._field("e.g. 144  (leave blank if N/A)")
        self.f_fh    = self._field("e.g. 28  (leave blank if N/A)")
        self.f_pres  = self._combo(self.PRESENTATIONS)
        self.f_risk  = self._combo(self.RISKS)

        for label, w in [
            ("Visit Date *",       self.f_date),
            ("AOG (weeks) *",      self.f_aog),
            ("Staff / Doctor *",   self.f_staff),   # now a dropdown
            ("Blood Pressure *",   self.f_bp),
            ("Weight (kg) *",      self.f_wt),
            ("FHT (bpm)",          self.f_fht),
            ("Fundal Height (cm)", self.f_fh),
            ("Presentation",       self.f_pres),
            ("Risk Assessment",    self.f_risk),
        ]:
            self._row(label, w)

        # pre-fill when editing an existing visit
        if existing:
            self.f_date.setDate(QDate.fromString(str(existing.get("visit_date", "")), "yyyy-MM-dd"))
            self.f_aog.setText(str(existing.get("aog_weeks", "")))

            # match the saved staff name back to the dropdown
            saved_staff = existing.get("staff", "")
            idx = self.f_staff.findText(saved_staff)
            if idx >= 0:
                self.f_staff.setCurrentIndex(idx)

            self.f_bp.setText(existing.get("bp", ""))
            self.f_wt.setText(str(existing.get("weight_kg", "")))
            self.f_fht.setText(str(existing.get("fht_bpm", "")) if existing.get("fht_bpm") else "")
            self.f_fh.setText(str(existing.get("fh_cm", ""))   if existing.get("fh_cm")   else "")
            idx = self.f_pres.findText(existing.get("presentation", ""))
            if idx >= 0: self.f_pres.setCurrentIndex(idx)
            idx = self.f_risk.findText(existing.get("risk_assessment", ""))
            if idx >= 0: self.f_risk.setCurrentIndex(idx)
        # ← called here, after all fields exist
        self._add_buttons(self._on_save)

        # set staff dropdown to existing value AFTER loading
        if existing and existing.get("staff"):
            idx = self.f_staff.findText(existing.get("staff", ""))
            if idx >= 0: self.f_staff.setCurrentIndex(idx)

    def _on_save(self):
        aog = self.f_aog.text().strip()
        bp  = self.f_bp.text().strip()
        wt  = self.f_wt.text().strip()
        staff_name = self.f_staff.currentText()
        staff_id   = self._staff_map.get(staff_name)

        if not all([aog, bp, wt, staff_id]):
            QMessageBox.warning(self, "Missing", "Please fill in all required (*) fields.")
            return
        try:
            aog_v = int(aog)
            wt_v  = float(wt)
        except ValueError:
            QMessageBox.warning(self, "Bad input", "AOG must be a whole number; weight must be numeric.")
            return

        fht = self.f_fht.text().strip()
        fh  = self.f_fh.text().strip()
        try:
            fht_v = int(fht)   if fht else None
            fh_v  = float(fh)  if fh  else None
        except ValueError:
            QMessageBox.warning(self, "Bad input", "FHT and FH must be numbers if provided.")
            return

        self.result_data = {
            "pregnancy_id":        self.pregnancy_id,
            "visit_num":           self.next_num if not self.existing else self.existing["visit_num"],
            "visit_date":          self.f_date.date().toString("yyyy-MM-dd"),
            "gestational_age_weeks": aog_v,          # ← corrected column name
            "staff_id":            staff_id,          # ← now included (NOT NULL)
            "staff":               staff_name,        # ← denormalized display copy
            "blood_pressure":      bp,                # ← corrected column name
            "weight_kg":           wt_v,
            "fht_bpm":             fht_v,
            "fh_cm":               fh_v,
            "presentation":        self.f_pres.currentText(),
            "risk_assessment":     self.f_risk.currentText(),
        }
        self.accept()

class DiagnosisDialog(QDialog):
    RISK_STYLES = {
        "Low Risk":      "background-color: rgb(220,240,220); color: rgb(30,100,30);",
        "Moderate Risk": "background-color: rgb(255,243,205); color: rgb(130,80,0);",
        "High Risk":     "background-color: rgb(255,220,220); color: rgb(150,30,30);",
    }

    def __init__(self, visit: dict, parent=None):
        super().__init__(parent)
        self.visit = visit
        self.setWindowTitle(f"Visit #{visit.get('visit_num', '?')} – Diagnosis")
        self.setMinimumWidth(420)
        self.setStyleSheet("QDialog { background-color: rgb(240,230,240); }")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QWidget()
        header.setStyleSheet("background-color: rgb(21,23,61);")
        header.setFixedHeight(72)
        h = QVBoxLayout(header)
        h.setContentsMargins(22, 12, 22, 12)
        t = QLabel(f"Visit #{self.visit.get('visit_num','?')} Diagnosis")
        t.setStyleSheet("color: white; font-size: 15px; font-weight: bold; font-family: 'Arial Black';")
        s = QLabel(f"{fmt_date(self.visit.get('visit_date',''))}  ·  AOG: {self.visit.get('aog_weeks','—')} Weeks  ·  {self.visit.get('staff','—')}")
        s.setStyleSheet("color: rgba(255,255,255,0.72); font-size: 10px;")
        h.addWidget(t); h.addWidget(s)
        layout.addWidget(header)

        body = QWidget()
        body.setStyleSheet("background-color: rgb(240,230,240);")
        b = QVBoxLayout(body)
        b.setContentsMargins(22, 18, 22, 22)
        b.setSpacing(12)

        def row(lbl, val):
            r = QHBoxLayout()
            l = QLabel(lbl); l.setFixedWidth(180)
            l.setStyleSheet("color: rgb(100,80,110); font-size: 11px;")
            v = QLabel(str(val) if val else "—")
            v.setStyleSheet("color: rgb(21,23,61); font-size: 12px; font-weight: bold;")
            r.addWidget(l); r.addWidget(v); r.addStretch()
            return r

        b.addLayout(row("Age of Gestation (AOG)", f"{self.visit.get('aog_weeks','—')} Weeks"))
        b.addLayout(row("Blood Pressure (BP)",    f"{self.visit.get('bp','—')} mmHg"))
        b.addLayout(row("Weight",                 f"{self.visit.get('weight_kg','—')} kg"))
        fht = self.visit.get("fht_bpm")
        b.addLayout(row("Fetal Heart Tone (FHT)", f"{fht} bpm" if fht else "—"))
        fh = self.visit.get("fh_cm")
        b.addLayout(row("Fundal Height (FH)",     f"{fh} cm" if fh else "—"))
        b.addLayout(row("Presentation",           self.visit.get("presentation","—")))
        b.addLayout(row("Staff / Attendant",      self.visit.get("staff","—")))

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: rgb(210,180,210); max-height: 1px;")
        b.addWidget(sep)

        risk = self.visit.get("risk_assessment", "Low Risk")
        rr = QHBoxLayout()
        rl = QLabel("Risk Assessment"); rl.setFixedWidth(180)
        rl.setStyleSheet("color: rgb(100,80,110); font-size: 11px;")
        chip = QLabel(f"  {risk}  ")
        chip.setStyleSheet(
            (self.RISK_STYLES.get(risk, "")) +
            " border-radius: 10px; padding: 3px 8px; font-size: 11px; font-weight: bold;"
        )
        rr.addWidget(rl); rr.addWidget(chip); rr.addStretch()
        b.addLayout(rr)

        b.addSpacing(6)
        btn = QPushButton("Close")
        btn.setFixedHeight(36)
        btn.setStyleSheet(BTN_PRIMARY)
        btn.clicked.connect(self.accept)
        b.addWidget(btn)
        layout.addWidget(body)


# ═══════════════════════════════════════════════════════════════════════════
# LAB & REFERRALS DIALOGS
# ═══════════════════════════════════════════════════════════════════════════

class LabReferralDialog(_BaseDialog):
    LAB_TYPES = [
        "CBC", "Pap Smear", "Urinalysis", "Blood Typing", "Blood Sugar (FBS)",
        "HbsAg", "HIV Test", "Syphilis Test", "STI Screening",
        "Ultrasound", "GCT", "OGTT", "Other"
    ]
    RESULTS = ["Pending", "Normal", "Abnormal", "Referred"]

    def __init__(self, pregnancy_id, existing=None, parent=None):
        super().__init__("Edit Lab / Referral" if existing else "Add Lab / Referral", parent)
        self.pregnancy_id = pregnancy_id
        self.existing = existing

        self.f_collection_date = self._date()
        self.f_date_sent       = self._date()
        self.f_result_date     = self._date()
        self.f_lab_name        = self._field("e.g. Materna Diagnostic Lab")
        self.f_test_name       = self._combo(self.LAB_TYPES)
        self.f_result          = self._combo(self.RESULTS)
        self.f_remarks         = QTextEdit()
        self.f_remarks.setFixedHeight(70)
        self.f_remarks.setPlaceholderText("Additional remarks...")
        self.f_remarks.setStyleSheet(FIELD_STYLE)

        self._row("Collection Date *", self.f_collection_date)
        self._row("Date Sent *",       self.f_date_sent)
        self._row("Result Date",       self.f_result_date)
        self._row("Lab / Facility *",  self.f_lab_name)
        self._row("Test Name *",       self.f_test_name)
        self._row("Result",            self.f_result)
        self._row("Remarks",           self.f_remarks)

        if existing:
            for field, col in [
                (self.f_collection_date, "collection_date"),
                (self.f_date_sent,       "date_sent"),
                (self.f_result_date,     "result_date"),
            ]:
                d = existing.get(col)
                if d:
                    field.setDate(QDate.fromString(str(d), "yyyy-MM-dd"))
            self.f_lab_name.setText(existing.get("lab_name", "") or "")
            idx = self.f_test_name.findText(existing.get("test_name", ""))
            if idx >= 0: self.f_test_name.setCurrentIndex(idx)
            idx = self.f_result.findText(existing.get("result", ""))
            if idx >= 0: self.f_result.setCurrentIndex(idx)
            self.f_remarks.setPlainText(existing.get("remarks", "") or "")

        self._add_buttons(self._on_save)

    def _on_save(self):
        lab_name  = self.f_lab_name.text().strip()
        test_name = self.f_test_name.currentText()
        if not lab_name:
            QMessageBox.warning(self, "Missing", "Lab / Facility name is required.")
            return
        self.result_data = {
            "pregnancy_id":    self.pregnancy_id,
            "collection_date": self.f_collection_date.date().toString("yyyy-MM-dd"),
            "date_sent":       self.f_date_sent.date().toString("yyyy-MM-dd"),
            "result_date":     self.f_result_date.date().toString("yyyy-MM-dd"),
            "lab_name":        lab_name,
            "test_name":       test_name,
            "result":          self.f_result.currentText(),
            "remarks":         self.f_remarks.toPlainText().strip() or None,
        }
        self.accept()


# ═══════════════════════════════════════════════════════════════════════════
# MEDICATION DIALOGS
# ═══════════════════════════════════════════════════════════════════════════

class MedicationDialog(_BaseDialog):
    ROUTES = ["Oral", "IV", "IM", "Topical", "Sublingual", "Other"]
    TIMINGS = ["Before meal", "After meal", "With meal", "Bedtime", "As needed"]

    def __init__(self, patient_id, existing=None, parent=None):
        super().__init__("Edit Medication" if existing else "Add Medication", parent)
        self.patient_id = patient_id
        self.existing   = existing

        self.f_name     = self._field("e.g. Ferrous Sulfate")
        self.f_dosage   = self._field("e.g. 325 mg")
        self.f_freq     = self._field("e.g. Once daily")
        self.f_duration = self._field("e.g. 7 days, 2 weeks")
        self.f_route    = self._combo(self.ROUTES)
        self.f_timing   = self._combo(self.TIMINGS)
        self.f_date     = self._date()
        self.f_notes    = self._field("Optional notes")

        # staff dropdown
        self._staff_map = {}
        self.f_staff = self._combo([])
        conn = get_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("""
                    SELECT staff_id,
                        CONCAT(first_name, ' ', last_name, ' (', role, ')')
                    FROM staff WHERE status = 'Active'
                    ORDER BY last_name, first_name
                """)
                for sid, name in cur.fetchall():
                    self._staff_map[name] = sid
                    self.f_staff.addItem(name)
                conn.close()
            except Exception as e:
                print(f"staff load error: {e}")
                if conn: conn.close()

        self._row("Medicine Name *",  self.f_name)
        self._row("Dosage *",         self.f_dosage)
        self._row("Frequency *",      self.f_freq)
        self._row("Duration *",       self.f_duration)
        self._row("Route",            self.f_route)
        self._row("Timing",           self.f_timing)
        self._row("Prescribed By *",  self.f_staff)
        self._row("Prescription Date", self.f_date)
        self._row("Notes",            self.f_notes)

        if existing:
            self.f_name.setText(existing.get("medicine_name", ""))
            self.f_dosage.setText(existing.get("dosage", ""))
            self.f_freq.setText(existing.get("frequency", ""))
            self.f_duration.setText(existing.get("duration", ""))
            idx = self.f_route.findText(existing.get("route", "") or "")
            if idx >= 0: self.f_route.setCurrentIndex(idx)
            idx = self.f_timing.findText(existing.get("timing", "") or "")
            if idx >= 0: self.f_timing.setCurrentIndex(idx)
            saved_staff = existing.get("staff_display", "")
            idx = self.f_staff.findText(saved_staff)
            if idx >= 0: self.f_staff.setCurrentIndex(idx)
            d = existing.get("prescription_date")
            if d: self.f_date.setDate(QDate.fromString(str(d), "yyyy-MM-dd"))
            self.f_notes.setText(existing.get("notes", "") or "")

        self._add_buttons(self._on_save)

    def _on_save(self):
        name     = self.f_name.text().strip()
        dosage   = self.f_dosage.text().strip()
        freq     = self.f_freq.text().strip()
        duration = self.f_duration.text().strip()
        staff_name = self.f_staff.currentText()
        staff_id   = self._staff_map.get(staff_name)

        if not all([name, dosage, freq, duration, staff_id]):
            QMessageBox.warning(self, "Missing",
                "Medicine name, dosage, frequency, duration, and prescriber are required.")
            return
        self.result_data = {
            "medicine_name":     name,
            "dosage":            dosage,
            "frequency":         freq,
            "duration":          duration,
            "route":             self.f_route.currentText(),
            "timing":            self.f_timing.currentText(),
            "staff_id":          staff_id,
            "staff_display":     staff_name,
            "prescription_date": self.f_date.date().toString("yyyy-MM-dd"),
            "notes":             self.f_notes.text().strip() or None,
        }
        self.accept()


# ═══════════════════════════════════════════════════════════════════════════
# DELIVERY & NEWBORN DIALOGS
# ═══════════════════════════════════════════════════════════════════════════

class DeliveryDialog(_BaseDialog):
    DELIVERY_TYPES   = ["Normal", "CS"]
    DELIVERY_OUTCOMES = ["Completed", "Referred"]
    BIRTH_OUTCOMES   = ["Live Birth", "Stillbirth"]

    def __init__(self, pregnancy_id, existing=None, parent=None):
        super().__init__("Edit Delivery Record" if existing else "Record Delivery", parent)
        self.pregnancy_id = pregnancy_id
        self.existing = existing

        # staff dropdown
        self._staff_map = {}
        self.f_staff = self._combo([])
        conn = get_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("""
                    SELECT staff_id,
                        CONCAT(first_name, ' ', last_name, ' (', role, ')')
                    FROM staff WHERE status = 'Active'
                    ORDER BY last_name, first_name
                """)
                for sid, name in cur.fetchall():
                    self._staff_map[name] = sid
                    self.f_staff.addItem(name)
                conn.close()
            except Exception as e:
                print(f"staff load error: {e}")
                if conn: conn.close()

        self.f_date          = self._date()
        self.f_time = self._time()
        self.f_type          = self._combo(self.DELIVERY_TYPES)
        self.f_outcome       = self._combo(self.DELIVERY_OUTCOMES)
        self.f_birth_outcome = self._combo(self.BIRTH_OUTCOMES)
        self.f_location      = self._field("e.g. Materna Clinic")
        self.f_referred_to   = self._field("e.g. Provincial Hospital (leave blank if none)")
        self.f_remarks       = self._field("Additional remarks")

        self._row("Delivery Date *",    self.f_date)
        self._row("Delivery Time *",    self.f_time)
        self._row("Staff / Attendant *", self.f_staff)
        self._row("Delivery Type",      self.f_type)
        self._row("Delivery Outcome *", self.f_outcome)
        self._row("Birth Outcome",      self.f_birth_outcome)
        self._row("Delivery Location *", self.f_location)
        self._row("Referred To",        self.f_referred_to)
        self._row("Remarks",            self.f_remarks)

        if existing:
            d = existing.get("delivery_date")
            if d: self.f_date.setDate(QDate.fromString(str(d), "yyyy-MM-dd"))
            from PyQt6.QtCore import QTime
            t = existing.get("delivery_time")
            if t:
                self.f_time.setTime(QTime.fromString(str(t)[:5], "HH:mm"))
            saved_staff = existing.get("staff_display", "")
            idx = self.f_staff.findText(saved_staff)
            if idx >= 0: self.f_staff.setCurrentIndex(idx)
            idx = self.f_type.findText(existing.get("delivery_type", ""))
            if idx >= 0: self.f_type.setCurrentIndex(idx)
            idx = self.f_outcome.findText(existing.get("delivery_outcome", ""))
            if idx >= 0: self.f_outcome.setCurrentIndex(idx)
            idx = self.f_birth_outcome.findText(existing.get("birth_outcome", ""))
            if idx >= 0: self.f_birth_outcome.setCurrentIndex(idx)
            self.f_location.setText(existing.get("delivery_location", "") or "")
            self.f_referred_to.setText(existing.get("referred_to", "") or "")
            self.f_remarks.setText(existing.get("remarks", "") or "")

        self._add_buttons(self._on_save)

    def _on_save(self):
        staff_name = self.f_staff.currentText()
        staff_id   = self._staff_map.get(staff_name)
        location   = self.f_location.text().strip()
        time_str = self.f_time.time().toString("HH:mm:ss")

        if not all([staff_id, location]):
            QMessageBox.warning(self, "Missing", "Staff, delivery time, and location are required.")
            return

        self.result_data = {
            "pregnancy_id":      self.pregnancy_id,
            "staff_id":          staff_id,
            "staff_display":     staff_name,
            "delivery_date":     self.f_date.date().toString("yyyy-MM-dd"),
            "delivery_time":     time_str,
            "delivery_type":     self.f_type.currentText(),
            "delivery_outcome":  self.f_outcome.currentText(),
            "birth_outcome":     self.f_birth_outcome.currentText(),
            "delivery_location": location,
            "referred_to":       self.f_referred_to.text().strip() or None,
            "remarks":           self.f_remarks.text().strip() or None,
        }
        self.accept()

class NewbornDialog(_BaseDialog):
    SEX = ["Male", "Female"]   # matches DB check constraint

    def __init__(self, delivery_id, pregnancy_id, delivery_time=None, existing=None, parent=None):
        super().__init__("Edit Newborn Record" if existing else "Record Newborn", parent)
        self.delivery_id  = delivery_id
        self.pregnancy_id = pregnancy_id
        self.existing     = existing

        self.f_last_name  = self._field("e.g. Santos")
        self.f_first_name = self._field("e.g. Baby Girl")
        self.f_dob        = self._date()
        self.f_tob        = self._time(delivery_time)   # QTimeEdit, defaults to delivery time
        self.f_sex        = self._combo(self.SEX)
        self.f_weight     = self._field("e.g. 3.2  (kg)")
        self.f_length     = self._field("e.g. 50  (cm)")
        self.f_apgar      = self._field("e.g. 8  (0-10)")

        self._row("Last Name *",       self.f_last_name)
        self._row("First Name *",      self.f_first_name)
        self._row("Date of Birth",     self.f_dob)
        self._row("Time of Birth *",   self.f_tob)
        self._row("Sex *",             self.f_sex)
        self._row("Weight (kg) *",     self.f_weight)
        self._row("Length (cm) *",     self.f_length)
        self._row("APGAR Score (0-10) *", self.f_apgar)

        if existing:
            self.f_last_name.setText(existing.get("baby_last_name", ""))
            self.f_first_name.setText(existing.get("baby_first_name", ""))
            d = existing.get("date_of_birth")
            if d: self.f_dob.setDate(QDate.fromString(str(d), "yyyy-MM-dd"))
            from PyQt6.QtCore import QTime
            t = existing.get("time_of_birth")
            if t:
                self.f_tob.setTime(QTime(t.hour, t.minute) if hasattr(t, 'hour') else QTime.fromString(str(t)[:5], "HH:mm"))
            idx = self.f_sex.findText(existing.get("sex", ""))
            if idx >= 0: self.f_sex.setCurrentIndex(idx)
            self.f_weight.setText(str(existing.get("birth_weight_kg", "")) if existing.get("birth_weight_kg") else "")
            self.f_length.setText(str(existing.get("birth_length_cm", "")) if existing.get("birth_length_cm") else "")
            self.f_apgar.setText(str(existing.get("apgar_score", "")) if existing.get("apgar_score") is not None else "")

        self._add_buttons(self._on_save)

    def _on_save(self):
        last  = self.f_last_name.text().strip()
        first = self.f_first_name.text().strip()
        tob = self.f_tob.time().toString("HH:mm:ss")
        wt    = self.f_weight.text().strip()
        ln    = self.f_length.text().strip()
        apgar = self.f_apgar.text().strip()

        if not all([last, first, wt, ln, apgar]):   # ← removed tob
            QMessageBox.warning(self, "Missing", "All required fields must be filled.")
            return
        try:
            wt_v    = float(wt)
            ln_v    = float(ln)
            apgar_v = int(apgar)
            if not (0 <= apgar_v <= 10):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Bad input", "Weight/length must be numbers; APGAR must be 0–10.")
            return

        self.result_data = {
            "delivery_id":     self.delivery_id,
            "pregnancy_id":    self.pregnancy_id,
            "baby_last_name":  last,
            "baby_first_name": first,
            "date_of_birth":   self.f_dob.date().toString("yyyy-MM-dd"),
            "time_of_birth":   tob,
            "sex":             self.f_sex.currentText(),
            "birth_weight_kg": wt_v,
            "birth_length_cm": ln_v,
            "apgar_score":     apgar_v,
        }
        self.accept()


# ═══════════════════════════════════════════════════════════════════════════
# VISIT CARD (prenatal visit tab)
# ═══════════════════════════════════════════════════════════════════════════

class VisitCard(QWidget):
    def __init__(self, visit: dict, on_view_diagnosis, on_edit, on_delete, parent=None):
        super().__init__(parent)
        self.visit = visit
        self.on_view_diagnosis = on_view_diagnosis
        self.on_edit = on_edit
        self.on_delete = on_delete
        self._build()

    def _build(self):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(4, 0, 4, 0)
        outer.setSpacing(12)

        badge = CircleBadge(f"V{self.visit.get('visit_num', '?')}")
        outer.addWidget(badge, alignment=Qt.AlignmentFlag.AlignTop)

        card = QFrame()
        card.setStyleSheet(CARD_STYLE)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(5)

        top = QHBoxLayout()
        aog = self.visit.get("aog_weeks", "?")
        num = self.visit.get("visit_num", "?")
        t = QLabel(f"{ordinal(num)} Prenatal Visit – AOG: {aog} Weeks")
        t.setStyleSheet("color: rgb(21,23,61); font-size: 13px; font-weight: bold; border: none;")

        btn_diag = QPushButton("View Diagnosis")
        btn_diag.setFixedHeight(28)
        btn_diag.setStyleSheet("""
            QPushButton {
                background-color: rgb(240,230,240); color: rgb(21,23,61);
                border: 1px solid rgb(21,23,61); border-radius: 6px;
                font-size: 11px; padding: 0 10px;
            }
            QPushButton:hover { background-color: rgb(21,23,61); color: white; }
        """)
        btn_diag.clicked.connect(lambda: self.on_view_diagnosis(self.visit))

        btn_edit = QPushButton("Edit")
        btn_edit.setFixedHeight(28)
        btn_edit.setStyleSheet("""
            QPushButton {
                background-color: rgb(192,116,182); color: white;
                border: none; border-radius: 6px; font-size: 11px; padding: 0 10px;
            }
            QPushButton:hover { background-color: rgb(160,80,150); }
        """)
        btn_edit.clicked.connect(lambda: self.on_edit(self.visit))

        btn_del = QPushButton("Delete")
        btn_del.setFixedHeight(28)
        btn_del.setStyleSheet("""
            QPushButton {
                background-color: rgb(200,50,50); color: white;
                border: none; border-radius: 6px; font-size: 11px; padding: 0 10px;
            }
            QPushButton:hover { background-color: rgb(160,30,30); }
        """)
        btn_del.clicked.connect(lambda: self.on_delete(self.visit))

        top.addWidget(t)
        top.addStretch()
        top.addWidget(btn_diag)
        top.addWidget(btn_edit)
        top.addWidget(btn_del)
        lay.addLayout(top)

        sub = QLabel(f"{fmt_date(self.visit.get('visit_date',''))}  |  {self.visit.get('staff','—')}")
        sub.setStyleSheet("color: rgb(80,60,90); font-size: 10px; border: none;")
        lay.addWidget(sub)

        stats = QHBoxLayout(); stats.setSpacing(20)
        def stat(k, v):
            l = QLabel(f"<b>{k}</b> {v}")
            l.setStyleSheet("color: rgb(21,23,61); font-size: 11px; border: none;")
            l.setTextFormat(Qt.TextFormat.RichText)
            return l
        stats.addWidget(stat("BP:", f"{self.visit.get('bp','—')} mmHg"))
        stats.addWidget(stat("Weight:", f"{self.visit.get('weight_kg','—')} kg"))
        fht = self.visit.get("fht_bpm")
        if fht: stats.addWidget(stat("FHT:", f"{fht} bpm"))
        fh = self.visit.get("fh_cm")
        if fh: stats.addWidget(stat("FH:", f"{fh} cm"))
        pres = self.visit.get("presentation", "Cephalic")
        if pres and pres != "Cephalic": stats.addWidget(stat("Presentation:", pres))
        stats.addStretch()
        lay.addLayout(stats)

        outer.addWidget(card, stretch=1)


# ═══════════════════════════════════════════════════════════════════════════
# MAIN SCREEN
# ═══════════════════════════════════════════════════════════════════════════

# tab name constants — one source of truth
TAB_PRENATAL = "prenatal"
TAB_LAB      = "lab"
TAB_MED      = "medication"
TAB_DELIVERY = "delivery"


class PrenatalCareScreen(QMainWindow):
    def __init__(self, pregnancy_id: int, pregnancy_num: int, patient_id: int):
        super().__init__()
        self.ui = Ui_PrenatalCareScreen()
        self.ui.setupUi(self)
        self._pregnancy_id  = pregnancy_id
        self._pregnancy_num = pregnancy_num
        self._patient_id    = patient_id
        self._initialized   = False
        self._active_tab    = TAB_PRENATAL

        o = ordinal(pregnancy_num)
        self.setWindowTitle(f"MaternaDB – Prenatal Care ({o} Pregnancy)")

        # sidebar nav
        self.ui.pushButton.clicked.connect(self.go_to_dashboard)
        self.ui.pushButton_2.clicked.connect(self.go_to_patient_records)
        self.ui.pushButton_3.clicked.connect(self.go_to_prenatal_care)
        self.ui.pushButton_4.clicked.connect(self.go_to_appointments)
        self.ui.pushButton_5.clicked.connect(self.logout)

        # tab buttons — tab_visit_history repurposed as Medications
        self.ui.tab_visit_history.clicked.connect(lambda: self._switch_tab(TAB_MED))
        self.ui.tab_prenatal.clicked.connect(lambda: self._switch_tab(TAB_PRENATAL))
        self.ui.tab_lab.clicked.connect(lambda: self._switch_tab(TAB_LAB))
        self.ui.tab_delivery.clicked.connect(lambda: self._switch_tab(TAB_DELIVERY))

        # record visit button (top right of patient card)
        self.ui.btn_record_visit.clicked.connect(self.on_record_new_visit)

        # the "add prescription" slot is repurposed as "add item" for the active tab
        self.ui.btn_add_prescription.clicked.connect(self._on_tab_add)

        self._build_sidebar_profile()

    # ── sidebar profile (same pattern as every other screen) ─────────────────
    def _build_sidebar_profile(self):
        user = session.get()
        name = user["name"] if user else "User"
        role = user.get("role", "Staff") if user else "Staff"

        self.profile_avatar = QLabel("👤", parent=self.ui.frame)
        self.profile_avatar.setFixedSize(64, 64)
        self.profile_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_avatar.setStyleSheet(
            "background-color: #ECC6DC; border-radius: 32px; font-size: 28px; border: none;"
        )
        self.profile_avatar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.profile_avatar.mousePressEvent = lambda _: self._open_profile_dialog()

        self.profile_name_lbl = QLabel(name, parent=self.ui.frame)
        self.profile_name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_name_lbl.setWordWrap(True)
        self.profile_name_lbl.setCursor(Qt.CursorShape.PointingHandCursor)
        self.profile_name_lbl.mousePressEvent = lambda _: self._open_profile_dialog()
        self.profile_name_lbl.setStyleSheet(
            "color: white; font-size: 13px; font-weight: bold; background: transparent; border: none;"
        )

        self.profile_role_lbl = QLabel(role, parent=self.ui.frame)
        self.profile_role_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_role_lbl.setStyleSheet("color: rgba(255,255,255,0.65); font-size: 11px; background: transparent; border: none;")

        self.profile_divider = QLabel(parent=self.ui.frame)
        self.profile_divider.setFixedHeight(1)
        self.profile_divider.setStyleSheet("background-color: rgba(255,255,255,0.2); border: none;")

        for w in (self.profile_avatar, self.profile_name_lbl, self.profile_role_lbl, self.profile_divider):
            w.raise_(); w.show()

    def _reposition_sidebar_profile(self):
        sw = self.ui.frame.width()
        pad, av = 16, 64
        self.profile_avatar.setGeometry((sw - av) // 2, 20, av, av)
        self.profile_name_lbl.setGeometry(pad, 94, sw - pad * 2, 36)
        self.profile_role_lbl.setGeometry(pad, 128, sw - pad * 2, 18)
        self.profile_divider.setGeometry(pad, 148, sw - pad * 2, 1)

    def _open_profile_dialog(self):
        from user_profile.user_profile_dialog import UserProfileDialog
        dlg = UserProfileDialog(parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            user = session.get()
            if user:
                self.profile_name_lbl.setText(user.get("name", ""))
                self.profile_role_lbl.setText(user.get("role", ""))

    # ── show / resize ─────────────────────────────────────────────────────────
    def showEvent(self, event):
        super().showEvent(event)
        if not self._initialized:
            self._initialized = True
            self.reposition_elements()
            self.load_logo()
            self.ui.patient_combo.hide()
            self.ui.patient_selector_label.hide()
            self.ui.btn_record_visit.hide()          # ← add this line
            self.ui.tab_visit_history.setText("Medications")
            o = ordinal(self._pregnancy_num)
            self.ui.title_label.setText(f"PRENATAL CARE  –  {o.upper()} PREGNANCY")
            self._update_tab_styles()
            self._update_add_btn_label()
            self.load_patient_info_by_pregnancy()
            self._load_active_tab()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.reposition_elements()

    def reposition_elements(self):
        w, h = self.width(), self.height()
        self.ui.frame_2.setGeometry(0, 0, w, 61)
        self.ui.frame.setGeometry(0, 61, 231, h - 61)
        mx, mw, mh = 231, w - 231, h - 61
        self.ui.frame_3.setGeometry(mx, 61, mw, mh)
        cw = mw - 80
        self.ui.title_label.setGeometry(40, 20, cw, 61)
        self.ui.patient_selector_label.setGeometry(40, 88, 110, 28)
        self.ui.patient_combo.setGeometry(155, 85, min(320, cw - 200), 28)
        self.ui.patient_info_frame.setGeometry(40, 122, cw, 70)
        self.ui.btn_record_visit.setGeometry(cw - 120, 18, 110, 32)
        self.ui.btn_add_prescription.setGeometry(cw - 240, 18, 110, 32)
        self.ui.tab_frame.setGeometry(40, 200, cw, 40)
        self.ui.tab_line.setGeometry(40, 238, cw, 1)
        self.ui.scroll_area.setGeometry(40, 245, cw, max(mh - 260, 200))
        self._reposition_sidebar_profile()

    def load_logo(self):
        px = QPixmap("Asset/MaternaDB_logo.png")
        if not px.isNull():
            self.ui.logo.setPixmap(px.scaled(
                self.ui.logo.width(), self.ui.logo.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
            self.ui.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # ── tab switching ─────────────────────────────────────────────────────────
    TAB_INACTIVE = """
        QPushButton {
            background: transparent; color: rgb(21,23,61);
            border: none; border-bottom: 2px solid transparent;
            font-size: 12px; padding: 0 4px;
        }
        QPushButton:hover { border-bottom: 2px solid rgb(192,116,182); }
    """
    TAB_ACTIVE = """
        QPushButton {
            background: transparent; color: rgb(21,23,61);
            border: none; border-bottom: 3px solid rgb(21,23,61);
            font-size: 12px; font-weight: bold; padding: 0 4px;
        }
    """

    def _switch_tab(self, tab_name):
        self._active_tab = tab_name
        self._update_tab_styles()
        self._update_add_btn_label()
        self._load_active_tab()

    def _update_tab_styles(self):
        # tab_visit_history is repurposed as Medications
        mapping = {
            TAB_MED:      self.ui.tab_visit_history,
            TAB_LAB:      self.ui.tab_lab,
            TAB_DELIVERY: self.ui.tab_delivery,
            TAB_PRENATAL: self.ui.tab_prenatal,
        }
        for name, btn in mapping.items():
            btn.setStyleSheet(self.TAB_ACTIVE if name == self._active_tab else self.TAB_INACTIVE)

    def _update_add_btn_label(self):
        labels = {
            TAB_PRENATAL: "+ Record Visit",
            TAB_LAB:      "+ Add Lab",
            TAB_MED:      "+ Add Medication",
            TAB_DELIVERY: "+ Add Delivery",
        }
        self.ui.btn_add_prescription.setText(labels.get(self._active_tab, "+ Add"))

    def _on_tab_add(self):
        if self._active_tab == TAB_PRENATAL:
            self.on_record_new_visit()
        elif self._active_tab == TAB_LAB:
            self._add_lab_referral()
        elif self._active_tab == TAB_MED:
            self._add_medication()
        elif self._active_tab == TAB_DELIVERY:
            self._add_delivery()

    def _load_active_tab(self):
        self._clear_scroll()
        if self._active_tab == TAB_PRENATAL:
            self._load_prenatal_visits()
        elif self._active_tab == TAB_LAB:
            self._load_lab_referrals()
        elif self._active_tab == TAB_MED:
            self._load_medications()
        elif self._active_tab == TAB_DELIVERY:
            self._load_delivery()

    def _clear_scroll(self):
        lay = self.ui.scroll_layout
        while lay.count() > 1:
            item = lay.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.hide()
                widget.deleteLater()

    # ── patient header ────────────────────────────────────────────────────────
    def load_patient_info_by_pregnancy(self):
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT patient_id,
                    CONCAT(last_name, ', ', first_name,
                            CASE WHEN middle_name IS NOT NULL AND middle_name <> ''
                                THEN ' ' || middle_name ELSE '' END),
                    EXTRACT(YEAR FROM AGE(date_of_birth))
                FROM patient_profile WHERE patient_id = %s
            """, (self._patient_id,))
            p = cur.fetchone()
            cur.execute("SELECT edd FROM pregnancy WHERE pregnancy_id = %s", (self._pregnancy_id,))
            edd = cur.fetchone()
            conn.close()
            if p:
                edd_txt = f"  •  EDD: {fmt_date(edd[0])}" if edd and edd[0] else ""
                o = ordinal(self._pregnancy_num)
                self.ui.patient_name_label.setText(p[1])
                self.ui.patient_sub_label.setText(
                    f"Patient ID: #{p[0]}  •  Age: {int(p[2]) if p[2] else '—'}  •  {o} Pregnancy{edd_txt}"
                )
        except Exception as e:
            print(f"patient info load error: {e}")
            if conn: conn.close()

    # ═══════════════════════════════════════════════════════════════════════
    # PRENATAL VISITS TAB
    # ═══════════════════════════════════════════════════════════════════════

    def _load_prenatal_visits(self):
        self._clear_scroll()

        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT visit_id, pregnancy_id, visit_num, visit_date,
                    gestational_age_weeks,
                    staff, blood_pressure,
                    weight_kg, fht_bpm, fh_cm,
                    presentation, risk_assessment
                FROM prenatal_visit
                WHERE pregnancy_id = %s
                ORDER BY visit_num DESC
            """, (self._pregnancy_id,))
            rows = cur.fetchall()
            conn.close()
        except Exception as e:
            print(f"prenatal visits load error: {e}")
            if conn: conn.close()
            rows = []

        cols = ["visit_id", "pregnancy_id", "visit_num", "visit_date", "aog_weeks",
                "staff", "bp", "weight_kg", "fht_bpm", "fh_cm",
                "presentation", "risk_assessment"]

        if not rows:
            self._empty_msg("No prenatal visits yet. Click '+ Record Visit' to add the first one.")
            return

        lay = self.ui.scroll_layout
        for row in rows:
            v = dict(zip(cols, row))
            card = VisitCard(v,
                on_view_diagnosis=self._show_diagnosis,
                on_edit=self._edit_visit,
                on_delete=self._delete_visit,
            )
            lay.insertWidget(lay.count() - 1, card)

    def on_record_new_visit(self):
        conn = get_connection()
        next_num = 1
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT COALESCE(MAX(visit_num),0)+1 FROM prenatal_visit WHERE pregnancy_id=%s", (self._pregnancy_id,))
                res = cur.fetchone()
                next_num = res[0] if res else 1
                conn.close()
            except Exception as e:
                print(f"next visit num error: {e}")
                if conn: conn.close()

        dlg = PrenatalVisitDialog(self._pregnancy_id, next_num, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._save_visit(dlg.result_data)

    def _edit_visit(self, visit: dict):
        dlg = PrenatalVisitDialog(self._pregnancy_id, None, existing=visit, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._update_visit(visit["visit_id"], dlg.result_data)

    def _delete_visit(self, visit: dict):
        if QMessageBox.question(self, "Delete Visit",
            f"Delete Visit #{visit.get('visit_num','?')}? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM prenatal_visit WHERE visit_id=%s", (visit["visit_id"],))
            conn.commit(); conn.close()
            self._load_prenatal_visits()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not delete:\n{e}")
            if conn: conn.close()

    def _show_diagnosis(self, visit: dict):
        DiagnosisDialog(visit, parent=self).exec()

    def _save_visit(self, data: dict):
        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "DB Error", "Could not connect.")
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO prenatal_visit
                    (pregnancy_id, visit_num, visit_date, gestational_age_weeks,
                    staff_id, staff, blood_pressure, weight_kg,
                    fht_bpm, fh_cm, presentation, risk_assessment)
                VALUES
                    (%(pregnancy_id)s, %(visit_num)s, %(visit_date)s, %(gestational_age_weeks)s,
                    %(staff_id)s, %(staff)s, %(blood_pressure)s, %(weight_kg)s,
                    %(fht_bpm)s, %(fh_cm)s, %(presentation)s, %(risk_assessment)s)
            """, data)
            conn.commit(); conn.close()
            self._load_prenatal_visits()
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))
            if conn: conn.close()

    def _update_visit(self, visit_id, data: dict):
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE prenatal_visit SET
                    visit_date            = %(visit_date)s,
                    gestational_age_weeks = %(gestational_age_weeks)s,
                    staff_id              = %(staff_id)s,
                    staff                 = %(staff)s,
                    blood_pressure        = %(blood_pressure)s,
                    weight_kg             = %(weight_kg)s,
                    fht_bpm               = %(fht_bpm)s,
                    fh_cm                 = %(fh_cm)s,
                    presentation          = %(presentation)s,
                    risk_assessment       = %(risk_assessment)s
                WHERE visit_id = %(visit_id)s
            """, {**data, "visit_id": visit_id})
            conn.commit(); conn.close()
            self._load_prenatal_visits()
        except Exception as e:
            QMessageBox.critical(self, "Update Error", str(e))
            if conn: conn.close()

    # ═══════════════════════════════════════════════════════════════════════
    # LAB & REFERRALS TAB
    # ═══════════════════════════════════════════════════════════════════════

    def _load_lab_referrals(self):
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT lr.referral_id, lr.visit_id, lr.patient_id,
                    lr.lab_name, lr.test_name,
                    lr.collection_date, lr.date_sent, lr.result_date,
                    lr.result, lr.remarks
                FROM laboratory_referral lr
                WHERE lr.patient_id = (
                    SELECT patient_id FROM pregnancy WHERE pregnancy_id = %s
                )
                ORDER BY lr.collection_date DESC
            """, (self._pregnancy_id,))
            rows = cur.fetchall()
            conn.close()
        except Exception as e:
            print(f"lab referral load error: {e}")
            if conn: conn.close()
            rows = []

        if not rows:
            self._empty_msg("No lab results or referrals yet. Click '+ Add Lab' to add one.")
            return

        cols = ["referral_id", "visit_id", "patient_id", "lab_name", "test_name",
                "collection_date", "date_sent", "result_date", "result", "remarks"]
        tbl = self._make_table(["Collected", "Lab / Facility", "Test", "Result", "Remarks", "", ""])
        lay = self.ui.scroll_layout
        lay.insertWidget(lay.count() - 1, tbl)

        RESULT_COLORS = {
            "Normal":   QColor(220, 240, 220),
            "Abnormal": QColor(255, 220, 220),
            "Pending":  QColor(255, 243, 205),
            "Referred": QColor(220, 230, 255),
        }

        for row in rows:
            r = dict(zip(cols, row))
            ri = tbl.rowCount(); tbl.insertRow(ri)
            tbl.setItem(ri, 0, self._cell(fmt_date(r["collection_date"])))
            tbl.setItem(ri, 1, self._cell(r["lab_name"] or ""))
            tbl.setItem(ri, 2, self._cell(r["test_name"]))
            res_item = self._cell(r["result"] or "Pending")
            res_item.setBackground(QBrush(RESULT_COLORS.get(r["result"] or "Pending", QColor(240, 230, 240))))
            tbl.setItem(ri, 3, res_item)
            tbl.setItem(ri, 4, self._cell(r["remarks"] or ""))

            btn_e = QPushButton("Edit")
            btn_e.setStyleSheet("background-color: rgb(192,116,182); color: white; border-radius:4px; font-size:11px;")
            btn_e.clicked.connect((lambda rec: lambda: self._edit_lab(rec))(r))
            tbl.setCellWidget(ri, 5, btn_e)

            btn_d = QPushButton("Delete")
            btn_d.setStyleSheet("background-color: rgb(200,50,50); color: white; border-radius:4px; font-size:11px;")
            btn_d.clicked.connect((lambda rec: lambda: self._delete_lab(rec))(r))
            tbl.setCellWidget(ri, 6, btn_d)

    def _add_lab_referral(self):
        dlg = LabReferralDialog(self._pregnancy_id, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._save_lab(dlg.result_data)

    def _edit_lab(self, rec: dict):
        dlg = LabReferralDialog(self._pregnancy_id, existing=rec, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._update_lab(rec["referral_id"], dlg.result_data)

    def _delete_lab(self, rec: dict):
        from PyQt6.QtCore import QTimer
        # Step off the button's signal entirely before showing the dialog
        QTimer.singleShot(0, lambda: self._confirm_delete_lab(rec))

    def _confirm_delete_lab(self, rec: dict):
        if QMessageBox.question(
            self, "Delete",
            f"Delete this lab record ({rec.get('test_name', '')})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM laboratory_referral WHERE referral_id = %s", (rec["referral_id"],))
            conn.commit(); conn.close()
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(0, lambda: self._switch_tab(TAB_LAB))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            if conn: conn.close()

    def _save_lab(self, data: dict):
        # Auto-fetch the most recent visit_id for this pregnancy
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT visit_id FROM prenatal_visit
                WHERE pregnancy_id = %s
                ORDER BY visit_date DESC LIMIT 1
            """, (self._pregnancy_id,))
            row = cur.fetchone()
            if not row:
                QMessageBox.warning(self, "No Visit",
                    "Please record a prenatal visit before adding a lab referral.")
                conn.close()
                return
            visit_id = row[0]

            cur.execute("""
                SELECT patient_id FROM pregnancy WHERE pregnancy_id = %s
            """, (self._pregnancy_id,))
            patient_row = cur.fetchone()
            if not patient_row:
                QMessageBox.critical(self, "Error", "Could not find patient for this pregnancy.")
                conn.close()
                return
            patient_id = patient_row[0]

            cur.execute("""
                INSERT INTO laboratory_referral
                    (visit_id, patient_id, lab_name, test_name,
                    collection_date, date_sent, result_date, result, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                visit_id, patient_id,
                data["lab_name"], data["test_name"],
                data["collection_date"], data["date_sent"],
                data["result_date"], data["result"], data["remarks"],
            ))
            conn.commit(); conn.close()
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(0, lambda: self._switch_tab(TAB_LAB))
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))
            if conn: conn.close()

    def _update_lab(self, referral_id: int, data: dict):
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE laboratory_referral SET
                    lab_name        = %s,
                    test_name       = %s,
                    collection_date = %s,
                    date_sent       = %s,
                    result_date     = %s,
                    result          = %s,
                    remarks         = %s
                WHERE referral_id = %s
            """, (
                data["lab_name"], data["test_name"],
                data["collection_date"], data["date_sent"],
                data["result_date"], data["result"], data["remarks"],
                referral_id,
            ))
            conn.commit(); conn.close()
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(0, lambda: self._switch_tab(TAB_LAB))
        except Exception as e:
            QMessageBox.critical(self, "Update Error", str(e))
            if conn: conn.close()

    # ═══════════════════════════════════════════════════════════════════════
    # MEDICATIONS TAB  (no dedicated tab button in UI — wired via visit history btn for now)
    # ═══════════════════════════════════════════════════════════════════════
    def _add_medication(self):
        # get patient_id first
        conn = get_connection()
        patient_id = None
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT patient_id FROM pregnancy WHERE pregnancy_id = %s",
                            (self._pregnancy_id,))
                row = cur.fetchone()
                patient_id = row[0] if row else None
                conn.close()
            except Exception as e:
                print(f"patient_id fetch error: {e}")
                if conn: conn.close()

        if not patient_id:
            QMessageBox.critical(self, "Error", "Could not find patient for this pregnancy.")
            return

        dlg = MedicationDialog(patient_id, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                d = dlg.result_data
                cur.execute("""
                    INSERT INTO prescription
                        (patient_id, pregnancy_id, prescribed_by, medicine_name, dosage,
                        frequency, duration, route, timing,
                        prescription_date, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (patient_id, self._pregnancy_id, d["staff_id"], d["medicine_name"], d["dosage"],
                    d["frequency"], d["duration"], d["route"], d["timing"],
                    d["prescription_date"], d["notes"]))
                conn.commit(); conn.close()
                from PyQt6.QtCore import QTimer
                QTimer.singleShot(0, lambda: self._switch_tab(TAB_MED))
            except Exception as e:
                QMessageBox.critical(self, "Save Error", str(e))
                if conn: conn.close()

    def _load_medications(self):
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT p.prescription_id,
                    p.medicine_name, p.dosage, p.frequency, p.duration,
                    p.route, p.timing, p.prescription_date, p.notes,
                    p.prescribed_by,
                    CONCAT(s.first_name, ' ', s.last_name, ' (', s.role, ')') AS staff_display
                FROM prescription p
                LEFT JOIN staff s ON p.prescribed_by = s.staff_id
                WHERE p.pregnancy_id = %s
                ORDER BY p.prescription_date DESC
            """, (self._pregnancy_id,))
            rows = cur.fetchall()
            conn.close()
        except Exception as e:
            print(f"medication load error: {e}")
            if conn: conn.close()
            rows = []

        if not rows:
            self._empty_msg("No medications recorded. Click '+ Add Medication' to add one.")
            return

        cols = ["prescription_id", "medicine_name", "dosage", "frequency", "duration",
                "route", "timing", "prescription_date", "notes",
                "prescribed_by", "staff_display"]

        tbl = self._make_table(["Medicine", "Dosage", "Frequency", "Duration",
                                "Route", "Prescribed By", "Date", "Notes", "", ""])
        self.ui.scroll_layout.insertWidget(self.ui.scroll_layout.count() - 1, tbl)

        for row in rows:
            r = dict(zip(cols, row))
            ri = tbl.rowCount(); tbl.insertRow(ri)
            tbl.setItem(ri, 0, self._cell(r["medicine_name"]))
            tbl.setItem(ri, 1, self._cell(r["dosage"]))
            tbl.setItem(ri, 2, self._cell(r["frequency"]))
            tbl.setItem(ri, 3, self._cell(r["duration"] or ""))
            tbl.setItem(ri, 4, self._cell(r["route"] or ""))
            tbl.setItem(ri, 5, self._cell(r["staff_display"] or ""))
            tbl.setItem(ri, 6, self._cell(fmt_date(r["prescription_date"])))
            tbl.setItem(ri, 7, self._cell(r["notes"] or ""))

            btn_e = QPushButton("Edit")
            btn_e.setStyleSheet("background-color: rgb(192,116,182); color: white; border-radius:4px; font-size:11px;")
            btn_e.clicked.connect((lambda rec: lambda: self._edit_medication(rec))(r))
            tbl.setCellWidget(ri, 8, btn_e)

            btn_d = QPushButton("Delete")
            btn_d.setStyleSheet("background-color: rgb(200,50,50); color: white; border-radius:4px; font-size:11px;")
            btn_d.clicked.connect((lambda rec: lambda: self._delete_medication(rec))(r))
            tbl.setCellWidget(ri, 9, btn_d)

    def _edit_medication(self, rec: dict):
        conn = get_connection()
        patient_id = None
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT patient_id FROM pregnancy WHERE pregnancy_id = %s",
                            (self._pregnancy_id,))
                row = cur.fetchone()
                patient_id = row[0] if row else None
                conn.close()
            except Exception as e:
                print(f"patient_id fetch error: {e}")
                if conn: conn.close()

        dlg = MedicationDialog(patient_id, existing=rec, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                d = dlg.result_data
                cur.execute("""
                    UPDATE prescription SET
                        prescribed_by     = %s,
                        medicine_name     = %s,
                        dosage            = %s,
                        frequency         = %s,
                        duration          = %s,
                        route             = %s,
                        timing            = %s,
                        prescription_date = %s,
                        notes             = %s
                    WHERE prescription_id = %s
                """, (d["staff_id"], d["medicine_name"], d["dosage"],
                    d["frequency"], d["duration"], d["route"], d["timing"],
                    d["prescription_date"], d["notes"],
                    rec["prescription_id"]))
                conn.commit(); conn.close()
                from PyQt6.QtCore import QTimer
                QTimer.singleShot(0, lambda: self._switch_tab(TAB_MED))
            except Exception as e:
                QMessageBox.critical(self, "Update Error", str(e))
                if conn: conn.close()

    def _delete_medication(self, rec: dict):
        if QMessageBox.question(
            self, "Delete", f"Delete {rec.get('medicine_name', '')}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes: return
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, lambda: self._do_delete_medication(rec))

    def _do_delete_medication(self, rec: dict):
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM prescription WHERE prescription_id = %s",
                        (rec["prescription_id"],))
            conn.commit(); conn.close()
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(0, lambda: self._switch_tab(TAB_MED))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            if conn: conn.close()
    # ═══════════════════════════════════════════════════════════════════════
    # DELIVERY & NEWBORN TAB
    # ═══════════════════════════════════════════════════════════════════════
    def _load_delivery(self):
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT dr.delivery_id, dr.pregnancy_id, dr.delivery_date, dr.delivery_time,
                    dr.delivery_type, dr.delivery_outcome, dr.birth_outcome,
                    dr.delivery_location, dr.referred_to, dr.remarks,
                    CONCAT(s.first_name, ' ', s.last_name, ' (', s.role, ')') as staff_display
                FROM delivery_record dr
                LEFT JOIN staff s ON dr.staff_id = s.staff_id
                WHERE dr.pregnancy_id = %s
            """, (self._pregnancy_id,))
            deliveries = cur.fetchall()

            cur.execute("""
                SELECT newborn_id, delivery_id, pregnancy_id, baby_last_name,
                    baby_first_name, sex, birth_weight_kg, birth_length_cm,
                    apgar_score, date_of_birth, time_of_birth
                FROM newborn WHERE pregnancy_id = %s
            """, (self._pregnancy_id,))
            newborns = cur.fetchall()
            conn.close()
        except Exception as e:
            print(f"delivery load error: {e}")
            if conn: conn.close()
            deliveries, newborns = [], []

        lay = self.ui.scroll_layout
        d_cols = ["delivery_id","pregnancy_id","delivery_date","delivery_time",
                "delivery_type","delivery_outcome","birth_outcome",
                "delivery_location","referred_to","remarks","staff_display"]
        n_cols = ["newborn_id","delivery_id","pregnancy_id","baby_last_name",
                "baby_first_name","sex","birth_weight_kg","birth_length_cm",
                "apgar_score","date_of_birth","time_of_birth"]

        hdr = self._section_header("Delivery Record", self._add_delivery)
        lay.insertWidget(lay.count() - 1, hdr)

        if deliveries:
            for row in deliveries:
                d = dict(zip(d_cols, row))
                card = self._delivery_card(d)
                lay.insertWidget(lay.count() - 1, card)
        else:
            lay.insertWidget(lay.count() - 1, self._inline_msg("No delivery record yet."))

        hdr2 = self._section_header("Newborn Record(s)", self._add_newborn)
        lay.insertWidget(lay.count() - 1, hdr2)

        if newborns:
            for row in newborns:
                n = dict(zip(n_cols, row))
                card = self._newborn_card(n)
                lay.insertWidget(lay.count() - 1, card)
        else:
            lay.insertWidget(lay.count() - 1, self._inline_msg("No newborn record yet."))

    def _add_delivery(self):
        dlg = DeliveryDialog(self._pregnancy_id, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO delivery_record
                        (pregnancy_id, staff_id, delivery_date, delivery_time,
                        delivery_type, delivery_outcome, birth_outcome,
                        delivery_location, referred_to, remarks)
                    VALUES (%(pregnancy_id)s, %(staff_id)s, %(delivery_date)s, %(delivery_time)s,
                            %(delivery_type)s, %(delivery_outcome)s, %(birth_outcome)s,
                            %(delivery_location)s, %(referred_to)s, %(remarks)s)
                """, dlg.result_data)
                conn.commit(); conn.close()
                self._switch_tab(TAB_DELIVERY)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                if conn: conn.close()

    def _edit_delivery(self, rec: dict):
        dlg = DeliveryDialog(self._pregnancy_id, existing=rec, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE delivery_record SET
                        staff_id          = %(staff_id)s,
                        delivery_date     = %(delivery_date)s,
                        delivery_time     = %(delivery_time)s,
                        delivery_type     = %(delivery_type)s,
                        delivery_outcome  = %(delivery_outcome)s,
                        birth_outcome     = %(birth_outcome)s,
                        delivery_location = %(delivery_location)s,
                        referred_to       = %(referred_to)s,
                        remarks           = %(remarks)s
                    WHERE delivery_id = %(delivery_id)s
                """, {**dlg.result_data, "delivery_id": rec["delivery_id"]})
                conn.commit(); conn.close()
                self._switch_tab(TAB_DELIVERY)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                if conn: conn.close()

    def _add_newborn(self):
        conn = get_connection()
        delivery_id = None
        delivery_time = None
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("""
                    SELECT delivery_id, delivery_time FROM delivery_record
                    WHERE pregnancy_id = %s
                    ORDER BY delivery_id DESC LIMIT 1
                """, (self._pregnancy_id,))
                row = cur.fetchone()
                if row:
                    delivery_id   = row[0]
                    delivery_time = row[1]   # datetime.time object from psycopg2
                conn.close()
            except Exception as e:
                print(f"delivery_id fetch error: {e}")
                if conn: conn.close()

        if not delivery_id:
            QMessageBox.warning(self, "No Delivery", "Please add a delivery record first.")
            return

        # convert Python time → QTime
        from PyQt6.QtCore import QTime
        qt_time = QTime(delivery_time.hour, delivery_time.minute) if delivery_time else QTime.currentTime()

        dlg = NewbornDialog(delivery_id, self._pregnancy_id, delivery_time=qt_time, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO newborn
                        (delivery_id, pregnancy_id, baby_last_name, baby_first_name,
                        sex, birth_weight_kg, birth_length_cm, apgar_score,
                        date_of_birth, time_of_birth)
                    VALUES (%(delivery_id)s, %(pregnancy_id)s, %(baby_last_name)s, %(baby_first_name)s,
                            %(sex)s, %(birth_weight_kg)s, %(birth_length_cm)s, %(apgar_score)s,
                            %(date_of_birth)s, %(time_of_birth)s)
                """, dlg.result_data)
                conn.commit(); conn.close()
                self._switch_tab(TAB_DELIVERY)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                if conn: conn.close()
        
    def _edit_newborn(self, rec: dict):
        dlg = NewbornDialog(rec["delivery_id"], self._pregnancy_id, existing=rec, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE newborn SET
                        baby_last_name  = %(baby_last_name)s,
                        baby_first_name = %(baby_first_name)s,
                        date_of_birth   = %(date_of_birth)s,
                        time_of_birth   = %(time_of_birth)s,
                        sex             = %(sex)s,
                        birth_weight_kg = %(birth_weight_kg)s,
                        birth_length_cm = %(birth_length_cm)s,
                        apgar_score     = %(apgar_score)s
                    WHERE newborn_id = %(newborn_id)s
                """, {**dlg.result_data, "newborn_id": rec["newborn_id"]})
                conn.commit(); conn.close()
                self._switch_tab(TAB_DELIVERY)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                if conn: conn.close()

    def _delete_newborn(self, rec: dict):
        name = f"{rec.get('baby_first_name','')} {rec.get('baby_last_name','')}".strip() or "this baby"
        if QMessageBox.question(self, "Delete", f"Delete newborn record for {name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes: return
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM newborn WHERE newborn_id=%s", (rec["newborn_id"],))
            conn.commit(); conn.close()
            self._switch_tab(TAB_DELIVERY)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            if conn: conn.close()

    def _delete_delivery(self, rec: dict):
        if QMessageBox.question(self, "Delete", "Delete this delivery record?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes: return
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM delivery_record WHERE delivery_id=%s", (rec["delivery_id"],))
            conn.commit(); conn.close()
            self._switch_tab(TAB_DELIVERY)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            if conn: conn.close()

    # ── small card builders for delivery/newborn ──────────────────────────────
    def _delivery_card(self, d: dict) -> QFrame:
        card = QFrame()
        card.setStyleSheet(CARD_STYLE)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(6)

        top = QHBoxLayout()
        t = QLabel(f"{d.get('delivery_type','—')}  –  {fmt_date(d.get('delivery_date',''))}")
        t.setStyleSheet("color: rgb(21,23,61); font-size: 13px; font-weight: bold; border: none;")
        btn_e = QPushButton("Edit")
        btn_e.setFixedHeight(28)
        btn_e.setStyleSheet("background-color: rgb(192,116,182); color: white; border: none; border-radius:6px; font-size:11px; padding: 0 10px;")
        btn_e.clicked.connect(lambda: self._edit_delivery(d))
        btn_d = QPushButton("Delete")
        btn_d.setFixedHeight(28)
        btn_d.setStyleSheet("background-color: rgb(200,50,50); color: white; border: none; border-radius:6px; font-size:11px; padding: 0 10px;")
        btn_d.clicked.connect(lambda: self._delete_delivery(d))
        top.addWidget(t); top.addStretch(); top.addWidget(btn_e); top.addWidget(btn_d)
        lay.addLayout(top)

        info = QHBoxLayout(); info.setSpacing(20)
        def stat(k, v):
            l = QLabel(f"<b>{k}</b> {v}")
            l.setTextFormat(Qt.TextFormat.RichText)
            l.setStyleSheet("color: rgb(21,23,61); font-size: 11px; border: none;")
            return l
        info.addWidget(stat("Outcome:", d.get("delivery_outcome","—")))
        info.addWidget(stat("Birth:", d.get("birth_outcome","—")))
        info.addWidget(stat("Attendant:", d.get("staff_display","—")))
        if d.get("delivery_location"):
            info.addWidget(stat("Location:", d["delivery_location"]))
        if d.get("referred_to"):
            info.addWidget(stat("Referred to:", d["referred_to"]))
        info.addStretch()
        lay.addLayout(info)
        return card

    def _newborn_card(self, n: dict) -> QFrame:
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: rgb(220,235,255); border-radius: 12px; border: 1px solid rgb(190,210,240); }")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(6)

        top = QHBoxLayout()
        name = f"{n.get('baby_first_name','')} {n.get('baby_last_name','')}".strip() or "Baby"
        t = QLabel(f"{name}  –  {n.get('sex','—')}")
        t.setStyleSheet("color: rgb(21,23,61); font-size: 13px; font-weight: bold; border: none;")
        btn_e = QPushButton("Edit")
        btn_e.setFixedHeight(28)
        btn_e.setStyleSheet("background-color: rgb(100,130,200); color: white; border: none; border-radius:6px; font-size:11px; padding: 0 10px;")
        btn_e.clicked.connect(lambda: self._edit_newborn(n))
        btn_d = QPushButton("Delete")
        btn_d.setFixedHeight(28)
        btn_d.setStyleSheet("background-color: rgb(200,50,50); color: white; border: none; border-radius:6px; font-size:11px; padding: 0 10px;")
        btn_d.clicked.connect(lambda: self._delete_newborn(n))
        top.addWidget(t); top.addStretch(); top.addWidget(btn_e); top.addWidget(btn_d)
        lay.addLayout(top)

        info = QHBoxLayout(); info.setSpacing(20)
        def stat(k, v):
            l = QLabel(f"<b>{k}</b> {v}")
            l.setTextFormat(Qt.TextFormat.RichText)
            l.setStyleSheet("color: rgb(21,23,61); font-size: 11px; border: none;")
            return l
        info.addWidget(stat("DOB:", fmt_date(n.get("date_of_birth",""))))
        info.addWidget(stat("Time:", str(n.get("time_of_birth","—"))))
        if n.get("birth_weight_kg"): info.addWidget(stat("Weight:", f"{n['birth_weight_kg']} kg"))
        if n.get("birth_length_cm"): info.addWidget(stat("Length:", f"{n['birth_length_cm']} cm"))
        if n.get("apgar_score") is not None: info.addWidget(stat("APGAR:", str(n["apgar_score"])))
        info.addStretch()
        lay.addLayout(info)
        return card
    # ── small UI helpers ──────────────────────────────────────────────────────
    def _empty_msg(self, text):
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: rgb(100,80,110); font-size: 13px; padding: 30px;")
        self.ui.scroll_layout.insertWidget(self.ui.scroll_layout.count() - 1, lbl)

    def _inline_msg(self, text) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet("color: rgb(120,90,120); font-size: 12px; padding: 8px 4px;")
        return lbl

    def _section_header(self, title, on_add) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 8, 0, 4)
        lbl = QLabel(title)
        lbl.setStyleSheet("color: rgb(21,23,61); font-size: 14px; font-weight: bold;")
        btn = QPushButton(f"+ Add")
        btn.setFixedHeight(28)
        btn.setStyleSheet(BTN_PRIMARY)
        btn.clicked.connect(on_add)
        lay.addWidget(lbl); lay.addStretch(); lay.addWidget(btn)
        return w

    def _make_table(self, headers) -> QTableWidget:
        tbl = QTableWidget()
        tbl.setColumnCount(len(headers))
        tbl.setHorizontalHeaderLabels(headers)
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tbl.verticalHeader().setVisible(False)
        tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tbl.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        tbl.setAlternatingRowColors(True)
        tbl.setStyleSheet("""
            QTableWidget { background: white; border-radius: 8px; font-size: 12px; }
            QHeaderView::section {
                background-color: rgb(192,116,182); color: white;
                font-weight: bold; padding: 6px; border: none;
            }
        """)
        return tbl

    def _cell(self, text) -> QTableWidgetItem:
        item = QTableWidgetItem(str(text) if text else "")
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

    # ── navigation ────────────────────────────────────────────────────────────
    def go_to_dashboard(self):
        from screens.dashboard_screen import DashboardScreen
        self.w = DashboardScreen(); self.w.showMaximized(); self.close()

    def go_to_patient_records(self):
        from screens.patient_records_screen import PatientRecordScreen
        self.w = PatientRecordScreen(); self.w.showMaximized(); self.close()

    def go_to_prenatal_care(self):
        from screens.prenatal_dashboard_screen import PrenatalDashboardScreen
        self.w = PrenatalDashboardScreen(); self.w.showMaximized(); self.close()

    def go_to_appointments(self):
        from screens.appointments_screen import AppointmentsScreen
        self.w = AppointmentsScreen(); self.w.showMaximized(); self.close()

    def logout(self):
        session.clear()
        from screens.login_screen import LoginScreen
        self.w = LoginScreen(); self.w.showMaximized(); self.close()
