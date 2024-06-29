from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Signal
from PySide6.QtGui import QActionGroup

from .SwitchModeAction import SwitchModeAction


class Menu(QMenu):

    teachers_mode_on = Signal()
    teachers_mode_off = Signal()
    students_mode_on = Signal()
    students_mode_off = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle('Mode')

        self.__mode_action_group = grp = QActionGroup(self)
        grp.setExclusive(True)

        self.__teachers_mode_action = act = SwitchModeAction(
            parent=self,
            title=self.tr('Teachers'),
            enable=self.teachers_mode_on,
            disable=self.teachers_mode_off)
        self.addAction(act)
        grp.addAction(act)

        self.__students_mode_action = act = SwitchModeAction(
            parent=self,
            title=self.tr('Students'),
            enable=self.students_mode_on,
            disable=self.students_mode_off)
        self.addAction(act)
        grp.addAction(act)
