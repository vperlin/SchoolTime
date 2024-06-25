from PySide6.QtWidgets import QMenuBar
from PySide6.QtCore import Signal

from . import mfile
from . import mode
from . import help


class MainMenu(QMenuBar):
    
    quit = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.__file_menu = mnu = mfile.Menu(parent=self)
        mnu.quit.connect( self.quit )
        self.addMenu(mnu)
        
        self.__mode_menu = mnu = mode.Menu(parent=self)
        self.addMenu(mnu)

        
        self.__help_menu = mnu = help.Menu(parent=self)
        self.addMenu(mnu)
