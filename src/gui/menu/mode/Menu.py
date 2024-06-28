from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QActionGroup
from PySide6.QtCore import Signal

from .TeachersModeAction import SwitchModeAction


class Menu(QMenu):

    teachers_mode_on = Signal()
    teachers_mode_off = Signal()
    students_mode_on = Signal()
    students_mode_off = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle('Mode')

        grp = QActionGroup(self)
        grp.setExclusive(True)

        self.__teachers_mode_action = act = SwitchModeAction(
            self,
            self.tr('Teachers'),
            self.teachers_mode_on,
            self.teachers_mode_off)
        self.addAction(act)
        grp.addAction(act)

        self.__students_mode_action = act = SwitchModeAction(
            self,
            self.tr('Students'),
            self.students_mode_on,
            self.students_mode_off)
        self.addAction(act)
        grp.addAction(act)
