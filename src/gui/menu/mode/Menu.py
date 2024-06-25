from PySide6.QtWidgets import QMenu

from .TeachersModeAction import TeachersModeAction
from .StudentsModeAction import StudentsModeAction

class Menu(QMenu):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setTitle('Mode')

        self.__teachers_mode_action = act = TeachersModeAction(parent=self)
        self.addAction(act)
        
        self.__students_mode_action = act = StudentsModeAction(parent=self)
        self.addAction(act)
