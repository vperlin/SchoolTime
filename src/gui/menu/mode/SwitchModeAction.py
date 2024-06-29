from PySide6.QtGui import QAction
from PySide6.QtCore import Signal, Slot


class SwitchModeAction(QAction):

    def __init__(self, parent=None,
                 title=None,
                 enable: Signal=None,
                 disable: Signal=None):
        super().__init__(parent)

        self.setText(title)
        self.setCheckable(True)
        self.__enable = enable
        self.__disable = disable
        self.toggled.connect(self.on_toggle)

    @Slot()
    def on_toggle(self, value):
        if value:
            if self.__enable:
                self.__enable.emit()
        else:
            if self.__disable:
                self.__disable.emit()
