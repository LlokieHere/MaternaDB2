from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtGui import QPixmap
from screens.login_ui import Ui_MainWindow
from database import get_connection


class LoginScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB")
        self._initialized = False  # ← add this flag

        self.ui.signupButton.clicked.connect(self.sign_up)
        self.ui.signinButton.clicked.connect(self.sign_in)
        self.ui.forgotButton.clicked.connect(self.forgot_password)

    def showEvent(self, event):
        super().showEvent(event)
        if not self._initialized:  # ← only run ONCE
            self._initialized = True
            self.center_card()
            self.load_logo()

    def load_logo(self):
        pixmap = QPixmap("Asset/MaternaDB_logo.png")
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                self.ui.label.width(),
                self.ui.label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.ui.label.setPixmap(scaled)
            self.ui.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def center_card(self):
        screen = self.screen().geometry()
        screen_width = screen.width()
        screen_height = screen.height()

        card_width = 385
        card_height = 460

        x = (screen_width - card_width) - 100
        y = (screen_height - card_height) // 2

        self.ui.log_inFrame.setGeometry(x, y, card_width, card_height)

    def sign_in(self):
        email = self.ui.EmailInput.text()
        password = self.ui.PasswordInput.text()

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE email = %s AND password = %s",
                (email, password)
            )
            user = cursor.fetchone()
            conn.close()

            if user:
                from screens.dashboard_screen import DashboardScreen
                self.dashboard = DashboardScreen()
                self.dashboard.showMaximized()  # ← only this, remove .show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Invalid email or password!")

    def sign_up(self):
        from screens.signup_screen import SignUpScreen
        self.signup_window = SignUpScreen()
        self.signup_window.showMaximized()  # ← only this, remove .show()
        self.close()

    def forgot_password(self):
        print("Forgot password clicked")