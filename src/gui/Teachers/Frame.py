from PySide6.QtWidgets import QFrame, QVBoxLayout, QFileDialog
from PySide6.QtCore import Slot

from . import menu
from .View import View
from .Model import Model


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__menu = mnu = menu.Menu(parent=self)
        self.__layout = lay = QVBoxLayout(self)

        self.__load_action = act = mnu.addAction(self.tr('Load...'))
        act.triggered.connect(self.load)

        # Временно
        tbl = View(parent=self)
        lay.addWidget(tbl)

        mdl = Model(parent=self)
        mdl.load()
        tbl.setModel(mdl)

    @property
    def menus(self):
        return [self.__menu]

    @Slot()
    def load(self):
        res = QFileDialog.getOpenFileName(self, self.tr('Open file'), '/', self.tr('CSV files (*.csv);;Excel files (*.xls *.xlsx);;All files (* *.*)'))
        print(res)
