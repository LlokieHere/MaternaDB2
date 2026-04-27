# Form implementation generated for MaternaDB Sign Up Screen
# Matches the style of login_ui.py

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SignUpWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        # Same light pink background as login
        MainWindow.setStyleSheet("background-color: rgb(241, 233, 233);")

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Same purple card frame as login
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(230, 50, 341, 480))
        self.frame.setStyleSheet("border-radius:30px;\n"
                                 "background-color: rgb(178, 100, 168);")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        # LOGO label
        self.logoLabel = QtWidgets.QLabel(parent=self.frame)
        self.logoLabel.setGeometry(QtCore.QRect(140, 20, 60, 40))
        self.logoLabel.setStyleSheet("color: rgb(247, 247, 247);\n"
                                     "font-weight: bold;\n"
                                     "font-size: 14px;\n"
                                     "border: none;")
        self.logoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logoLabel.setObjectName("logoLabel")

        # Welcome label
        self.welcomeLabel = QtWidgets.QLabel(parent=self.frame)
        self.welcomeLabel.setGeometry(QtCore.QRect(90, 65, 161, 20))
        self.welcomeLabel.setStyleSheet("color: rgb(247, 247, 247);\n"
                                        "font-weight: bold;\n"
                                        "font-size: 14px;\n"
                                        "border: none;")
        self.welcomeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.welcomeLabel.setObjectName("welcomeLabel")

        # Full Name label
        self.fullNameLabel = QtWidgets.QLabel(parent=self.frame)
        self.fullNameLabel.setGeometry(QtCore.QRect(40, 100, 80, 16))
        self.fullNameLabel.setStyleSheet("color: rgb(247, 247, 247);\n"
                                         "font-size: 11px;\n"
                                         "border: none;")
        self.fullNameLabel.setObjectName("fullNameLabel")

        # Full Name input
        self.fullNameInput = QtWidgets.QLineEdit(parent=self.frame)
        self.fullNameInput.setGeometry(QtCore.QRect(40, 118, 261, 31))
        self.fullNameInput.setStyleSheet("background-color: rgb(247, 247, 247);\n"
                                          "border-radius: 5px;\n"
                                          "padding-left: 8px;\n"
                                          "border: none;")
        self.fullNameInput.setObjectName("fullNameInput")

        # Email label
        self.emailLabel = QtWidgets.QLabel(parent=self.frame)
        self.emailLabel.setGeometry(QtCore.QRect(40, 160, 49, 16))
        self.emailLabel.setStyleSheet("color: rgb(247, 247, 247);\n"
                                       "font-size: 11px;\n"
                                       "border: none;")
        self.emailLabel.setObjectName("emailLabel")

        # Email input
        self.emailInput = QtWidgets.QLineEdit(parent=self.frame)
        self.emailInput.setGeometry(QtCore.QRect(40, 178, 261, 31))
        self.emailInput.setStyleSheet("background-color: rgb(247, 247, 247);\n"
                                       "border-radius: 5px;\n"
                                       "padding-left: 8px;\n"
                                       "border: none;")
        self.emailInput.setObjectName("emailInput")

        # Password label
        self.passwordLabel = QtWidgets.QLabel(parent=self.frame)
        self.passwordLabel.setGeometry(QtCore.QRect(40, 220, 70, 16))
        self.passwordLabel.setStyleSheet("color: rgb(247, 247, 247);\n"
                                          "font-size: 11px;\n"
                                          "border: none;")
        self.passwordLabel.setObjectName("passwordLabel")

        # Password input
        self.passwordInput = QtWidgets.QLineEdit(parent=self.frame)
        self.passwordInput.setGeometry(QtCore.QRect(40, 238, 261, 31))
        self.passwordInput.setStyleSheet("background-color: rgb(247, 247, 247);\n"
                                          "border-radius: 5px;\n"
                                          "padding-left: 8px;\n"
                                          "border: none;")
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.passwordInput.setObjectName("passwordInput")

        # Confirm Password label
        self.confirmPasswordLabel = QtWidgets.QLabel(parent=self.frame)
        self.confirmPasswordLabel.setGeometry(QtCore.QRect(40, 280, 120, 16))
        self.confirmPasswordLabel.setStyleSheet("color: rgb(247, 247, 247);\n"
                                                 "font-size: 11px;\n"
                                                 "border: none;")
        self.confirmPasswordLabel.setObjectName("confirmPasswordLabel")

        # Confirm Password input
        self.confirmPasswordInput = QtWidgets.QLineEdit(parent=self.frame)
        self.confirmPasswordInput.setGeometry(QtCore.QRect(40, 298, 261, 31))
        self.confirmPasswordInput.setStyleSheet("background-color: rgb(247, 247, 247);\n"
                                                 "border-radius: 5px;\n"
                                                 "padding-left: 8px;\n"
                                                 "border: none;")
        self.confirmPasswordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirmPasswordInput.setObjectName("confirmPasswordInput")

        # Sign Up button (same dark navy color as login buttons)
        self.signUpButton = QtWidgets.QPushButton(parent=self.frame)
        self.signUpButton.setGeometry(QtCore.QRect(40, 350, 261, 35))
        self.signUpButton.setStyleSheet("background-color: rgb(21, 23, 61);\n"
                                         "color: rgb(247, 247, 247);\n"
                                         "border-radius: 8px;\n"
                                         "font-size: 13px;\n"
                                         "font-weight: bold;\n"
                                         "border: none;")
        self.signUpButton.setCheckable(False)
        self.signUpButton.setObjectName("signUpButton")

        # Already have account label
        self.alreadyLabel = QtWidgets.QLabel(parent=self.frame)
        self.alreadyLabel.setGeometry(QtCore.QRect(60, 400, 130, 16))
        self.alreadyLabel.setStyleSheet("color: rgb(247, 247, 247);\n"
                                         "font-size: 11px;\n"
                                         "border: none;")
        self.alreadyLabel.setObjectName("alreadyLabel")

        # Sign In link button
        self.signInLinkButton = QtWidgets.QPushButton(parent=self.frame)
        self.signInLinkButton.setGeometry(QtCore.QRect(190, 396, 80, 24))
        self.signInLinkButton.setStyleSheet("color: rgb(247, 247, 247);\n"
                                             "font-size: 11px;\n"
                                             "text-decoration: underline;\n"
                                             "background-color: transparent;\n"
                                             "border: none;")
        self.signInLinkButton.setCheckable(False)
        self.signInLinkButton.setObjectName("signInLinkButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MaternaDB - Sign Up"))
        self.logoLabel.setText(_translate("MainWindow", "LOGO"))
        self.welcomeLabel.setText(_translate("MainWindow", "Create an Account"))
        self.fullNameLabel.setText(_translate("MainWindow", "Full Name"))
        self.fullNameInput.setPlaceholderText(_translate("MainWindow", "Enter your full name"))
        self.emailLabel.setText(_translate("MainWindow", "Email"))
        self.emailInput.setPlaceholderText(_translate("MainWindow", "Enter your email"))
        self.passwordLabel.setText(_translate("MainWindow", "Password"))
        self.passwordInput.setPlaceholderText(_translate("MainWindow", "Enter your password"))
        self.confirmPasswordLabel.setText(_translate("MainWindow", "Confirm Password"))
        self.confirmPasswordInput.setPlaceholderText(_translate("MainWindow", "Confirm your password"))
        self.signUpButton.setText(_translate("MainWindow", "Sign Up"))
        self.alreadyLabel.setText(_translate("MainWindow", "Already have an account?"))
        self.signInLinkButton.setText(_translate("MainWindow", "Sign In"))
