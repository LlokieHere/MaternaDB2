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
        # Biggest blob, anchored off-screen bottom-left, peeks in
        painter.setBrush(QBrush(QColor(220, 110, 170, 200)))
        painter.drawEllipse(
            int(w * -0.10),   # x: starts slightly off left edge
            int(h *  0.55),   # y: starts at 55% down
            int(w *  0.55),   # width: half the screen wide
            int(h *  0.70),   # height: tall, bleeds off bottom
        )

        # ── BLOB 2: Medium blob — top right ───────────────────────────────────
        # Peeks from top-right corner
        painter.setBrush(QBrush(QColor(232, 138, 180, 180)))
        painter.drawEllipse(
            int(w *  0.60),   # x: starts at 60% from left
            int(h * -0.20),   # y: starts above top edge
            int(w *  0.55),   # width: bleeds off right
            int(h *  0.55),   # height: moderate height
        )

        # ── BLOB 3: Small accent blob — top left ──────────────────────────────
        # Small decorative blob top-left corner
        painter.setBrush(QBrush(QColor(240, 180, 215, 150)))
        painter.drawEllipse(
            int(w * -0.08),   # x: slightly off left
            int(h * -0.10),   # y: slightly off top
            int(w *  0.28),   # width: small
            int(h *  0.35),   # height: small
        )

        # ── BLOB 4: Small accent blob — bottom right ──────────────────────────
        # Tiny blob bottom-right to balance composition
        painter.setBrush(QBrush(QColor(225, 150, 190, 130)))
        painter.drawEllipse(
            int(w *  0.78),   # x: far right
            int(h *  0.70),   # y: lower area
            int(w *  0.30),   # width: small
            int(h *  0.40),   # height: small, bleeds off bottom-right
        )


class SignUpScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SignUpWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB - Sign Up")

        # ✅ Clear solid background
        self.setStyleSheet("")

        # ✅ Replace centralwidget with BlobBackground
        self.blob_bg = BlobBackground(self)
        self.setCentralWidget(self.blob_bg)

        # ✅ Re-parent the card onto the blob background
        self.ui.frame.setParent(self.blob_bg)
        self.ui.frame.show()

        self.ui.signUpButton.clicked.connect(self.sign_up)
        self.ui.signInLinkButton.clicked.connect(self.go_to_login)

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
        card_height = 480

        x = (parent_w - card_width)  // 2
        y = (parent_h - card_height) // 2

        self.ui.frame.setGeometry(x, y, card_width, card_height)

    def sign_up(self):
        name             = self.ui.fullNameInput.text().strip()
        email            = self.ui.emailInput.text().strip()
        password         = self.ui.passwordInput.text()
        confirm_password = self.ui.confirmPasswordInput.text()

        if not name or not email or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "Please fill in all fields!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters!")
            return

        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "Error", "Cannot connect to database.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Account created successfully!")
            self.go_to_login()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Registration failed: {e}")
            conn.close()

    def go_to_login(self):
        from screens.login_screen import LoginScreen
        self.login_window = LoginScreen()
        self.login_window.showMaximized()
        self.close()