from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QWidget, QHBoxLayout, QVBoxLayout,
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


# ═══════════════════════════════════════════════════════════════════════════
# PRENATAL VISIT DIALOGS
# ═══════════════════════════════════════════════════════════════════════════

class PrenatalVisitDialog(_BaseDialog):
    PRESENTATIONS = ["Cephalic", "Breech", "Transverse", "Oblique"]
    RISKS = ["Low Risk", "Moderate Risk", "High Risk"]

    def __init__(self, pregnancy_id, next_num, existing=None, parent=None):
        verb = "Edit" if existing else "Record"
        super().__init__(f"{verb} Visit #{next_num if not existing else existing.get('visit_num', '?')}", parent)
        self.pregnancy_id = pregnancy_id
        self.next_num = next_num
        self.existing = existing

        self.f_date  = self._date()
        self.f_aog   = self._field("e.g. 28")
        self.f_staff = self._field("e.g. Dr. Reyes")
        self.f_bp    = self._field("e.g. 120/80")
        self.f_wt    = self._field("e.g. 62.5")
        self.f_fht   = self._field("e.g. 144  (leave blank if N/A)")
        self.f_fh    = self._field("e.g. 28  (leave blank if N/A)")
        self.f_pres  = self._combo(self.PRESENTATIONS)
        self.f_risk  = self._combo(self.RISKS)

        for label, w in [
            ("Visit Date *",       self.f_date),
            ("AOG (weeks) *",      self.f_aog),
            ("Staff / Doctor *",   self.f_staff),
            ("Blood Pressure *",   self.f_bp),
            ("Weight (kg) *",      self.f_wt),
            ("FHT (bpm)",          self.f_fht),
            ("Fundal Height (cm)", self.f_fh),
            ("Presentation",       self.f_pres),
            ("Risk Assessment",    self.f_risk),
        ]:
            self._row(label, w)

        if existing:
            self.f_date.setDate(QDate.fromString(str(existing.get("visit_date", "")), "yyyy-MM-dd"))
            self.f_aog.setText(str(existing.get("aog_weeks", "")))
            self.f_staff.setText(existing.get("staff", ""))
            self.f_bp.setText(existing.get("bp", ""))
            self.f_wt.setText(str(existing.get("weight_kg", "")))
            self.f_fht.setText(str(existing.get("fht_bpm", "")) if existing.get("fht_bpm") else "")
            self.f_fh.setText(str(existing.get("fh_cm", "")) if existing.get("fh_cm") else "")
            idx = self.f_pres.findText(existing.get("presentation", ""))
            if idx >= 0: self.f_pres.setCurrentIndex(idx)
            idx = self.f_risk.findText(existing.get("risk_assessment", ""))
            if idx >= 0: self.f_risk.setCurrentIndex(idx)

        self._add_buttons(self._on_save)

    def _on_save(self):
        aog = self.f_aog.text().strip()
        staff = self.f_staff.text().strip()
        bp = self.f_bp.text().strip()
        wt = self.f_wt.text().strip()
        if not all([aog, staff, bp, wt]):
            QMessageBox.warning(self, "Missing", "Please fill in all required (*) fields.")
            return
        try:
            aog_v = int(aog)
            wt_v = float(wt)
        except ValueError:
            QMessageBox.warning(self, "Bad input", "AOG must be a whole number; weight must be numeric.")
            return
        fht = self.f_fht.text().strip()
        fh = self.f_fh.text().strip()
        try:
            fht_v = int(fht) if fht else None
            fh_v = float(fh) if fh else None
        except ValueError:
            QMessageBox.warning(self, "Bad input", "FHT and FH must be numbers if provided.")
            return

        self.result_data = {
            "pregnancy_id":    self.pregnancy_id,
            "visit_num":       self.next_num if not self.existing else self.existing["visit_num"],
            "visit_date":      self.f_date.date().toString("yyyy-MM-dd"),
            "aog_weeks":       aog_v,
            "staff":           staff,
            "bp":              bp,
            "weight_kg":       wt_v,
            "fht_bpm":         fht_v,
            "fh_cm":           fh_v,
            "presentation":    self.f_pres.currentText(),
            "risk_assessment": self.f_risk.currentText(),
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
        "CBC", "Urinalysis", "Blood Typing", "Blood Sugar (FBS)",
        "HbsAg", "HIV Test", "Syphilis Test", "STI Screening",
        "Ultrasound", "GCT", "OGTT", "Other"
    ]
    RESULTS = ["Pending", "Normal", "Abnormal", "Referred"]

    def __init__(self, pregnancy_id, existing=None, parent=None):
        super().__init__("Edit Lab / Referral" if existing else "Add Lab / Referral", parent)
        self.pregnancy_id = pregnancy_id
        self.existing = existing

        self.f_date   = self._date()
        self.f_type   = self._combo(self.LAB_TYPES)
        self.f_result = self._combo(self.RESULTS)
        self.f_notes  = QTextEdit()
        self.f_notes.setFixedHeight(70)
        self.f_notes.setPlaceholderText("Additional notes...")
        self.f_notes.setStyleSheet(FIELD_STYLE)

        self._row("Date *",      self.f_date)
        self._row("Lab / Test *", self.f_type)
        self._row("Result",      self.f_result)
        self._row("Notes",       self.f_notes)

        if existing:
            d = existing.get("lab_date")
            if d:
                self.f_date.setDate(QDate.fromString(str(d), "yyyy-MM-dd"))
            idx = self.f_type.findText(existing.get("lab_type", ""))
            if idx >= 0: self.f_type.setCurrentIndex(idx)
            idx = self.f_result.findText(existing.get("result", ""))
            if idx >= 0: self.f_result.setCurrentIndex(idx)
            self.f_notes.setPlainText(existing.get("notes", "") or "")

        self._add_buttons(self._on_save)

    def _on_save(self):
        self.result_data = {
            "pregnancy_id": self.pregnancy_id,
            "lab_date":     self.f_date.date().toString("yyyy-MM-dd"),
            "lab_type":     self.f_type.currentText(),
            "result":       self.f_result.currentText(),
            "notes":        self.f_notes.toPlainText().strip() or None,
        }
        self.accept()


# ═══════════════════════════════════════════════════════════════════════════
# MEDICATION DIALOGS
# ═══════════════════════════════════════════════════════════════════════════

class MedicationDialog(_BaseDialog):
    ROUTES = ["Oral", "IV", "IM", "Topical", "Sublingual", "Other"]

    def __init__(self, pregnancy_id, existing=None, parent=None):
        super().__init__("Edit Medication" if existing else "Add Medication", parent)
        self.pregnancy_id = pregnancy_id
        self.existing = existing

        self.f_name    = self._field("e.g. Ferrous Sulfate")
        self.f_dosage  = self._field("e.g. 325 mg")
        self.f_freq    = self._field("e.g. Once daily")
        self.f_route   = self._combo(self.ROUTES)
        self.f_start   = self._date()
        self.f_end     = self._date(QDate.currentDate().addDays(30))
        self.f_notes   = self._field("Optional notes")

        self._row("Medicine Name *", self.f_name)
        self._row("Dosage *",        self.f_dosage)
        self._row("Frequency *",     self.f_freq)
        self._row("Route",           self.f_route)
        self._row("Start Date",      self.f_start)
        self._row("End Date",        self.f_end)
        self._row("Notes",           self.f_notes)

        if existing:
            self.f_name.setText(existing.get("medicine_name", ""))
            self.f_dosage.setText(existing.get("dosage", ""))
            self.f_freq.setText(existing.get("frequency", ""))
            idx = self.f_route.findText(existing.get("route", ""))
            if idx >= 0: self.f_route.setCurrentIndex(idx)
            d = existing.get("start_date")
            if d: self.f_start.setDate(QDate.fromString(str(d), "yyyy-MM-dd"))
            d = existing.get("end_date")
            if d: self.f_end.setDate(QDate.fromString(str(d), "yyyy-MM-dd"))
            self.f_notes.setText(existing.get("notes", "") or "")

        self._add_buttons(self._on_save)

    def _on_save(self):
        name = self.f_name.text().strip()
        dosage = self.f_dosage.text().strip()
        freq = self.f_freq.text().strip()
        if not all([name, dosage, freq]):
            QMessageBox.warning(self, "Missing", "Medicine name, dosage, and frequency are required.")
            return
        self.result_data = {
            "pregnancy_id":  self.pregnancy_id,
            "medicine_name": name,
            "dosage":        dosage,
            "frequency":     freq,
            "route":         self.f_route.currentText(),
            "start_date":    self.f_start.date().toString("yyyy-MM-dd"),
            "end_date":      self.f_end.date().toString("yyyy-MM-dd"),
            "notes":         self.f_notes.text().strip() or None,
        }
        self.accept()


# ═══════════════════════════════════════════════════════════════════════════
# DELIVERY & NEWBORN DIALOGS
# ═══════════════════════════════════════════════════════════════════════════

class DeliveryDialog(_BaseDialog):
    DELIVERY_TYPES = ["Normal Spontaneous Delivery", "Cesarean Section",
                      "Assisted Vaginal Delivery", "Other"]
    OUTCOMES = ["Live Birth", "Stillbirth", "Miscarriage"]

    def __init__(self, pregnancy_id, existing=None, parent=None):
        super().__init__("Edit Delivery Record" if existing else "Record Delivery", parent)
        self.pregnancy_id = pregnancy_id
        self.existing = existing

        self.f_date         = self._date()
        self.f_type         = self._combo(self.DELIVERY_TYPES)
        self.f_outcome      = self._combo(self.OUTCOMES)
        self.f_attendant    = self._field("e.g. Dr. Reyes")
        self.f_place        = self._field("e.g. Materna Clinic")
        self.f_complications = self._field("e.g. None  (leave blank if none)")
        self.f_notes        = self._field("Additional notes")

        self._row("Delivery Date *",   self.f_date)
        self._row("Delivery Type *",   self.f_type)
        self._row("Outcome *",         self.f_outcome)
        self._row("Attendant *",       self.f_attendant)
        self._row("Place of Delivery", self.f_place)
        self._row("Complications",     self.f_complications)
        self._row("Notes",             self.f_notes)

        if existing:
            d = existing.get("delivery_date")
            if d: self.f_date.setDate(QDate.fromString(str(d), "yyyy-MM-dd"))
            idx = self.f_type.findText(existing.get("delivery_type", ""))
            if idx >= 0: self.f_type.setCurrentIndex(idx)
            idx = self.f_outcome.findText(existing.get("outcome", ""))
            if idx >= 0: self.f_outcome.setCurrentIndex(idx)
            self.f_attendant.setText(existing.get("attendant", ""))
            self.f_place.setText(existing.get("place_of_delivery", "") or "")
            self.f_complications.setText(existing.get("complications", "") or "")
            self.f_notes.setText(existing.get("notes", "") or "")

        self._add_buttons(self._on_save)

    def _on_save(self):
        attendant = self.f_attendant.text().strip()
        if not attendant:
            QMessageBox.warning(self, "Missing", "Attendant is required.")
            return
        self.result_data = {
            "pregnancy_id":   self.pregnancy_id,
            "delivery_date":  self.f_date.date().toString("yyyy-MM-dd"),
            "delivery_type":  self.f_type.currentText(),
            "outcome":        self.f_outcome.currentText(),
            "attendant":      attendant,
            "place_of_delivery": self.f_place.text().strip() or None,
            "complications":  self.f_complications.text().strip() or None,
            "notes":          self.f_notes.text().strip() or None,
        }
        self.accept()


class NewbornDialog(_BaseDialog):
    SEX = ["Female", "Male", "Undetermined"]

    def __init__(self, pregnancy_id, existing=None, parent=None):
        super().__init__("Edit Newborn Record" if existing else "Record Newborn", parent)
        self.pregnancy_id = pregnancy_id
        self.existing = existing

        self.f_name     = self._field("e.g. Baby Girl Santos")
        self.f_dob      = self._date()
        self.f_sex      = self._combo(self.SEX)
        self.f_weight   = self._field("e.g. 3.2")
        self.f_length   = self._field("e.g. 50  (cm)")
        self.f_apgar1   = self._field("e.g. 8")
        self.f_apgar5   = self._field("e.g. 9")
        self.f_notes    = self._field("Additional notes")

        self._row("Baby's Name",     self.f_name)
        self._row("Date of Birth",   self.f_dob)
        self._row("Sex *",           self.f_sex)
        self._row("Weight (kg) *",   self.f_weight)
        self._row("Length (cm)",     self.f_length)
        self._row("APGAR Score (1 min)", self.f_apgar1)
        self._row("APGAR Score (5 min)", self.f_apgar5)
        self._row("Notes",           self.f_notes)

        if existing:
            self.f_name.setText(existing.get("baby_name", "") or "")
            d = existing.get("date_of_birth")
            if d: self.f_dob.setDate(QDate.fromString(str(d), "yyyy-MM-dd"))
            idx = self.f_sex.findText(existing.get("sex", ""))
            if idx >= 0: self.f_sex.setCurrentIndex(idx)
            self.f_weight.setText(str(existing.get("birth_weight_kg", "")) if existing.get("birth_weight_kg") else "")
            self.f_length.setText(str(existing.get("birth_length_cm", "")) if existing.get("birth_length_cm") else "")
            self.f_apgar1.setText(str(existing.get("apgar_1min", "")) if existing.get("apgar_1min") is not None else "")
            self.f_apgar5.setText(str(existing.get("apgar_5min", "")) if existing.get("apgar_5min") is not None else "")
            self.f_notes.setText(existing.get("notes", "") or "")

        self._add_buttons(self._on_save)

    def _on_save(self):
        wt = self.f_weight.text().strip()
        sex = self.f_sex.currentText()
        if not wt:
            QMessageBox.warning(self, "Missing", "Birth weight is required.")
            return
        try:
            wt_v = float(wt)
        except ValueError:
            QMessageBox.warning(self, "Bad input", "Weight must be a number.")
            return
        a1 = self.f_apgar1.text().strip()
        a5 = self.f_apgar5.text().strip()
        ln = self.f_length.text().strip()
        try:
            a1_v = int(a1) if a1 else None
            a5_v = int(a5) if a5 else None
            ln_v = float(ln) if ln else None
        except ValueError:
            QMessageBox.warning(self, "Bad input", "APGAR scores must be whole numbers; length must be numeric.")
            return
        self.result_data = {
            "pregnancy_id":    self.pregnancy_id,
            "baby_name":       self.f_name.text().strip() or None,
            "date_of_birth":   self.f_dob.date().toString("yyyy-MM-dd"),
            "sex":             sex,
            "birth_weight_kg": wt_v,
            "birth_length_cm": ln_v,
            "apgar_1min":      a1_v,
            "apgar_5min":      a5_v,
            "notes":           self.f_notes.text().strip() or None,
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
            # rename the repurposed tab at runtime
            self.ui.tab_visit_history.setText("Medications")
            o = ordinal(self._pregnancy_num)
            self.ui.title_label.setText(f"PRENATAL CARE  –  {o.upper()} PREGNANCY")
            # relabel the "add prescription" button to match the active tab
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
            if item.widget():
                item.widget().deleteLater()

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
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT visit_id, pregnancy_id, visit_num, visit_date, aog_weeks,
                       staff, bp, weight_kg, fht_bpm, fh_cm,
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

        lay = self.ui.scroll_layout
        cols = ["visit_id","pregnancy_id","visit_num","visit_date","aog_weeks",
                "staff","bp","weight_kg","fht_bpm","fh_cm","presentation","risk_assessment"]

        if not rows:
            self._empty_msg("No prenatal visits yet. Click '+ Record Visit' to add the first one.")
            return

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
                    (pregnancy_id, visit_num, visit_date, aog_weeks, staff,
                     bp, weight_kg, fht_bpm, fh_cm, presentation, risk_assessment)
                VALUES (%(pregnancy_id)s,%(visit_num)s,%(visit_date)s,%(aog_weeks)s,%(staff)s,
                        %(bp)s,%(weight_kg)s,%(fht_bpm)s,%(fh_cm)s,%(presentation)s,%(risk_assessment)s)
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
                    visit_date=%(visit_date)s, aog_weeks=%(aog_weeks)s, staff=%(staff)s,
                    bp=%(bp)s, weight_kg=%(weight_kg)s, fht_bpm=%(fht_bpm)s, fh_cm=%(fh_cm)s,
                    presentation=%(presentation)s, risk_assessment=%(risk_assessment)s
                WHERE visit_id=%(visit_id)s
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
                SELECT lab_id, pregnancy_id, lab_date, lab_type, result, notes
                FROM lab_referral
                WHERE pregnancy_id=%s ORDER BY lab_date DESC
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

        cols = ["lab_id","pregnancy_id","lab_date","lab_type","result","notes"]
        tbl = self._make_table(["Date","Lab / Test","Result","Notes","",""])
        lay = self.ui.scroll_layout
        lay.insertWidget(lay.count() - 1, tbl)

        RESULT_COLORS = {
            "Normal":   QColor(220,240,220),
            "Abnormal": QColor(255,220,220),
            "Pending":  QColor(255,243,205),
            "Referred": QColor(220,230,255),
        }

        for row in rows:
            r = dict(zip(cols, row))
            ri = tbl.rowCount(); tbl.insertRow(ri)
            tbl.setItem(ri, 0, self._cell(fmt_date(r["lab_date"])))
            tbl.setItem(ri, 1, self._cell(r["lab_type"]))
            res_item = self._cell(r["result"])
            res_item.setBackground(QBrush(RESULT_COLORS.get(r["result"], QColor(240,230,240))))
            tbl.setItem(ri, 2, res_item)
            tbl.setItem(ri, 3, self._cell(r["notes"] or ""))

            btn_e = QPushButton("Edit")
            btn_e.setStyleSheet("background-color: rgb(192,116,182); color: white; border-radius:4px; font-size:11px;")
            btn_e.clicked.connect((lambda rec: lambda: self._edit_lab(rec))(r))
            tbl.setCellWidget(ri, 4, btn_e)

            btn_d = QPushButton("Delete")
            btn_d.setStyleSheet("background-color: rgb(200,50,50); color: white; border-radius:4px; font-size:11px;")
            btn_d.clicked.connect((lambda rec: lambda: self._delete_lab(rec))(r))
            tbl.setCellWidget(ri, 5, btn_d)

    def _add_lab_referral(self):
        dlg = LabReferralDialog(self._pregnancy_id, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._save_lab(dlg.result_data)

    def _edit_lab(self, rec: dict):
        dlg = LabReferralDialog(self._pregnancy_id, existing=rec, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._update_lab(rec["lab_id"], dlg.result_data)

    def _delete_lab(self, rec: dict):
        if QMessageBox.question(self, "Delete", f"Delete this lab record ({rec.get('lab_type','')})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes: return
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM lab_referral WHERE lab_id=%s", (rec["lab_id"],))
            conn.commit(); conn.close()
            self._switch_tab(TAB_LAB)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            if conn: conn.close()

    def _save_lab(self, data):
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO lab_referral (pregnancy_id, lab_date, lab_type, result, notes)
                VALUES (%(pregnancy_id)s,%(lab_date)s,%(lab_type)s,%(result)s,%(notes)s)
            """, data)
            conn.commit(); conn.close()
            self._switch_tab(TAB_LAB)
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))
            if conn: conn.close()

    def _update_lab(self, lab_id, data):
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE lab_referral SET lab_date=%(lab_date)s, lab_type=%(lab_type)s,
                    result=%(result)s, notes=%(notes)s
                WHERE lab_id=%(lab_id)s
            """, {**data, "lab_id": lab_id})
            conn.commit(); conn.close()
            self._switch_tab(TAB_LAB)
        except Exception as e:
            QMessageBox.critical(self, "Update Error", str(e))
            if conn: conn.close()

    # ═══════════════════════════════════════════════════════════════════════
    # MEDICATIONS TAB  (no dedicated tab button in UI — wired via visit history btn for now)
    # ═══════════════════════════════════════════════════════════════════════

    def _load_medications(self):
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT med_id, pregnancy_id, medicine_name, dosage, frequency,
                       route, start_date, end_date, notes
                FROM pregnancy_medication
                WHERE pregnancy_id=%s ORDER BY start_date DESC
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

        cols = ["med_id","pregnancy_id","medicine_name","dosage","frequency","route","start_date","end_date","notes"]
        tbl = self._make_table(["Medicine","Dosage","Frequency","Route","Start","End","Notes","",""])
        lay = self.ui.scroll_layout
        lay.insertWidget(lay.count() - 1, tbl)

        for row in rows:
            r = dict(zip(cols, row))
            ri = tbl.rowCount(); tbl.insertRow(ri)
            tbl.setItem(ri, 0, self._cell(r["medicine_name"]))
            tbl.setItem(ri, 1, self._cell(r["dosage"]))
            tbl.setItem(ri, 2, self._cell(r["frequency"]))
            tbl.setItem(ri, 3, self._cell(r["route"]))
            tbl.setItem(ri, 4, self._cell(fmt_date(r["start_date"])))
            tbl.setItem(ri, 5, self._cell(fmt_date(r["end_date"])))
            tbl.setItem(ri, 6, self._cell(r["notes"] or ""))

            btn_e = QPushButton("Edit")
            btn_e.setStyleSheet("background-color: rgb(192,116,182); color: white; border-radius:4px; font-size:11px;")
            btn_e.clicked.connect((lambda rec: lambda: self._edit_medication(rec))(r))
            tbl.setCellWidget(ri, 7, btn_e)

            btn_d = QPushButton("Delete")
            btn_d.setStyleSheet("background-color: rgb(200,50,50); color: white; border-radius:4px; font-size:11px;")
            btn_d.clicked.connect((lambda rec: lambda: self._delete_medication(rec))(r))
            tbl.setCellWidget(ri, 8, btn_d)

    def _add_medication(self):
        dlg = MedicationDialog(self._pregnancy_id, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO pregnancy_medication
                        (pregnancy_id, medicine_name, dosage, frequency, route, start_date, end_date, notes)
                    VALUES (%(pregnancy_id)s,%(medicine_name)s,%(dosage)s,%(frequency)s,
                            %(route)s,%(start_date)s,%(end_date)s,%(notes)s)
                """, dlg.result_data)
                conn.commit(); conn.close()
                self._switch_tab(TAB_MED)
            except Exception as e:
                QMessageBox.critical(self, "Save Error", str(e))
                if conn: conn.close()

    def _edit_medication(self, rec: dict):
        dlg = MedicationDialog(self._pregnancy_id, existing=rec, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE pregnancy_medication SET medicine_name=%(medicine_name)s, dosage=%(dosage)s,
                        frequency=%(frequency)s, route=%(route)s, start_date=%(start_date)s,
                        end_date=%(end_date)s, notes=%(notes)s
                    WHERE med_id=%(med_id)s
                """, {**dlg.result_data, "med_id": rec["med_id"]})
                conn.commit(); conn.close()
                self._switch_tab(TAB_MED)
            except Exception as e:
                QMessageBox.critical(self, "Update Error", str(e))
                if conn: conn.close()

    def _delete_medication(self, rec: dict):
        if QMessageBox.question(self, "Delete", f"Delete {rec.get('medicine_name','')}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes: return
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM pregnancy_medication WHERE med_id=%s", (rec["med_id"],))
            conn.commit(); conn.close()
            self._switch_tab(TAB_MED)
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
                SELECT delivery_id, pregnancy_id, delivery_date, delivery_type,
                       outcome, attendant, place_of_delivery, complications, notes
                FROM delivery_record WHERE pregnancy_id=%s
            """, (self._pregnancy_id,))
            deliveries = cur.fetchall()
            cur.execute("""
                SELECT newborn_id, pregnancy_id, baby_name, date_of_birth, sex,
                       birth_weight_kg, birth_length_cm, apgar_1min, apgar_5min, notes
                FROM newborn_record WHERE pregnancy_id=%s
            """, (self._pregnancy_id,))
            newborns = cur.fetchall()
            conn.close()
        except Exception as e:
            print(f"delivery load error: {e}")
            if conn: conn.close()
            deliveries, newborns = [], []

        lay = self.ui.scroll_layout
        d_cols = ["delivery_id","pregnancy_id","delivery_date","delivery_type",
                  "outcome","attendant","place_of_delivery","complications","notes"]
        n_cols = ["newborn_id","pregnancy_id","baby_name","date_of_birth","sex",
                  "birth_weight_kg","birth_length_cm","apgar_1min","apgar_5min","notes"]

        # delivery section header
        hdr = self._section_header("Delivery Record", self._add_delivery)
        lay.insertWidget(lay.count() - 1, hdr)

        if deliveries:
            for row in deliveries:
                d = dict(zip(d_cols, row))
                card = self._delivery_card(d)
                lay.insertWidget(lay.count() - 1, card)
        else:
            lay.insertWidget(lay.count() - 1, self._inline_msg("No delivery record yet."))

        # newborn section header
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
                        (pregnancy_id, delivery_date, delivery_type, outcome,
                         attendant, place_of_delivery, complications, notes)
                    VALUES (%(pregnancy_id)s,%(delivery_date)s,%(delivery_type)s,%(outcome)s,
                            %(attendant)s,%(place_of_delivery)s,%(complications)s,%(notes)s)
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
                    UPDATE delivery_record SET delivery_date=%(delivery_date)s,
                        delivery_type=%(delivery_type)s, outcome=%(outcome)s,
                        attendant=%(attendant)s, place_of_delivery=%(place_of_delivery)s,
                        complications=%(complications)s, notes=%(notes)s
                    WHERE delivery_id=%(delivery_id)s
                """, {**dlg.result_data, "delivery_id": rec["delivery_id"]})
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

    def _add_newborn(self):
        dlg = NewbornDialog(self._pregnancy_id, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO newborn_record
                        (pregnancy_id, baby_name, date_of_birth, sex,
                         birth_weight_kg, birth_length_cm, apgar_1min, apgar_5min, notes)
                    VALUES (%(pregnancy_id)s,%(baby_name)s,%(date_of_birth)s,%(sex)s,
                            %(birth_weight_kg)s,%(birth_length_cm)s,%(apgar_1min)s,%(apgar_5min)s,%(notes)s)
                """, dlg.result_data)
                conn.commit(); conn.close()
                self._switch_tab(TAB_DELIVERY)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                if conn: conn.close()

    def _edit_newborn(self, rec: dict):
        dlg = NewbornDialog(self._pregnancy_id, existing=rec, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE newborn_record SET baby_name=%(baby_name)s, date_of_birth=%(date_of_birth)s,
                        sex=%(sex)s, birth_weight_kg=%(birth_weight_kg)s, birth_length_cm=%(birth_length_cm)s,
                        apgar_1min=%(apgar_1min)s, apgar_5min=%(apgar_5min)s, notes=%(notes)s
                    WHERE newborn_id=%(newborn_id)s
                """, {**dlg.result_data, "newborn_id": rec["newborn_id"]})
                conn.commit(); conn.close()
                self._switch_tab(TAB_DELIVERY)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                if conn: conn.close()

    def _delete_newborn(self, rec: dict):
        if QMessageBox.question(self, "Delete", f"Delete newborn record for {rec.get('baby_name','this baby')}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes: return
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM newborn_record WHERE newborn_id=%s", (rec["newborn_id"],))
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
        info.addWidget(stat("Outcome:", d.get("outcome","—")))
        info.addWidget(stat("Attendant:", d.get("attendant","—")))
        if d.get("place_of_delivery"):
            info.addWidget(stat("Place:", d["place_of_delivery"]))
        if d.get("complications"):
            info.addWidget(stat("Complications:", d["complications"]))
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
        name = n.get("baby_name") or "Baby"
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
        if n.get("birth_weight_kg"): info.addWidget(stat("Weight:", f"{n['birth_weight_kg']} kg"))
        if n.get("birth_length_cm"): info.addWidget(stat("Length:", f"{n['birth_length_cm']} cm"))
        if n.get("apgar_1min") is not None: info.addWidget(stat("APGAR 1min:", str(n["apgar_1min"])))
        if n.get("apgar_5min") is not None: info.addWidget(stat("APGAR 5min:", str(n["apgar_5min"])))
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
