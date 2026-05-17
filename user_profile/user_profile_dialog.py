from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QFrame,
    QMessageBox, QComboBox, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from database import get_connection
import user_profile.session as session  # ✅ FIXED


_DIALOG_STYLE = """
    QDialog { background-color: #F1E9E9; }
    QLabel  { color: #15173D; font-size: 13px; }
    QLineEdit, QComboBox {
        border: 1px solid #15173D;
        border-radius: 8px;
        padding: 5px 10px;
        background-color: #F1E9E9;
        color: #15173D;
        font-size: 13px;
    }
    QPushButton#btn_save {
        background-color: #15173D; color: white;
        border-radius: 10px; padding: 6px 20px; font-size: 13px;
    }
    QPushButton#btn_save:hover { background-color: #2a2c5a; }
    QPushButton#btn_cancel {
        background-color: #ECC6DC; color: #15173D;
        border-radius: 10px; padding: 6px 20px; font-size: 13px;
        border: 1px solid #c9a0ba;
    }
    QPushButton#btn_cancel:hover { background-color: #ddb0cc; }
    QPushButton#btn_change_pw {
        background-color: transparent; color: #15173D;
        border: 1px solid #15173D; border-radius: 8px;
        padding: 5px 14px; font-size: 12px;
    }
    QPushButton#btn_change_pw:hover { background-color: #e0d0e0; }
"""


class UserProfileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Profile")
        self.setMinimumWidth(420)
        self.setStyleSheet(_DIALOG_STYLE)

        self.user = session.get()

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(28, 24, 28, 24)

        # ── Header ────────────────────────────────────────────────────────────
        header = QHBoxLayout()

        avatar = QLabel("👤")
        avatar.setFixedSize(64, 64)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            "background-color: #ECC6DC; border-radius: 32px;"
            "font-size: 30px; border: none;"
        )
        header.addWidget(avatar)

        title_col = QVBoxLayout()
        title_col.setSpacing(2)

        self.lbl_name = QLabel(self.user.get("name", "—") if self.user else "—")
        self.lbl_name.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #15173D; border: none;"
        )

        self.lbl_role = QLabel(self.user.get("role", "Admin") if self.user else "Admin")
        self.lbl_role.setStyleSheet("font-size: 13px; color: #555; border: none;")

        title_col.addWidget(self.lbl_name)
        title_col.addWidget(self.lbl_role)
        title_col.addStretch()
        header.addLayout(title_col, stretch=1)
        layout.addLayout(header)

        # ── Divider ───────────────────────────────────────────────────────────
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #ccc;")
        layout.addWidget(line)

        # ── Edit form ─────────────────────────────────────────────────────────
        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.inp_name = QLineEdit(self.user.get("name", "") if self.user else "")
        self.inp_name.setPlaceholderText("Full name")
        form.addRow("Full Name *", self.inp_name)

        self.inp_email = QLineEdit(self.user.get("email", "") if self.user else "")
        self.inp_email.setPlaceholderText("Email address")
        form.addRow("Email *", self.inp_email)

        self.inp_contact = QLineEdit(self.user.get("contact", "") if self.user else "")
        self.inp_contact.setPlaceholderText("e.g. 09123456789")
        form.addRow("Contact #", self.inp_contact)

        self.cmb_role = QComboBox()
        for r in ["Admin", "Doctor", "Midwife", "Nurse"]:
            self.cmb_role.addItem(r)
        current_role = self.user.get("role", "Admin") if self.user else "Admin"
        idx = self.cmb_role.findText(current_role)
        if idx >= 0:
            self.cmb_role.setCurrentIndex(idx)
        form.addRow("Role", self.cmb_role)

        lbl_joined = QLabel(self.user.get("date_joined", "—") if self.user else "—")
        lbl_joined.setStyleSheet("border: none; color: #555; font-size: 13px;")
        form.addRow("Date Joined", lbl_joined)

        layout.addLayout(form)

        # ── Change password button ────────────────────────────────────────────
        self.btn_change_pw = QPushButton("Change Password")
        self.btn_change_pw.setObjectName("btn_change_pw")
        self.btn_change_pw.clicked.connect(self.open_change_password)
        layout.addWidget(self.btn_change_pw)

        # ── Action buttons ────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_save = QPushButton("Save Changes")
        self.btn_save.setObjectName("btn_save")
        self.btn_save.clicked.connect(self.save)

        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_save)
        layout.addLayout(btn_row)

    def save(self):
        if not self.user:
            QMessageBox.warning(self, "Error", "No user session found.")
            return

        name    = self.inp_name.text().strip()
        email   = self.inp_email.text().strip()
        contact = self.inp_contact.text().strip()
        role    = self.cmb_role.currentText()

        if not name or not email:
            QMessageBox.warning(self, "Validation", "Name and email are required.")
            return

        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "DB Error", "Cannot connect to database.")
            return

        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE users
                SET name = %s, email = %s, contact = %s, role = %s
                WHERE user_id = %s
            """, (name, email, contact, role, self.user["user_id"]))
            conn.commit()
            cur.close()
            conn.close()

            session.current_user["name"]    = name
            session.current_user["email"]   = email
            session.current_user["contact"] = contact
            session.current_user["role"]    = role

            QMessageBox.information(self, "Success", "Profile updated successfully!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{e}")
            conn.close()

    def open_change_password(self):
        if not self.user:
            return
        dlg = ChangePasswordDialog(self.user["user_id"], parent=self)
        dlg.exec()


class ChangePasswordDialog(QDialog):
    def __init__(self, user_id: int, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setWindowTitle("Change Password")
        self.setMinimumWidth(360)
        self.setStyleSheet(_DIALOG_STYLE)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)

        title = QLabel("Change Password")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #15173D;")
        layout.addWidget(title)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #ccc;")
        layout.addWidget(line)

        form = QFormLayout()
        form.setSpacing(10)

        self.inp_current = QLineEdit()
        self.inp_current.setEchoMode(QLineEdit.EchoMode.Password)
        self.inp_current.setPlaceholderText("Enter current password")
        form.addRow("Current Password", self.inp_current)

        self.inp_new = QLineEdit()
        self.inp_new.setEchoMode(QLineEdit.EchoMode.Password)
        self.inp_new.setPlaceholderText("Enter new password")
        form.addRow("New Password", self.inp_new)

        self.inp_confirm = QLineEdit()
        self.inp_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.inp_confirm.setPlaceholderText("Confirm new password")
        form.addRow("Confirm Password", self.inp_confirm)

        layout.addLayout(form)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("btn_cancel")
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("Update")
        btn_save.setObjectName("btn_save")
        btn_save.clicked.connect(self.update_password)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def update_password(self):
        current = self.inp_current.text()
        new_pw  = self.inp_new.text()
        confirm = self.inp_confirm.text()

        if not current or not new_pw or not confirm:
            QMessageBox.warning(self, "Validation", "Please fill in all fields.")
            return
        if new_pw != confirm:
            QMessageBox.warning(self, "Validation", "New passwords do not match.")
            return
        if len(new_pw) < 6:
            QMessageBox.warning(self, "Validation", "Password must be at least 6 characters.")
            return

        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "DB Error", "Cannot connect to database.")
            return

        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT user_id FROM users WHERE user_id = %s AND password = %s",
                (self.user_id, current)
            )
            if not cur.fetchone():
                QMessageBox.warning(self, "Error", "Current password is incorrect.")
                cur.close()
                conn.close()
                return

            cur.execute(
                "UPDATE users SET password = %s WHERE user_id = %s",
                (new_pw, self.user_id)
            )
            conn.commit()
            cur.close()
            conn.close()

            QMessageBox.information(self, "Success", "Password updated successfully!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update password:\n{e}")
            conn.close()