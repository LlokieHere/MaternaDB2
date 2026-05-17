from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QLabel, QMainWindow, QTableWidgetItem, QMessageBox
from screens.patient_records_ui import Ui_PatientRecord
from Dialog.add_patient_dialog import EditPatientDialog
from PyQt6.QtWidgets import QDialog
from database import get_connection
from PyQt6.QtCore import Qt
import user_profile.session as session


class PatientRecordScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dialog = None
        self.ui = Ui_PatientRecord()
        self.ui.setupUi(self)

        self.ui.patient_table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.ui.patient_table.horizontalHeader().setStretchLastSection(True)

        self.setWindowTitle("MaternaDB - Patient Records")

        # connections
        self.ui.add_patient_btn.clicked.connect(self.open_add_patient_dialog)
        self.ui.remove_patient_btn.clicked.connect(self.remove_patient)
        self.ui.lineEdit.textChanged.connect(self.search_patient)

        self.setup_navigation()  # ← add this
        self.load_patients()
        self.reposition_ui()
        self.load_logo()

        self._build_sidebar_profile()
    
    # -------------------------
    # SIDEBAR PROFILE
    # -------------------------
    def _build_sidebar_profile(self):
        user = session.get()
        name = user["name"] if user else "User"
        role = user.get("role", "Admin") if user else "Admin"

        # Avatar — clicking opens the profile dialog
        self.profile_avatar = QLabel("👤", parent=self.ui.frame)
        self.profile_avatar.setFixedSize(64, 64)
        self.profile_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_avatar.setStyleSheet(
            "background-color: #ECC6DC; border-radius: 32px;"
            "font-size: 28px; border: none;"
        )
        self.profile_avatar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.profile_avatar.mousePressEvent = lambda _: self._open_profile_dialog()

        self.profile_name_lbl = QLabel(name, parent=self.ui.frame)
        self.profile_name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_name_lbl.setWordWrap(True)
        self.profile_name_lbl.setCursor(Qt.CursorShape.PointingHandCursor)
        self.profile_name_lbl.mousePressEvent = lambda _: self._open_profile_dialog()
        self.profile_name_lbl.setStyleSheet(
            "color: white; font-size: 13px; font-weight: bold;"
            "background: transparent; border: none;"
        )

        self.profile_role_lbl = QLabel(role, parent=self.ui.frame)
        self.profile_role_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_role_lbl.setStyleSheet(
            "color: rgba(255,255,255,0.65); font-size: 11px;"
            "background: transparent; border: none;"
        )

        self.profile_divider = QLabel(parent=self.ui.frame)
        self.profile_divider.setFixedHeight(1)
        self.profile_divider.setStyleSheet(
            "background-color: rgba(255,255,255,0.2); border: none;"
        )

        for w in (self.profile_avatar, self.profile_name_lbl,
                  self.profile_role_lbl, self.profile_divider):
            w.show()

    def _reposition_sidebar_profile(self):
        sidebar_w = self.ui.frame.width()
        pad     = 16
        av_size = 64

        av_x = (sidebar_w - av_size) // 2
        av_y = 20
        self.profile_avatar.setGeometry(av_x, av_y, av_size, av_size)

        name_y = av_y + av_size + 8
        self.profile_name_lbl.setGeometry(pad, name_y, sidebar_w - pad * 2, 36)

        role_y = name_y + 38
        self.profile_role_lbl.setGeometry(pad, role_y, sidebar_w - pad * 2, 18)

        div_y = role_y + 26
        self.profile_divider.setGeometry(pad, div_y, sidebar_w - pad * 2, 1)

    def _open_profile_dialog(self):
        from user_profile.user_profile_dialog import UserProfileDialog  # ✅ correct path
        dlg = UserProfileDialog(parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            # Refresh sidebar labels if name/role changed
            user = session.get()
            if user:
                self.profile_name_lbl.setText(user.get("name", ""))
                self.profile_role_lbl.setText(user.get("role", ""))

    
    def load_logo(self):
        from PyQt6.QtGui import QPixmap
        from PyQt6.QtCore import Qt
        pixmap = QPixmap("Asset/MaternaDB_logo.png")
        if not pixmap.isNull():
            self.ui.label_3.setPixmap(
                pixmap.scaled(
                    40, 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
            self.ui.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.reposition_ui()
        self._reposition_sidebar_profile()

    def reposition_ui(self):
        w = self.width()
        h = self.height()

        # LEFT SIDEBAR
        self.ui.frame.setGeometry(0, 60, 231, h - 60)

        # TOP BAR
        self.ui.frame_2.setGeometry(0, 0, w, 60)

        # MAIN AREA
        main_x = 231
        main_w = w - 231
        main_h = h - 60

        self.ui.frame_3.setGeometry(main_x, 60, main_w, main_h)

        # TITLE
        self.ui.label.setGeometry(40, 20, 500, 60)

        # SEARCH BAR
        self.ui.lineEdit.setGeometry(40, 90, int(main_w * 0.3), 40)

        # BUTTONS
        self.ui.add_patient_btn.setGeometry(main_w - 280, 90, 120, 35)
        self.ui.remove_patient_btn.setGeometry(main_w - 150, 90, 120, 35)

        # TABLE
        table_x = 40
        table_y = 140
        table_w = main_w - 80
        table_h = main_h - 180

        self.ui.patient_table.setGeometry(table_x, table_y, table_w, table_h)

    def fix_table_alignment(self):
        for row in range(self.ui.patient_table.rowCount()):
            for col in range(self.ui.patient_table.columnCount()):
                item = self.ui.patient_table.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    # =====================================================
    # 🔁 REUSABLE TABLE POPULATION
    # =====================================================
    def populate_table(self, rows):
        self.ui.patient_table.setRowCount(0)

        for row_index, row_data in enumerate(rows):
            self.ui.patient_table.insertRow(row_index)

            # Fill columns 0–3
            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value) if value else "")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.patient_table.setItem(row_index, col_index, item)

            # VIEW BUTTON (column 4)
            btn = QtWidgets.QPushButton("View")
            btn.setStyleSheet("""
                background-color: rgb(236, 198, 220);
                border-radius: 8px;
                margin: 2px;
            """)

            patient_id = row_data[0]
            btn.clicked.connect(
                lambda _, pid=patient_id: self.view_patient_by_id(pid)
            )

            self.ui.patient_table.setCellWidget(row_index, 4, btn)

        self.fix_table_alignment()

    # =====================================================
    # 📥 LOAD PATIENTS
    # =====================================================
    def load_patients(self):
        conn = get_connection()

        self.ui.patient_table.setColumnCount(5)
        self.ui.patient_table.setHorizontalHeaderLabels([
            "ID", "NAME", "DATE OF BIRTH", "CONTACT", "ACTION"
        ])

        if not conn:
            QMessageBox.critical(self, "DB Error", "Cannot connect to database")
            return

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT patient_id,
                       CONCAT(first_name, ' ', COALESCE(middle_name || ' ', ''), last_name),
                       date_of_birth,
                       contact_number
                FROM patient_profile
                ORDER BY patient_id ASC
            """)

            rows = cursor.fetchall()
            conn.close()

            self.populate_table(rows)

        except Exception as e:
            QMessageBox.critical(self, "Query Error", str(e))

    # =====================================================
    # 👁 VIEW PATIENT
    # =====================================================
    def view_patient_by_id(self, patient_id):
        from screens.patient_profile_screen import PatientProfileScreen

        self.profile_window = PatientProfileScreen(patient_id, parent=self)
        self.profile_window.show()

        # Optional: hide current screen
        self.hide()
    # =====================================================
    # ➕ ADD PATIENT
    # =====================================================
    def open_add_patient_dialog(self):
        self.dialog = EditPatientDialog(mode="add", parent=self)

        if self.dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_patients()  # refresh your table after adding

    # =====================================================
    # ❌ REMOVE PATIENT
    # =====================================================
    def remove_patient(self):
        row = self.ui.patient_table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Warning", "Select a patient first")
            return

        patient_id = self.ui.patient_table.item(row, 0).text()

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM patient_profile WHERE patient_id = %s",
                (patient_id,)
            )

            conn.commit()
            conn.close()

            self.load_patients()

        except Exception as e:
            QMessageBox.critical(self, "Delete Error", str(e))

    # =====================================================
    # 🔎 SEARCH PATIENT
    # =====================================================
    def search_patient(self, text):
        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT patient_id,
                       CONCAT(first_name, ' ', COALESCE(middle_name || ' ', ''), last_name),
                       date_of_birth,
                       contact_number
                FROM patient_profile
                WHERE LOWER(first_name) LIKE LOWER(%s)
                   OR LOWER(last_name) LIKE LOWER(%s)
                   OR CAST(patient_id AS TEXT) LIKE %s
                ORDER BY patient_id
            """, (f"%{text}%", f"%{text}%", f"%{text}%"))

            rows = cursor.fetchall()
            conn.close()

            self.populate_table(rows)

        except Exception as e:
            print("Search error:", e)

    def setup_navigation(self):
        self.ui.pushButton.clicked.connect(self.go_to_dashboard)
        self.ui.pushButton_2.clicked.connect(self.go_to_patient_records)
        self.ui.pushButton_3.clicked.connect(self.go_to_prenatal_care)
        self.ui.pushButton_4.clicked.connect(self.go_to_appointments)
        self.ui.pushButton_5.clicked.connect(self.logout)

    def go_to_dashboard(self):
        from screens.dashboard_screen import DashboardScreen
        self.new_window = DashboardScreen()
        self.new_window.showMaximized()
        self.close()

    def go_to_patient_records(self):
        pass  # already here

    def go_to_prenatal_care(self):
        from screens.prenatal_dashboard_screen import PrenatalDashboardScreen
        self.new_window = PrenatalDashboardScreen()
        self.new_window.showMaximized()
        self.close()

    def go_to_appointments(self):
        from screens.appointments_screen import AppointmentsScreen
        self.new_window = AppointmentsScreen()
        self.new_window.showMaximized()
        self.close()

    def logout(self):
        from screens.login_screen import LoginScreen
        self.new_window = LoginScreen()
        self.new_window.showMaximized()
        self.close()