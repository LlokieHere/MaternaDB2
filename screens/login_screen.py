from PyQt6.QtWidgets import QMainWindow, QMessageBox
from screens.login_ui import Ui_MainWindow


class LoginScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB")

        # Connect buttons
        self.ui.signupButton.clicked.connect(self.sign_up)
        self.ui.signinButton.clicked.connect(self.sign_in)
        self.ui.forgotButton.clicked.connect(self.forgot_password)

    def showEvent(self, event):
        super().showEvent(event)
        self.center_card()

    def center_card(self):
        screen = self.screen().geometry()
        screen_width = screen.width()
        screen_height = screen.height()

        card_width = 341
        card_height = 381

        x = (screen_width - card_width) - 100
        y = (screen_height - card_height) // 2

        # ✔ correct name from your login_ui.py
        self.ui.log_inFrame.setGeometry(x, y, card_width, card_height)

    def sign_in(self):
        email = self.ui.EmailInput.text()     # ✔ correct
        password = self.ui.PasswordInput.text() # ✔ correct
        print(f"Signing in: {email}")

    def sign_up(self):
        from screens.signup_screen import SignUpScreen
        self.signup_window = SignUpScreen()
        self.signup_window.showMaximized()
        self.signup_window.show()
        self.close()

    def forgot_password(self):
        print("Forgot password clicked")