# ── HOW TO ADD THE PROFILE BUTTON TO ANY SCREEN ─────────────────────────────
#
# 1. In that screen's __init__, after setupUi, call:
#       self._setup_profile_button()
#
# 2. Paste the two methods below into the screen class.
#
# Requires: import session
#           from user_profile.user_profile_dialog import UserProfileDialog
#           from PyQt6.QtWidgets import QDialog, QPushButton
# ─────────────────────────────────────────────────────────────────────────────

import session
from PyQt6.QtWidgets import QPushButton, QDialog
from user_profile_dialog import UserProfileDialog


def _setup_profile_button(self):
    """Call this in __init__ after setupUi."""
    user = session.get()
    display_name = user["name"] if user else "Profile"

    # ✅ Add profile button to the right side of the top bar (frame_2)
    self.profile_btn = QPushButton(f"👤  {display_name}", parent=self.ui.frame_2)
    self.profile_btn.setStyleSheet(
        "QPushButton {"
        "    background-color: transparent;"
        "    color: white;"
        "    font-size: 13px;"
        "    border: 1px solid rgba(255,255,255,0.4);"
        "    border-radius: 8px;"
        "    padding: 4px 14px;"
        "}"
        "QPushButton:hover { background-color: rgba(255,255,255,0.15); }"
    )
    self.profile_btn.setCursor(self.profile_btn.cursor())
    self.profile_btn.adjustSize()

    # Position it on the right end of the top bar
    self.profile_btn.clicked.connect(self._open_profile)
    self.profile_btn.show()
    self._reposition_profile_btn()


def _reposition_profile_btn(self):
    """Call this in resizeEvent too so it stays right-aligned."""
    if hasattr(self, "profile_btn"):
        bar_h  = self.ui.frame_2.height()
        btn_w  = self.profile_btn.width() or 160
        btn_h  = 30
        bar_w  = self.ui.frame_2.width()
        self.profile_btn.setGeometry(
            bar_w - btn_w - 16,
            (bar_h - btn_h) // 2,
            btn_w,
            btn_h,
        )


def _open_profile(self):
    dlg = UserProfileDialog(parent=self)
    if dlg.exec() == QDialog.DialogCode.Accepted:
        # Refresh button label if name changed
        user = session.get()
        if user and hasattr(self, "profile_btn"):
            self.profile_btn.setText(f"👤  {user['name']}")
            self.profile_btn.adjustSize()
            self._reposition_profile_btn()


# ── USAGE EXAMPLE in any screen ───────────────────────────────────────────────
#
# class DashboardScreen(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_DashboardScreen()
#         self.ui.setupUi(self)
#         ...
#         self._setup_profile_button()   # ← add this
#
#     def resizeEvent(self, event):
#         super().resizeEvent(event)
#         self._reposition_profile_btn() # ← add this
#         ...
#
# Then bind the methods:
#     _setup_profile_button  = _setup_profile_button
#     _reposition_profile_btn = _reposition_profile_btn
#     _open_profile           = _open_profile