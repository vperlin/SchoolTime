from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

from . import menu
from . import Teachers
from . import Students

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

        self.__current_mode = None

    @Slot()
    def teachers_mode_on(self):
        self.__current_mode = cur = Teachers.Frame(parent=self)
        self.setCentralWidget(cur)
        self.__main_menu.add_menus(cur.menus)
        LOG.debug('Teacher mode enabled')

    @Slot()
    def students_mode_on(self):
        self.__current_mode = cur = Students.Frame(parent=self)
        self.setCentralWidget(cur)
        self.__main_menu.add_menus(cur.menus)
        LOG.debug('Students mode enabled')

    @Slot()
    def mode_off(self):
        if self.__current_mode:
            self.__current_mode.deleteLater()
            self.__current_mode = None
        LOG.debug('Current mode disabled')
