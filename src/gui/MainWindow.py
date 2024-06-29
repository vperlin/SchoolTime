from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

from . import menu

import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__main_menu = mm = menu.MainMenu(parent=self)
        mm.teachers_mode_on.connect(self.teachers_mode_on)
        mm.students_mode_on.connect(self.students_mode_on)
        mm.teachers_mode_off.connect(self.mode_off)
        mm.students_mode_off.connect(self.mode_off)
        mm.quit.connect(self.close)
        self.setMenuBar(mm)

    @Slot()
    def teachers_mode_on(self):
        LOG.debug('teachers_mode_on')

    @Slot()
    def students_mode_on(self):
        LOG.debug('teachers_mode_on')

    @Slot()
    def mode_off(self):
        LOG.debug('mode_off')
