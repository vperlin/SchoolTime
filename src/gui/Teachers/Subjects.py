from PySide6.QtWidgets import QFrame, QTableView, QVBoxLayout
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, Slot
import data


class Model(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)

    def rowCount(self, idx_parent=QModelIndex()):
        # @TODO С потолка
        return 0 if idx_parent.isValid() else 10

    def columnCount(self, idx_parent=QModelIndex()):
        return 0 if idx_parent.isValid() else 4

    def data(self, idx, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return '???'
        else:
            return None

    @Slot()
    def reload(self):
        with data.connect(data.Subject) as cursor:
            cursor.execute('''
                select iid, code, title, note
                    from subjects ;
            ''')
            for dt in cursor:
                print(dt, type(dt))


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
