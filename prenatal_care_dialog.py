"""
PregnancyDialog
===============
Opens when a user clicks "Open →" on an existing pregnancy OR after picking a
patient in the SelectPatientDialog.

Modes
-----
• pregnancy_id=None  → Create mode (new pregnancy for patient_id)
• pregnancy_id=<int> → View/Edit mode (existing pregnancy)

Layout (tabs)
-------------
1. Overview   – pregnancy-level fields (LMP, EDD, status, gravida, para)
2. Visits     – list of prenatal visits + Add Visit button
3. Delivery   – delivery_record fields (if status is Completed / birth happened)
"""

from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QLineEdit, QTextEdit,
    QComboBox, QDateEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QHBoxLayout, QVBoxLayout,
    QFormLayout, QFrame, QWidget, QTabWidget, QSpinBox,
    QMessageBox, QDoubleSpinBox, QScrollArea
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QCursor, QFont, QColor
from database import get_connection
import user_profile.session as session

# ── Colours ──────────────────────────────────────────────────────────────────
CLR_ACCENT    = "#C2607A"
CLR_ONGOING   = "#2E7D6E"
CLR_COMPLETED = "#5C6BC0"
CLR_BORDER    = "#E8DDE6"
CLR_TEXT      = "#2D1B2E"
CLR_MUTED     = "#7A6878"
CLR_BG        = "#F8F4F6"

BASE_STYLE = f"""
    QDialog    {{ background: {CLR_BG}; }}
    QTabWidget::pane {{
        background: white;
        border: 1px solid {CLR_BORDER};
        border-radius: 10px;
    }}
    QTabBar::tab {{
        background: #EDE4EC;
        color: {CLR_MUTED};
        padding: 8px 20px;
        border-radius: 6px 6px 0 0;
        font-size: 13px;
        margin-right: 3px;
    }}
    QTabBar::tab:selected {{
        background: white;
        color: {CLR_TEXT};
        font-weight: bold;
        border-bottom: 2px solid {CLR_ACCENT};
    }}
"""

FIELD_STYLE = f"""
    QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QComboBox {{
        background: white;
        border: 1.5px solid {CLR_BORDER};
        border-radius: 7px;
        padding: 6px 10px;
        font-size: 13px;
        color: {CLR_TEXT};
        min-height: 32px;
    }}
    QLineEdit:focus, QTextEdit:focus, QSpinBox:focus,
    QDoubleSpinBox:focus, QDateEdit:focus, QComboBox:focus {{
        border-color: {CLR_ACCENT};
    }}
    QLabel {{
        font-size: 13px;
        color: {CLR_MUTED};
        background: transparent;
    }}
"""

TABLE_STYLE = """
    QTableWidget {
        background: white;
        border: 1px solid #E8DDE6;
        border-radius: 10px;
        gridline-color: transparent;
        font-size: 13px;
        color: #2D1B2E;
    }
    QTableWidget::item {
        padding: 6px 10px;
        border-bottom: 1px solid #F0E8EE;
    }
    QTableWidget::item:selected {
        background: #F3E8F0;
        color: #2D1B2E;
    }
    QHeaderView::section {
        background: #F8F4F6;
        color: #7A6878;
        font-size: 11px;
        font-weight: bold;
        padding: 8px 10px;
        border: none;
        border-bottom: 2px solid #E8DDE6;
    }
"""

def _primary_btn(text, parent=None):
    b = QPushButton(text, parent)
    b.setFixedHeight(38)
    b.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    b.setStyleSheet(f"""
        QPushButton {{
            background: {CLR_ACCENT};
            color: white; border: none;
            border-radius: 8px;
            font-size: 13px; font-weight: bold;
            padding: 0 18px;
        }}
        QPushButton:hover {{ background: #A84F68; }}
        QPushButton:pressed {{ background: #8E3F55; }}
    """)
    return b

def _ghost_btn(text, parent=None):
    b = QPushButton(text, parent)
    b.setFixedHeight(38)
    b.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    b.setStyleSheet(f"""
        QPushButton {{
            background: white;
            color: {CLR_MUTED};
            border: 1.5px solid {CLR_BORDER};
            border-radius: 8px;
            font-size: 13px;
            padding: 0 18px;
        }}
        QPushButton:hover {{ background: #F8F4F6; }}
    """)
    return b

def _section_label(text):
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"font-size: 12px; font-weight: bold; color: {CLR_MUTED};"
        "text-transform: uppercase; letter-spacing: 0.5px;"
        "background: transparent; padding: 0;"
    )
    return lbl


# ─────────────────────────────────────────────────────────────────────────────
class PregnancyDialog(QDialog):
    def __init__(self, patient_id, pregnancy_id=None, parent=None):
        super().__init__(parent)
        self.patient_id   = patient_id
        self.pregnancy_id = pregnancy_id
        self.is_new       = pregnancy_id is None
        self._staff_id    = self._current_staff_id()

        self.setWindowTitle(
            "New Pregnancy Record" if self.is_new else "Pregnancy Record"
        )
        self.setMinimumSize(820, 640)
        self.setStyleSheet(BASE_STYLE + FIELD_STYLE)
        self._build_ui()

        if not self.is_new:
            self._load_pregnancy()
            self._load_visits()

    # ── Helpers ──────────────────────────────────────────────────────────────
    def _current_staff_id(self):
        user = session.get()
        if not user:
            return None
        conn = get_connection()
        if not conn:
            return None
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT staff_id FROM users WHERE user_id = %s",
                (user.get("id"),)
            )
            row = cur.fetchone()
            return row[0] if row else None
        except Exception:
            return None
        finally:
            conn.close()

    def _patient_name(self):
        conn = get_connection()
        if not conn:
            return ""
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT last_name || ', ' || first_name FROM patient_profile"
                " WHERE patient_id = %s",
                (self.patient_id,)
            )
            row = cur.fetchone()
            return row[0] if row else ""
        except Exception:
            return ""
        finally:
            conn.close()

    # ── UI ───────────────────────────────────────────────────────────────────
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 16)
        root.setSpacing(12)

        # Header
        hdr = QHBoxLayout()
        name = self._patient_name()
        title_lbl = QLabel(
            f"{'New Pregnancy' if self.is_new else 'Pregnancy #' + str(self.pregnancy_id)}"
            f"  –  {name}"
        )
        title_lbl.setStyleSheet(
            f"font-size: 17px; font-weight: bold; color: {CLR_TEXT};"
            "background: transparent;"
        )
        hdr.addWidget(title_lbl)
        hdr.addStretch()
        root.addLayout(hdr)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_overview_tab(), "📋  Overview")
        self.tabs.addTab(self._build_visits_tab(),   "🩺  Prenatal Visits")
        self.tabs.addTab(self._build_delivery_tab(), "👶  Delivery")
        root.addWidget(self.tabs)

        # Footer buttons
        foot = QHBoxLayout()
        foot.setSpacing(10)
        foot.addStretch()

        cancel = _ghost_btn("Close")
        cancel.clicked.connect(self.reject)
        foot.addWidget(cancel)

        self.save_btn = _primary_btn(
            "Create Pregnancy" if self.is_new else "Save Changes"
        )
        self.save_btn.clicked.connect(self._save_pregnancy)
        foot.addWidget(self.save_btn)

        root.addLayout(foot)

    # ── Tab 1: Overview ───────────────────────────────────────────────────────
    def _build_overview_tab(self):
        w = QWidget()
        scroll = QScrollArea()
        scroll.setWidget(w)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(16)

        # ── Pregnancy info ────────────────────────────────────────────────
        lay.addWidget(_section_label("Pregnancy Information"))

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setSpacing(10)
        form.setContentsMargins(0, 0, 0, 0)

        self.lmp_edit = QDateEdit()
        self.lmp_edit.setCalendarPopup(True)
        self.lmp_edit.setDate(QDate.currentDate())
        self.lmp_edit.dateChanged.connect(self._auto_edd)

        self.edd_edit = QDateEdit()
        self.edd_edit.setCalendarPopup(True)
        self.edd_edit.setDate(QDate.currentDate().addDays(280))

        self.gravida_spin = QSpinBox()
        self.gravida_spin.setRange(1, 20)
        self.gravida_spin.setValue(1)

        self.para_spin = QSpinBox()
        self.para_spin.setRange(0, 20)
        self.para_spin.setValue(0)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Ongoing", "Completed"])

        self.remarks_edit = QTextEdit()
        self.remarks_edit.setFixedHeight(70)
        self.remarks_edit.setPlaceholderText("Optional remarks…")

        form.addRow("Last Menstrual Period *", self.lmp_edit)
        form.addRow("Expected Delivery Date", self.edd_edit)
        form.addRow("Gravida *", self.gravida_spin)
        form.addRow("Para", self.para_spin)
        form.addRow("Status *", self.status_combo)
        form.addRow("Remarks", self.remarks_edit)
        lay.addLayout(form)

        lay.addStretch()

        container = QWidget()
        vl = QVBoxLayout(container)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.addWidget(scroll)
        return container

    def _auto_edd(self, lmp_date):
        """Auto-compute EDD = LMP + 280 days (Naegele's rule)."""
        self.edd_edit.setDate(lmp_date.addDays(280))

    # ── Tab 2: Visits ─────────────────────────────────────────────────────────
    def _build_visits_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(10)

        # toolbar
        tb = QHBoxLayout()
        tb.addWidget(
            QLabel("Prenatal checkup visits for this pregnancy")
        )
        tb.addStretch()

        self.add_visit_btn = _primary_btn("＋  Add Visit")
        self.add_visit_btn.setEnabled(not self.is_new)
        self.add_visit_btn.clicked.connect(self._open_add_visit)
        tb.addWidget(self.add_visit_btn)
        lay.addLayout(tb)

        if self.is_new:
            hint = QLabel(
                "ℹ  Save the pregnancy record first to add visits."
            )
            hint.setStyleSheet(
                f"color: {CLR_MUTED}; font-size: 12px; background: transparent;"
            )
            lay.addWidget(hint)

        # visits table
        cols = ["Visit #", "Date", "Gest. Age (wks)",
                "Weight (kg)", "BP", "FHR", "Actions"]
        self.visits_table = QTableWidget(0, len(cols))
        self.visits_table.setHorizontalHeaderLabels(cols)
        self.visits_table.setStyleSheet(TABLE_STYLE)
        self.visits_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self.visits_table.setEditTriggers(
            QAbstractItemView.EditTriggerFlag.NoEditTriggers)
        self.visits_table.setShowGrid(False)
        self.visits_table.verticalHeader().setVisible(False)
        self.visits_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        hdr = self.visits_table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)

        lay.addWidget(self.visits_table)
        return w

    # ── Tab 3: Delivery ───────────────────────────────────────────────────────
    def _build_delivery_tab(self):
        w = QWidget()
        scroll = QScrollArea()
        scroll.setWidget(w)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(16)

        lay.addWidget(_section_label("Delivery Record"))

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setSpacing(10)

        self.del_date = QDateEdit()
        self.del_date.setCalendarPopup(True)
        self.del_date.setDate(QDate.currentDate())

        self.del_time = QLineEdit()
        self.del_time.setPlaceholderText("e.g. 14:30")

        self.del_outcome = QComboBox()
        self.del_outcome.addItems(["Completed", "Referred"])

        self.del_type = QComboBox()
        self.del_type.addItems(["", "Normal", "CS"])

        self.del_location = QLineEdit()
        self.del_location.setPlaceholderText("Facility or home")

        self.birth_outcome = QComboBox()
        self.birth_outcome.addItems(["", "Live Birth", "Stillbirth"])

        self.referred_to = QLineEdit()
        self.referred_to.setPlaceholderText("If referred, where?")

        self.referral_reason = QTextEdit()
        self.referral_reason.setFixedHeight(60)
        self.referral_reason.setPlaceholderText("Reason for referral…")

        self.del_remarks = QTextEdit()
        self.del_remarks.setFixedHeight(60)
        self.del_remarks.setPlaceholderText("Remarks…")

        form.addRow("Delivery Date *",   self.del_date)
        form.addRow("Delivery Time *",   self.del_time)
        form.addRow("Outcome *",         self.del_outcome)
        form.addRow("Type",              self.del_type)
        form.addRow("Location *",        self.del_location)
        form.addRow("Birth Outcome",     self.birth_outcome)
        form.addRow("Referred To",       self.referred_to)
        form.addRow("Reason for Referral", self.referral_reason)
        form.addRow("Remarks",           self.del_remarks)
        lay.addLayout(form)

        # Save delivery button
        save_del_btn = _primary_btn("💾  Save Delivery Record")
        save_del_btn.clicked.connect(self._save_delivery)
        save_del_btn.setEnabled(not self.is_new)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(save_del_btn)
        lay.addLayout(btn_row)
        lay.addStretch()

        container = QWidget()
        vl = QVBoxLayout(container)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.addWidget(scroll)
        return container

    # ── Data load ─────────────────────────────────────────────────────────────
    def _load_pregnancy(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT lmp, edd, gravida, para, status, remarks
                FROM pregnancy WHERE pregnancy_id = %s
            """, (self.pregnancy_id,))
            row = cur.fetchone()
            if not row:
                return
            lmp, edd, gravida, para, status, remarks = row

            if lmp:
                self.lmp_edit.setDate(
                    QDate(lmp.year, lmp.month, lmp.day))
            if edd:
                self.edd_edit.setDate(
                    QDate(edd.year, edd.month, edd.day))
            if gravida:
                self.gravida_spin.setValue(gravida)
            if para is not None:
                self.para_spin.setValue(para)
            idx = self.status_combo.findText(status or "Ongoing")
            if idx >= 0:
                self.status_combo.setCurrentIndex(idx)
            if remarks:
                self.remarks_edit.setPlainText(remarks)

            # Also load delivery record if exists
            cur.execute("""
                SELECT delivery_date, delivery_time, delivery_outcome,
                       delivery_type, delivery_location, birth_outcome,
                       referred_to, reason_for_referral, remarks
                FROM delivery_record WHERE pregnancy_id = %s
                LIMIT 1
            """, (self.pregnancy_id,))
            dr = cur.fetchone()
            if dr:
                (dd, dt, do, dtype, dloc,
                 bo, rto, rfr, drr) = dr
                if dd:
                    self.del_date.setDate(QDate(dd.year, dd.month, dd.day))
                if dt:
                    self.del_time.setText(str(dt)[:5])
                i = self.del_outcome.findText(do or "")
                if i >= 0: self.del_outcome.setCurrentIndex(i)
                i = self.del_type.findText(dtype or "")
                if i >= 0: self.del_type.setCurrentIndex(i)
                if dloc: self.del_location.setText(dloc)
                i = self.birth_outcome.findText(bo or "")
                if i >= 0: self.birth_outcome.setCurrentIndex(i)
                if rto:  self.referred_to.setText(rto)
                if rfr:  self.referral_reason.setPlainText(rfr)
                if drr:  self.del_remarks.setPlainText(drr)

            cur.close()
        except Exception as e:
            print("Load pregnancy error:", e)
        finally:
            conn.close()

    def _load_visits(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT visit_id, visit_date, gestational_age_weeks,
                       weight_kg, blood_pressure, fetal_heart_rate
                FROM prenatal_visit
                WHERE pregnancy_id = %s
                ORDER BY visit_date
            """, (self.pregnancy_id,))
            rows = cur.fetchall()
            cur.close()

            self.visits_table.setRowCount(0)
            for idx, (vid, vdate, ga, wt, bp, fhr) in enumerate(rows, 1):
                r = self.visits_table.rowCount()
                self.visits_table.insertRow(r)
                self.visits_table.setRowHeight(r, 44)

                def _it(val, center=True):
                    it = QTableWidgetItem(str(val) if val is not None else "—")
                    if center:
                        it.setTextAlignment(
                            Qt.AlignmentFlag.AlignCenter |
                            Qt.AlignmentFlag.AlignVCenter
                        )
                    it.setData(Qt.ItemDataRole.UserRole, vid)
                    return it

                self.visits_table.setItem(r, 0, _it(idx))
                self.visits_table.setItem(r, 1, _it(str(vdate) if vdate else "—"))
                self.visits_table.setItem(r, 2, _it(ga))
                self.visits_table.setItem(r, 3, _it(f"{wt:.2f}" if wt else "—"))
                self.visits_table.setItem(r, 4, _it(bp or "—"))
                self.visits_table.setItem(r, 5, _it(fhr))

                # View/Edit button
                open_btn = QPushButton("View →")
                open_btn.setStyleSheet(f"""
                    QPushButton {{
                        background: #F3E8F0; color: {CLR_ACCENT};
                        border: none; border-radius: 6px;
                        font-size: 12px; font-weight: bold;
                        padding: 4px 14px;
                    }}
                    QPushButton:hover {{ background: #E8D5E8; }}
                """)
                open_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                open_btn.clicked.connect(
                    lambda _, v=vid: self._open_visit(v)
                )
                cell = QWidget()
                cell.setStyleSheet("background: transparent;")
                hl = QHBoxLayout(cell)
                hl.setContentsMargins(8, 4, 8, 4)
                hl.addWidget(open_btn)
                hl.addStretch()
                self.visits_table.setCellWidget(r, 6, cell)

        except Exception as e:
            print("Load visits error:", e)
        finally:
            conn.close()

    # ── Save pregnancy ────────────────────────────────────────────────────────
    def _save_pregnancy(self):
        lmp     = self.lmp_edit.date().toPyDate()
        edd     = self.edd_edit.date().toPyDate()
        gravida = self.gravida_spin.value()
        para    = self.para_spin.value()
        status  = self.status_combo.currentText()
        remarks = self.remarks_edit.toPlainText().strip() or None

        if not self._staff_id:
            QMessageBox.warning(self, "Error",
                "Could not determine current staff. Please log in again.")
            return

        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            if self.is_new:
                cur.execute("""
                    INSERT INTO pregnancy
                        (patient_id, staff_id, lmp, edd,
                         gravida, para, status, remarks)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING pregnancy_id
                """, (self.patient_id, self._staff_id,
                      lmp, edd, gravida, para, status, remarks))
                self.pregnancy_id = cur.fetchone()[0]
                self.is_new = False
                self.save_btn.setText("Save Changes")
                self.add_visit_btn.setEnabled(True)
                conn.commit()
                QMessageBox.information(self, "Success",
                    f"Pregnancy record created (ID: {self.pregnancy_id}).")
                self.accept()
            else:
                cur.execute("""
                    UPDATE pregnancy
                    SET lmp=%s, edd=%s, gravida=%s, para=%s,
                        status=%s, remarks=%s
                    WHERE pregnancy_id=%s
                """, (lmp, edd, gravida, para, status,
                      remarks, self.pregnancy_id))
                conn.commit()
                QMessageBox.information(self, "Saved",
                    "Pregnancy record updated.")
                self.accept()
            cur.close()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()

    # ── Save delivery ─────────────────────────────────────────────────────────
    def _save_delivery(self):
        if not self.pregnancy_id:
            return
        if not self.del_location.text().strip():
            QMessageBox.warning(self, "Validation", "Delivery location is required.")
            return
        if not self.del_time.text().strip():
            QMessageBox.warning(self, "Validation", "Delivery time is required (HH:MM).")
            return

        dd  = self.del_date.date().toPyDate()
        dt  = self.del_time.text().strip()
        do  = self.del_outcome.currentText()
        dtp = self.del_type.currentText() or None
        dlc = self.del_location.text().strip()
        bo  = self.birth_outcome.currentText() or None
        rto = self.referred_to.text().strip() or None
        rfr = self.referral_reason.toPlainText().strip() or None
        drr = self.del_remarks.toPlainText().strip() or None

        if not self._staff_id:
            QMessageBox.warning(self, "Error",
                "Could not determine current staff. Please log in again.")
            return

        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            # Upsert: delete old then insert (simple approach)
            cur.execute(
                "DELETE FROM delivery_record WHERE pregnancy_id = %s",
                (self.pregnancy_id,)
            )
            cur.execute("""
                INSERT INTO delivery_record
                    (pregnancy_id, patient_id, staff_id,
                     delivery_date, delivery_time, delivery_outcome,
                     delivery_type, delivery_location, birth_outcome,
                     referred_to, reason_for_referral, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (self.pregnancy_id, self.patient_id, self._staff_id,
                  dd, dt, do, dtp, dlc, bo, rto, rfr, drr))
            conn.commit()
            cur.close()
            QMessageBox.information(self, "Saved", "Delivery record saved.")
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()

    # ── Visit dialogs ─────────────────────────────────────────────────────────
    def _open_add_visit(self):
        dlg = VisitDialog(
            pregnancy_id=self.pregnancy_id,
            patient_id=self.patient_id,
            visit_id=None,
            parent=self
        )
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._load_visits()

    def _open_visit(self, visit_id):
        dlg = VisitDialog(
            pregnancy_id=self.pregnancy_id,
            patient_id=self.patient_id,
            visit_id=visit_id,
            parent=self
        )
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._load_visits()


# ─────────────────────────────────────────────────────────────────────────────
class VisitDialog(QDialog):
    """
    Add or view/edit a single prenatal_visit row.
    Also shows visit_diagnosis entries below the main form.
    """
    def __init__(self, pregnancy_id, patient_id, visit_id=None, parent=None):
        super().__init__(parent)
        self.pregnancy_id = pregnancy_id
        self.patient_id   = patient_id
        self.visit_id     = visit_id
        self.is_new       = visit_id is None
        self._staff_id    = self._current_staff_id()

        self.setWindowTitle("Add Visit" if self.is_new else "Visit Details")
        self.setMinimumSize(680, 580)
        self.setStyleSheet(BASE_STYLE + FIELD_STYLE)
        self._build_ui()

        if not self.is_new:
            self._load_visit()

    def _current_staff_id(self):
        user = session.get()
        if not user:
            return None
        conn = get_connection()
        if not conn:
            return None
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT staff_id FROM users WHERE user_id = %s",
                (user.get("id"),)
            )
            row = cur.fetchone()
            return row[0] if row else None
        except Exception:
            return None
        finally:
            conn.close()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 16)
        root.setSpacing(14)

        title = QLabel(
            "New Prenatal Visit" if self.is_new
            else f"Visit #{self.visit_id}"
        )
        title.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {CLR_TEXT};"
            "background: transparent;"
        )
        root.addWidget(title)

        root.addWidget(_section_label("Checkup Measurements"))

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setSpacing(10)

        self.visit_date   = QDateEdit()
        self.visit_date.setCalendarPopup(True)
        self.visit_date.setDate(QDate.currentDate())

        self.gest_age     = QSpinBox()
        self.gest_age.setRange(0, 45)
        self.gest_age.setSuffix(" weeks")

        self.weight       = QDoubleSpinBox()
        self.weight.setRange(0, 200)
        self.weight.setDecimals(2)
        self.weight.setSuffix(" kg")

        self.bp           = QLineEdit()
        self.bp.setPlaceholderText("e.g. 120/80")
        self.bp.setMaxLength(10)

        self.fundal_ht    = QDoubleSpinBox()
        self.fundal_ht.setRange(0, 50)
        self.fundal_ht.setDecimals(2)
        self.fundal_ht.setSuffix(" cm")

        self.fhr          = QSpinBox()
        self.fhr.setRange(0, 250)
        self.fhr.setSuffix(" bpm")
        self.fhr.setSpecialValueText("—")

        self.presentation = QComboBox()
        self.presentation.addItems(["", "Cephalic", "Breech", "Transverse"])

        self.next_visit   = QDateEdit()
        self.next_visit.setCalendarPopup(True)
        self.next_visit.setDate(QDate.currentDate().addDays(28))
        self.next_visit.setSpecialValueText("Not set")

        self.remarks      = QTextEdit()
        self.remarks.setFixedHeight(60)
        self.remarks.setPlaceholderText("Remarks…")

        form.addRow("Visit Date *",          self.visit_date)
        form.addRow("Gestational Age *",     self.gest_age)
        form.addRow("Weight *",              self.weight)
        form.addRow("Blood Pressure *",      self.bp)
        form.addRow("Fundal Height",         self.fundal_ht)
        form.addRow("Fetal Heart Rate",      self.fhr)
        form.addRow("Presentation",          self.presentation)
        form.addRow("Next Visit Date",       self.next_visit)
        form.addRow("Remarks",               self.remarks)
        root.addLayout(form)

        # Diagnosis section
        root.addWidget(_section_label("Diagnosis / Treatment"))

        diag_row = QHBoxLayout()
        self.diag_input = QLineEdit()
        self.diag_input.setPlaceholderText("Diagnosis…")
        self.treat_input = QLineEdit()
        self.treat_input.setPlaceholderText("Treatment given…")
        add_diag = _primary_btn("Add")
        add_diag.setFixedWidth(70)
        add_diag.clicked.connect(self._add_diagnosis_row)
        diag_row.addWidget(self.diag_input)
        diag_row.addWidget(self.treat_input)
        diag_row.addWidget(add_diag)
        root.addLayout(diag_row)

        self.diag_table = QTableWidget(0, 3)
        self.diag_table.setHorizontalHeaderLabels(
            ["Diagnosis", "Treatment Given", ""])
        self.diag_table.setStyleSheet(TABLE_STYLE)
        self.diag_table.setEditTriggers(
            QAbstractItemView.EditTriggerFlag.NoEditTriggers)
        self.diag_table.setShowGrid(False)
        self.diag_table.verticalHeader().setVisible(False)
        self.diag_table.setFixedHeight(130)
        hdr = self.diag_table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        root.addWidget(self.diag_table)

        # Footer
        foot = QHBoxLayout()
        foot.setSpacing(10)
        foot.addStretch()
        cancel = _ghost_btn("Cancel")
        cancel.clicked.connect(self.reject)
        foot.addWidget(cancel)

        save_btn = _primary_btn(
            "Save Visit" if self.is_new else "Update Visit"
        )
        save_btn.clicked.connect(self._save_visit)
        foot.addWidget(save_btn)
        root.addLayout(foot)

    def _add_diagnosis_row(self, diag=None, treat=None, diag_id=None):
        d = diag or self.diag_input.text().strip()
        t = treat or self.treat_input.text().strip()
        if not d:
            return

        r = self.diag_table.rowCount()
        self.diag_table.insertRow(r)
        self.diag_table.setRowHeight(r, 40)

        d_it = QTableWidgetItem(d)
        d_it.setData(Qt.ItemDataRole.UserRole, diag_id)
        self.diag_table.setItem(r, 0, d_it)
        self.diag_table.setItem(r, 1, QTableWidgetItem(t or ""))

        rm_btn = QPushButton("✕")
        rm_btn.setStyleSheet(f"""
            QPushButton {{
                background: #FDECEA; color: #C62828;
                border: none; border-radius: 5px;
                font-size: 11px; padding: 2px 8px;
            }}
            QPushButton:hover {{ background: #FFCDD2; }}
        """)
        rm_btn.clicked.connect(
            lambda _, row=r: self.diag_table.removeRow(row)
        )
        cell = QWidget()
        cell.setStyleSheet("background: transparent;")
        hl = QHBoxLayout(cell)
        hl.setContentsMargins(4, 4, 4, 4)
        hl.addWidget(rm_btn)
        self.diag_table.setCellWidget(r, 2, cell)

        self.diag_input.clear()
        self.treat_input.clear()

    def _load_visit(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT visit_date, gestational_age_weeks, weight_kg,
                       blood_pressure, fundal_height_cm, fetal_heart_rate,
                       presentation, next_visit_date, remarks
                FROM prenatal_visit WHERE visit_id = %s
            """, (self.visit_id,))
            row = cur.fetchone()
            if row:
                (vd, ga, wt, bp, fh, fhr,
                 pres, nv, rmk) = row
                self.visit_date.setDate(QDate(vd.year, vd.month, vd.day))
                self.gest_age.setValue(ga or 0)
                self.weight.setValue(float(wt) if wt else 0)
                self.bp.setText(bp or "")
                self.fundal_ht.setValue(float(fh) if fh else 0)
                self.fhr.setValue(fhr or 0)
                i = self.presentation.findText(pres or "")
                if i >= 0: self.presentation.setCurrentIndex(i)
                if nv:
                    self.next_visit.setDate(QDate(nv.year, nv.month, nv.day))
                if rmk: self.remarks.setPlainText(rmk)

            # Load diagnoses
            cur.execute("""
                SELECT diagnosis_id, diagnosis, treatment_given
                FROM visit_diagnosis WHERE visit_id = %s
            """, (self.visit_id,))
            for did, d, t in cur.fetchall():
                self._add_diagnosis_row(d, t, did)

            cur.close()
        except Exception as e:
            print("Load visit error:", e)
        finally:
            conn.close()

    def _save_visit(self):
        if not self.bp.text().strip():
            QMessageBox.warning(self, "Validation",
                "Blood pressure is required.")
            return

        vd  = self.visit_date.date().toPyDate()
        ga  = self.gest_age.value()
        wt  = self.weight.value()
        bp  = self.bp.text().strip()
        fh  = self.fundal_ht.value() or None
        fhr = self.fhr.value() or None
        pr  = self.presentation.currentText() or None
        nv  = self.next_visit.date().toPyDate()
        rmk = self.remarks.toPlainText().strip() or None

        if not self._staff_id:
            QMessageBox.warning(self, "Error",
                "Could not determine current staff.")
            return

        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            if self.is_new:
                cur.execute("""
                    INSERT INTO prenatal_visit
                        (pregnancy_id, staff_id, visit_date,
                         gestational_age_weeks, weight_kg, blood_pressure,
                         fundal_height_cm, fetal_heart_rate, presentation,
                         next_visit_date, remarks)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    RETURNING visit_id
                """, (self.pregnancy_id, self._staff_id, vd,
                      ga, wt, bp, fh, fhr, pr, nv, rmk))
                self.visit_id = cur.fetchone()[0]
            else:
                cur.execute("""
                    UPDATE prenatal_visit SET
                        visit_date=%s, gestational_age_weeks=%s,
                        weight_kg=%s, blood_pressure=%s,
                        fundal_height_cm=%s, fetal_heart_rate=%s,
                        presentation=%s, next_visit_date=%s, remarks=%s
                    WHERE visit_id=%s
                """, (vd, ga, wt, bp, fh, fhr, pr, nv, rmk,
                      self.visit_id))
                # Clear old diagnoses (re-insert all)
                cur.execute(
                    "DELETE FROM visit_diagnosis WHERE visit_id=%s",
                    (self.visit_id,)
                )

            # Save diagnoses
            for r in range(self.diag_table.rowCount()):
                d = self.diag_table.item(r, 0)
                t = self.diag_table.item(r, 1)
                if d and d.text():
                    cur.execute("""
                        INSERT INTO visit_diagnosis
                            (visit_id, diagnosis, treatment_given)
                        VALUES (%s, %s, %s)
                    """, (self.visit_id,
                          d.text(),
                          t.text() if t else None))

            conn.commit()
            cur.close()
            QMessageBox.information(self, "Saved", "Visit saved successfully.")
            self.accept()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()
