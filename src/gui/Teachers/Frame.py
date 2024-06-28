from PySide6.QtWidgets import QFrame

from .Menu import Menu


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__menu = Menu(parent=self)

    @property
    def menu(self):
        return self.__menu
