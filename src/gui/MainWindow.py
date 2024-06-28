from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

from . import menu
from . import Teachers

import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__main_menu = mm = menu.MainMenu(parent=self)
        mm.quit.connect(self.close)
        mm.teachers_mode_on.connect(self.on_teachers_mode_enabled)
        mm.students_mode_on.connect(self.on_students_mode_enabled)
        mm.teachers_mode_off.connect(self.on_mode_disabled)
        mm.students_mode_off.connect(self.on_mode_disabled)
        self.setMenuBar(mm)

        self.__current_mode = None

    @Slot()
    def on_teachers_mode_enabled(self):
        self.__current_mode = frm = Teachers.Frame(parent=self)
        self.__main_menu.add_menu(frm.menu)
        self.setCentralWidget(frm)
        LOG.debug('Teachers mode enabled')

    @Slot()
    def on_students_mode_enabled(self):
        LOG.debug('Students mode enabled')

    @Slot()
    def on_mode_disabled(self):
        if self.__current_mode:
            self.__current_mode.deleteLater()
            self.__current_mode = None
        LOG.debug('Mode disabled')
