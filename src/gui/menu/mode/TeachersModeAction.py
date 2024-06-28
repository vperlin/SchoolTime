from PySide6.QtGui import QAction
from PySide6.QtCore import Slot


class SwitchModeAction(QAction):

    def __init__(self, parent=None, title='Mode', on=None, off=None):
        self.__on = on
        self.__off = off
        super().__init__(parent)

        self.setText(title)
        self.setCheckable(True)

    @Slot()
    def on_toggle(self, state):
        if state:
            if self.__on:
                self.__on.emit()
        else:
            if self.__off:
                self.__off.emit()