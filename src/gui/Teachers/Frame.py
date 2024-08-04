from PySide6.QtWidgets import QFrame, QVBoxLayout, QTableView, QDockWidget, QTreeView
from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex, Slot

import data
from . import menu
from .SubjectsView import SubjectsView
from .TeachersView import TeachersView
from .Model import Model

import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__model = Model(parent=self)
        self.__model.reload()

        self.__menu = menu.Menu(parent=self)
        self.__layout = lay = QVBoxLayout(self)

        self.__load_teachers_action = self.__menu.addAction(self.tr('Load teachers...'))

        self.__teachers_view = tbl = TeachersView(parent=self)
        tbl.setModel(self.__model)
        lay.addWidget(tbl)

        dock = QDockWidget(self.tr('Subjects'), parent=self)
        self.__subjects_dock = dock
        self.__subjects_view = wid = SubjectsView(parent=dock)
        wid.setModel(self.__model)
        dock.setWidget(wid)

        self.__load_teachers_action.triggered.connect(self.__teachers_view.load_teachers)
        

    def __del__(self):
        self.__subjects_dock.deleteLater()

    @property
    def menus(self):
        return [self.__menu]

    @property
    def docks(self):
        return [
            ( self.__subjects_dock, Qt.RightDockWidgetArea )
        ]
