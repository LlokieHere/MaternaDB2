from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtGui import QPainter, QColor, QBrush
from screens.signup_ui import Ui_SignUpWindow
from database import get_connection


class SignUpScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SignUpWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB - Sign Up")

        # Connect buttons
        self.ui.signUpButton.clicked.connect(self.sign_up)
        self.ui.signInLinkButton.clicked.connect(self.go_to_login)

        # This runs AFTER window is shown to get real screen size
        self.showMaximized()
        self.center_card()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Big pink blob — bottom right
        painter.setBrush(QBrush(QColor(232, 138, 180)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(400, 150, 900, 800)

        # Smaller lighter blob — top right
        painter.setBrush(QBrush(QColor(240, 180, 210)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(600, -100, 500, 400)

    def center_card(self):
        # Get the full screen size
        screen = self.screen().geometry()
        screen_width = screen.width()
        screen_height = screen.height()

        # Size of your card
        card_width = 341
        card_height = 480

        # Calculate center position
        x = (screen_width - card_width) // 2
        y = (screen_height - card_height) // 2

        # Move the card to center
        self.ui.frame.setGeometry(x, y, card_width, card_height)

    def sign_up(self):
        name = self.ui.fullNameInput.text()
        email = self.ui.emailInput.text()
        password = self.ui.passwordInput.text()
        confirm_password = self.ui.confirmPasswordInput.text()

        # Basic validation
        if not name or not email or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "Please fill in all fields!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters!")
            return

        # Save directly to database
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                    (name, email, password)
                )
                conn.commit()
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
        self.login_window.show()
        self.close()
