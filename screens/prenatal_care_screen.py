"""
MaternaDB - Prenatal Care Screen
==================================
Logic file for the Prenatal Care screen.
Follows the same _screen.py pattern as dashboard_screen.py.

Required PostgreSQL table (run once in your DB):
-------------------------------------------------
CREATE TABLE IF NOT EXISTS prenatal_visit (
    visit_id     SERIAL PRIMARY KEY,
    patient_id   INTEGER REFERENCES patient_profile(patient_id),
    visit_num    INTEGER NOT NULL,
    visit_date   DATE NOT NULL,
    aog_weeks    INTEGER NOT NULL,
    staff        TEXT NOT NULL,
    bp           TEXT NOT NULL,
    weight_kg    DECIMAL(5, 2),
    fht_bpm      INTEGER,
    fh_cm        DECIMAL(4, 1),
    presentation TEXT DEFAULT 'Cephalic',
    risk_assessment TEXT DEFAULT 'Low Risk',
    edd          DATE
);
-------------------------------------------------
"""

from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame, QDialog, QFormLayout, QLineEdit,
    QComboBox, QDateEdit, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QPainter, QColor, QBrush, QPen, QFont

from screens.prenatal_care_ui import Ui_PrenatalCareScreen
from database import get_connection


# ── Small helper: the colored circle badge (V1, V2, V3) ───────────────────
class CircleBadge(QLabel):
    """Draws a filled circle with a visit number label inside."""
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self._text = text
        self.setFixedSize(50, 50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor(178, 100, 168)))   # rgb(178,100,168) — same purple as scrollbar
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, 50, 50)
        painter.setPen(QPen(QColor(255, 255, 255)))
        font = QFont("Segoe UI", 12)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._text)


# ── Diagnosis Dialog ────────────────────────────────────────────────────────
class DiagnosisDialog(QDialog):
    """
    Pop-up shown when 'View Diagnosis' is clicked.
    Displays: AOG, BP, Weight, FHT, FH, Presentation, Staff, Risk Assessment.
    """
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
        self.setStyleSheet("QDialog { background-color: rgb(240, 230, 240); }")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header strip (dark navy, same as navbar)
        header = QWidget()
        header.setStyleSheet("background-color: rgb(21, 23, 61);")
        header.setFixedHeight(72)
        h_lay = QVBoxLayout(header)
        h_lay.setContentsMargins(22, 12, 22, 12)

        title_lbl = QLabel(f"Visit #{self.visit.get('visit_num', '?')} Diagnosis")
        title_lbl.setStyleSheet(
            "color: white; font-size: 15px; font-weight: bold; font-family: 'Arial Black';"
        )
        sub_lbl = QLabel(
            f"{self._fmt_date(self.visit.get('visit_date', ''))}  ·  "
            f"AOG: {self.visit.get('aog_weeks', '—')} Weeks  ·  "
            f"{self.visit.get('staff', '—')}"
        )
        sub_lbl.setStyleSheet("color: rgba(255,255,255,0.72); font-size: 10px;")
        h_lay.addWidget(title_lbl)
        h_lay.addWidget(sub_lbl)
        layout.addWidget(header)

        # Body
        body = QWidget()
        body.setStyleSheet("background-color: rgb(240, 230, 240);")
        b_lay = QVBoxLayout(body)
        b_lay.setContentsMargins(22, 18, 22, 22)
        b_lay.setSpacing(12)

        def row(label_text, value_text):
            r = QHBoxLayout()
            lbl = QLabel(label_text)
            lbl.setFixedWidth(180)
            lbl.setStyleSheet("color: rgb(100, 80, 110); font-size: 11px;")
            val = QLabel(str(value_text) if value_text else "—")
            val.setStyleSheet(
                "color: rgb(21, 23, 61); font-size: 12px; font-weight: bold;"
            )
            r.addWidget(lbl)
            r.addWidget(val)
            r.addStretch()
            return r

        b_lay.addLayout(row("Age of Gestation (AOG)",
                            f"{self.visit.get('aog_weeks', '—')} Weeks"))
        b_lay.addLayout(row("Blood Pressure (BP)",
                            f"{self.visit.get('bp', '—')} mmHg"))
        b_lay.addLayout(row("Weight",
                            f"{self.visit.get('weight_kg', '—')} kg"))
        fht = self.visit.get('fht_bpm')
        b_lay.addLayout(row("Fetal Heart Tone (FHT)",
                            f"{fht} bpm" if fht else "—"))
        fh = self.visit.get('fh_cm')
        b_lay.addLayout(row("Fundal Height (FH)",
                            f"{fh} cm" if fh else "—"))
        b_lay.addLayout(row("Presentation",
                            self.visit.get('presentation', '—')))
        b_lay.addLayout(row("Staff / Attendant",
                            self.visit.get('staff', '—')))

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: rgb(210, 180, 210); max-height: 1px;")
        b_lay.addWidget(sep)

        # Risk Assessment chip
        risk = self.visit.get('risk_assessment', 'Low Risk')
        risk_row = QHBoxLayout()
        risk_lbl = QLabel("Risk Assessment")
        risk_lbl.setFixedWidth(180)
        risk_lbl.setStyleSheet("color: rgb(100, 80, 110); font-size: 11px;")
        risk_chip = QLabel(f"  {risk}  ")
        chip_style = self.RISK_STYLES.get(risk, "background-color: rgb(236,198,220);")
        risk_chip.setStyleSheet(
            f"{chip_style} border-radius: 10px; padding: 3px 8px; font-size: 11px; font-weight: bold;"
        )
        risk_row.addWidget(risk_lbl)
        risk_row.addWidget(risk_chip)
        risk_row.addStretch()
        b_lay.addLayout(risk_row)

        # Close button
        b_lay.addSpacing(6)
        btn_close = QPushButton("Close")
        btn_close.setFixedHeight(36)
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: rgb(21, 23, 61);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: rgb(192, 116, 182); }
        """)
        btn_close.clicked.connect(self.accept)
        b_lay.addWidget(btn_close)

        layout.addWidget(body)

    def _fmt_date(self, d):
        try:
            if hasattr(d, 'strftime'):
                return d.strftime("%B %d, %Y")
            from datetime import datetime
            return datetime.strptime(str(d), "%Y-%m-%d").strftime("%B %d, %Y")
        except Exception:
            return str(d)


# ── New Visit Dialog ─────────────────────────────────────────────────────────
class NewVisitDialog(QDialog):
    PRESENTATIONS = ["Cephalic", "Breech", "Transverse", "Oblique"]
    RISKS = ["Low Risk", "Moderate Risk", "High Risk"]

    def __init__(self, patient_id, next_visit_num, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.next_visit_num = next_visit_num
        self.setWindowTitle(f"Record Visit #{next_visit_num}")
        self.setMinimumWidth(400)
        self.setStyleSheet("QDialog { background-color: rgb(240, 230, 240); }")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)

        title = QLabel(f"Record Visit #{self.next_visit_num}")
        title.setStyleSheet(
            "color: rgb(21,23,61); font-size: 15px; font-weight: bold; font-family: 'Arial Black';"
        )
        layout.addWidget(title)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: rgb(210,180,210); max-height: 1px;")
        layout.addWidget(sep)

        field_style = """
            border: 1px solid rgb(158, 136, 163);
            border-radius: 6px;
            padding: 5px 8px;
            background-color: rgb(247, 247, 247);
            color: rgb(21, 23, 61);
            font-size: 12px;
        """

        form = QFormLayout()
        form.setSpacing(10)

        self.f_date = QDateEdit()
        self.f_date.setCalendarPopup(True)
        self.f_date.setDate(QDate.currentDate())
        self.f_date.setStyleSheet(field_style)

        self.f_aog = QLineEdit()
        self.f_aog.setPlaceholderText("e.g. 28")
        self.f_aog.setStyleSheet(field_style)

        self.f_staff = QLineEdit()
        self.f_staff.setPlaceholderText("e.g. Dr. Reyes")
        self.f_staff.setStyleSheet(field_style)

        self.f_bp = QLineEdit()
        self.f_bp.setPlaceholderText("e.g. 120/80")
        self.f_bp.setStyleSheet(field_style)

        self.f_weight = QLineEdit()
        self.f_weight.setPlaceholderText("e.g. 62.5")
        self.f_weight.setStyleSheet(field_style)

        self.f_fht = QLineEdit()
        self.f_fht.setPlaceholderText("e.g. 144  (leave blank if N/A)")
        self.f_fht.setStyleSheet(field_style)

        self.f_fh = QLineEdit()
        self.f_fh.setPlaceholderText("e.g. 28  (leave blank if N/A)")
        self.f_fh.setStyleSheet(field_style)

        self.f_presentation = QComboBox()
        self.f_presentation.addItems(self.PRESENTATIONS)
        self.f_presentation.setStyleSheet("""
            QComboBox {
                background-color: rgb(247,247,247);
                border: 1px solid rgb(158,136,163);
                border-radius: 6px;
                padding: 5px 8px;
                color: rgb(21,23,61);
                font-size: 12px;
            }
        """)

        self.f_risk = QComboBox()
        self.f_risk.addItems(self.RISKS)
        self.f_risk.setStyleSheet(self.f_presentation.styleSheet())

        self.f_edd = QDateEdit()
        self.f_edd.setCalendarPopup(True)
        self.f_edd.setDate(QDate.currentDate().addDays(120))
        self.f_edd.setStyleSheet(field_style)

        lbl_style = "color: rgb(21,23,61); font-size: 12px;"
        for lbl_text, widget in [
            ("Visit Date *",       self.f_date),
            ("AOG (weeks) *",      self.f_aog),
            ("Staff / Doctor *",   self.f_staff),
            ("Blood Pressure *",   self.f_bp),
            ("Weight (kg) *",      self.f_weight),
            ("FHT (bpm)",          self.f_fht),
            ("Fundal Height (cm)", self.f_fh),
            ("Presentation",       self.f_presentation),
            ("Risk Assessment",    self.f_risk),
            ("EDD",                self.f_edd),
        ]:
            lbl = QLabel(lbl_text)
            lbl.setStyleSheet(lbl_style)
            form.addRow(lbl, widget)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btns.addStretch()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: rgb(240,230,240);
                color: rgb(21,23,61);
                border: 1px solid rgb(158,136,163);
                border-radius: 8px;
                padding: 7px 18px;
                font-size: 12px;
            }
        """)
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("Save Visit")
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: rgb(21, 23, 61);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 7px 18px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: rgb(192, 116, 182); }
        """)
        btn_save.clicked.connect(self._on_save)

        btns.addWidget(btn_cancel)
        btns.addWidget(btn_save)
        layout.addLayout(btns)

    def _on_save(self):
        aog_text   = self.f_aog.text().strip()
        staff_text = self.f_staff.text().strip()
        bp_text    = self.f_bp.text().strip()
        weight_text = self.f_weight.text().strip()

        if not all([aog_text, staff_text, bp_text, weight_text]):
            QMessageBox.warning(self, "Missing Fields",
                                "Please fill in all required (*) fields.")
            return
        try:
            aog_val    = int(aog_text)
            weight_val = float(weight_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input",
                                "AOG must be a whole number. Weight must be a number.")
            return

        fht_text = self.f_fht.text().strip()
        fh_text  = self.f_fh.text().strip()
        try:
            fht_val = int(fht_text)   if fht_text else None
            fh_val  = float(fh_text)  if fh_text  else None
        except ValueError:
            QMessageBox.warning(self, "Invalid Input",
                                "FHT and FH must be numbers if provided.")
            return

        self.result_data = {
            "patient_id":       self.patient_id,
            "visit_num":        self.next_visit_num,
            "visit_date":       self.f_date.date().toString("yyyy-MM-dd"),
            "aog_weeks":        aog_val,
            "staff":            staff_text,
            "bp":               bp_text,
            "weight_kg":        weight_val,
            "fht_bpm":          fht_val,
            "fh_cm":            fh_val,
            "presentation":     self.f_presentation.currentText(),
            "risk_assessment":  self.f_risk.currentText(),
            "edd":              self.f_edd.date().toString("yyyy-MM-dd"),
        }
        self.accept()


# ── Visit Card Widget ────────────────────────────────────────────────────────
class VisitCard(QWidget):
    """
    One row in the prenatal visits list.
    Shows: visit number badge, title, date/staff, and vital signs.
    Includes a 'View Diagnosis' button.
    """
    def __init__(self, visit: dict, on_view_diagnosis, parent=None):
        super().__init__(parent)
        self.visit = visit
        self.on_view_diagnosis = on_view_diagnosis
        self._build()

    def _build(self):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(4, 0, 4, 0)
        outer.setSpacing(12)

        # Circle badge
        badge = CircleBadge(f"V{self.visit.get('visit_num', '?')}")
        outer.addWidget(badge, alignment=Qt.AlignmentFlag.AlignTop)

        # Card body
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgb(236, 198, 220);
                border-radius: 12px;
                border: 1px solid rgb(210, 177, 200);
            }
        """)
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(16, 12, 16, 12)
        card_lay.setSpacing(5)

        # Top row: title + button
        top_row = QHBoxLayout()

        aog = self.visit.get('aog_weeks', '?')
        num = self.visit.get('visit_num', '?')
        title_lbl = QLabel(f"{self._ordinal(num)} Prenatal Visit – AOG: {aog} Weeks")
        title_lbl.setStyleSheet(
            "color: rgb(21,23,61); font-size: 13px; font-weight: bold; border: none;"
        )

        btn_diag = QPushButton("View Diagnosis")
        btn_diag.setFixedHeight(28)
        btn_diag.setStyleSheet("""
            QPushButton {
                background-color: rgb(240, 230, 240);
                color: rgb(21, 23, 61);
                border: 1px solid rgb(21, 23, 61);
                border-radius: 6px;
                font-size: 11px;
                padding: 0 10px;
            }
            QPushButton:hover {
                background-color: rgb(21, 23, 61);
                color: white;
            }
        """)
        btn_diag.clicked.connect(lambda: self.on_view_diagnosis(self.visit))

        top_row.addWidget(title_lbl)
        top_row.addStretch()
        top_row.addWidget(btn_diag)
        card_lay.addLayout(top_row)

        # Subtitle: date | staff
        date_str = self._fmt_date(self.visit.get('visit_date', ''))
        staff = self.visit.get('staff', '—')
        sub_lbl = QLabel(f"{date_str}  |  {staff}")
        sub_lbl.setStyleSheet(
            "color: rgb(80, 60, 90); font-size: 10px; border: none;"
        )
        card_lay.addWidget(sub_lbl)

        # Stats row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(20)

        def stat(key_label, value):
            lbl = QLabel(f"<b>{key_label}</b> {value}")
            lbl.setStyleSheet("color: rgb(21,23,61); font-size: 11px; border: none;")
            lbl.setTextFormat(Qt.TextFormat.RichText)
            return lbl

        stats_row.addWidget(stat("BP:", f"{self.visit.get('bp', '—')} mmHg"))
        stats_row.addWidget(stat("Weight:", f"{self.visit.get('weight_kg', '—')} kg"))
        fht = self.visit.get('fht_bpm')
        if fht:
            stats_row.addWidget(stat("FHT:", f"{fht} bpm"))
        fh = self.visit.get('fh_cm')
        if fh:
            stats_row.addWidget(stat("FH:", f"{fh} cm"))
        pres = self.visit.get('presentation', 'Cephalic')
        if pres and pres != 'Cephalic':
            stats_row.addWidget(stat("Presentation:", pres))
        stats_row.addStretch()
        card_lay.addLayout(stats_row)

        outer.addWidget(card, stretch=1)

    def _ordinal(self, n):
        try:
            n = int(n)
            return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")
        except Exception:
            return str(n)

    def _fmt_date(self, d):
        try:
            if hasattr(d, 'strftime'):
                return d.strftime("%B %d, %Y")
            from datetime import datetime
            return datetime.strptime(str(d), "%Y-%m-%d").strftime("%B %d, %Y")
        except Exception:
            return str(d)


# ── Main Screen ─────────────────────────────────────────────────────────────
class PrenatalCareScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PrenatalCareScreen()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB - Prenatal Care")
        self._initialized = False
        self._current_patient_id = None

        # Sidebar navigation — same as dashboard_screen.py
        self.ui.pushButton.clicked.connect(self.go_to_dashboard)
        self.ui.pushButton_2.clicked.connect(self.go_to_patient_records)
        self.ui.pushButton_3.clicked.connect(self.go_to_prenatal_care)
        self.ui.pushButton_4.clicked.connect(self.go_to_appointments)
        self.ui.pushButton_5.clicked.connect(self.logout)

        # Prenatal-specific actions
        self.ui.patient_combo.currentIndexChanged.connect(self.on_patient_selected)
        self.ui.btn_record_visit.clicked.connect(self.on_record_new_visit)

    def showEvent(self, event):
        super().showEvent(event)
        if not self._initialized:
            self._initialized = True
            self.reposition_elements()
            self.load_logo()
            self.load_patients()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.reposition_elements()

    def reposition_elements(self):
        w = self.width()
        h = self.height()

        # Navbar
        self.ui.frame_2.setGeometry(0, 0, w, 61)

        # Sidebar
        self.ui.frame.setGeometry(0, 61, 231, h - 61)

        # Main content area
        main_x = 231
        main_w = w - 231
        main_h = h - 61
        self.ui.frame_3.setGeometry(main_x, 61, main_w, main_h)

        card_w = main_w - 80   # 40px margin on each side

        # Title
        self.ui.title_label.setGeometry(40, 20, 400, 61)

        # Patient selector
        self.ui.patient_selector_label.setGeometry(40, 88, 110, 28)
        self.ui.patient_combo.setGeometry(155, 85, min(320, card_w - 200), 28)

        # Patient info card
        self.ui.patient_info_frame.setGeometry(40, 122, card_w, 70)
        self.ui.btn_record_visit.setGeometry(card_w - 120, 18, 110, 32)
        self.ui.btn_add_prescription.setGeometry(card_w - 240, 18, 110, 32)

        # Tab bar
        self.ui.tab_frame.setGeometry(40, 200, card_w, 40)
        self.ui.tab_line.setGeometry(40, 238, card_w, 1)

        # Scroll area — fills the rest of the content area
        scroll_h = main_h - 260
        self.ui.scroll_area.setGeometry(40, 245, card_w, max(scroll_h, 200))

    def load_logo(self):
        pixmap = QPixmap("Asset/MaternaDB_logo.png")
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                self.ui.logo.width(),
                self.ui.logo.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.ui.logo.setPixmap(scaled)
            self.ui.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # ── Patient loading ──────────────────────────────────────────────────────
    def load_patients(self):
        """Populate the patient combo box from the database."""
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT patient_id,
                       CONCAT(last_name, ', ', first_name,
                              CASE WHEN middle_name IS NOT NULL AND middle_name <> ''
                                   THEN ' ' || middle_name ELSE '' END)
                FROM patient_profile
                WHERE patient_type = 'Maternal'
                ORDER BY last_name, first_name
            """)
            patients = cursor.fetchall()
            conn.close()

            self.ui.patient_combo.blockSignals(True)
            self.ui.patient_combo.clear()
            self.ui.patient_combo.addItem("— Select a patient —", userData=None)
            for pid, name in patients:
                self.ui.patient_combo.addItem(name, userData=pid)
            self.ui.patient_combo.blockSignals(False)

        except Exception as e:
            print(f"Error loading patients: {e}")
            if conn:
                conn.close()

    def on_patient_selected(self, index):
        patient_id = self.ui.patient_combo.currentData()
        if patient_id is None:
            self._current_patient_id = None
            self.ui.patient_name_label.setText("—")
            self.ui.patient_sub_label.setText(
                "Select a patient above to view their prenatal visits."
            )
            self._clear_visit_cards()
            return
        self._current_patient_id = patient_id
        self.load_patient_info(patient_id)
        self.load_prenatal_visits(patient_id)

    def load_patient_info(self, patient_id):
        """Load and display the selected patient's header info."""
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT patient_id,
                       CONCAT(last_name, ', ', first_name,
                              CASE WHEN middle_name IS NOT NULL AND middle_name <> ''
                                   THEN ' ' || middle_name ELSE '' END),
                       age, patient_type
                FROM patient_profile
                WHERE patient_id = %s
            """, (patient_id,))
            row = cursor.fetchone()

            # Get latest EDD from prenatal_visit
            cursor.execute("""
                SELECT edd FROM prenatal_visit
                WHERE patient_id = %s
                ORDER BY visit_num DESC LIMIT 1
            """, (patient_id,))
            edd_row = cursor.fetchone()
            conn.close()

            if row:
                pid, name, age, ptype = row
                edd_text = ""
                if edd_row and edd_row[0]:
                    edd_text = f"  •  EDD: {self._fmt_date(edd_row[0])}"
                self.ui.patient_name_label.setText(name)
                self.ui.patient_sub_label.setText(
                    f"Patient ID: #{pid}  •  Age: {age or '—'}  "
                    f"•  Type: {ptype or '—'}{edd_text}"
                )

        except Exception as e:
            print(f"Error loading patient info: {e}")
            if conn:
                conn.close()

    # ── Visit cards ──────────────────────────────────────────────────────────
    def load_prenatal_visits(self, patient_id):
        """Fetch prenatal visits from DB and render as cards in the scroll area."""
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT visit_id, patient_id, visit_num, visit_date, aog_weeks,
                       staff, bp, weight_kg, fht_bpm, fh_cm,
                       presentation, risk_assessment, edd
                FROM prenatal_visit
                WHERE patient_id = %s
                ORDER BY visit_num DESC
            """, (patient_id,))
            rows = cursor.fetchall()

            # Also get EDD from latest visit for the top card
            edd = None
            if rows:
                # edd is the 13th column (index 12)
                edd = rows[0][12]

            conn.close()
        except Exception as e:
            print(f"Error loading prenatal visits: {e}")
            if conn:
                conn.close()
            rows = []
            edd = None

        self._clear_visit_cards()

        layout = self.ui.scroll_layout

        # EDD banner card
        if edd:
            edd_card = QFrame()
            edd_card.setStyleSheet("""
                QFrame {
                    background-color: rgb(236, 198, 220);
                    border-radius: 10px;
                    border: 1px solid rgb(210, 177, 200);
                }
            """)
            edd_card.setFixedHeight(46)
            edd_lay = QHBoxLayout(edd_card)
            edd_lay.setContentsMargins(16, 0, 16, 0)
            edd_lbl = QLabel(f"<b>EDD:</b>  {self._fmt_date(edd)}")
            edd_lbl.setTextFormat(Qt.TextFormat.RichText)
            edd_lbl.setStyleSheet(
                "color: rgb(21,23,61); font-size: 12px; border: none;"
            )
            edd_lay.addWidget(edd_lbl)
            edd_lay.addStretch()
            # Insert before the stretch at end
            layout.insertWidget(layout.count() - 1, edd_card)

        if not rows:
            empty_lbl = QLabel("No prenatal visits recorded yet for this patient.")
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_lbl.setStyleSheet(
                "color: rgb(100,80,110); font-size: 13px; padding: 30px;"
            )
            layout.insertWidget(layout.count() - 1, empty_lbl)
            return

        columns = [
            "visit_id", "patient_id", "visit_num", "visit_date", "aog_weeks",
            "staff", "bp", "weight_kg", "fht_bpm", "fh_cm",
            "presentation", "risk_assessment", "edd"
        ]
        for row in rows:
            visit = dict(zip(columns, row))
            card = VisitCard(visit, on_view_diagnosis=self._show_diagnosis)
            layout.insertWidget(layout.count() - 1, card)

    def _clear_visit_cards(self):
        """Remove all dynamically-added visit cards from the scroll area."""
        layout = self.ui.scroll_layout
        # Remove everything except the final stretch item
        while layout.count() > 1:
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _show_diagnosis(self, visit: dict):
        dlg = DiagnosisDialog(visit, parent=self)
        dlg.exec()

    # ── Record new visit ─────────────────────────────────────────────────────
    def on_record_new_visit(self):
        if self._current_patient_id is None:
            QMessageBox.warning(self, "No Patient Selected",
                                "Please select a patient first.")
            return

        # Determine next visit number
        conn = get_connection()
        next_num = 1
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COALESCE(MAX(visit_num), 0) + 1
                    FROM prenatal_visit
                    WHERE patient_id = %s
                """, (self._current_patient_id,))
                result = cursor.fetchone()
                next_num = result[0] if result else 1
                conn.close()
            except Exception as e:
                print(f"Error getting next visit num: {e}")
                if conn:
                    conn.close()

        dlg = NewVisitDialog(self._current_patient_id, next_num, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._save_visit(dlg.result_data)

    def _save_visit(self, data: dict):
        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "DB Error", "Could not connect to the database.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO prenatal_visit
                    (patient_id, visit_num, visit_date, aog_weeks, staff,
                     bp, weight_kg, fht_bpm, fh_cm, presentation,
                     risk_assessment, edd)
                VALUES
                    (%(patient_id)s, %(visit_num)s, %(visit_date)s, %(aog_weeks)s,
                     %(staff)s, %(bp)s, %(weight_kg)s, %(fht_bpm)s, %(fh_cm)s,
                     %(presentation)s, %(risk_assessment)s, %(edd)s)
            """, data)
            conn.commit()
            conn.close()
            # Refresh the cards
            self.load_patient_info(self._current_patient_id)
            self.load_prenatal_visits(self._current_patient_id)
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Could not save visit:\n{e}")
            if conn:
                conn.close()

    # ── Sidebar navigation (same as dashboard_screen.py) ────────────────────
    def go_to_dashboard(self):
        from screens.dashboard_screen import DashboardScreen
        self.dashboard = DashboardScreen()
        self.dashboard.showMaximized()
        self.close()

    def go_to_patient_records(self):
        print("Go to Patient Records")

    def go_to_prenatal_care(self):
        pass   # Already here

    def go_to_appointments(self):
        print("Go to Appointments")

    def logout(self):
        from screens.login_screen import LoginScreen
        self.login_window = LoginScreen()
        self.login_window.showMaximized()
        self.close()

    # ── Utility ─────────────────────────────────────────────────────────────
    def _fmt_date(self, d):
        try:
            if hasattr(d, 'strftime'):
                return d.strftime("%B %d, %Y")
            from datetime import datetime
            return datetime.strptime(str(d), "%Y-%m-%d").strftime("%B %d, %Y")
        except Exception:
            return str(d)
