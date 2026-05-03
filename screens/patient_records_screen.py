from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from screens.patient_records_ui import Ui_PatientRecord
from database import get_connection
from PyQt6.QtCore import Qt


class PatientRecordScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PatientRecord()
        self.ui.setupUi(self)

        self.ui.patient_table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.ui.patient_table.horizontalHeader().setStretchLastSection(True)

        self.setWindowTitle("MaternaDB - Patient Records")

        # connections
        self.ui.add_patient_btn.clicked.connect(self.add_patient)
        self.ui.remove_patient_btn.clicked.connect(self.remove_patient)
        self.ui.lineEdit.textChanged.connect(self.search_patient)

        self.load_patients()
        self.reposition_ui()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.reposition_ui()

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
                padding: 4px;
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
    def add_patient(self):
        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO patient_profile 
                (first_name, middle_name, last_name, date_of_birth, contact_number)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                "Juan",
                "D",
                "Cruz",
                "2000-01-01",
                "09123456789"
            ))

            conn.commit()
            conn.close()

            self.load_patients()

        except Exception as e:
            QMessageBox.critical(self, "Insert Error", str(e))

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