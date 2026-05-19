# calendar_dropdown.py
# Drop-in custom widget that looks and behaves like the screenshot:
# a rounded button showing the selected date + dropdown arrow,
# clicking it reveals a styled floating calendar popup.
#
# Usage in any dialog:
#   from calendar_dropdown import CalendarDropdown
#   self.dateOfBirth_placeholder = CalendarDropdown(parent=self.frame)
#   self.dateOfBirth_placeholder.setGeometry(QtCore.QRect(40, 210, 200, 36))
#   selected = self.dateOfBirth_placeholder.date()  # returns QDate

from PyQt6 import QtCore, QtGui, QtWidgets


class CalendarDropdown(QtWidgets.QWidget):
    """
    A styled date-picker button that opens a floating calendar on click.
    Matches the screenshot: white rounded field, displayed date + arrow,
    blue calendar header, today highlighted in blue.
    """

    dateChanged = QtCore.pyqtSignal(QtCore.QDate)

    def __init__(self, parent=None, max_date: QtCore.QDate = None):
        super().__init__(parent)
        self._date = QtCore.QDate.currentDate()
        self._max_date = max_date or QtCore.QDate.currentDate()
        self._popup: "_CalendarPopup | None" = None
        self._build()

    # ── public API ───────────────────────────────────────────────────────────
    def date(self) -> QtCore.QDate:
        return self._date

    def setDate(self, d: QtCore.QDate):
        if d.isValid():
            self._date = d
            self._refresh_label()

    def setMaximumDate(self, d: QtCore.QDate):
        self._max_date = d

    def setDisplayFormat(self, fmt: str):
        """Kept for API compatibility — we always display 'MMMM dd, yyyy'."""
        pass

    # ── internal ─────────────────────────────────────────────────────────────
    def _build(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 8, 0)
        layout.setSpacing(6)

        self._label = QtWidgets.QLabel()
        self._label.setStyleSheet(
            "color: rgb(26,26,62); font: 10pt 'Segoe UI';"
            "background: transparent; border: none;"
        )
        self._refresh_label()

        arrow = QtWidgets.QLabel("▾")
        arrow.setStyleSheet(
            "color: rgb(80,80,120); font-size: 14px;"
            "background: transparent; border: none;"
        )
        arrow.setFixedWidth(16)

        layout.addWidget(self._label, 1)
        layout.addWidget(arrow)

        self.setStyleSheet(
            "CalendarDropdown {"
            "  background-color: white;"
            "  border: 1.5px solid rgb(108,108,138);"
            "  border-radius: 10px;"
            "}"
            "CalendarDropdown:hover {"
            "  border-color: rgb(80,80,160);"
            "}"
        )
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(36)

    def _refresh_label(self):
        self._label.setText(self._date.toString("MMMM dd, yyyy"))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._open_popup()

    def _open_popup(self):
        if self._popup and self._popup.isVisible():
            self._popup.close()
            return

        self._popup = _CalendarPopup(self._date, self._max_date, parent=None)
        self._popup.dateSelected.connect(self._on_date_selected)

        # Position below this widget
        global_pos = self.mapToGlobal(QtCore.QPoint(0, self.height()))
        self._popup.move(global_pos)
        self._popup.show()
        self._popup.raise_()

    def _on_date_selected(self, d: QtCore.QDate):
        self._date = d
        self._refresh_label()
        self.dateChanged.emit(d)


# ─────────────────────────────────────────────────────────────────────────────
class _CalendarPopup(QtWidgets.QWidget):
    """Floating calendar panel that appears below the CalendarDropdown."""

    dateSelected = QtCore.pyqtSignal(QtCore.QDate)

    def __init__(self, current: QtCore.QDate, max_date: QtCore.QDate, parent=None):
        super().__init__(parent, QtCore.Qt.WindowType.Popup)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedWidth(370)
        self._max_date = max_date
        self._viewing = QtCore.QDate(current.year(), current.month(), 1)
        self._selected = current
        self._build()
        self._render()

    # ── layout ───────────────────────────────────────────────────────────────
    def _build(self):
        self.setStyleSheet(
            "background-color: white;"
            "border: 1px solid rgb(180,160,180);"
            "border-radius: 10px;"
        )
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 10)
        root.setSpacing(0)

        # ── Header (blue bar) ─────────────────────────────────────────────
        self._header = QtWidgets.QWidget()
        self._header.setFixedHeight(42)
        self._header.setStyleSheet("background-color: rgb(33,115,196); border-radius: 0px;")
        h_layout = QtWidgets.QHBoxLayout(self._header)
        h_layout.setContentsMargins(12, 0, 12, 0)

        self._prev_btn = self._nav_btn("◀")
        self._prev_btn.clicked.connect(self._prev_month)

        self._month_label = QtWidgets.QLabel()
        self._month_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._month_label.setStyleSheet(
            "color: white; font: bold 12pt 'Segoe UI';"
            "background: transparent; border: none;"
        )

        self._next_btn = self._nav_btn("▶")
        self._next_btn.clicked.connect(self._next_month)

        h_layout.addWidget(self._prev_btn)
        h_layout.addWidget(self._month_label, 1)
        h_layout.addWidget(self._next_btn)
        root.addWidget(self._header)

        # ── Day-of-week header row ────────────────────────────────────────
        dow_widget = QtWidgets.QWidget()
        dow_widget.setStyleSheet("background: white; border: none;")
        dow_layout = QtWidgets.QGridLayout(dow_widget)
        dow_layout.setContentsMargins(8, 6, 8, 2)
        dow_layout.setSpacing(0)
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for col, d in enumerate(days):
            lbl = QtWidgets.QLabel(d)
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            color = "rgb(200,50,50)" if col in (0, 6) else "rgb(80,80,120)"
            lbl.setStyleSheet(
                f"color: {color}; font: bold 9pt 'Segoe UI';"
                "background: transparent; border: none;"
            )
            dow_layout.addWidget(lbl, 0, col)
        root.addWidget(dow_widget)

        # ── Day grid ──────────────────────────────────────────────────────
        self._grid_widget = QtWidgets.QWidget()
        self._grid_widget.setStyleSheet("background: white; border: none;")
        self._grid = QtWidgets.QGridLayout(self._grid_widget)
        self._grid.setContentsMargins(8, 2, 8, 4)
        self._grid.setSpacing(2)
        root.addWidget(self._grid_widget)

        self._day_btns: list[QtWidgets.QPushButton] = []

    def _nav_btn(self, text: str) -> QtWidgets.QPushButton:
        btn = QtWidgets.QPushButton(text)
        btn.setFixedSize(28, 28)
        btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(
            "QPushButton { background: transparent; color: white;"
            "  border: none; font: bold 11pt 'Segoe UI'; border-radius: 14px; }"
            "QPushButton:hover { background: rgba(255,255,255,0.25); }"
        )
        return btn

    # ── render calendar grid ─────────────────────────────────────────────────
    def _render(self):
        # Clear old buttons
        for btn in self._day_btns:
            btn.deleteLater()
        self._day_btns.clear()

        y, m = self._viewing.year(), self._viewing.month()
        self._month_label.setText(
            QtCore.QDate(y, m, 1).toString("MMMM") + f"   {y}"
        )

        first_dow = QtCore.QDate(y, m, 1).dayOfWeek() % 7  # Sun=0..Sat=6
        days_in_month = self._viewing.daysInMonth()

        # Days from previous month
        prev_month = self._viewing.addMonths(-1)
        prev_days = prev_month.daysInMonth()

        cell = 0
        for col in range(first_dow):
            day_num = prev_days - first_dow + col + 1
            btn = self._make_day_btn(
                str(day_num),
                QtCore.QDate(prev_month.year(), prev_month.month(), day_num),
                faded=True,
            )
            self._grid.addWidget(btn, cell // 7, cell % 7)
            self._day_btns.append(btn)
            cell += 1

        # Days in current month
        for d in range(1, days_in_month + 1):
            date = QtCore.QDate(y, m, d)
            is_selected = date == self._selected
            is_today = date == QtCore.QDate.currentDate()
            is_disabled = date > self._max_date
            is_weekend = (cell % 7) in (0, 6)

            btn = self._make_day_btn(
                str(d), date,
                selected=is_selected,
                today=is_today,
                disabled=is_disabled,
                weekend=is_weekend,
            )
            self._grid.addWidget(btn, cell // 7, cell % 7)
            self._day_btns.append(btn)
            cell += 1

        # Fill remaining cells with next-month days
        next_month = self._viewing.addMonths(1)
        nd = 1
        while cell % 7 != 0:
            date = QtCore.QDate(next_month.year(), next_month.month(), nd)
            btn = self._make_day_btn(str(nd), date, faded=True)
            self._grid.addWidget(btn, cell // 7, cell % 7)
            self._day_btns.append(btn)
            cell += 1
            nd += 1

        # Resize popup to fit rows
        rows = cell // 7
        self.setFixedHeight(42 + 32 + rows * 36 + 16)

    def _make_day_btn(
        self, label: str, date: QtCore.QDate,
        faded=False, selected=False, today=False,
        disabled=False, weekend=False,
    ) -> QtWidgets.QPushButton:
        btn = QtWidgets.QPushButton(label)
        btn.setFixedSize(44, 32)
        btn.setCursor(
            QtCore.Qt.CursorShape.ArrowCursor if disabled
            else QtCore.Qt.CursorShape.PointingHandCursor
        )

        if selected:
            style = (
                "background-color: rgb(33,115,196); color: white;"
                "border-radius: 6px; font: bold 10pt 'Segoe UI'; border: none;"
            )
        elif today and not faded:
            style = (
                "background-color: rgb(210,230,255); color: rgb(33,115,196);"
                "border-radius: 6px; font: bold 10pt 'Segoe UI';"
                "border: 1.5px solid rgb(33,115,196);"
            )
        elif disabled:
            style = (
                "background: transparent; color: rgb(200,200,200);"
                "border: none; font: 10pt 'Segoe UI';"
            )
        elif faded:
            style = (
                "background: transparent; color: rgb(190,180,200);"
                "border: none; font: 10pt 'Segoe UI';"
            )
        elif weekend:
            style = (
                "background: transparent; color: rgb(200,50,50);"
                "border: none; font: 10pt 'Segoe UI';"
                "border-radius: 6px;"
            )
        else:
            style = (
                "background: transparent; color: rgb(40,40,80);"
                "border: none; font: 10pt 'Segoe UI';"
                "border-radius: 6px;"
            )

        hover_extra = (
            "" if disabled or selected else
            "QPushButton:hover { background-color: rgb(220,235,255);"
            "border-radius: 6px; }"
        )
        btn.setStyleSheet(f"QPushButton {{ {style} }} {hover_extra}")
        btn.setEnabled(not disabled)

        if not disabled:
            btn.clicked.connect(lambda _, d=date: self._pick(d))

        return btn

    def _pick(self, d: QtCore.QDate):
        self._selected = d
        self.dateSelected.emit(d)
        self.close()

    def _prev_month(self):
        self._viewing = self._viewing.addMonths(-1)
        self._render()

    def _next_month(self):
        nxt = self._viewing.addMonths(1)
        # Don't navigate past the max-date month
        if nxt <= QtCore.QDate(self._max_date.year(), self._max_date.month(), 1):
            self._viewing = nxt
            self._render()