from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget
from PyQt6.QtGui import QPainter, QColor, QBrush, QPixmap
from screens.login_ui import Ui_MainWindow
from database import get_connection
import user_profile.session as session  # ✅ FIXED: was `import user_profile.session`
from PyQt6.QtCore import QSettings

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

        painter.setBrush(QBrush(QColor(220, 110, 170, 200)))
        painter.drawEllipse(int(w*-0.10), int(h*0.55), int(w*0.55), int(h*0.70))

        painter.setBrush(QBrush(QColor(232, 138, 180, 180)))
        painter.drawEllipse(int(w*0.60), int(h*-0.20), int(w*0.55), int(h*0.55))

        painter.setBrush(QBrush(QColor(240, 180, 215, 150)))
        painter.drawEllipse(int(w*-0.08), int(h*-0.10), int(w*0.28), int(h*0.35))

        painter.setBrush(QBrush(QColor(225, 150, 190, 130)))
        painter.drawEllipse(int(w*0.78), int(h*0.70), int(w*0.30), int(h*0.40))


class LoginScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB")
        self._initialized = False
        self._password_visible = False

        settings = QSettings("MaternaDB", "Login")
        saved_email = settings.value("email")
        saved_password = settings.value("password")

        if saved_email:
            self.ui.EmailInput.setText(saved_email)
            self.ui.checkBox.setChecked(True)
        if saved_password:
            self.ui.PasswordInput.setText(saved_password)
            self.ui.checkBox.setChecked(True)
        self.setStyleSheet("")

        self.blob_bg = BlobBackground(self)
        self.setCentralWidget(self.blob_bg)

        self.ui.log_inFrame.setParent(self.blob_bg)
        self.ui.log_inFrame.show()

        self._fix_contrast()

        self.ui.PasswordInput.setEchoMode(self.ui.PasswordInput.EchoMode.Password)
        self.ui.pushButton.setText("Show")
        self.ui.pushButton.setCheckable(False)
        self.ui.pushButton.clicked.connect(self.toggle_password)

        self.ui.signupButton.clicked.connect(self.sign_up)
        self.ui.signinButton.clicked.connect(self.sign_in)
        self.ui.forgotButton.clicked.connect(self.forgot_password)

    def _fix_contrast(self):
        light = (
            "color: rgb(247,247,247); font-size: 13px;"
            "font-weight: bold; border: none; background: transparent;"
        )
        input_s = (
            "background-color: rgb(247,247,247); border-radius: 5px;"
            "padding-left: 8px; border: none; font-size: 13px; color: rgb(30,30,30);"
        )
        btn_s = (
            "background-color: rgb(21,23,61); color: rgb(247,247,247);"
            "border-radius: 8px; font-size: 13px; font-weight: bold; border: none;"
        )
        self.ui.label_2.setStyleSheet(
            "color: rgb(247,247,247); font-size: 18px;"
            "font-weight: bold; border: none; background: transparent;"
        )
        self.ui.label_3.setStyleSheet(light)
        self.ui.label_4.setStyleSheet(light)
        self.ui.EmailInput.setStyleSheet(input_s)
        self.ui.PasswordInput.setStyleSheet(input_s)
        self.ui.signinButton.setStyleSheet(btn_s)
        self.ui.signupButton.setStyleSheet(btn_s)
        self.ui.forgotButton.setStyleSheet(
            "color: rgb(247,247,247); font-size: 12px;"
            "background: transparent; border: none; text-decoration: underline;"
        )
        self.ui.checkBox.setStyleSheet(
            "color: rgb(247,247,247); font-size: 12px;"
            "background: transparent; border: none;"
        )
        self.ui.pushButton.setStyleSheet(
            "background-color: rgb(247,247,247); color: rgb(30,30,30);"
            "border-radius: 5px; font-size: 12px; border: none;"
        )

    def toggle_password(self):
        self._password_visible = not self._password_visible
        self.ui.PasswordInput.setEchoMode(
            self.ui.PasswordInput.EchoMode.Normal
            if self._password_visible else
            self.ui.PasswordInput.EchoMode.Password
        )
        self.ui.pushButton.setText("Hide" if self._password_visible else "Show")

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
            self.ui.label.setPixmap(pixmap.scaled(
                self.ui.label.width(), self.ui.label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
            self.ui.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def center_card(self):
        if not self.centralWidget():
            return
        w = self.centralWidget().width()
        h = self.centralWidget().height()
        card_w, card_h = 385, 460
        x = w - card_w - int(w * 0.07)
        y = (h - card_h) // 2
        self.ui.log_inFrame.setGeometry(x, y, card_w, card_h)

    def sign_in(self):
        email = self.ui.EmailInput.text().strip()
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
            cursor.execute("""
                SELECT user_id, name, email, password,
                    role, contact, profile_pic, date_joined
                FROM users
                WHERE email = %s AND password = %s
            """, (email, password))

            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if not user:
                QMessageBox.warning(self, "Error", "Invalid email or password!")
                return

            # ✅ ONLY RUN IF LOGIN IS SUCCESSFUL
            session.set_user(user)

            settings = QSettings("MaternaDB", "Login")

            if self.ui.checkBox.isChecked():
                settings.setValue("email", email)
                settings.setValue("password", password)  # ⚠️ not recommended
            else:
                settings.remove("email")
                settings.remove("password")

            from screens.dashboard_screen import DashboardScreen
            self.dashboard = DashboardScreen()
            self.dashboard.showMaximized()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed:\n{e}")

    def sign_up(self):
        from screens.signup_screen import SignUpScreen
        self.signup_window = SignUpScreen()
        self.signup_window.showMaximized()
        self.close()

    def forgot_password(self):
        email = self.ui.EmailInput.text().strip()

        if not email:
            QMessageBox.warning(self, "Error", "Enter your email first.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            QMessageBox.warning(self, "Error", "Email not found.")
            return

        new_password, ok = QtWidgets.QInputDialog.getText(
            self, "Reset Password", "Enter new password:"
        )

        if ok and new_password:
            cursor.execute(
                "UPDATE users SET password = %s WHERE email = %s",
                (new_password, email)
            )
            conn.commit()
            QMessageBox.information(self, "Success", "Password updated!")

        cursor.close()
        conn.close()