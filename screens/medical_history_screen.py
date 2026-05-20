from PyQt6.QtWidgets import (
    QLabel, QMainWindow, QMessageBox, QTableWidgetItem, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
from screens.medical_history_ui import Ui_MainWindow
from database import get_connection
import user_profile.session as session


class MedicalHistoryScreen(QMainWindow):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.patient_id = patient_id
        self.setWindowTitle("Medical History")

        self.setup_navigation()
        self.load_patient_data()
        self.load_medical_history()

        self.ui.add_condition_btn.clicked.connect(self.open_add_dialog)
        self.load_logo()
        self._build_sidebar_profile()


    def load_logo(self):
        from PyQt6.QtGui import QPixmap
        from PyQt6.QtCore import Qt
        pixmap = QPixmap("Asset/MaternaDB_logo.png")
        if not pixmap.isNull():
            self.ui.label_3.setText("")
            self.ui.label_3.setStyleSheet("")  # ✅ clear the stylesheet
            self.ui.label_3.setPixmap(
                pixmap.scaled(
                    40, 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
            self.ui.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
            """
            color: white;
            font-size: 11px;
            border: none;
            """
        )

        self.profile_divider = QLabel(parent=self.ui.frame)
        self.profile_divider.setFixedHeight(1)
        self.profile_divider.setStyleSheet(
            "background-color: rgba(255,255,255,0.2); border: none;"
        )

        for w in (
            self.profile_avatar,
            self.profile_name_lbl,
            self.profile_role_lbl,
            self.profile_divider
        ):
            w.raise_()
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

        role_y = name_y + 24
        self.profile_role_lbl.setGeometry(pad, role_y, sidebar_w - pad * 2, 18)

        div_y = role_y + 18
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

    # =====================================================
    # 📏 AUTO REPOSITION SIDEBAR PROFILE ON RESIZE
    # =====================================================

    def layout_sidebar(self):
        h = self.height()

        sidebar_w = 230

        # Profile section
        self.profile_avatar.setGeometry(73, 20, 64, 64)

        self.profile_name_lbl.setGeometry(20, 95, 190, 30)

        self.profile_role_lbl.setGeometry(20, 120, 190, 20)

        self.profile_divider.setGeometry(15, 150, 200, 1)

        # Navigation buttons
        btn_top = 170
        btn_h = 41
        btn_gap = 8
        btn_x = 10
        btn_w = sidebar_w - 20

        buttons = [
            self.ui.pushButton,
            self.ui.pushButton_2,
            self.ui.pushButton_3,
            self.ui.pushButton_4,
        ]

        for i, btn in enumerate(buttons):
            btn.setGeometry(
                btn_x,
                btn_top + i * (btn_h + btn_gap),
                btn_w,
                btn_h
            )

        # Logout button
        self.ui.pushButton_5.setGeometry(
            btn_x,
            h - 120,
            btn_w,
            btn_h
        )

    def layout_nav(self):
        w = self.width()
        h = self.height()

        sidebar_w = 230
        navbar_h = 60
        padding = 30

        # Top navbar
        self.ui.frame_2.setGeometry(0, 0, w, navbar_h)

        # Sidebar
        self.ui.frame.setGeometry(0, navbar_h, sidebar_w, h - navbar_h)

        # Main content
        self.ui.frame_3.setGeometry(
            sidebar_w,
            navbar_h,
            w - sidebar_w,
            h - navbar_h
        )

        # Sidebar buttons
        btn_x = 20
        btn_w = 191
        btn_h = 41
        gap = 10

        start_y = 180

        buttons = [
            self.ui.pushButton,
            self.ui.pushButton_2,
            self.ui.pushButton_3,
            self.ui.pushButton_4,
        ]

        for i, btn in enumerate(buttons):
            btn.setGeometry(
                btn_x,
                start_y + i * (btn_h + gap),
                btn_w,
                btn_h
            )

        # Logout button pinned near bottom
        self.ui.pushButton_5.setGeometry(
            btn_x,
            h - navbar_h - 70,
            btn_w,
            btn_h
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.width()
        h = self.height()

        self.ui.frame_2.setGeometry(0, 0, w, 61)

        sidebar_w = int(w * 0.19)
        self.ui.frame.setGeometry(0, 61, sidebar_w, h - 61)
        btn_x, btn_w = 20, sidebar_w - 30
        self.ui.pushButton.setGeometry(btn_x, 180, btn_w, 41)
        self.ui.pushButton_2.setGeometry(btn_x, 230, btn_w, 41)
        self.ui.pushButton_3.setGeometry(btn_x, 280, btn_w, 41)
        self.ui.pushButton_4.setGeometry(btn_x, 330, btn_w, 41)
        self.ui.pushButton_5.setGeometry(btn_x, h - 200, btn_w, 41)

        content_x = sidebar_w
        content_w = w - sidebar_w
        content_h = h - 61
        self.ui.frame_3.setGeometry(content_x, 61, content_w, content_h)

        pad = 40
        inner_w = content_w - (pad * 2)

        self.ui.label.setGeometry(pad, 20, inner_w // 2, 61)

        header_h = 141
        self.ui.frame_4.setGeometry(pad, 80, inner_w, header_h)
        self.ui.frame_5.setGeometry(20, 20, 111, 91)
        self.ui.patient_name.setGeometry(170, 15, inner_w - 320, 30)
        self.ui.layoutWidget.setGeometry(170, 55, inner_w - 320, 75)

        tab_y = 80 + header_h + 20
        self.ui.layoutWidget1.setGeometry(pad, tab_y, inner_w, 40)

        btn_y = tab_y + 50
        self.ui.add_condition_btn.setGeometry(pad, btn_y, 130, 31)

        table_y = btn_y + 41
        table_h = content_h - table_y - pad
        self.ui.left.setGeometry(pad, table_y, inner_w, table_h)
        self.ui.medical_history_table.setGeometry(0, 0, inner_w, table_h)
        self.ui.medical_history_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        
        self._reposition_sidebar_profile()
        self.layout_sidebar()
        self.layout_nav()

    def setup_navigation(self):
        try:
            self.ui.pushButton.clicked.connect(self.go_to_dashboard)
            self.ui.pushButton_2.clicked.connect(self.go_to_patient_records)
            self.ui.pushButton_3.clicked.connect(self.go_to_prenatal_care)
            self.ui.pushButton_4.clicked.connect(self.go_to_appointments)
            self.ui.pushButton_5.clicked.connect(self.logout)
            self.ui.pushButton_6.clicked.connect(self.go_to_patient_profile)
            self.ui.pushButton_7.clicked.connect(self.go_to_past_pregnancy)
            self.ui.pushButton_8.clicked.connect(self.go_to_prescription)
            self.ui.pushButton_9.clicked.connect(self.go_to_medical_history)
            self.ui.pushButton_10.clicked.connect(self.go_to_family_planning)
            self.ui.pushButton_11.clicked.connect(self.go_to_appointment)
        except Exception as e:
            print("Navigation error:", e)

    def load_patient_data(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT patient_id, first_name, middle_name, last_name,
                       date_registered, blood_type, philhealth_no
                FROM patient_profile WHERE patient_id = %s
            """, (self.patient_id,))
            data = cursor.fetchone()
            cursor.close()
            conn.close()

            if not data:
                return

            full_name = " ".join(filter(None, [data[1], data[2], data[3]]))
            register  = data[4].strftime("%B %d, %Y") if data[4] else ""

            self.ui.patient_name.setText(full_name)
            self.ui.placeholder_p_ID.setText(str(data[0]))
            self.ui.placeholder_register_date.setText(register)
            self.ui.placeholder_p_bloodType.setText(data[5] or "")
            self.ui.placeholder_philhealth_num.setText(str(data[6]))
            self._build_patient_avatar(full_name)
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load patient:\n{e}")

    def _build_patient_avatar(self, full_name: str):
        from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont

        # Generate initials
        parts    = full_name.strip().split()
        initials = ""
        if len(parts) == 1:
            initials = parts[0][0].upper()
        elif len(parts) >= 2:
            initials = parts[0][0].upper() + parts[-1][0].upper()

        # Create avatar label inside frame_5
        avatar = QLabel(initials, parent=self.ui.frame_5)
        avatar.setGeometry(0, 0, self.ui.frame_5.width(), self.ui.frame_5.height())
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            "background-color: rgb(192, 116, 182);"
            "color: white;"
            "font-size: 32px;"
            "font-weight: bold;"
            "border-radius: 6px;"
            "border: none;"
        )
        avatar.show()
    def load_medical_history(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT condition, diagnosis_date, status, remarks
                FROM medical_history
                WHERE patient_id = %s
                ORDER BY diagnosis_date DESC
            """, (self.patient_id,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            tbl = self.ui.medical_history_table
            tbl.setRowCount(0)
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            tbl.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

            for row_data in rows:
                condition      = row_data[0] or ""
                diagnosis_date = row_data[1].strftime("%B %d, %Y") if row_data[1] else ""
                status         = row_data[2] or ""
                remarks        = row_data[3] or ""

                row_index = tbl.rowCount()
                tbl.insertRow(row_index)

                for col, val in enumerate([condition, diagnosis_date, status, remarks]):
                    item = QTableWidgetItem(val)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    tbl.setItem(row_index, col, item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load medical history:\n{e}")

    def open_add_dialog(self):
        from Dialog.add_medical_history_dialog import AddMedicalHistoryDialog
        dialog = AddMedicalHistoryDialog(self.patient_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_medical_history()

    # ── Outer navigation ──────────────────────────────────────
    def go_to_dashboard(self):
        from screens.dashboard_screen import DashboardScreen
        self.new_window = DashboardScreen()
        self.new_window.showMaximized()
        self.close()

    def go_to_patient_records(self):
        from screens.patient_records_screen import PatientRecordScreen
        self.new_window = PatientRecordScreen()
        self.new_window.showMaximized()
        self.close()

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

    # ── Inner navigation ──────────────────────────────────────
    def go_to_patient_profile(self):
        from screens.patient_profile_screen import PatientProfileScreen
        self.new_window = PatientProfileScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_past_pregnancy(self):
        from screens.past_pregnancy_screen import pastPregnancyScreen
        self.new_window = pastPregnancyScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_prescription(self):
        from screens.prescription_screen import PrescriptionScreen
        self.new_window = PrescriptionScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_medical_history(self):
        pass

    def go_to_family_planning(self):
        from screens.family_planning_screen import FamilyPlanningScreen
        self.new_window = FamilyPlanningScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_appointment(self):
        from screens.appointment_patient_record_screen import PatientAppointmentScreen
        self.new_window = PatientAppointmentScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()