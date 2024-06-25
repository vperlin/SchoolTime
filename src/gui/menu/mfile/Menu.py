from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Signal, Slot

from .QuitAction import QuitAction


class Menu(QMenu):
    
    quit = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setTitle( self.tr('File') )

        self.__quit_action = act = QuitAction(parent=self)
        act.triggered.connect(self.on_quit)
        self.addAction(act)

    @Slot()
    def on_quit(self):
        # Здесь могут быть дополнитеьные проверки
        self.quit.emit()
