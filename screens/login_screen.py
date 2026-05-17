from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget
from PyQt6.QtGui import QPainter, QColor, QBrush, QPixmap
from screens.login_ui import Ui_MainWindow
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


class LoginScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB")
        self._initialized = False
        self._password_visible = False

        # ✅ Clear solid background
        self.setStyleSheet("")

        # ✅ Replace centralwidget with BlobBackground
        self.blob_bg = BlobBackground(self)
        self.setCentralWidget(self.blob_bg)

        # ✅ Re-parent the card onto the blob background
        self.ui.log_inFrame.setParent(self.blob_bg)
        self.ui.log_inFrame.show()

        # ✅ Fix label and input text contrast
        self._fix_contrast()

        # ✅ Fix show/hide password button
        self.ui.PasswordInput.setEchoMode(
            self.ui.PasswordInput.EchoMode.Password
        )
        self.ui.pushButton.setText("Show")
        self.ui.pushButton.setCheckable(False)
        self.ui.pushButton.clicked.connect(self.toggle_password)

        self.ui.signupButton.clicked.connect(self.sign_up)
        self.ui.signinButton.clicked.connect(self.sign_in)
        self.ui.forgotButton.clicked.connect(self.forgot_password)

    def _fix_contrast(self):
        """Make all labels inside the card light and readable."""
        light_style = (
            "color: rgb(247, 247, 247);"
            "font-size: 13px;"
            "font-weight: bold;"
            "border: none;"
            "background: transparent;"
        )
        input_style = (
            "background-color: rgb(247, 247, 247);"
            "border-radius: 5px;"
            "padding-left: 8px;"
            "border: none;"
            "font-size: 13px;"
            "color: rgb(30, 30, 30);"
        )
        btn_style = (
            "background-color: rgb(21, 23, 61);"
            "color: rgb(247, 247, 247);"
            "border-radius: 8px;"
            "font-size: 13px;"
            "font-weight: bold;"
            "border: none;"
        )
        forgot_style = (
            "color: rgb(247, 247, 247);"
            "font-size: 12px;"
            "background: transparent;"
            "border: none;"
            "text-decoration: underline;"
        )
        remember_style = (
            "color: rgb(247, 247, 247);"
            "font-size: 12px;"
            "background: transparent;"
            "border: none;"
        )
        show_style = (
            "background-color: rgb(247, 247, 247);"
            "color: rgb(30, 30, 30);"
            "border-radius: 5px;"
            "font-size: 12px;"
            "border: none;"
        )

        self.ui.label_2.setStyleSheet(
            "color: rgb(247, 247, 247); font-size: 18px;"
            "font-weight: bold; border: none; background: transparent;"
        )
        self.ui.label_3.setStyleSheet(light_style)
        self.ui.label_4.setStyleSheet(light_style)
        self.ui.EmailInput.setStyleSheet(input_style)
        self.ui.PasswordInput.setStyleSheet(input_style)
        self.ui.signinButton.setStyleSheet(btn_style)
        self.ui.signupButton.setStyleSheet(btn_style)
        self.ui.forgotButton.setStyleSheet(forgot_style)
        self.ui.checkBox.setStyleSheet(remember_style)
        self.ui.pushButton.setStyleSheet(show_style)

    def toggle_password(self):
        """Toggle password visibility."""
        self._password_visible = not self._password_visible
        if self._password_visible:
            self.ui.PasswordInput.setEchoMode(
                self.ui.PasswordInput.EchoMode.Normal
            )
            self.ui.pushButton.setText("Hide")
        else:
            self.ui.PasswordInput.setEchoMode(
                self.ui.PasswordInput.EchoMode.Password
            )
            self.ui.pushButton.setText("Show")

    def showEvent(self, event):
        super().showEvent(event)
        if not self._initialized:
            self._initialized = True
            self.center_card()
            self.load_logo()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.centralWidget():
            self.centralWidget().setGeometry(0, 0, self.width(), self.height())
            self.centralWidget().update()
        self.center_card()

    def load_logo(self):
        pixmap = QPixmap("Asset/MaternaDB_logo.png")
        if not pixmap.isNull():
            self.ui.label.setText("")
            self.ui.label.setStyleSheet("border: none; background: transparent;")
            scaled = pixmap.scaled(
                self.ui.label.width(),
                self.ui.label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.ui.label.setPixmap(scaled)
            self.ui.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def center_card(self):
        if not self.centralWidget():
            return
        w = self.centralWidget().width()
        h = self.centralWidget().height()

        card_width  = 385
        card_height = 460

        x = w - card_width - int(w * 0.07)   # right side with margin
        y = (h - card_height) // 2

        self.ui.log_inFrame.setGeometry(x, y, card_width, card_height)

    def sign_in(self):
        email    = self.ui.EmailInput.text().strip()
        password = self.ui.PasswordInput.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields!")
            return

        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "Error", "Cannot connect to database.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE email = %s AND password = %s",
                (email, password)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                from screens.dashboard_screen import DashboardScreen
                self.dashboard = DashboardScreen()
                self.dashboard.showMaximized()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Invalid email or password!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed:\n{e}")

    def sign_up(self):
        from screens.signup_screen import SignUpScreen
        self.signup_window = SignUpScreen()
        self.signup_window.showMaximized()
        self.close()

    def forgot_password(self):
        print("Forgot password clicked")