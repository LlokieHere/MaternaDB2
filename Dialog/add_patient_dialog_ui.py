# patient_profile_dialog_ui.py — fixed placeholders, calendar inputs, corrected labels

from PyQt6 import QtCore, QtGui, QtWidgets
from Dialog.calendar_dropdown import CalendarDropdown

FIELD_STYLE = (
    "border-radius: 12px;"
    "background-color: rgb(240, 230, 240);"
    "border: 1px solid rgb(26, 26, 62);"
)

BTN_STYLE = (
    "border-radius: 12px;"
    "padding: 4px;"
    "background-color: rgb(240, 230, 240);"
    "border: 1px solid rgb(26, 26, 62);"
)

LBL_STYLE = 'font: 10pt "Segoe UI";'


class Ui_StackedWidget(object):
    def setupUi(self, StackedWidget):
        StackedWidget.setObjectName("StackedWidget")
        StackedWidget.resize(400, 533)

        # ════════════════════════════════════════════════════════════════════
        # PAGE 1 — Personal Information
        # ════════════════════════════════════════════════════════════════════
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")

        self.frame = QtWidgets.QFrame(parent=self.page)
        self.frame.setGeometry(QtCore.QRect(0, 0, 401, 531))
        self.frame.setStyleSheet("background-color: rgb(240, 230, 240);")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        # ── Section heading ──────────────────────────────────────────────────
        self.personalInformation_label = QtWidgets.QLabel(parent=self.frame)
        self.personalInformation_label.setGeometry(QtCore.QRect(80, 10, 241, 41))
        self.personalInformation_label.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Expanding,
            )
        )
        self.personalInformation_label.setStyleSheet('font: 16pt "Segoe UI";')
        self.personalInformation_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.personalInformation_label.setObjectName("personalInformation_label")

        # ── Row 1: First Name | Last Name ────────────────────────────────────
        self.firstName = QtWidgets.QLabel(parent=self.frame)
        self.firstName.setGeometry(QtCore.QRect(40, 70, 91, 16))
        self.firstName.setStyleSheet(LBL_STYLE)
        self.firstName.setObjectName("firstName")

        self.firstName_placeholder = QtWidgets.QLineEdit(parent=self.frame)
        self.firstName_placeholder.setGeometry(QtCore.QRect(40, 90, 151, 31))
        self.firstName_placeholder.setStyleSheet(FIELD_STYLE)
        self.firstName_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.firstName_placeholder.setObjectName("firstName_placeholder")

        self.lastName = QtWidgets.QLabel(parent=self.frame)
        self.lastName.setGeometry(QtCore.QRect(200, 70, 91, 16))
        self.lastName.setStyleSheet(LBL_STYLE)
        self.lastName.setObjectName("lastName")

        self.lastName_placeholder = QtWidgets.QLineEdit(parent=self.frame)
        self.lastName_placeholder.setGeometry(QtCore.QRect(200, 90, 151, 31))
        self.lastName_placeholder.setStyleSheet(FIELD_STYLE)
        self.lastName_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lastName_placeholder.setObjectName("lastName_placeholder")

        # ── Row 2: Middle Name | Suffix ──────────────────────────────────────
        self.middleName = QtWidgets.QLabel(parent=self.frame)
        self.middleName.setGeometry(QtCore.QRect(40, 130, 141, 16))
        self.middleName.setStyleSheet(LBL_STYLE)
        self.middleName.setObjectName("middleName")

        self.middleName_placeholder = QtWidgets.QLineEdit(parent=self.frame)
        self.middleName_placeholder.setGeometry(QtCore.QRect(40, 150, 151, 31))
        self.middleName_placeholder.setStyleSheet(FIELD_STYLE)
        self.middleName_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.middleName_placeholder.setObjectName("middleName_placeholder")

        self.suffix = QtWidgets.QLabel(parent=self.frame)
        self.suffix.setGeometry(QtCore.QRect(200, 130, 91, 16))
        self.suffix.setStyleSheet(LBL_STYLE)
        self.suffix.setObjectName("suffix")

        self.suffix_placeholder = QtWidgets.QLineEdit(parent=self.frame)
        self.suffix_placeholder.setGeometry(QtCore.QRect(200, 150, 151, 31))
        self.suffix_placeholder.setStyleSheet(FIELD_STYLE)
        self.suffix_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.suffix_placeholder.setObjectName("suffix_placeholder")

        # ── Row 3: Date of Birth (calendar) | Civil Status ───────────────────
        self.dateOfBirth = QtWidgets.QLabel(parent=self.frame)
        self.dateOfBirth.setGeometry(QtCore.QRect(40, 190, 91, 16))
        self.dateOfBirth.setStyleSheet(LBL_STYLE)
        self.dateOfBirth.setObjectName("dateOfBirth")

        self.dateOfBirth_placeholder = CalendarDropdown(parent=self.frame)
        self.dateOfBirth_placeholder.setGeometry(QtCore.QRect(40, 210, 151, 36))
        self.dateOfBirth_placeholder.setDate(QtCore.QDate(2000, 1, 1))
        self.dateOfBirth_placeholder.setMaximumDate(QtCore.QDate.currentDate())
        self.dateOfBirth_placeholder.setObjectName("dateOfBirth_placeholder")

        self.civilStatus = QtWidgets.QLabel(parent=self.frame)
        self.civilStatus.setGeometry(QtCore.QRect(200, 190, 91, 16))
        self.civilStatus.setStyleSheet(LBL_STYLE)
        self.civilStatus.setObjectName("civilStatus")

        self.civilStatus_placeholder = QtWidgets.QComboBox(parent=self.frame)
        self.civilStatus_placeholder.setGeometry(QtCore.QRect(200, 210, 151, 31))
        self.civilStatus_placeholder.setStyleSheet(
            "border-radius: 12px;"
            "background-color: rgb(240, 230, 240);"
            "border: 1px solid rgb(26, 26, 62);"
            "padding: 4px 10px;"
        )
        self.civilStatus_placeholder.setObjectName("civilStatus_placeholder")
        for status in ["Single", "Married", "Widowed", "Separated", "Annulled"]:
            self.civilStatus_placeholder.addItem(status)

        # ── Row 4: Contact Number | Occupation ──────────────────────────────
        self.contactNum = QtWidgets.QLabel(parent=self.frame)
        self.contactNum.setGeometry(QtCore.QRect(40, 250, 101, 16))
        self.contactNum.setStyleSheet(LBL_STYLE)
        self.contactNum.setObjectName("contactNum")

        self.contactNum_placeholder = QtWidgets.QLineEdit(parent=self.frame)
        self.contactNum_placeholder.setGeometry(QtCore.QRect(40, 270, 151, 31))
        self.contactNum_placeholder.setStyleSheet(FIELD_STYLE)
        self.contactNum_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.contactNum_placeholder.setObjectName("contactNum_placeholder")

        self.occupation = QtWidgets.QLabel(parent=self.frame)
        self.occupation.setGeometry(QtCore.QRect(200, 250, 141, 16))
        self.occupation.setStyleSheet(LBL_STYLE)
        self.occupation.setObjectName("occupation")

        self.occupation_placeholder = QtWidgets.QLineEdit(parent=self.frame)
        self.occupation_placeholder.setGeometry(QtCore.QRect(200, 270, 151, 31))
        self.occupation_placeholder.setStyleSheet(FIELD_STYLE)
        self.occupation_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.occupation_placeholder.setObjectName("occupation_placeholder")

        # ── Row 5: PhilHealth# | Nationality ────────────────────────────────
        self.philHealth = QtWidgets.QLabel(parent=self.frame)
        self.philHealth.setGeometry(QtCore.QRect(40, 310, 91, 16))
        self.philHealth.setStyleSheet(LBL_STYLE)
        self.philHealth.setObjectName("philHealth")

        self.philHealth_placeholder = QtWidgets.QLineEdit(parent=self.frame)
        self.philHealth_placeholder.setGeometry(QtCore.QRect(40, 330, 151, 31))
        self.philHealth_placeholder.setStyleSheet(FIELD_STYLE)
        self.philHealth_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.philHealth_placeholder.setObjectName("philHealth_placeholder")

        self.nationality = QtWidgets.QLabel(parent=self.frame)
        self.nationality.setGeometry(QtCore.QRect(200, 310, 91, 16))
        self.nationality.setStyleSheet(LBL_STYLE)
        self.nationality.setObjectName("nationality")

        self.nationality_placeholder = QtWidgets.QLineEdit(parent=self.frame)
        self.nationality_placeholder.setGeometry(QtCore.QRect(200, 330, 151, 31))
        self.nationality_placeholder.setStyleSheet(FIELD_STYLE)
        self.nationality_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.nationality_placeholder.setObjectName("nationality_placeholder")

        # ── Row 6: Religion | Blood Type ─────────────────────────────────────
        self.Religion = QtWidgets.QLabel(parent=self.frame)
        self.Religion.setGeometry(QtCore.QRect(40, 370, 91, 21))
        self.Religion.setStyleSheet(LBL_STYLE)
        self.Religion.setObjectName("Religion")

        self.religion_placeholder = QtWidgets.QLineEdit(parent=self.frame)
        self.religion_placeholder.setGeometry(QtCore.QRect(40, 390, 151, 31))
        self.religion_placeholder.setStyleSheet(FIELD_STYLE)
        self.religion_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.religion_placeholder.setObjectName("religion_placeholder")

        self.Religion_2 = QtWidgets.QLabel(parent=self.frame)
        self.Religion_2.setGeometry(QtCore.QRect(200, 370, 91, 21))
        self.Religion_2.setStyleSheet(LBL_STYLE)
        self.Religion_2.setObjectName("Religion_2")

        self.religion_placeholder_2 = QtWidgets.QComboBox(parent=self.frame)
        self.religion_placeholder_2.setGeometry(QtCore.QRect(200, 390, 151, 31))
        self.religion_placeholder_2.setStyleSheet(
            "border-radius: 12px;"
            "background-color: rgb(240, 230, 240);"
            "border: 1px solid rgb(26, 26, 62);"
            "padding: 4px 10px;"
        )
        self.religion_placeholder_2.setObjectName("religion_placeholder_2")
        for bt in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]:
            self.religion_placeholder_2.addItem(bt)

        # ── Buttons row ──────────────────────────────────────────────────────
        self.layoutWidget = QtWidgets.QWidget(parent=self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 450, 320, 28))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton.setStyleSheet(BTN_STYLE)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_2.setStyleSheet(BTN_STYLE)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_3.setStyleSheet(BTN_STYLE)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)

        StackedWidget.addWidget(self.page)

        # ════════════════════════════════════════════════════════════════════
        # PAGE 2 — Address + Emergency Contact
        # ════════════════════════════════════════════════════════════════════
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")

        self.frame_2 = QtWidgets.QFrame(parent=self.page_2)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 401, 531))
        self.frame_2.setStyleSheet("background-color: rgb(240, 230, 240);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")

        # ── Address heading ──────────────────────────────────────────────────
        self.address_label = QtWidgets.QLabel(parent=self.frame_2)
        self.address_label.setGeometry(QtCore.QRect(80, 10, 241, 41))
        self.address_label.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Expanding,
            )
        )
        self.address_label.setStyleSheet('font: 16pt "Segoe UI";')
        self.address_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.address_label.setObjectName("address_label")

        # ── Row 1: Street | Barangay ─────────────────────────────────────────
        self.street_label = QtWidgets.QLabel(parent=self.frame_2)
        self.street_label.setGeometry(QtCore.QRect(40, 60, 91, 16))
        self.street_label.setStyleSheet(LBL_STYLE)
        self.street_label.setObjectName("street_label")

        self.street_placeholder = QtWidgets.QLineEdit(parent=self.frame_2)
        self.street_placeholder.setGeometry(QtCore.QRect(40, 80, 151, 31))
        self.street_placeholder.setStyleSheet(FIELD_STYLE)
        self.street_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.street_placeholder.setObjectName("street_placeholder")

        self.barangay_label = QtWidgets.QLabel(parent=self.frame_2)
        self.barangay_label.setGeometry(QtCore.QRect(200, 60, 91, 16))
        self.barangay_label.setStyleSheet(LBL_STYLE)
        self.barangay_label.setObjectName("barangay_label")

        self.barangay_placeholder = QtWidgets.QLineEdit(parent=self.frame_2)
        self.barangay_placeholder.setGeometry(QtCore.QRect(200, 80, 151, 31))
        self.barangay_placeholder.setStyleSheet(FIELD_STYLE)
        self.barangay_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.barangay_placeholder.setObjectName("barangay_placeholder")

        # ── Row 2: City | Province ───────────────────────────────────────────
        self.city_label = QtWidgets.QLabel(parent=self.frame_2)
        self.city_label.setGeometry(QtCore.QRect(40, 120, 141, 16))
        self.city_label.setStyleSheet(LBL_STYLE)
        self.city_label.setObjectName("city_label")

        self.city_placeholder = QtWidgets.QLineEdit(parent=self.frame_2)
        self.city_placeholder.setGeometry(QtCore.QRect(40, 140, 151, 31))
        self.city_placeholder.setStyleSheet(FIELD_STYLE)
        self.city_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.city_placeholder.setObjectName("city_placeholder")

        self.province_label = QtWidgets.QLabel(parent=self.frame_2)
        self.province_label.setGeometry(QtCore.QRect(200, 120, 91, 16))
        self.province_label.setStyleSheet(LBL_STYLE)
        self.province_label.setObjectName("province_label")

        self.province_placeholder = QtWidgets.QLineEdit(parent=self.frame_2)
        self.province_placeholder.setGeometry(QtCore.QRect(200, 140, 151, 31))
        self.province_placeholder.setStyleSheet(FIELD_STYLE)
        self.province_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.province_placeholder.setObjectName("province_placeholder")

        # ── Emergency Contact heading ────────────────────────────────────────
        self.emergencyContact_label = QtWidgets.QLabel(parent=self.frame_2)
        self.emergencyContact_label.setGeometry(QtCore.QRect(80, 190, 241, 41))
        self.emergencyContact_label.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Expanding,
            )
        )
        self.emergencyContact_label.setStyleSheet('font: 16pt "Segoe UI";')
        self.emergencyContact_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.emergencyContact_label.setObjectName("emergencyContact_label")

        # ── Row 1: EC First Name | EC Last Name ──────────────────────────────
        self.EC_firstName_label_2 = QtWidgets.QLabel(parent=self.frame_2)
        self.EC_firstName_label_2.setGeometry(QtCore.QRect(40, 240, 91, 16))
        self.EC_firstName_label_2.setStyleSheet(LBL_STYLE)
        self.EC_firstName_label_2.setObjectName("EC_firstName_label_2")

        self.EC_firstName_placeholder_2 = QtWidgets.QLineEdit(parent=self.frame_2)
        self.EC_firstName_placeholder_2.setGeometry(QtCore.QRect(40, 260, 151, 31))
        self.EC_firstName_placeholder_2.setStyleSheet(FIELD_STYLE)
        self.EC_firstName_placeholder_2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.EC_firstName_placeholder_2.setObjectName("EC_firstName_placeholder_2")

        self.EC_lastName_label_2 = QtWidgets.QLabel(parent=self.frame_2)
        self.EC_lastName_label_2.setGeometry(QtCore.QRect(200, 240, 101, 16))
        self.EC_lastName_label_2.setStyleSheet(LBL_STYLE)
        self.EC_lastName_label_2.setObjectName("EC_lastName_label_2")

        self.EC_last_name_placeholder_2 = QtWidgets.QLineEdit(parent=self.frame_2)
        self.EC_last_name_placeholder_2.setGeometry(QtCore.QRect(200, 260, 151, 31))
        self.EC_last_name_placeholder_2.setStyleSheet(FIELD_STYLE)
        self.EC_last_name_placeholder_2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.EC_last_name_placeholder_2.setObjectName("EC_last_name_placeholder_2")

        # ── Row 2: EC Middle Name | Emergency # ──────────────────────────────
        self.EC_middleName_label_2 = QtWidgets.QLabel(parent=self.frame_2)
        self.EC_middleName_label_2.setGeometry(QtCore.QRect(40, 300, 141, 16))
        self.EC_middleName_label_2.setStyleSheet(LBL_STYLE)
        self.EC_middleName_label_2.setObjectName("EC_middleName_label_2")

        self.EC_middleName_placeholder_2 = QtWidgets.QLineEdit(parent=self.frame_2)
        self.EC_middleName_placeholder_2.setGeometry(QtCore.QRect(40, 320, 151, 31))
        self.EC_middleName_placeholder_2.setStyleSheet(FIELD_STYLE)
        self.EC_middleName_placeholder_2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.EC_middleName_placeholder_2.setObjectName("EC_middleName_placeholder_2")

        self.dateOfBirth_4 = QtWidgets.QLabel(parent=self.frame_2)
        self.dateOfBirth_4.setGeometry(QtCore.QRect(200, 300, 91, 16))
        self.dateOfBirth_4.setStyleSheet(LBL_STYLE)
        self.dateOfBirth_4.setObjectName("dateOfBirth_4")

        self.emergencyNum_placeholder_2 = QtWidgets.QLineEdit(parent=self.frame_2)
        self.emergencyNum_placeholder_2.setGeometry(QtCore.QRect(200, 320, 151, 31))
        self.emergencyNum_placeholder_2.setStyleSheet(FIELD_STYLE)
        self.emergencyNum_placeholder_2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.emergencyNum_placeholder_2.setObjectName("emergencyNum_placeholder_2")

        # ── Row 3: Relationship ──────────────────────────────────────────────
        self.relationship_label_2 = QtWidgets.QLabel(parent=self.frame_2)
        self.relationship_label_2.setGeometry(QtCore.QRect(40, 360, 91, 16))
        self.relationship_label_2.setStyleSheet(LBL_STYLE)
        self.relationship_label_2.setObjectName("relationship_label_2")

        self.relationship_placeholder_2 = QtWidgets.QLineEdit(parent=self.frame_2)
        self.relationship_placeholder_2.setGeometry(QtCore.QRect(40, 380, 151, 31))
        self.relationship_placeholder_2.setStyleSheet(FIELD_STYLE)
        self.relationship_placeholder_2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.relationship_placeholder_2.setObjectName("relationship_placeholder_2")

        # ── Buttons row ──────────────────────────────────────────────────────
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.frame_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(40, 450, 320, 28))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.back_btn_2 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.back_btn_2.setStyleSheet(BTN_STYLE)
        self.back_btn_2.setObjectName("back_btn_2")
        self.horizontalLayout_2.addWidget(self.back_btn_2)

        self.cancel_btn_2 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.cancel_btn_2.setStyleSheet(BTN_STYLE)
        self.cancel_btn_2.setObjectName("cancel_btn_2")
        self.horizontalLayout_2.addWidget(self.cancel_btn_2)

        self.save_btn_2 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.save_btn_2.setStyleSheet(BTN_STYLE)
        self.save_btn_2.setObjectName("save_btn_2")
        self.horizontalLayout_2.addWidget(self.save_btn_2)

        StackedWidget.addWidget(self.page_2)

        # ════════════════════════════════════════════════════════════════════
        # PAGE 3 — Emergency Contact (standalone / edit flow)
        # ════════════════════════════════════════════════════════════════════
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")

        self.frame_3 = QtWidgets.QFrame(parent=self.page_3)
        self.frame_3.setGeometry(QtCore.QRect(0, 0, 401, 331))
        self.frame_3.setStyleSheet("background-color: rgb(240, 230, 240);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")

        self.label_3 = QtWidgets.QLabel(parent=self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(80, 10, 241, 41))
        self.label_3.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Expanding,
            )
        )
        self.label_3.setStyleSheet('font: 16pt "Segoe UI";')
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")

        # ── Row 1: First Name | Last Name ────────────────────────────────────
        self.EC_firstName_label = QtWidgets.QLabel(parent=self.frame_3)
        self.EC_firstName_label.setGeometry(QtCore.QRect(40, 60, 91, 16))
        self.EC_firstName_label.setStyleSheet(LBL_STYLE)
        self.EC_firstName_label.setObjectName("EC_firstName_label")

        self.EC_firstName_placeholder = QtWidgets.QLineEdit(parent=self.frame_3)
        self.EC_firstName_placeholder.setGeometry(QtCore.QRect(40, 80, 151, 31))
        self.EC_firstName_placeholder.setStyleSheet(FIELD_STYLE)
        self.EC_firstName_placeholder.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.EC_firstName_placeholder.setObjectName("EC_firstName_placeholder")

        self.EC_lastName_label = QtWidgets.QLabel(parent=self.frame_3)
        self.EC_lastName_label.setGeometry(QtCore.QRect(200, 60, 101, 16))
        self.EC_lastName_label.setStyleSheet(LBL_STYLE)
        self.EC_lastName_label.setObjectName("EC_lastName_label")

        self.EC_last_name_placeholder = QtWidgets.QLineEdit(parent=self.frame_3)
        self.EC_last_name_placeholder.setGeometry(QtCore.QRect(200, 80, 151, 31))
        self.EC_last_name_placeholder.setStyleSheet(FIELD_STYLE)
        self.EC_last_name_placeholder.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.EC_last_name_placeholder.setObjectName("EC_last_name_placeholder")

        # ── Row 2: Middle Name | Emergency # ────────────────────────────────
        self.EC_middleName_label = QtWidgets.QLabel(parent=self.frame_3)
        self.EC_middleName_label.setGeometry(QtCore.QRect(40, 120, 141, 16))
        self.EC_middleName_label.setStyleSheet(LBL_STYLE)
        self.EC_middleName_label.setObjectName("EC_middleName_label")

        self.EC_middleName_placeholder = QtWidgets.QLineEdit(parent=self.frame_3)
        self.EC_middleName_placeholder.setGeometry(QtCore.QRect(40, 140, 151, 31))
        self.EC_middleName_placeholder.setStyleSheet(FIELD_STYLE)
        self.EC_middleName_placeholder.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.EC_middleName_placeholder.setObjectName("EC_middleName_placeholder")

        self.dateOfBirth_3 = QtWidgets.QLabel(parent=self.frame_3)
        self.dateOfBirth_3.setGeometry(QtCore.QRect(200, 110, 91, 31))
        self.dateOfBirth_3.setStyleSheet(LBL_STYLE)
        self.dateOfBirth_3.setObjectName("dateOfBirth_3")

        self.emergencyNum_placeholder = QtWidgets.QLineEdit(parent=self.frame_3)
        self.emergencyNum_placeholder.setGeometry(QtCore.QRect(200, 140, 151, 31))
        self.emergencyNum_placeholder.setStyleSheet(FIELD_STYLE)
        self.emergencyNum_placeholder.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.emergencyNum_placeholder.setObjectName("emergencyNum_placeholder")

        # ── Row 3: Relationship ──────────────────────────────────────────────
        self.relationship_label = QtWidgets.QLabel(parent=self.frame_3)
        self.relationship_label.setGeometry(QtCore.QRect(40, 180, 91, 16))
        self.relationship_label.setStyleSheet(LBL_STYLE)
        self.relationship_label.setObjectName("relationship_label")

        self.relationship_placeholder = QtWidgets.QLineEdit(parent=self.frame_3)
        self.relationship_placeholder.setGeometry(QtCore.QRect(40, 200, 151, 31))
        self.relationship_placeholder.setStyleSheet(FIELD_STYLE)
        self.relationship_placeholder.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.relationship_placeholder.setObjectName("relationship_placeholder")

        # ── Buttons row ──────────────────────────────────────────────────────
        self.layoutWidget_2 = QtWidgets.QWidget(parent=self.frame_3)
        self.layoutWidget_2.setGeometry(QtCore.QRect(40, 260, 320, 28))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.back_btn = QtWidgets.QPushButton(parent=self.layoutWidget_2)
        self.back_btn.setStyleSheet(BTN_STYLE)
        self.back_btn.setObjectName("back_btn")
        self.horizontalLayout_3.addWidget(self.back_btn)

        self.cancel_btn = QtWidgets.QPushButton(parent=self.layoutWidget_2)
        self.cancel_btn.setStyleSheet(BTN_STYLE)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_3.addWidget(self.cancel_btn)

        self.save_btn = QtWidgets.QPushButton(parent=self.layoutWidget_2)
        self.save_btn.setStyleSheet(BTN_STYLE)
        self.save_btn.setObjectName("save_btn")
        self.horizontalLayout_3.addWidget(self.save_btn)

        StackedWidget.addWidget(self.page_3)

        self.retranslateUi(StackedWidget)
        StackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(StackedWidget)

    # ── retranslateUi ────────────────────────────────────────────────────────
    def retranslateUi(self, StackedWidget):
        _t = QtCore.QCoreApplication.translate

        StackedWidget.setWindowTitle(_t("StackedWidget", "StackedWidget"))

        # PAGE 1 — Personal Information
        self.personalInformation_label.setText(
            _t("StackedWidget", "Personal Information")
        )
        self.firstName.setText(_t("StackedWidget", "First Name"))
        self.firstName_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., Maria")
        )
        self.lastName.setText(_t("StackedWidget", "Last Name"))
        self.lastName_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., Dela Cruz")
        )
        self.middleName.setText(_t("StackedWidget", "Middle Name (Optional)"))
        self.middleName_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., Santos")
        )
        self.suffix.setText(_t("StackedWidget", "Suffix (Optional)"))
        self.suffix_placeholder.setPlaceholderText(_t("StackedWidget", "e.g., Jr."))
        self.dateOfBirth.setText(_t("StackedWidget", "Date of Birth"))
        self.civilStatus.setText(_t("StackedWidget", "Civil Status"))
        self.contactNum.setText(_t("StackedWidget", "Contact Number"))
        self.contactNum_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., 09123456789")
        )
        self.occupation.setText(_t("StackedWidget", "Occupation (Optional)"))
        self.occupation_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., Housewife")
        )
        self.philHealth.setText(_t("StackedWidget", "PhilHealth #"))
        self.philHealth_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., 12-345678901-2")
        )
        self.nationality.setText(_t("StackedWidget", "Nationality"))
        self.nationality_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., Filipino")
        )
        self.Religion.setText(_t("StackedWidget", "Religion"))
        self.religion_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., Roman Catholic")
        )
        self.Religion_2.setText(_t("StackedWidget", "Blood Type"))

        self.pushButton.setText(_t("StackedWidget", "Cancel"))
        self.pushButton_2.setText(_t("StackedWidget", "Save"))
        self.pushButton_3.setText(_t("StackedWidget", "Next"))

        # PAGE 2 — Address + Emergency Contact
        self.address_label.setText(_t("StackedWidget", "Address"))
        self.street_label.setText(_t("StackedWidget", "Street / House No."))
        self.street_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., 123 Rizal St.")
        )
        self.barangay_label.setText(_t("StackedWidget", "Barangay"))
        self.barangay_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., Brgy. San Antonio")
        )
        self.city_label.setText(_t("StackedWidget", "City / Municipality"))
        self.city_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., Cebu City")
        )
        self.province_label.setText(_t("StackedWidget", "Province"))
        self.province_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., Cebu")
        )

        self.emergencyContact_label.setText(
            _t("StackedWidget", "Emergency Contact")
        )
        self.EC_firstName_label_2.setText(_t("StackedWidget", "First Name"))
        self.EC_firstName_placeholder_2.setPlaceholderText(
            _t("StackedWidget", "e.g., Juan")
        )
        self.EC_lastName_label_2.setText(_t("StackedWidget", "Last Name"))
        self.EC_last_name_placeholder_2.setPlaceholderText(
            _t("StackedWidget", "e.g., Dela Cruz")
        )
        self.EC_middleName_label_2.setText(
            _t("StackedWidget", "Middle Name (Optional)")
        )
        self.EC_middleName_placeholder_2.setPlaceholderText(
            _t("StackedWidget", "e.g., Reyes")
        )
        self.dateOfBirth_4.setText(_t("StackedWidget", "Emergency Number"))
        self.emergencyNum_placeholder_2.setPlaceholderText(
            _t("StackedWidget", "e.g., 09123456789")
        )
        self.relationship_label_2.setText(_t("StackedWidget", "Relationship"))
        self.relationship_placeholder_2.setPlaceholderText(
            _t("StackedWidget", "e.g., Husband")
        )

        self.back_btn_2.setText(_t("StackedWidget", "Back"))
        self.cancel_btn_2.setText(_t("StackedWidget", "Cancel"))
        self.save_btn_2.setText(_t("StackedWidget", "Save"))

        # PAGE 3 — Emergency Contact (standalone)
        self.label_3.setText(_t("StackedWidget", "Emergency Contact"))
        self.EC_firstName_label.setText(_t("StackedWidget", "First Name"))
        self.EC_firstName_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., Juan")
        )
        self.EC_lastName_label.setText(_t("StackedWidget", "Last Name"))
        self.EC_last_name_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., Dela Cruz")
        )
        self.EC_middleName_label.setText(
            _t("StackedWidget", "Middle Name (Optional)")
        )
        self.EC_middleName_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., Reyes")
        )
        self.dateOfBirth_3.setText(_t("StackedWidget", "Emergency Number"))
        self.emergencyNum_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., 09123456789")
        )
        self.relationship_label.setText(_t("StackedWidget", "Relationship"))
        self.relationship_placeholder.setPlaceholderText(
            _t("StackedWidget", "e.g., Husband")
        )

        self.back_btn.setText(_t("StackedWidget", "Back"))
        self.cancel_btn.setText(_t("StackedWidget", "Cancel"))
        self.save_btn.setText(_t("StackedWidget", "Save"))