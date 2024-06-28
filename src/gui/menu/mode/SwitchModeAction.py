from PySide6.QtGui import QAction
from PySide6.QtCore import Slot

import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.WARNING)


class SwitchModeAction(QAction):

    def __init__(self, parent=None, title='Mode', on=None, off=None):
        self.__on = on
        self.__off = off
        super().__init__(parent)

        self.setText(title)
        self.setCheckable(True)

        LOG.debug('SwitchModeAction')
        self.toggled.connect(self.on_toggle)

    @Slot()
    def on_toggle(self, state):
        LOG.debug(f'{self.text()}->{state}')
        if state:
            if self.__on:
                self.__on.emit()
        else:
            if self.__off:
                self.__off.emit()
