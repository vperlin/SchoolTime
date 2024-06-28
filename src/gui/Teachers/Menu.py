from PySide6.QtWidgets import QMenu


class Menu(QMenu):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle(self.tr('Teachers'))
