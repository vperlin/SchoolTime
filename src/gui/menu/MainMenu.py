from PySide6.QtWidgets import QMenuBar


class MainMenu(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Временно
        self.__file_menu = self.addMenu('File')
        self.__mode_menu = self.addMenu('Mode')
        self.__help_menu = self.addMenu('Help')
