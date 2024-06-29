from PySide6.QtWidgets import QFrame, QVBoxLayout, QTableView

from . import menu


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__menu = menu.Menu(parent=self)
        self.__layout = lay = QVBoxLayout(self)

        # Временно
        tbl = QTableView(parent=self)
        lay.addWidget(tbl)

    @property
    def menus(self):
        return [self.__menu]
