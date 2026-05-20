from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget
from PyQt6.QtGui import QPainter, QColor, QBrush
from screens.signup_ui import Ui_SignUpWindow
from database import get_connection


# ── Painted background widget ─────────────────────────────────────────────────
class BlobBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgb(241, 233, 233);")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        w = self.width()
        h = self.height()

        # ── BLOB 1: Large anchor blob — bottom left corner ────────────────────
        painter.setBrush(QBrush(QColor(220, 110, 170, 200)))
        painter.drawEllipse(
            int(w * -0.10),
            int(h *  0.55),
            int(w *  0.55),
            int(h *  0.70),
        )

        # ── BLOB 2: Medium blob — top right ───────────────────────────────────
        painter.setBrush(QBrush(QColor(232, 138, 180, 180)))
        painter.drawEllipse(
            int(w *  0.60),
            int(h * -0.20),
            int(w *  0.55),
            int(h *  0.55),
        )

        # ── BLOB 3: Small accent blob — top left ──────────────────────────────
        painter.setBrush(QBrush(QColor(240, 180, 215, 150)))
        painter.drawEllipse(
            int(w * -0.08),
            int(h * -0.10),
            int(w *  0.28),
            int(h *  0.35),
        )

        # ── BLOB 4: Small accent blob — bottom right ──────────────────────────
        painter.setBrush(QBrush(QColor(225, 150, 190, 130)))
        painter.drawEllipse(
            int(w *  0.78),
            int(h *  0.70),
            int(w *  0.30),
            int(h *  0.40),
        )


class SignUpScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SignUpWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB - Sign Up")

        self.setStyleSheet("")

        # Replace centralwidget with BlobBackground
        self.blob_bg = BlobBackground(self)
        self.setCentralWidget(self.blob_bg)

        # Re-parent the card onto the blob background
        self.ui.frame.setParent(self.blob_bg)
        self.ui.frame.show()

        self.ui.signUpButton.clicked.connect(self.sign_up)
        self.ui.signInLinkButton.clicked.connect(self.go_to_login)

        self._load_staff()
        self.showMaximized()
        self.center_card()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.centralWidget():
            self.centralWidget().setGeometry(0, 0, self.width(), self.height())
            self.centralWidget().update()
        self.center_card()

    def center_card(self):
        if not self.centralWidget():
            return
        parent_w = self.centralWidget().width()
        parent_h = self.centralWidget().height()

        card_width  = 341
        card_height = 510   # increased to fit staff dropdown

        x = (parent_w - card_width)  // 2
        y = (parent_h - card_height) // 2

        self.ui.frame.setGeometry(x, y, card_width, card_height)

    # ── Staff loader ──────────────────────────────────────────────────────────
    def _load_staff(self):
        """Populate the staff combo with active staff who don't have an account yet."""
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT s.staff_id,
                       CONCAT(s.first_name, ' ', s.last_name, ' (', s.role, ')')
                FROM staff s
                WHERE s.status = 'Active'
                  AND s.staff_id NOT IN (
                      SELECT staff_id FROM users WHERE staff_id IS NOT NULL
                  )
                ORDER BY s.last_name, s.first_name
            """)
            rows = cur.fetchall()
            conn.close()

            self.ui.staffCombo.clear()
            self.ui.staffCombo.addItem("— Select your staff profile —", userData=None)
            for staff_id, name in rows:
                self.ui.staffCombo.addItem(name, userData=staff_id)

        except Exception as e:
            print(f"load staff error: {e}")
            if conn:
                conn.close()

    # ── Sign up ───────────────────────────────────────────────────────────────
    def sign_up(self):
        name             = self.ui.fullNameInput.text().strip()
        email            = self.ui.emailInput.text().strip()
        password         = self.ui.passwordInput.text()
        confirm_password = self.ui.confirmPasswordInput.text()
        staff_id         = self.ui.staffCombo.currentData()

        # ── Validation ────────────────────────────────────────────────────────
        if not name or not email or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        if staff_id is None:
            QMessageBox.warning(self, "Error", "Please select your staff profile.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters.")
            return

        # ── Save to DB ────────────────────────────────────────────────────────
        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "Error", "Cannot connect to database.")
            return

        try:
            cur = conn.cursor()

            # Fetch role from the selected staff record
            cur.execute("SELECT role FROM staff WHERE staff_id = %s", (staff_id,))
            row = cur.fetchone()
            if not row:
                QMessageBox.warning(self, "Error", "Selected staff profile not found.")
                conn.close()
                return
            role = row[0]

            # Insert the new user account
            cur.execute("""
                INSERT INTO users (name, email, password, role, staff_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, password, role, staff_id))

            conn.commit()
            conn.close()

            QMessageBox.information(
                self, "Success",
                f"Account created successfully!\nRegistered as: {role}"
            )
            self.go_to_login()

        except Exception as e:
            if "users_email_unique" in str(e):
                QMessageBox.warning(self, "Error", "That email address is already registered.")
            else:
                QMessageBox.warning(self, "Error", f"Registration failed:\n{e}")
            if conn:
                conn.close()

    # ── Navigation ────────────────────────────────────────────────────────────
    def go_to_login(self):
        from screens.login_screen import LoginScreen
        self.login_window = LoginScreen()
        self.login_window.showMaximized()
        self.close()