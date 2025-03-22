from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

import data
import helpers

import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


SUBJECTS_SELECT_SQL = '''
    select iid, code, title, note
        from subjects
        order by title, code ;
'''


class Model(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__subjects = []

    @property
    def selected_iids(self):
        return [ s.iid for s in self.__subjects if s.is_selected ]

    def rowCount(self, idx_parent=QModelIndex()):
        return len(self.__subjects)

    def columnCount(self, idx_parent=QModelIndex()):
        return 3

    def data(self, idx, role):
        sbj = self.__subjects[idx.row()]
        if role == Qt.DisplayRole:
            match idx.column():
                case 0: return sbj.code
                case 1: return sbj.title
                case 2: return '*' if sbj.note else None
        elif role == Qt.CheckStateRole:
            if idx.column() == 0:
                return Qt.Checked if sbj.is_selected else Qt.Unchecked
            else:
                return None
        elif role == Qt.UserRole+1:
            return sbj.iid
        else:
            return None

    @helpers.resetting_model
    def setData(self, idx, value, role):
        if role != Qt.CheckStateRole or idx.column() != 0:
            return super().setData(idx, value, role)
        sbj = self.__subjects[idx.row()]
        sbj.is_selected = (value == Qt.Checked.value)
        return True

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return super().headerData(section, orientation, role)
        if orientation == Qt.Horizontal:
            match section:
                case 0: return self.tr('Code')
                case 1: return self.tr('Title')
                case 2: return ''
                case _: None
        return super().headerData(section, orientation, role)

    @helpers.resetting_model
    def reload(self):
        self.__subjects = []
        with data.connect() as cursor:
            cursor.execute(SUBJECTS_SELECT_SQL)
            self.__subjects = [data.Subject(**x) for x in cursor]

    def flags(self, idx):
        result = super().flags(idx)
        if idx.column() == 0:
            result |= Qt.ItemIsUserCheckable
        return result
