from PySide6.QtWidgets import QFrame, QVBoxLayout, QTableView, QDockWidget
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Slot

import data
from . import menu
from . import Subjects


class Model(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__content = []

    def rowCount(self, idx_parent=QModelIndex()):
        return 0 if idx_parent.isValid() else len(self.__content)

    def columnCount(self, idx_parent=QModelIndex()):
        return 0 if idx_parent.isValid() else 8

    def data(self, idx, role=Qt.DisplayRole):
        match role:
            case Qt.DisplayRole:
                dt = self.__content[idx.row()]
                match idx.column():
                    case 0:
                        return dt.iid
                    case 1:
                        return dt.last_name
                    case 2:
                        return dt.first_name
                    case 3:
                        return dt.middle_name
                    case 4:
                        return dt.phone
                    case 5:
                        return 'subjects'
                    case 6:
                        return 'класс'
                    case 7:
                        return dt.note
                    case _:
                        return None
            case _:
                return None

    @Slot()
    def reload(self):
        with data.connect(data.Teacher) as cursor:
            cursor.execute('''
                select iid, last_name, first_name, middle_name, phone, note
                    from teachers ;
            ''')
            self.beginResetModel()
            try:
                self.__content = list(cursor)
            finally:
                self.endResetModel()


class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__model = mdl = Model(parent=self)
        self.setModel(mdl)
        mdl.reload()


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__menu = menu.Menu(parent=self)
        self.__layout = lay = QVBoxLayout(self)

        tbl = View(parent=self)
        lay.addWidget(tbl)

        dock = QDockWidget(self.tr('Subjects'), parent=self)
        self.__subjects_dock = dock
        self.__subjects_frame = frm = Subjects.Frame(parent=dock)
        dock.setWidget(frm)

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
