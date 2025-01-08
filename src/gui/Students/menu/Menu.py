from PySide6.QtWidgets import QMenu


class Menu(QMenu):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle(self.tr('Students'))

        self.__act_add_subgroup = self.addAction(self.tr('Add subgroup'))
        self.__act_rename_subgroup = self.addAction(self.tr('Rename subgroup'))
        self.__act_attach_subject = self.addAction(self.tr('Attach subject'))
        self.__act_detach_subject = self.addAction(self.tr('Detach subject'))
