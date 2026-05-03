from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QFrame, QDialog, QFormLayout, QDateEdit,
    QComboBox, QMessageBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QFont, QPainter, QColor, QBrush, QPen

from screens.prenatal_dashboard_ui import Ui_PrenatalDashboardScreen
from database import get_connection

# ── Number badge
class NumberBadge(QLabel):
    def __init__(self, number: int, parent=None):
        super().__init__(parent)
        self._text = str(number)
        self.setFixedSize(54, 54)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor(21, 23, 61)))   # navy — matches buttons
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, 54, 54)
        painter.setPen(QPen(QColor(255, 255, 255)))
        font = QFont("Segoe UI", 16)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._text)


# ── Pregnancy card widget
class PregnancyCard(QWidget):
    """
    One card per pregnancy. Shows: number, EDD, status, visit count.
    Has a 'View Prenatal Care' button.
    """
    STATUS_STYLES = {
        "Active":    "background-color: rgb(220,240,220); color: rgb(30,100,30);",
        "Delivered": "background-color: rgb(220,230,255); color: rgb(21,23,100);",
        "Lost":      "background-color: rgb(255,220,220); color: rgb(150,30,30);",
    }

    def __init__(self, pregnancy: dict, visit_count: int, on_open, parent=None):
        super().__init__(parent)
        self.pregnancy   = pregnancy
        self.visit_count = visit_count
        self.on_open     = on_open
        self._build()

    def _build(self):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(4, 0, 4, 0)
        outer.setSpacing(14)

        # Number badge
        badge = NumberBadge(self.pregnancy.get("pregnancy_num", "?"))
        outer.addWidget(badge, alignment=Qt.AlignmentFlag.AlignVCenter)

        # Card
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgb(236, 198, 220);
                border-radius: 12px;
                border: 1px solid rgb(210, 177, 200);
            }
        """)
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(18, 12, 18, 12)
        card_lay.setSpacing(6)

        # Top row — title + open button
        top = QHBoxLayout()

        num  = self.pregnancy.get("pregnancy_num", "?")
        title = QLabel(f"{self._ordinal(num)} Pregnancy")
        title.setStyleSheet(
            "color: rgb(21,23,61); font-size: 14px; font-weight: bold; border: none;"
        )

        btn_open = QPushButton("View Prenatal Care →")
        btn_open.setFixedHeight(30)
        btn_open.setStyleSheet("""
            QPushButton {
                background-color: rgb(21, 23, 61);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 11px;
                font-weight: bold;
                padding: 0 12px;
            }
            QPushButton:hover { background-color: rgb(192, 116, 182); }
        """)
        btn_open.clicked.connect(lambda: self.on_open(self.pregnancy))

        top.addWidget(title)
        top.addStretch()
        top.addWidget(btn_open)
        card_lay.addLayout(top)

        # Info row — EDD, visits, status
        info = QHBoxLayout()
        info.setSpacing(24)

        def stat(label, value):
            lbl = QLabel(f"<b>{label}</b> {value}")
            lbl.setTextFormat(Qt.TextFormat.RichText)
            lbl.setStyleSheet(
                "color: rgb(21,23,61); font-size: 11px; border: none;"
            )
            return lbl

        edd = self.pregnancy.get("edd")
        edd_text = self._fmt_date(edd) if edd else "Not set"
        info.addWidget(stat("EDD:", edd_text))

        start = self.pregnancy.get("start_date")
        if start:
            info.addWidget(stat("Started:", self._fmt_date(start)))

        info.addWidget(stat("Prenatal Visits:", str(self.visit_count)))

        # Status chip
        status = self.pregnancy.get("status", "Active")
        chip = QLabel(f"  {status}  ")
        chip_style = self.STATUS_STYLES.get(status,
            "background-color: rgb(240,230,240); color: rgb(21,23,61);")
        chip.setStyleSheet(
            f"{chip_style} border-radius: 10px; padding: 2px 8px; "
            f"font-size: 11px; font-weight: bold; border: none;"
        )
        info.addWidget(chip)
        info.addStretch()

        card_lay.addLayout(info)
        outer.addWidget(card, stretch=1)

    def _ordinal(self, n):
        try:
            n = int(n)
            return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")
        except Exception:
            return str(n)

    def _fmt_date(self, d):
        try:
            if hasattr(d, "strftime"):
                return d.strftime("%B %d, %Y")
            from datetime import datetime
            return datetime.strptime(str(d), "%Y-%m-%d").strftime("%B %d, %Y")
        except Exception:
            return str(d)


# ── New Pregnancy Dialog ────────────────────────────────────────────────────
class NewPregnancyDialog(QDialog):
    STATUSES = ["Active", "Delivered", "Lost"]

    def __init__(self, patient_id: int, next_num: int, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.next_num   = next_num
        self.setWindowTitle(f"Add Pregnancy #{next_num}")
        self.setMinimumWidth(380)
        self.setStyleSheet("QDialog { background-color: rgb(240, 230, 240); }")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)

        title = QLabel(f"Add {self._ordinal(self.next_num)} Pregnancy")
        title.setStyleSheet(
            "color: rgb(21,23,61); font-size: 15px; font-weight: bold;"
            " font-family: 'Arial Black';"
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
        lbl_style = "color: rgb(21,23,61); font-size: 12px;"

        form = QFormLayout()
        form.setSpacing(10)

        self.f_start = QDateEdit()
        self.f_start.setCalendarPopup(True)
        self.f_start.setDate(QDate.currentDate())
        self.f_start.setStyleSheet(field_style)

        self.f_edd = QDateEdit()
        self.f_edd.setCalendarPopup(True)
        self.f_edd.setDate(QDate.currentDate().addDays(280))
        self.f_edd.setStyleSheet(field_style)

        self.f_status = QComboBox()
        self.f_status.addItems(self.STATUSES)
        self.f_status.setStyleSheet("""
            QComboBox {
                background-color: rgb(247,247,247);
                border: 1px solid rgb(158,136,163);
                border-radius: 6px;
                padding: 5px 8px;
                color: rgb(21,23,61);
                font-size: 12px;
            }
        """)

        for text, widget in [
            ("Start Date", self.f_start),
            ("EDD (Due Date)", self.f_edd),
            ("Status", self.f_status),
        ]:
            lbl = QLabel(text)
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

        btn_save = QPushButton("Save")
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
        self.result_data = {
            "patient_id":    self.patient_id,
            "pregnancy_num": self.next_num,
            "start_date":    self.f_start.date().toString("yyyy-MM-dd"),
            "edd":           self.f_edd.date().toString("yyyy-MM-dd"),
            "status":        self.f_status.currentText(),
        }
        self.accept()

    def _ordinal(self, n):
        return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")


# ── Main Screen ─────────────────────────────────────────────────────────────
class PrenatalDashboardScreen(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_PrenatalDashboardScreen()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB - Prenatal Care")
        self._initialized = False
        self._current_patient_id = None

        # Sidebar navigation
        self.ui.pushButton.clicked.connect(self.go_to_dashboard)
        self.ui.pushButton_2.clicked.connect(self.go_to_patient_records)
        self.ui.pushButton_3.clicked.connect(self.go_to_prenatal_care)
        self.ui.pushButton_4.clicked.connect(self.go_to_appointments)
        self.ui.pushButton_5.clicked.connect(self.logout)

        # Dashboard-specific
        self.ui.patient_combo.currentIndexChanged.connect(self.on_patient_selected)
        self.ui.btn_add_pregnancy.clicked.connect(self.on_add_pregnancy)

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

        self.ui.frame_2.setGeometry(0, 0, w, 61)
        self.ui.frame.setGeometry(0, 61, 231, h - 61)

        main_x = 231
        main_w = w - 231
        main_h = h - 61
        self.ui.frame_3.setGeometry(main_x, 61, main_w, main_h)

        card_w = main_w - 80

        self.ui.title_label.setGeometry(40, 20, 500, 61)
        self.ui.patient_selector_label.setGeometry(40, 92, 110, 28)
        self.ui.patient_combo.setGeometry(155, 89, min(320, card_w - 200), 28)
        self.ui.pregnancies_label.setGeometry(40, 132, 200, 24)
        self.ui.btn_add_pregnancy.setGeometry(card_w - 120, 128, 160, 32)
        self.ui.sep_line.setGeometry(40, 162, card_w, 1)
        self.ui.scroll_area.setGeometry(40, 170, card_w, max(main_h - 200, 200))

    def load_logo(self):
        pixmap = QPixmap("Asset/MaternaDB_logo.png")
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                self.ui.logo.width(), self.ui.logo.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.ui.logo.setPixmap(scaled)
            self.ui.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # ── Patient loading ──────────────────────────────────────────────────────
    def load_patients(self):
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
        self._current_patient_id = patient_id
        self._clear_cards()
        if patient_id is not None:
            self.load_pregnancies(patient_id)

    # ── Pregnancy loading ────────────────────────────────────────────────────
    def load_pregnancies(self, patient_id: int):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            # Get all pregnancies for this patient
            cursor.execute("""
                SELECT pregnancy_id, patient_id, pregnancy_num,
                       edd, start_date, status
                FROM pregnancy
                WHERE patient_id = %s
                ORDER BY pregnancy_num DESC
            """, (patient_id,))
            rows = cursor.fetchall()

            # Get visit counts per pregnancy in one query
            cursor.execute("""
                SELECT pregnancy_id, COUNT(*) AS visit_count
                FROM prenatal_visit
                WHERE pregnancy_id IN (
                    SELECT pregnancy_id FROM pregnancy WHERE patient_id = %s
                )
                GROUP BY pregnancy_id
            """, (patient_id,))
            counts = {row[0]: row[1] for row in cursor.fetchall()}
            conn.close()

        except Exception as e:
            print(f"Error loading pregnancies: {e}")
            if conn:
                conn.close()
            rows = []
            counts = {}

        self._clear_cards()
        layout = self.ui.scroll_layout

        if not rows:
            empty = QLabel(
                "No pregnancies recorded yet for this patient.\n"
                "Click '+ New Pregnancy' to add one."
            )
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet(
                "color: rgb(100,80,110); font-size: 13px; padding: 40px;"
            )
            layout.insertWidget(layout.count() - 1, empty)
            return

        columns = ["pregnancy_id", "patient_id", "pregnancy_num",
                   "edd", "start_date", "status"]
        for row in rows:
            pregnancy = dict(zip(columns, row))
            visit_count = counts.get(pregnancy["pregnancy_id"], 0)
            card = PregnancyCard(
                pregnancy, visit_count,
                on_open=self._open_prenatal_care
            )
            layout.insertWidget(layout.count() - 1, card)

    def _clear_cards(self):
        layout = self.ui.scroll_layout
        while layout.count() > 1:
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _open_prenatal_care(self, pregnancy: dict):
        """Open the Prenatal Care detail screen for the selected pregnancy."""
        from screens.prenatal_care_screen import PrenatalCareScreen
        self.prenatal_window = PrenatalCareScreen(
            pregnancy_id=pregnancy["pregnancy_id"],
            pregnancy_num=pregnancy["pregnancy_num"],
            patient_id=pregnancy["patient_id"]
        )
        self.prenatal_window.showMaximized()
        self.close()

    # ── Add pregnancy ────────────────────────────────────────────────────────
    def on_add_pregnancy(self):
        if self._current_patient_id is None:
            QMessageBox.warning(self, "No Patient Selected",
                                "Please select a patient first.")
            return

        # Figure out next pregnancy number
        conn = get_connection()
        next_num = 1
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COALESCE(MAX(pregnancy_num), 0) + 1
                    FROM pregnancy
                    WHERE patient_id = %s
                """, (self._current_patient_id,))
                result = cursor.fetchone()
                next_num = result[0] if result else 1
                conn.close()
            except Exception as e:
                print(f"Error getting next pregnancy num: {e}")
                if conn:
                    conn.close()

        dlg = NewPregnancyDialog(self._current_patient_id, next_num, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._save_pregnancy(dlg.result_data)

    def _save_pregnancy(self, data: dict):
        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "DB Error",
                                 "Could not connect to the database.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pregnancy
                    (patient_id, pregnancy_num, start_date, edd, status)
                VALUES
                    (%(patient_id)s, %(pregnancy_num)s, %(start_date)s,
                     %(edd)s, %(status)s)
            """, data)
            conn.commit()
            conn.close()
            self.load_pregnancies(self._current_patient_id)
        except Exception as e:
            QMessageBox.critical(self, "Save Error",
                                 f"Could not save pregnancy:\n{e}")
            if conn:
                conn.close()

    # ── Sidebar navigation ───────────────────────────────────────────────────
    def go_to_dashboard(self):
        from screens.dashboard_screen import DashboardScreen
        self.dashboard = DashboardScreen()
        self.dashboard.showMaximized()
        self.close()

    def go_to_patient_records(self):
        print("Go to Patient Records")

    def go_to_prenatal_care(self):
        pass  # Already here

    def go_to_appointments(self):
        print("Go to Appointments")

    def logout(self):
        from screens.login_screen import LoginScreen
        self.login_window = LoginScreen()
        self.login_window.showMaximized()
        self.close()
