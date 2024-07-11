from PySide6.QtWidgets import QMenu


class ToolsMenu(QMenu):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle(self.tr('Tools'))
        self.__docks = self.addMenu(self.tr('Dock windows'))
        self.__tools = self.addMenu(self.tr('Toolbars'))

    def add_dock(self, dock_action):
        self.__docks.addAction(dock_action)

    def add_tool(self, tool_action):
        self.__tools.addAction(tool_action)
