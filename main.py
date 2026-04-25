import sys
from PyQt6.QtWidgets import QApplication
from screens.login_screen import LoginScreen  # ← fix this line

def main():
    app = QApplication(sys.argv)
    window = LoginScreen()
    window.showMaximized()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()