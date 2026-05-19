# past_pregnancy_add_dialog_ui.py — fixed placeholders, calendar date input,
# corrected delivery_type to QComboBox

from PyQt6 import QtCore, QtGui, QtWidgets
from Dialog.calendar_dropdown import CalendarDropdown

FIELD_STYLE = (
    "border-radius: 12px;"
    "background-color: rgb(240, 230, 240);"
    "border: 1px solid rgb(26, 26, 62);"
)

COMBO_STYLE = (
    "border-radius: 12px;"
    "background-color: rgb(240, 230, 240);"
    "border: 1px solid rgb(26, 26, 62);"
    "padding: 4px 10px;"
)

BTN_STYLE = (
    "border-radius: 12px;"
    "padding: 4px;"
    "background-color: rgb(240, 230, 240);"
    "border: 1px solid rgb(26, 26, 62);"
)

LBL_STYLE = 'font: 10pt "Segoe UI";'


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(391, 390)

        self.frame_2 = QtWidgets.QFrame(parent=Dialog)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 401, 391))
        self.frame_2.setStyleSheet("background-color: rgb(240, 230, 240);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")

        # ── Heading ──────────────────────────────────────────────────────────
        self.address_label = QtWidgets.QLabel(parent=self.frame_2)
        self.address_label.setGeometry(QtCore.QRect(60, 10, 271, 41))
        self.address_label.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Expanding,
            )
        )
        self.address_label.setStyleSheet('font: 16pt "Segoe UI";')
        self.address_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.address_label.setObjectName("address_label")

        # ── Row 1: Delivery Date (calendar) | Delivery Type (combo) ─────────
        self.delivery_date_label = QtWidgets.QLabel(parent=self.frame_2)
        self.delivery_date_label.setGeometry(QtCore.QRect(39, 69, 91, 16))
        self.delivery_date_label.setStyleSheet(LBL_STYLE)
        self.delivery_date_label.setObjectName("delivery_date_label")

        # ── Calendar date picker for Delivery Date ───────────────────────────
        self.delivery_dat_placeholder = CalendarDropdown(parent=self.frame_2)
        self.delivery_dat_placeholder.setGeometry(QtCore.QRect(39, 89, 151, 36))
        self.delivery_dat_placeholder.setDate(QtCore.QDate.currentDate())
        self.delivery_dat_placeholder.setMaximumDate(QtCore.QDate.currentDate())
        self.delivery_dat_placeholder.setObjectName("delivery_dat_placeholder")

        self.delivery_type_label = QtWidgets.QLabel(parent=self.frame_2)
        self.delivery_type_label.setGeometry(QtCore.QRect(199, 69, 101, 16))
        self.delivery_type_label.setStyleSheet(LBL_STYLE)
        self.delivery_type_label.setObjectName("delivery_type_label")

        # ── Delivery Type now a proper combo ─────────────────────────────────
        self.delivery_date_placeholder = QtWidgets.QComboBox(parent=self.frame_2)
        self.delivery_date_placeholder.setGeometry(QtCore.QRect(199, 89, 151, 31))
        self.delivery_date_placeholder.setStyleSheet(COMBO_STYLE)
        self.delivery_date_placeholder.setObjectName("delivery_date_placeholder")
        for dtype in ["Normal / Vaginal", "Cesarean Section (CS)",
                      "Vacuum-Assisted", "Forceps-Assisted"]:
            self.delivery_date_placeholder.addItem(dtype)

        # ── Row 2: Presentation | Episiotomy ─────────────────────────────────
        self.presentation_label = QtWidgets.QLabel(parent=self.frame_2)
        self.presentation_label.setGeometry(QtCore.QRect(39, 129, 141, 16))
        self.presentation_label.setStyleSheet(LBL_STYLE)
        self.presentation_label.setObjectName("presentation_label")

        self.presentation_placeholder = QtWidgets.QLineEdit(parent=self.frame_2)
        self.presentation_placeholder.setGeometry(QtCore.QRect(39, 149, 151, 31))
        self.presentation_placeholder.setStyleSheet(FIELD_STYLE)
        self.presentation_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.presentation_placeholder.setObjectName("presentation_placeholder")

        self.episiotomy_label = QtWidgets.QLabel(parent=self.frame_2)
        self.episiotomy_label.setGeometry(QtCore.QRect(199, 129, 91, 16))
        self.episiotomy_label.setStyleSheet(LBL_STYLE)
        self.episiotomy_label.setObjectName("episiotomy_label")

        self.Episiotomy_placeholder = QtWidgets.QComboBox(parent=self.frame_2)
        self.Episiotomy_placeholder.setGeometry(QtCore.QRect(200, 149, 151, 31))
        self.Episiotomy_placeholder.setStyleSheet(COMBO_STYLE)
        self.Episiotomy_placeholder.setObjectName("Episiotomy_placeholder")
        self.Episiotomy_placeholder.addItem("Yes")
        self.Episiotomy_placeholder.addItem("No")

        # ── Row 3: Complication | Baby Weight ────────────────────────────────
        self.complication_label = QtWidgets.QLabel(parent=self.frame_2)
        self.complication_label.setGeometry(QtCore.QRect(39, 189, 91, 16))
        self.complication_label.setStyleSheet(LBL_STYLE)
        self.complication_label.setObjectName("complication_label")

        self.complication_placeholder = QtWidgets.QLineEdit(parent=self.frame_2)
        self.complication_placeholder.setGeometry(QtCore.QRect(39, 209, 151, 31))
        self.complication_placeholder.setStyleSheet(FIELD_STYLE)
        self.complication_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.complication_placeholder.setObjectName("complication_placeholder")

        self.baby_weight_label = QtWidgets.QLabel(parent=self.frame_2)
        self.baby_weight_label.setGeometry(QtCore.QRect(199, 189, 91, 16))
        self.baby_weight_label.setStyleSheet(LBL_STYLE)
        self.baby_weight_label.setObjectName("baby_weight_label")

        self.baby_weight_placeholder = QtWidgets.QLineEdit(parent=self.frame_2)
        self.baby_weight_placeholder.setGeometry(QtCore.QRect(199, 209, 151, 31))
        self.baby_weight_placeholder.setStyleSheet(FIELD_STYLE)
        self.baby_weight_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.baby_weight_placeholder.setObjectName("baby_weight_placeholder")

        # ── Row 4: Outcome ────────────────────────────────────────────────────
        self.outcome_label = QtWidgets.QLabel(parent=self.frame_2)
        self.outcome_label.setGeometry(QtCore.QRect(39, 249, 91, 16))
        self.outcome_label.setStyleSheet(LBL_STYLE)
        self.outcome_label.setObjectName("outcome_label")

        self.comboBox = QtWidgets.QComboBox(parent=self.frame_2)
        self.comboBox.setGeometry(QtCore.QRect(39, 269, 151, 31))
        self.comboBox.setStyleSheet(COMBO_STYLE)
        self.comboBox.setObjectName("comboBox")
        for outcome in ["Full Term", "Preterm", "Miscarriage", "Abortion"]:
            self.comboBox.addItem(outcome)

        # ── Buttons ───────────────────────────────────────────────────────────
        self.cancel_btn_2 = QtWidgets.QPushButton(parent=self.frame_2)
        self.cancel_btn_2.setGeometry(QtCore.QRect(100, 340, 92, 26))
        self.cancel_btn_2.setStyleSheet(BTN_STYLE)
        self.cancel_btn_2.setObjectName("cancel_btn_2")

        self.save_btn_2 = QtWidgets.QPushButton(parent=self.frame_2)
        self.save_btn_2.setGeometry(QtCore.QRect(198, 340, 91, 26))
        self.save_btn_2.setStyleSheet(BTN_STYLE)
        self.save_btn_2.setObjectName("save_btn_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _t = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_t("Dialog", "Dialog"))

        self.address_label.setText(_t("Dialog", "Add Past Pregnancy"))
        self.delivery_date_label.setText(_t("Dialog", "Delivery Date"))
        self.delivery_type_label.setText(_t("Dialog", "Delivery Type"))
        self.presentation_label.setText(_t("Dialog", "Presentation"))
        self.presentation_placeholder.setPlaceholderText(
            _t("Dialog", "e.g., Cephalic")
        )
        self.episiotomy_label.setText(_t("Dialog", "Episiotomy"))
        self.complication_label.setText(_t("Dialog", "Complication"))
        self.complication_placeholder.setPlaceholderText(
            _t("Dialog", "e.g., Perineal tear, None")
        )
        self.baby_weight_label.setText(_t("Dialog", "Baby Weight (kg)"))
        self.baby_weight_placeholder.setPlaceholderText(
            _t("Dialog", "e.g., 3.2")
        )
        self.outcome_label.setText(_t("Dialog", "Outcome"))
        self.cancel_btn_2.setText(_t("Dialog", "Cancel"))
        self.save_btn_2.setText(_t("Dialog", "Save"))