from PyQt6.QtWidgets import QMainWindow, QMessageBox
from screens.dashboard_ui import Ui_DashboardScreen

class dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DashboardScreen()
        self.ui.setupUi(self)
        self.setWindowTitle("MaternaDB - Dashboard")

