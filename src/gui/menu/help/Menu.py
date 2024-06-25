from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Signal, Slot

from .AboutQtAction import AboutQtAction


class Menu(QMenu):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setTitle( self.tr('Help') )
        
        self.__about_qt_action = act = AboutQtAction(parent=self)
        self.addAction(act)