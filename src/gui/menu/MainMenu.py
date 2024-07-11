from PySide6.QtWidgets import QMenuBar
from PySide6.QtCore import Signal

from . import mfile
from . import mode
from . import help
from .ToolsMenu import ToolsMenu


class MainMenu(QMenuBar):

    teachers_mode_on = Signal()
    teachers_mode_off = Signal()
    students_mode_on = Signal()
    students_mode_off = Signal()
    quit = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__file_menu = mnu = mfile.Menu(parent=self)
        mnu.quit.connect( self.quit )
        self.addMenu(mnu)

        self.__zone0 = self.addSeparator()

        self.__dock_tools = mnu = ToolsMenu(parent=self)
        self.addMenu(mnu)

        self.__mode_menu = mnu = mode.Menu(parent=self)
        mnu.teachers_mode_on.connect(self.teachers_mode_on)
        mnu.teachers_mode_off.connect(self.teachers_mode_off)
        mnu.students_mode_on.connect(self.students_mode_on)
        mnu.students_mode_off.connect(self.students_mode_off)
        self.addMenu(mnu)

        self.__help_menu = mnu = help.Menu(parent=self)
        self.addMenu(mnu)

    def add_menus(self, menus):
        for m in menus:
            self.insertMenu(self.__zone0, m)

    def add_dock(self, dock_action):
        self.__dock_tools.add_dock(dock_action)

    def add_tool(self, tool_action):
        self.__dock_tools.add_tool(tool_action)
