from PyQt6.QtWidgets import QMainWindow
from screens.login_ui import Ui_MainWindow

class LoginScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB")

        # Connect buttons
        self.ui.pushButton.clicked.connect(self.sign_up)    # Sign up
        self.ui.pushButton_2.clicked.connect(self.sign_in)  # Sign in
        self.ui.pushButton_3.clicked.connect(self.forgot_password)  # Forgot password

    def sign_in(self):
        email = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        print(f"Signing in: {email}")

    def sign_up(self):
        print("Redirect to sign up")

    def forgot_password(self):
        print("Forgot password clicked")