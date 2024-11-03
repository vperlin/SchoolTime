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

        # Временно
        self.__sclass_frame = frm = SClassFrame(parent=self)
        lay.addWidget(frm)

        self.__sclasses.iid_sclass_selected.connect(self.__sclass_frame.setSClassId)
        self.__sclass_frame.setSClassId(self.__sclasses.currentData())

    @property
    def menus(self):
        return [self.__menu]
