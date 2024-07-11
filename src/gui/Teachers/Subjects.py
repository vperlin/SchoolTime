from PySide6.QtWidgets import QFrame, QTableView, QVBoxLayout
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, Slot
import data


class Model(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__content = []

    def rowCount(self, idx_parent=QModelIndex()):
        return 0 if idx_parent.isValid() else len(self.__content)

    def columnCount(self, idx_parent=QModelIndex()):
        return 0 if idx_parent.isValid() else 4

    def data(self, idx, role=Qt.DisplayRole):
        match role:
            case Qt.DisplayRole:
                dt = self.__content[idx.row()]
                match idx.column():
                    case 0:
                        return dt.iid
                    case 1:
                        return dt.code
                    case 2:
                        return dt.title
                    case 3:
                        return dt.note
                    case _:
                        return None
            case _:
                return None

    @Slot()
    def reload(self):
        with data.connect(data.Subject) as cursor:
            cursor.execute('''
                select iid, code, title, note
                    from subjects ;
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

        self.__layout = lay = QVBoxLayout(self)

        # Временно
        tbl = View(parent=self)
        lay.addWidget(tbl)
