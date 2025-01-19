from PySide6.QtWidgets import QFrame, QVBoxLayout

from . import menu
from . import SClasses
from .SClassFrame import SClassFrame


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__menu = menu.Menu(parent=self)
        self.__layout = lay = QVBoxLayout(self)

        self.__sclasses = wid = SClasses.View(parent=self)
        lay.addWidget(wid)

        self.__sclass_frame = frm = SClassFrame(parent=self)
        # frm.setStyleSheet('background: yellow')
        lay.addWidget(frm)

        self.__sclasses.iid_sclass_selected.connect(self.__sclass_frame.setSClassId)
        self.__sclass_frame.setSClassId(self.__sclasses.currentData())

        self.__menu.addActions(self.actions_list)

    @property
    def actions_list(self):
        return self.__sclass_frame.actions_list

    @property
    def menus(self):
        return [self.__menu]
