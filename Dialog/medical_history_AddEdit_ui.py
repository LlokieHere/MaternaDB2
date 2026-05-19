# medical_history_addEdit_dialog_ui.py — fixed placeholders and calendar date input

from PyQt6 import QtCore, QtGui, QtWidgets
from Dialog.calendar_dropdown import CalendarDropdown


class Ui_MedicalHistoryDialog(object):
    def setupUi(self, MedicalHistoryDialog):
        MedicalHistoryDialog.setObjectName("MedicalHistoryDialog")
        MedicalHistoryDialog.resize(600, 650)
        MedicalHistoryDialog.setStyleSheet(
            "background-color: rgb(240, 230, 240);"
        )

        self.verticalLayout = QtWidgets.QVBoxLayout(MedicalHistoryDialog)
        self.verticalLayout.setObjectName("verticalLayout")

        # ── Title ─────────────────────────────────────────────────────────────
        self.title_label = QtWidgets.QLabel(parent=MedicalHistoryDialog)
        self.title_label.setStyleSheet(
            "font-family: 'Arial Black'; font-size: 20px;"
            "color: rgb(26, 26, 62); padding: 10px;"
        )
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label)

        # ── Form frame ────────────────────────────────────────────────────────
        self.form_frame = QtWidgets.QFrame(parent=MedicalHistoryDialog)
        self.form_frame.setStyleSheet(
            "background-color: rgb(236, 198, 220);"
            "border-radius: 15px;"
            "border: 1px solid rgb(158, 136, 163);"
        )
        self.form_frame.setObjectName("form_frame")

        self.gridLayout = QtWidgets.QGridLayout(self.form_frame)
        self.gridLayout.setObjectName("gridLayout")

        _lbl_style = (
            "font-weight: bold; color: rgb(26, 26, 62); border: none;"
        )
        _field_style = (
            "background-color: white; border-radius: 8px;"
            "padding: 5px; border: 1px solid rgb(158, 136, 163);"
        )

        # ── Row 0: Medical Condition ──────────────────────────────────────────
        self.condition_label = QtWidgets.QLabel(parent=self.form_frame)
        self.condition_label.setStyleSheet(_lbl_style)
        self.condition_label.setObjectName("condition_label")
        self.gridLayout.addWidget(self.condition_label, 0, 0, 1, 1)

        self.condition_combo = QtWidgets.QComboBox(parent=self.form_frame)
        self.condition_combo.setStyleSheet(_field_style)
        self.condition_combo.setEditable(True)
        self.condition_combo.setObjectName("condition_combo")
        self.condition_combo.lineEdit().setPlaceholderText(
            "Select or type a condition"
        )
        for cond in [
            "Gestational Diabetes",
            "Anemia",
            "Urinary Tract Infection (UTI)",
            "Hypothyroidism",
            "Hypertension",
            "Preeclampsia",
        ]:
            self.condition_combo.addItem(cond)
        self.gridLayout.addWidget(self.condition_combo, 0, 1, 1, 1)

        # ── Row 1: Diagnosed Date (calendar) ─────────────────────────────────
        self.diagnosed_label = QtWidgets.QLabel(parent=self.form_frame)
        self.diagnosed_label.setStyleSheet(_lbl_style)
        self.diagnosed_label.setObjectName("diagnosed_label")
        self.gridLayout.addWidget(self.diagnosed_label, 1, 0, 1, 1)

        self.diagnosed_date = CalendarDropdown(parent=self.form_frame)
        self.diagnosed_date.setDate(QtCore.QDate.currentDate())
        self.diagnosed_date.setMaximumDate(QtCore.QDate.currentDate())
        self.diagnosed_date.setObjectName("diagnosed_date")
        self.gridLayout.addWidget(self.diagnosed_date, 1, 1, 1, 1)

        # ── Row 2: Status ─────────────────────────────────────────────────────
        self.status_label = QtWidgets.QLabel(parent=self.form_frame)
        self.status_label.setStyleSheet(_lbl_style)
        self.status_label.setObjectName("status_label")
        self.gridLayout.addWidget(self.status_label, 2, 0, 1, 1)

        self.status_combo = QtWidgets.QComboBox(parent=self.form_frame)
        self.status_combo.setStyleSheet(_field_style)
        self.status_combo.setObjectName("status_combo")
        for s in ["Ongoing", "Resolved", "In Remission", "Chronic"]:
            self.status_combo.addItem(s)
        self.gridLayout.addWidget(self.status_combo, 2, 1, 1, 1)

        # ── Row 3: Clinical Notes ─────────────────────────────────────────────
        self.notes_label = QtWidgets.QLabel(parent=self.form_frame)
        self.notes_label.setStyleSheet(_lbl_style)
        self.notes_label.setObjectName("notes_label")
        self.gridLayout.addWidget(self.notes_label, 3, 0, 1, 1)

        self.notes_text = QtWidgets.QTextEdit(parent=self.form_frame)
        self.notes_text.setStyleSheet(_field_style)
        self.notes_text.setPlaceholderText(
            "e.g., Patient was diagnosed during the second trimester. "
            "Currently on medication and responding well."
        )
        self.notes_text.setObjectName("notes_text")
        self.gridLayout.addWidget(self.notes_text, 3, 1, 1, 1)

        self.verticalLayout.addWidget(self.form_frame)

        # ── Button frame ──────────────────────────────────────────────────────
        self.button_frame = QtWidgets.QFrame(parent=MedicalHistoryDialog)
        self.button_frame.setStyleSheet("background-color: transparent;")
        self.button_frame.setObjectName("button_frame")

        self.button_layout = QtWidgets.QHBoxLayout(self.button_frame)
        self.button_layout.setObjectName("button_layout")

        self.save_btn = QtWidgets.QPushButton(parent=self.button_frame)
        self.save_btn.setStyleSheet(
            "QPushButton {"
            "  background-color: rgb(192, 116, 182);"
            "  color: white; border-radius: 12px;"
            "  padding: 10px 20px; font-weight: bold; font-size: 14px;"
            "}"
            "QPushButton:hover {"
            "  background-color: rgb(170, 90, 160);"
            "}"
        )
        self.save_btn.setObjectName("save_btn")
        self.button_layout.addWidget(self.save_btn)

        self.cancel_btn = QtWidgets.QPushButton(parent=self.button_frame)
        self.cancel_btn.setStyleSheet(
            "QPushButton {"
            "  background-color: rgb(100, 100, 100);"
            "  color: white; border-radius: 12px;"
            "  padding: 10px 20px; font-weight: bold; font-size: 14px;"
            "}"
            "QPushButton:hover {"
            "  background-color: rgb(80, 80, 80);"
            "}"
        )
        self.cancel_btn.setObjectName("cancel_btn")
        self.button_layout.addWidget(self.cancel_btn)

        self.verticalLayout.addWidget(self.button_frame)

        self.retranslateUi(MedicalHistoryDialog)
        QtCore.QMetaObject.connectSlotsByName(MedicalHistoryDialog)

    def retranslateUi(self, MedicalHistoryDialog):
        _t = QtCore.QCoreApplication.translate
        MedicalHistoryDialog.setWindowTitle(
            _t("MedicalHistoryDialog", "Add / Edit Medical Condition")
        )
        self.title_label.setText(
            _t("MedicalHistoryDialog", "Medical Condition Details")
        )
        self.condition_label.setText(
            _t("MedicalHistoryDialog", "Medical Condition: *")
        )
        self.diagnosed_label.setText(
            _t("MedicalHistoryDialog", "Diagnosed Date: *")
        )
        self.status_label.setText(_t("MedicalHistoryDialog", "Status: *"))
        self.notes_label.setText(_t("MedicalHistoryDialog", "Clinical Notes:"))
        self.save_btn.setText(_t("MedicalHistoryDialog", "Save"))
        self.cancel_btn.setText(_t("MedicalHistoryDialog", "Cancel"))