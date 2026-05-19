from PyQt6.QtWidgets import QLabel, QMainWindow, QMessageBox
from screens.patient_profile_ui import Ui_MainWindow
from Dialog.add_patient_dialog import EditPatientDialog
from PyQt6.QtWidgets import QDialog
from database import get_connection
from PyQt6.QtCore import Qt
import user_profile.session as session


class PatientProfileScreen(QMainWindow):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.patient_id = patient_id

        self.setWindowTitle("Patient Profile")

        # Inner Navigation
        self.ui.pushButton_7.clicked.connect(self.go_to_pastPregnancy)
        self.ui.pushButton_8.clicked.connect(self.go_to_prescription)
        self.ui.pushButton_9.clicked.connect(self.go_to_medicalHistory)
        self.ui.pushButton_10.clicked.connect(self.go_to_family_planning)
        self.ui.pushButton_11.clicked.connect(self.go_to_appointment)

        self.setup_navigation()
        self.load_patient_data()
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

        if hasattr(self, "profile_avatar"):
            self._reposition_sidebar_profile()
        
        self.layout_sidebar()
        self.layout_nav()

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

    # =====================================================
    # 🔁 NAVIGATION
    # =====================================================
    def setup_navigation(self):
        self.ui.pushButton.clicked.connect(self.got_to_dashboard)
        self.ui.pushButton_2.clicked.connect(self.go_to_patient_records)
        self.ui.pushButton_3.clicked.connect(self.go_to_prenatal_care)
        self.ui.pushButton_4.clicked.connect(self.go_to_appointments)
        self.ui.pushButton_5.clicked.connect(self.logout)

        self.ui.remove_patient_btn.clicked.connect(self.open_edit_dialog)

    # =====================================================
    # 📥 LOAD DATA
    # =====================================================
    def load_patient_data(self):
        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "DB Error", "Cannot connect to database")
            return

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT patient_id,
                    first_name,
                    middle_name,
                    last_name,
                    date_registered,
                    blood_type,
                    date_of_birth,
                    philhealth_no,
                    civil_status,
                    religion,
                    nationality,
                    occupation,
                    contact_number,
                    street,
                    barangay,
                    city,
                    province,
                    emergency_first_name,
                    emergency_middle_name,
                    emergency_last_name,
                    emergency_contact_number,
                    emergency_relationship
                FROM patient_profile
                WHERE patient_id = %s
            """, (self.patient_id,))

            data = cursor.fetchone()
            cursor.close()
            conn.close()

            if not data:
                QMessageBox.warning(self, "Not Found", "Patient not found")
                return

            full_name = " ".join(filter(None, [data[1], data[2], data[3]]))
            register = data[4].strftime("%B %d, %Y") if data[4] else ""
            bod = data[6].strftime("%B %d, %Y") if data[6] else ""

            self.ui.placeholder_p_bloodType.setText(data[5] or "")
            self.ui.patient_name.setText(full_name)
            self.ui.placeholder_p_ID.setText(str(data[0]))
            self.ui.placeholder_register_date_2.setText(register)
            self.ui.placeholder_philhealth_num.setText(str(data[7] or ""))

            conn2 = get_connection()
            cursor2 = conn2.cursor()
            cursor2.execute("""
                SELECT EXTRACT(YEAR FROM AGE(date_of_birth)) AS age
                FROM patient_profile
                WHERE patient_id = %s
            """, (self.patient_id,))
            result = cursor2.fetchone()
            cursor2.close()
            conn2.close()

            self.ui.age_placeholder.setText(str(int(result[0])) if result else "N/A")

            self.ui.first_name_placeholder.setText(data[1] or "")
            self.ui.middle_name_placeholder.setText(data[2] or "")
            self.ui.last_name_placeholder.setText(data[3] or "")
            self.ui.bday_placeholder.setText(bod)
            self.ui.civil_status_placeholder.setText(data[8] or "")
            self.ui.religion_placeholder.setText(data[9] or "")
            self.ui.nationality_placeholder.setText(data[10] or "")
            self.ui.occupation_placeholder.setText(data[11] or "")
            self.ui.contact_number_placeholder.setText(data[12] or "")

            self.ui.street_placeholder.setText(data[13] or "")
            self.ui.barangay_placeholder.setText(data[14] or "")
            self.ui.cit_placeholder.setText(data[15] or "")
            self.ui.province_placeholder.setText(data[16] or "")

            self.ui.EC_first_name_placeholder.setText(data[17] or "")
            self.ui.EC_middle_name_placeholder.setText(data[18] or "")
            self.ui.EC_last_name_placeholder.setText(data[19] or "")
            self.ui.EC_contact_placeholder.setText(data[20] or "")
            self.ui.EC_relationship_placeholder.setText(data[21] or "")

            self._build_patient_avatar(full_name)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load profile:\n{e}")

    
    def open_edit_dialog(self):
        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT first_name, middle_name, last_name, suffix,
                    date_of_birth, civil_status, contact_number,
                    philhealth_no, occupation, religion,
                    nationality, blood_type,
                    street, barangay, city, province,
                    emergency_first_name, emergency_last_name,
                    emergency_middle_name, emergency_contact_number,
                    emergency_relationship
                FROM patient_profile
                WHERE patient_id = %s
            """, (self.patient_id,))

            profile = cursor.fetchone()
            cursor.close()
            conn.close()

            if not profile:
                return

            patient_data = {
                # profile
                "first_name":      profile[0],
                "middle_name":     profile[1],
                "last_name":       profile[2],
                "suffix":          profile[3],
                "date_of_birth":   profile[4],
                "civil_status":    profile[5],
                "contact_number":  profile[6],
                "philhealth_no":   profile[7],
                "occupation":      profile[8],
                "religion":        profile[9],
                "nationality":     profile[10],
                "blood_type":      profile[11],
                # address
                "street":          profile[12],
                "barangay":        profile[13],
                "city":            profile[14],
                "province":        profile[15],
                # emergency
                "ec_first_name":   profile[16],
                "ec_last_name":    profile[17],
                "ec_middle_name":  profile[18],
                "ec_contact":      profile[19],
                "ec_relationship": profile[20],
            }

            self.dialog = EditPatientDialog(
                mode="edit",
                patient_data=patient_data,
                patient_id=self.patient_id,
                parent=self
            )

            if self.dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_patient_data()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load patient data:\n{e}")
    #navigation

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

    def go_to_patient_records(self):
        from screens.patient_records_screen import PatientRecordScreen
        self.window = PatientRecordScreen()
        self.window.showMaximized()
        self.close()

    def go_to_prenatal_care(self):
        from screens.prenatal_dashboard_screen import PrenatalDashboardScreen
        self.window = PrenatalDashboardScreen()
        self.window.showMaximized()
        self.close()

    def got_to_dashboard(self):
        from screens.dashboard_screen import DashboardScreen
        self.window = DashboardScreen()
        self.window.showMaximized()
        self.close()

    def go_to_appointments(self):
        from screens.appointments_screen import AppointmentsScreen
        self.new_window = AppointmentsScreen()
        self.new_window.showMaximized()
        self.close()

    #inner

    def logout(self):
        from screens.login_screen import LoginScreen
        self.window = LoginScreen()
        self.window.showMaximized()
        self.close()

    def go_to_pastPregnancy(self):
        from screens.past_pregnancy_screen import pastPregnancyScreen
        self.new_window = pastPregnancyScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_medicalHistory(self):
        from screens.medical_history_screen import MedicalHistoryScreen
        self.new_window = MedicalHistoryScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

    def go_to_prescription(self):
        from screens.prescription_screen import PrescriptionScreen  # ✅ add "screens."
        self.new_window = PrescriptionScreen(self.patient_id)
        self.new_window.showMaximized()
        self.close()

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