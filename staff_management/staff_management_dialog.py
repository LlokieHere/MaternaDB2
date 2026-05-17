"""
staff_management_dialog.py
Place this file at:  screens/staff_management_dialog.py

Opens as a QDialog from the Dashboard's "Manage Staff" button.
Supports: Add / Edit / View / Deactivate (soft-delete).
"""

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QComboBox, QDateEdit, QFormLayout, QFrame, QMessageBox,
    QDialogButtonBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate
from database import get_connection


# ─────────────────────────────────────────────
#  SHARED STYLE CONSTANTS  (match dashboard palette)
# ─────────────────────────────────────────────
DARK_BG   = "rgb(21, 23, 61)"
PINK_BG   = "rgb(236, 198, 220)"
PURPLE_BG = "rgb(192, 116, 182)"
WHITE     = "rgb(240, 230, 240)"

DIALOG_STYLE = f"""
    QDialog {{
        background-color: {WHITE};
    }}
    QLabel {{
        color: {DARK_BG};
        font-family: 'Segoe UI';
    }}
    QTableWidget {{
        background-color: {PINK_BG};
        border: 1px solid rgb(158, 136, 163);
        border-radius: 10px;
        gridline-color: transparent;
    }}
    QTableWidget::item {{
        background-color: {PINK_BG};
        color: {DARK_BG};
        padding: 6px;
        border: none;
        border-bottom: 1px solid rgb(210, 177, 200);
    }}
    QTableWidget::item:selected {{
        background-color: rgb(220, 170, 210);
        color: {DARK_BG};
    }}
    QHeaderView::section {{
        background-color: {PINK_BG};
        color: {DARK_BG};
        font-weight: bold;
        font-size: 11px;
        border: none;
        border-bottom: 1px solid rgb(155, 132, 160);
        padding: 6px;
    }}
    QPushButton {{
        border-radius: 8px;
        font-family: 'Segoe UI';
        font-size: 13px;
        padding: 6px 18px;
    }}
    QScrollBar:vertical {{
        background: white;
        width: 6px;
        border-radius: 3px;
    }}
    QScrollBar::handle:vertical {{
        background: rgb(178, 100, 168);
        border-radius: 3px;
    }}
"""

FORM_STYLE = f"""
    QDialog {{
        background-color: {WHITE};
    }}
    QLabel {{
        color: {DARK_BG};
        font-family: 'Segoe UI';
        font-size: 13px;
    }}
    QLineEdit, QComboBox, QDateEdit {{
        background-color: {PINK_BG};
        border: 1px solid rgb(158, 136, 163);
        border-radius: 8px;
        padding: 6px 10px;
        color: {DARK_BG};
        font-size: 13px;
        font-family: 'Segoe UI';
    }}
    QLineEdit:focus, QComboBox:focus, QDateEdit:focus {{
        border: 1.5px solid rgb(192, 116, 182);
    }}
    QComboBox::drop-down {{
        border: none;
    }}
    QPushButton {{
        border-radius: 8px;
        font-family: 'Segoe UI';
        font-size: 13px;
        padding: 7px 20px;
    }}
"""


# ─────────────────────────────────────────────
#  STAFF FORM DIALOG  (Add / Edit / View)
# ─────────────────────────────────────────────
class StaffFormDialog(QDialog):
    """
    Reusable form for Add, Edit, and View modes.
    mode: 'add' | 'edit' | 'view'
    staff_data: dict with keys matching DB columns (for edit/view)
    """

    ROLES = [
        "Doctor", "Midwife", "Nurse", "Nurse Aide",
        "Medical Technologist", "Pharmacist", "Receptionist",
        "Billing Staff", "Administrator", "Other"
    ]

    def __init__(self, parent=None, mode="add", staff_data=None):
        super().__init__(parent)
        self.mode        = mode
        self.staff_data  = staff_data or {}
        self.read_only   = (mode == "view")

        title_map = {"add": "Add Staff", "edit": "Edit Staff", "view": "Staff Details"}
        self.setWindowTitle(title_map.get(mode, "Staff"))
        self.setMinimumWidth(420)
        self.setStyleSheet(FORM_STYLE)

        self._build_ui()
        if mode in ("edit", "view"):
            self._populate()

    # ── UI ────────────────────────────────────
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(16)

        # Title bar
        title_lbl = QLabel(self.windowTitle())
        title_lbl.setStyleSheet(
            f"font-size: 18px; font-weight: bold; color: {DARK_BG};"
        )
        layout.addWidget(title_lbl)

        # Divider
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"background: rgb(192,116,182); border: none;")
        layout.addWidget(divider)

        # Form fields
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setSpacing(12)

        def lbl(text):
            l = QLabel(text)
            l.setStyleSheet(f"font-weight: bold; color: {DARK_BG};")
            return l

        self.first_name  = QLineEdit()
        self.last_name   = QLineEdit()
        self.middle_name = QLineEdit()

        self.role_cb = QComboBox()
        self.role_cb.addItems(self.ROLES)

        self.contact = QLineEdit()
        self.contact.setPlaceholderText("e.g. 09XXXXXXXXX")

        self.email = QLineEdit()
        self.email.setPlaceholderText("e.g. staff@clinic.com")

        self.date_hired = QDateEdit()
        self.date_hired.setCalendarPopup(True)
        self.date_hired.setDate(QDate.currentDate())
        self.date_hired.setDisplayFormat("yyyy-MM-dd")

        form.addRow(lbl("Last Name *"),    self.last_name)
        form.addRow(lbl("First Name *"),   self.first_name)
        form.addRow(lbl("Middle Name"),    self.middle_name)
        form.addRow(lbl("Role *"),         self.role_cb)
        form.addRow(lbl("Contact No."),    self.contact)
        form.addRow(lbl("Email"),          self.email)
        form.addRow(lbl("Date Hired *"),   self.date_hired)
        layout.addLayout(form)

        if self.read_only:
            for w in (self.first_name, self.last_name, self.middle_name,
                      self.contact, self.email):
                w.setReadOnly(True)
                w.setStyleSheet(
                    f"background: rgb(220,210,225); border: 1px solid rgb(158,136,163);"
                    f"border-radius: 8px; padding: 6px 10px; color: {DARK_BG};"
                )
            self.role_cb.setEnabled(False)
            self.date_hired.setReadOnly(True)
            self.date_hired.setButtonSymbols(
                QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons
            )

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        if self.read_only:
            close_btn = QPushButton("Close")
            close_btn.setStyleSheet(
                f"background-color: {DARK_BG}; color: white;"
            )
            close_btn.clicked.connect(self.reject)
            btn_layout.addWidget(close_btn)
        else:
            cancel_btn = QPushButton("Cancel")
            cancel_btn.setStyleSheet(
                "background-color: rgb(210,190,215); color: rgb(21,23,61);"
            )
            cancel_btn.clicked.connect(self.reject)

            save_btn = QPushButton("Save")
            save_btn.setStyleSheet(
                f"background-color: {PURPLE_BG}; color: white; font-weight: bold;"
            )
            save_btn.clicked.connect(self._save)

            btn_layout.addWidget(cancel_btn)
            btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def _populate(self):
        d = self.staff_data
        self.first_name.setText(d.get("first_name", ""))
        self.last_name.setText(d.get("last_name", ""))
        self.middle_name.setText(d.get("middle_name") or "")
        self.contact.setText(d.get("contact_no") or "")
        self.email.setText(d.get("email") or "")

        role = d.get("role", "")
        idx  = self.role_cb.findText(role)
        self.role_cb.setCurrentIndex(idx if idx >= 0 else 0)

        hired = d.get("date_hired")
        if hired:
            if hasattr(hired, "year"):            # datetime.date object
                self.date_hired.setDate(QDate(hired.year, hired.month, hired.day))
            else:                                  # string fallback
                self.date_hired.setDate(QDate.fromString(str(hired), "yyyy-MM-dd"))

    # ── SAVE ──────────────────────────────────
    def _save(self):
        first = self.first_name.text().strip()
        last  = self.last_name.text().strip()
        role  = self.role_cb.currentText()

        if not first or not last or not role:
            QMessageBox.warning(self, "Validation", "Last name, first name, and role are required.")
            return

        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "Error", "Cannot connect to database.")
            return

        try:
            cur = conn.cursor()
            if self.mode == "add":
                cur.execute("""
                    INSERT INTO staff
                        (first_name, last_name, middle_name, role,
                         contact_no, email, date_hired, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 'Active')
                """, (
                    first, last,
                    self.middle_name.text().strip() or None,
                    role,
                    self.contact.text().strip() or None,
                    self.email.text().strip() or None,
                    self.date_hired.date().toString("yyyy-MM-dd"),
                ))
            else:  # edit
                cur.execute("""
                    UPDATE staff
                    SET first_name=%s, last_name=%s, middle_name=%s,
                        role=%s, contact_no=%s, email=%s, date_hired=%s
                    WHERE staff_id=%s
                """, (
                    first, last,
                    self.middle_name.text().strip() or None,
                    role,
                    self.contact.text().strip() or None,
                    self.email.text().strip() or None,
                    self.date_hired.date().toString("yyyy-MM-dd"),
                    self.staff_data["staff_id"],
                ))
            conn.commit()
            cur.close()
            self.accept()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            conn.close()


# ─────────────────────────────────────────────
#  MAIN STAFF MANAGEMENT DIALOG
# ─────────────────────────────────────────────
class StaffManagementDialog(QDialog):
    """
    Main staff management screen opened from the Dashboard.
    Shows all staff in a table with Add / Edit / View / Deactivate actions.
    """

    COLUMNS = ["Name", "Role", "Contact", "Email", "Date Hired", "Status"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Staff")
        self.setMinimumSize(900, 580)
        self.setStyleSheet(DIALOG_STYLE)
        self._staff_cache = []   # list of dicts for the currently displayed rows
        self._filter_active = "All"

        self._build_ui()
        self.load_staff()

    # ── UI ────────────────────────────────────
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(16)

        # ── Header row ──────────────────────────────────────────────────────
        header_row = QHBoxLayout()

        title = QLabel("Staff Management")
        title.setStyleSheet(
            f"font-size: 22px; font-weight: bold; color: {DARK_BG}; font-family: 'Arial Black';"
        )
        header_row.addWidget(title)
        header_row.addStretch()

        self.add_btn = QPushButton("＋  Add Staff")
        self.add_btn.setStyleSheet(
            f"background-color: {PURPLE_BG}; color: white; font-weight: bold;"
            "border-radius: 8px; padding: 7px 18px;"
        )
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.clicked.connect(self._add_staff)
        header_row.addWidget(self.add_btn)
        root.addLayout(header_row)

        # ── Filter + Search row ─────────────────────────────────────────────
        filter_row = QHBoxLayout()
        filter_row.setSpacing(10)

        filter_lbl = QLabel("Show:")
        filter_lbl.setStyleSheet(f"color: {DARK_BG}; font-size: 13px;")
        filter_row.addWidget(filter_lbl)

        for label in ("All", "Active", "Inactive"):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setChecked(label == "All")
            btn.setObjectName(f"filter_{label}")
            btn.setStyleSheet(self._filter_btn_style(label == "All"))
            btn.clicked.connect(lambda checked, l=label: self._apply_filter(l))
            filter_row.addWidget(btn)

        filter_row.addStretch()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍  Search name or role…")
        self.search_box.setFixedWidth(240)
        self.search_box.setStyleSheet(
            f"background-color: {PINK_BG}; border: 1px solid rgb(158,136,163);"
            "border-radius: 8px; padding: 6px 10px; font-size: 13px;"
        )
        self.search_box.textChanged.connect(self._apply_filter_current)
        filter_row.addWidget(self.search_box)
        root.addLayout(filter_row)

        # ── Table ───────────────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)

        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)      # Name
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Role
        hdr.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Contact
        hdr.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)      # Email
        hdr.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Date
        hdr.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Status

        self.table.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        root.addWidget(self.table, stretch=1)

        # ── Action buttons row ──────────────────────────────────────────────
        action_row = QHBoxLayout()
        action_row.addStretch()

        self.view_btn = QPushButton("👁  View")
        self.edit_btn = QPushButton("✏  Edit")
        self.deact_btn = QPushButton("⊘  Deactivate")

        self.view_btn.setStyleSheet(
            f"background-color: {DARK_BG}; color: white; border-radius: 8px; padding: 7px 16px;"
        )
        self.edit_btn.setStyleSheet(
            "background-color: rgb(210,170,50); color: white; border-radius: 8px; padding: 7px 16px;"
        )
        self.deact_btn.setStyleSheet(
            "background-color: rgb(180,60,60); color: white; border-radius: 8px; padding: 7px 16px;"
        )

        for b in (self.view_btn, self.edit_btn, self.deact_btn):
            b.setCursor(Qt.CursorShape.PointingHandCursor)

        self.view_btn.clicked.connect(self._view_staff)
        self.edit_btn.clicked.connect(self._edit_staff)
        self.deact_btn.clicked.connect(self._deactivate_staff)

        action_row.addWidget(self.view_btn)
        action_row.addWidget(self.edit_btn)
        action_row.addWidget(self.deact_btn)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(
            "background-color: rgb(210,190,215); color: rgb(21,23,61);"
            "border-radius: 8px; padding: 7px 20px;"
        )
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        action_row.addWidget(close_btn)

        root.addLayout(action_row)

    def _filter_btn_style(self, active=False):
        if active:
            return (
                f"background-color: {PURPLE_BG}; color: white;"
                "border-radius: 7px; padding: 5px 14px; font-size: 12px;"
            )
        return (
            f"background-color: {PINK_BG}; color: {DARK_BG};"
            "border-radius: 7px; padding: 5px 14px; font-size: 12px;"
            "border: 1px solid rgb(158,136,163);"
        )

    # ── DATA ──────────────────────────────────
    def load_staff(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT staff_id, first_name, last_name, middle_name,
                       role, contact_no, email, date_hired, status
                FROM staff
                ORDER BY last_name, first_name
            """)
            rows = cur.fetchall()
            cur.close()

            self._staff_cache = [
                {
                    "staff_id":   r[0],
                    "first_name": r[1],
                    "last_name":  r[2],
                    "middle_name": r[3],
                    "role":       r[4],
                    "contact_no": r[5],
                    "email":      r[6],
                    "date_hired": r[7],
                    "status":     r[8],
                }
                for r in rows
            ]
            self._render_table(self._staff_cache)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load staff:\n{e}")
        finally:
            conn.close()

    def _render_table(self, data):
        self.table.setRowCount(0)
        for staff in data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            full_name = f"{staff['last_name']}, {staff['first_name']}"
            if staff.get("middle_name"):
                full_name += f" {staff['middle_name'][0]}."

            values = [
                full_name,
                staff.get("role", ""),
                staff.get("contact_no") or "—",
                staff.get("email") or "—",
                str(staff.get("date_hired") or ""),
                staff.get("status", ""),
            ]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

                # Colour-code status column
                if col == 5:
                    if val == "Active":
                        item.setForeground(QtGui.QColor("rgb(0,128,64)"))
                    else:
                        item.setForeground(QtGui.QColor("rgb(180,60,60)"))

                self.table.setItem(row, col, item)

            # Store staff_id as row data for easy retrieval
            self.table.item(row, 0).setData(Qt.ItemDataRole.UserRole, staff["staff_id"])

    # ── FILTER ────────────────────────────────
    def _apply_filter(self, status_label):
        self._filter_active = status_label

        # Update button styles
        for label in ("All", "Active", "Inactive"):
            btn = self.findChild(QPushButton, f"filter_{label}")
            if btn:
                btn.setStyleSheet(self._filter_btn_style(label == status_label))

        self._apply_filter_current()

    def _apply_filter_current(self):
        search  = self.search_box.text().strip().lower()
        status  = self._filter_active

        filtered = [
            s for s in self._staff_cache
            if (status == "All" or s["status"] == status)
            and (
                not search
                or search in s["first_name"].lower()
                or search in s["last_name"].lower()
                or search in (s.get("role") or "").lower()
            )
        ]
        self._render_table(filtered)

    # ── HELPERS ───────────────────────────────
    def _selected_staff(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Select Staff", "Please select a staff member first.")
            return None
        staff_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        return next((s for s in self._staff_cache if s["staff_id"] == staff_id), None)

    # ── ACTIONS ───────────────────────────────
    def _add_staff(self):
        dlg = StaffFormDialog(parent=self, mode="add")
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.load_staff()

    def _view_staff(self):
        staff = self._selected_staff()
        if not staff:
            return
        dlg = StaffFormDialog(parent=self, mode="view", staff_data=staff)
        dlg.exec()

    def _edit_staff(self):
        staff = self._selected_staff()
        if not staff:
            return
        dlg = StaffFormDialog(parent=self, mode="edit", staff_data=staff)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.load_staff()

    def _deactivate_staff(self):
        staff = self._selected_staff()
        if not staff:
            return

        current_status = staff["status"]
        if current_status == "Inactive":
            # Offer to reactivate instead
            reply = QMessageBox.question(
                self, "Reactivate Staff",
                f"{staff['first_name']} {staff['last_name']} is already Inactive.\n"
                "Do you want to set them back to Active?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
            new_status = "Active"
            msg_success = "Staff member reactivated."
        else:
            reply = QMessageBox.warning(
                self, "Deactivate Staff",
                f"Deactivate {staff['first_name']} {staff['last_name']}?\n\n"
                "They will no longer appear in active staff lists, "
                "but their historical records will be preserved.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
            new_status = "Inactive"
            msg_success = "Staff member deactivated."

        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE staff SET status=%s WHERE staff_id=%s",
                (new_status, staff["staff_id"])
            )
            conn.commit()
            cur.close()
            QMessageBox.information(self, "Done", msg_success)
            self.load_staff()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()