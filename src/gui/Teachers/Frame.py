from PySide6.QtWidgets import QFrame, QVBoxLayout, QTableView, QDockWidget
from PySide6.QtCore import Qt

from . import menu
from . import Subjects


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__menu = menu.Menu(parent=self)
        self.__layout = lay = QVBoxLayout(self)

        # Временно
        tbl = QTableView(parent=self)
        lay.addWidget(tbl)

        self.__subjects_dock = dock = QDockWidget(self.tr('Subjects'), parent=self)
        self.__subjects_frame = frm = Subjects.Frame(parent=dock)
        dock.setWidget(frm)

    @property
    def menus(self):
        return [self.__menu]

    @property
    def docks(self):
        return [
            ( self.__subjects_dock, Qt.RightDockWidgetArea )
        ]
