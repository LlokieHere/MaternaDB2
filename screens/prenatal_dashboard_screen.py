from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QFrame, QDialog, QFormLayout, QDateEdit,
    QComboBox, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QFont, QPainter, QColor, QBrush, QPen

from screens.prenatal_dashboard_ui import Ui_PrenatalDashboardScreen
from database import get_connection
import user_profile.session as session


def ordinal(n):
    try:
        n = int(n)
        return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")
    except Exception:
        return str(n)


def fmt_date(d):
    try:
        if hasattr(d, "strftime"):
            return d.strftime("%B %d, %Y")
        from datetime import datetime
        return datetime.strptime(str(d), "%Y-%m-%d").strftime("%B %d, %Y")
    except Exception:
        return str(d) if d else "—"


class NumberBadge(QLabel):
    def __init__(self, number: int, parent=None):
        super().__init__(parent)
        self._text = str(number)
        self.setFixedSize(54, 54)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QBrush(QColor(21, 23, 61)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(0, 0, 54, 54)
        p.setPen(QPen(QColor(255, 255, 255)))
        f = QFont("Segoe UI", 16)
        f.setBold(True)
        p.setFont(f)
        p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._text)


class PregnancyCard(QWidget):
    STATUS_STYLES = {
        "Active":    "background-color: rgb(220,240,220); color: rgb(30,100,30);",
        "Delivered": "background-color: rgb(220,230,255); color: rgb(21,23,100);",
        "Lost":      "background-color: rgb(255,220,220); color: rgb(150,30,30);",
    }

    def __init__(self, pregnancy: dict, visit_count: int, on_open, on_edit, parent=None):
            super().__init__(parent)
            self.pregnancy = pregnancy
            self.visit_count = visit_count
            self.on_open = on_open
            self.on_edit = on_edit   # ← new
            self._build()
                
    def _build(self):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(4, 0, 4, 0)
        outer.setSpacing(14)

        badge = NumberBadge(self.pregnancy.get("pregnancy_num", "?"))
        outer.addWidget(badge, alignment=Qt.AlignmentFlag.AlignVCenter)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgb(236, 198, 220);
                border-radius: 12px;
                border: 1px solid rgb(210, 177, 200);
            }
        """)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(18, 12, 18, 12)
        lay.setSpacing(6)

        top = QHBoxLayout()
        num = self.pregnancy.get("pregnancy_num", "?")
        title = QLabel(f"{ordinal(num)} Pregnancy")
        title.setStyleSheet("color: rgb(21,23,61); font-size: 14px; font-weight: bold; border: none;")

        btn_edit = QPushButton("Edit")
        btn_edit.setFixedHeight(30)
        btn_edit.setStyleSheet("""
            QPushButton {
                background-color: rgb(192,116,182); color: white;
                border: none; border-radius: 6px;
                font-size: 11px; font-weight: bold; padding: 0 12px;
            }
            QPushButton:hover { background-color: rgb(160,80,150); }
        """)
        btn_edit.clicked.connect(lambda: self.on_edit(self.pregnancy))

        btn = QPushButton("View Prenatal Care →")
        btn.setFixedHeight(30)
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(21,23,61); color: white;
                border: none; border-radius: 6px;
                font-size: 11px; font-weight: bold; padding: 0 12px;
            }
            QPushButton:hover { background-color: rgb(192,116,182); }
        """)
        btn.clicked.connect(lambda: self.on_open(self.pregnancy))
        top.addWidget(title)
        top.addStretch()
        top.addWidget(btn_edit)   # ← new
        top.addWidget(btn)
        lay.addLayout(top)

        # ── ADD THESE MISSING LINES ──
        info = QHBoxLayout(); info.setSpacing(24)

        def stat(label, value):
            lbl = QLabel(f"<b>{label}</b> {value}")
            lbl.setTextFormat(Qt.TextFormat.RichText)
            lbl.setStyleSheet("color: rgb(21,23,61); font-size: 11px; border: none;")
            return lbl

        edd = self.pregnancy.get("edd")
        info.addWidget(stat("EDD:", fmt_date(edd) if edd else "Not set"))
        start = self.pregnancy.get("start_date")
        if start:
            info.addWidget(stat("Started:", fmt_date(start)))
        info.addWidget(stat("Prenatal Visits:", str(self.visit_count)))

        status = self.pregnancy.get("status", "Active")
        chip = QLabel(f"  {status}  ")
        chip.setStyleSheet(
            self.STATUS_STYLES.get(status, "background-color: rgb(240,230,240);") +
            " border-radius: 10px; padding: 2px 8px; font-size: 11px; font-weight: bold; border: none;"
        )
        info.addWidget(chip)
        info.addStretch()
        lay.addLayout(info)

        outer.addWidget(card, stretch=1)


class NewPregnancyDialog(QDialog):
    STATUSES = ["Ongoing", "Completed"]

    def __init__(self, patient_id: int, next_num: int, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.next_num = next_num
        self._staff_list = []   # will hold (staff_id, display_name) tuples
        self.setWindowTitle(f"Add Pregnancy #{next_num}")
        self.setMinimumWidth(380)
        self.setStyleSheet("QDialog { background-color: rgb(240,230,240); }")
        self._load_staff()
        self._build()

    def _load_staff(self):
        from database import get_connection
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT staff_id,
                    CONCAT(first_name, ' ', last_name, ' (', role, ')')
                FROM staff
                WHERE status = 'Active'
                ORDER BY last_name, first_name
            """)
            self._staff_list = cur.fetchall()
            conn.close()
        except Exception as e:
            print(f"load staff error: {e}")
            if conn:
                conn.close()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(22, 22, 22, 22)
        lay.setSpacing(14)

        title = QLabel(f"Add {ordinal(self.next_num)} Pregnancy")
        title.setStyleSheet(
            "color: rgb(21,23,61); font-size: 15px; font-weight: bold; font-family: 'Arial Black';"
        )
        lay.addWidget(title)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: rgb(210,180,210); max-height: 1px;")
        lay.addWidget(sep)

        fs = "border: 1px solid rgb(158,136,163); border-radius: 6px; padding: 5px 8px; background-color: rgb(247,247,247); color: rgb(21,23,61); font-size: 12px;"
        cs = "QComboBox { background-color: rgb(247,247,247); border: 1px solid rgb(158,136,163); border-radius: 6px; padding: 5px 8px; color: rgb(21,23,61); font-size: 12px; }"
        ls = "color: rgb(21,23,61); font-size: 12px;"
        form = QFormLayout(); form.setSpacing(10)

        self.f_start = QDateEdit(); self.f_start.setCalendarPopup(True)
        self.f_start.setDate(QDate.currentDate()); self.f_start.setStyleSheet(fs)

        self.f_edd = QDateEdit(); self.f_edd.setCalendarPopup(True)
        self.f_edd.setDate(QDate.currentDate().addDays(280)); self.f_edd.setStyleSheet(fs)

        self.f_status = QComboBox(); self.f_status.addItems(self.STATUSES)
        self.f_status.setStyleSheet(cs)

        # ── staff dropdown ──────────────────────────────────────────────
        self.f_staff = QComboBox()
        self.f_staff.setStyleSheet(cs)
        if self._staff_list:
            for sid, name in self._staff_list:
                self.f_staff.addItem(name, userData=sid)
        else:
            self.f_staff.addItem("No staff found", userData=None)
        # ────────────────────────────────────────────────────────────────

        for text, widget in [
            ("Start Date",      self.f_start),
            ("EDD (Due Date)",  self.f_edd),
            ("Attended By *",   self.f_staff),   # ← new row
            ("Status",          self.f_status),
        ]:
            lbl = QLabel(text); lbl.setStyleSheet(ls)
            form.addRow(lbl, widget)
        lay.addLayout(form)

        btns = QHBoxLayout(); btns.addStretch()
        btn_c = QPushButton("Cancel")
        btn_c.setStyleSheet("QPushButton { background-color: rgb(240,230,240); color: rgb(21,23,61); border: 1px solid rgb(158,136,163); border-radius: 8px; padding: 7px 18px; font-size: 12px; }")
        btn_c.clicked.connect(self.reject)
        btn_s = QPushButton("Save")
        btn_s.setStyleSheet("QPushButton { background-color: rgb(21,23,61); color: white; border: none; border-radius: 8px; padding: 7px 18px; font-size: 12px; font-weight: bold; } QPushButton:hover { background-color: rgb(192,116,182); }")
        btn_s.clicked.connect(self._on_save)
        btns.addWidget(btn_c); btns.addWidget(btn_s)
        lay.addLayout(btns)

    def _on_save(self):
        staff_id = self.f_staff.currentData()
        if staff_id is None:
            QMessageBox.warning(self, "Missing", "Please select a staff member.")
            return

        self.result_data = {
            "patient_id":    self.patient_id,
            "pregnancy_num": self.next_num,
            "start_date":    self.f_start.date().toString("yyyy-MM-dd"),
            "edd":           self.f_edd.date().toString("yyyy-MM-dd"),
            "status":        self.f_status.currentText(),
            "staff_id":      staff_id,   # ← added
        }
        self.accept()

class EditPregnancyDialog(QDialog):
    STATUSES = ["Ongoing", "Completed"]

    def __init__(self, pregnancy: dict, parent=None):
        super().__init__(parent)
        self.pregnancy = pregnancy
        self._staff_list = []
        self.setWindowTitle(f"Edit {ordinal(pregnancy.get('pregnancy_num', '?'))} Pregnancy")
        self.setMinimumWidth(380)
        self.setStyleSheet("QDialog { background-color: rgb(240,230,240); }")
        self._load_staff()
        self._build()

    def _load_staff(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT staff_id,
                    CONCAT(first_name, ' ', last_name, ' (', role, ')')
                FROM staff
                WHERE status = 'Active'
                ORDER BY last_name, first_name
            """)
            self._staff_list = cur.fetchall()
            conn.close()
        except Exception as e:
            print(f"load staff error: {e}")
            if conn:
                conn.close()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(22, 22, 22, 22)
        lay.setSpacing(14)

        num = self.pregnancy.get("pregnancy_num", "?")
        title = QLabel(f"Edit {ordinal(num)} Pregnancy")
        title.setStyleSheet(
            "color: rgb(21,23,61); font-size: 15px; font-weight: bold; font-family: 'Arial Black';"
        )
        lay.addWidget(title)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: rgb(210,180,210); max-height: 1px;")
        lay.addWidget(sep)

        fs = ("border: 1px solid rgb(158,136,163); border-radius: 6px; padding: 5px 8px;"
              "background-color: rgb(247,247,247); color: rgb(21,23,61); font-size: 12px;")
        cs = ("QComboBox { background-color: rgb(247,247,247); border: 1px solid rgb(158,136,163);"
              "border-radius: 6px; padding: 5px 8px; color: rgb(21,23,61); font-size: 12px; }"
              "QComboBox QAbstractItemView { background-color: rgb(247,247,247); color: rgb(21,23,61);"
              "selection-background-color: rgb(192,116,182); }")
        ls = "color: rgb(21,23,61); font-size: 12px;"
        form = QFormLayout()
        form.setSpacing(10)

        # Start date
        self.f_start = QDateEdit()
        self.f_start.setCalendarPopup(True)
        self.f_start.setStyleSheet(fs)
        start = self.pregnancy.get("start_date")
        if start:
            self.f_start.setDate(QDate.fromString(str(start), "yyyy-MM-dd"))
        else:
            self.f_start.setDate(QDate.currentDate())

        # EDD
        self.f_edd = QDateEdit()
        self.f_edd.setCalendarPopup(True)
        self.f_edd.setStyleSheet(fs)
        edd = self.pregnancy.get("edd")
        if edd:
            self.f_edd.setDate(QDate.fromString(str(edd), "yyyy-MM-dd"))
        else:
            self.f_edd.setDate(QDate.currentDate().addDays(280))

        # Staff dropdown
        self.f_staff = QComboBox()
        self.f_staff.setStyleSheet(cs)
        for sid, name in self._staff_list:
            self.f_staff.addItem(name, userData=sid)
        # Pre-select current staff
        current_staff_id = self.pregnancy.get("staff_id")
        if current_staff_id:
            for i in range(self.f_staff.count()):
                if self.f_staff.itemData(i) == current_staff_id:
                    self.f_staff.setCurrentIndex(i)
                    break

        # Status
        self.f_status = QComboBox()
        self.f_status.addItems(self.STATUSES)
        self.f_status.setStyleSheet(cs)
        current_status = self.pregnancy.get("status", "Ongoing")
        idx = self.f_status.findText(current_status)
        if idx >= 0:
            self.f_status.setCurrentIndex(idx)

        for text, widget in [
            ("Start Date",     self.f_start),
            ("EDD (Due Date)", self.f_edd),
            ("Attended By *",  self.f_staff),
            ("Status",         self.f_status),
        ]:
            lbl = QLabel(text)
            lbl.setStyleSheet(ls)
            form.addRow(lbl, widget)
        lay.addLayout(form)

        btns = QHBoxLayout()
        btns.addStretch()
        btn_c = QPushButton("Cancel")
        btn_c.setStyleSheet(
            "QPushButton { background-color: rgb(240,230,240); color: rgb(21,23,61);"
            "border: 1px solid rgb(158,136,163); border-radius: 8px; padding: 7px 18px; font-size: 12px; }"
        )
        btn_c.clicked.connect(self.reject)
        btn_s = QPushButton("Save")
        btn_s.setStyleSheet(
            "QPushButton { background-color: rgb(21,23,61); color: white; border: none;"
            "border-radius: 8px; padding: 7px 18px; font-size: 12px; font-weight: bold; }"
            "QPushButton:hover { background-color: rgb(192,116,182); }"
        )
        btn_s.clicked.connect(self._on_save)
        btns.addWidget(btn_c)
        btns.addWidget(btn_s)
        lay.addLayout(btns)

    def _on_save(self):
        staff_id = self.f_staff.currentData()
        if staff_id is None:
            QMessageBox.warning(self, "Missing", "Please select a staff member.")
            return
        self.result_data = {
            "pregnancy_id": self.pregnancy["pregnancy_id"],
            "start_date":   self.f_start.date().toString("yyyy-MM-dd"),
            "edd":          self.f_edd.date().toString("yyyy-MM-dd"),
            "staff_id":     staff_id,
            "status":       self.f_status.currentText(),
        }
        self.accept()

class PrenatalDashboardScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PrenatalDashboardScreen()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB - Prenatal Care")
        self._initialized = False
        self._current_patient_id = None

        # sidebar
        self.ui.pushButton.clicked.connect(self.go_to_dashboard)
        self.ui.pushButton_2.clicked.connect(self.go_to_patient_records)
        self.ui.pushButton_3.clicked.connect(self.go_to_prenatal_care)
        self.ui.pushButton_4.clicked.connect(self.go_to_appointments)
        self.ui.pushButton_5.clicked.connect(self.logout)

        self.ui.patient_combo.currentIndexChanged.connect(self.on_patient_selected)
        self.ui.btn_add_pregnancy.clicked.connect(self.on_add_pregnancy)

        self._build_sidebar_profile()

    # ── sidebar profile ───────────────────────────────────────────────────────
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
        self.profile_role_lbl.setStyleSheet(
            "color: rgba(255,255,255,0.65); font-size: 11px; background: transparent; border: none;"
        )
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
            self.load_patients()

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
        self.ui.title_label.setGeometry(40, 20, 500, 61)
        self.ui.patient_selector_label.setGeometry(40, 92, 110, 28)
        self.ui.patient_combo.setGeometry(155, 89, min(320, cw - 200), 28)
        self.ui.pregnancies_label.setGeometry(40, 132, 300, 24)
        self.ui.btn_add_pregnancy.setGeometry(cw - 120, 128, 160, 32)
        self.ui.sep_line.setGeometry(40, 162, cw, 1)
        self.ui.scroll_area.setGeometry(40, 170, cw, max(mh - 200, 200))
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

    # ── patients (only maternal patients that exist in patient_profile) ───────

    def _edit_pregnancy(self, pregnancy: dict):
        # Fetch full pregnancy row so we have staff_id
        conn = get_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT staff_id FROM pregnancy WHERE pregnancy_id = %s",
                    (pregnancy["pregnancy_id"],)
                )
                row = cur.fetchone()
                if row:
                    pregnancy = {**pregnancy, "staff_id": row[0]}
                conn.close()
            except Exception as e:
                print(f"fetch staff_id error: {e}")
                if conn: conn.close()

        dlg = EditPregnancyDialog(pregnancy, parent=self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE pregnancy SET
                    start_date = %(start_date)s,
                    edd        = %(edd)s,
                    staff_id   = %(staff_id)s,
                    status     = %(status)s
                WHERE pregnancy_id = %(pregnancy_id)s
            """, dlg.result_data)
            conn.commit()
            conn.close()
            self.load_pregnancies(self._current_patient_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            if conn:
                conn.close()

    def load_patients(self):
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT patient_id,
                       CONCAT(last_name, ', ', first_name,
                              CASE WHEN middle_name IS NOT NULL AND middle_name <> ''
                                   THEN ' ' || middle_name ELSE '' END)
                FROM patient_profile
                ORDER BY last_name, first_name
            """)
            patients = cur.fetchall()
            conn.close()

            self.ui.patient_combo.blockSignals(True)
            self.ui.patient_combo.clear()
            self.ui.patient_combo.addItem("— Select a patient —", userData=None)
            for pid, name in patients:
                self.ui.patient_combo.addItem(name, userData=pid)
            self.ui.patient_combo.blockSignals(False)
        except Exception as e:
            print(f"load patients error: {e}")
            if conn: conn.close()

    def on_patient_selected(self, index):
        pid = self.ui.patient_combo.currentData()
        self._current_patient_id = pid
        self._clear_cards()
        if pid is not None:
            self.load_pregnancies(pid)

    # ── pregnancies — split into ongoing and completed ────────────────────────
    def load_pregnancies(self, patient_id: int):
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT pregnancy_id, patient_id, pregnancy_num, edd, start_date, status
                FROM pregnancy
                WHERE patient_id = %s
                ORDER BY pregnancy_num DESC
            """, (patient_id,))
            rows = cur.fetchall()

            cur.execute("""
                SELECT pregnancy_id, COUNT(*) FROM prenatal_visit
                WHERE pregnancy_id IN (SELECT pregnancy_id FROM pregnancy WHERE patient_id=%s)
                GROUP BY pregnancy_id
            """, (patient_id,))
            counts = {r[0]: r[1] for r in cur.fetchall()}
            conn.close()
        except Exception as e:
            print(f"load pregnancies error: {e}")
            if conn: conn.close()
            rows, counts = [], {}

        self._clear_cards()
        lay = self.ui.scroll_layout
        cols = ["pregnancy_id","patient_id","pregnancy_num","edd","start_date","status"]

        if not rows:
            empty = QLabel("No pregnancies recorded for this patient.\nUse '+ New Pregnancy' to add one.")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet("color: rgb(100,80,110); font-size: 13px; padding: 40px;")
            lay.insertWidget(lay.count() - 1, empty)
            return

        pregnancies = [dict(zip(cols, r)) for r in rows]
        ongoing   = [p for p in pregnancies if p["status"] == "Active"]
        completed = [p for p in pregnancies if p["status"] != "Active"]

        if ongoing:
            hdr = self._section_label("Ongoing")
            lay.insertWidget(lay.count() - 1, hdr)
            for p in ongoing:
                card = PregnancyCard(p, counts.get(p["pregnancy_id"], 0), on_open=self._open_prenatal_care, on_edit=self._edit_pregnancy)
                lay.insertWidget(lay.count() - 1, card)

        if completed:
            hdr2 = self._section_label("Completed / Past")
            lay.insertWidget(lay.count() - 1, hdr2)
            for p in completed:
                card = PregnancyCard(p, counts.get(p["pregnancy_id"], 0), on_open=self._open_prenatal_care, on_edit=self._edit_pregnancy)
                lay.insertWidget(lay.count() - 1, card)

    def _section_label(self, text) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "color: rgb(21,23,61); font-size: 13px; font-weight: bold;"
            "padding: 8px 4px 4px 4px;"
        )
        return lbl

    def _clear_cards(self):
        lay = self.ui.scroll_layout
        while lay.count() > 1:
            item = lay.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def _open_prenatal_care(self, pregnancy: dict):
        from screens.prenatal_care_screen import PrenatalCareScreen
        self.prenatal_window = PrenatalCareScreen(
            pregnancy_id=pregnancy["pregnancy_id"],
            pregnancy_num=pregnancy["pregnancy_num"],
            patient_id=pregnancy["patient_id"]
        )
        self.prenatal_window.showMaximized()
        self.close()

    # ── add pregnancy ─────────────────────────────────────────────────────────
    def on_add_pregnancy(self):
        if self._current_patient_id is None:
            QMessageBox.warning(self, "No Patient", "Please select a patient first.")
            return

        # ── 1. get the next pregnancy number ─────────────────────────────────
        conn = get_connection()
        next_num = 1
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT COALESCE(MAX(pregnancy_num), 0) + 1 FROM pregnancy WHERE patient_id = %s",
                    (self._current_patient_id,)
                )
                res = cur.fetchone()
                next_num = res[0] if res else 1
                conn.close()
            except Exception as e:
                print(f"next num error: {e}")
                if conn:
                    conn.close()

        # ── 2. show dialog ────────────────────────────────────────────────────
        dlg = NewPregnancyDialog(self._current_patient_id, next_num, parent=self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return

        # ── 3. save with staff_id ─────────────────────────────────────────────
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO pregnancy
                    (patient_id, pregnancy_num, start_date, edd, status, staff_id)
                VALUES
                    (%(patient_id)s, %(pregnancy_num)s, %(start_date)s,
                    %(edd)s, %(status)s, %(staff_id)s)
            """, dlg.result_data)
            conn.commit()
            conn.close()
            self.load_pregnancies(self._current_patient_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            if conn:
                conn.close()

    # ── navigation ────────────────────────────────────────────────────────────
    def go_to_dashboard(self):
        from screens.dashboard_screen import DashboardScreen
        self.w = DashboardScreen(); self.w.showMaximized(); self.close()

    def go_to_patient_records(self):
        from screens.patient_records_screen import PatientRecordScreen
        self.w = PatientRecordScreen(); self.w.showMaximized(); self.close()

    def go_to_prenatal_care(self):
        pass  # already here

    def go_to_appointments(self):
        from screens.appointments_screen import AppointmentsScreen
        self.w = AppointmentsScreen(); self.w.showMaximized(); self.close()

    def logout(self):
        session.clear()
        from screens.login_screen import LoginScreen
        self.w = LoginScreen(); self.w.showMaximized(); self.close()
