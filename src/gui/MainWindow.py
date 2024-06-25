from PySide6.QtWidgets import QMainWindow

from . import menu

class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__main_menu = mm = menu.MainMenu(parent=self)
        self.setMenuBar(mm)
