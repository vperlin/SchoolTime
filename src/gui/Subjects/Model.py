from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

import data
import helpers

import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


_SELECT_SUBJ_SQL = '''
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
        return [ sbj.iid for sbj in self.__subjects if sbj.is_selected ] 
        
    def rowCount(self, idx=QModelIndex()):
        return len(self.__subjects)
    
    def columnCount(self, idx=QModelIndex()):
        return 3
    
    def data(self, idx, role=Qt.DisplayRole):
        sbj = self.__subjects[idx.row()]
        if role == Qt.DisplayRole:
            match idx.column():
                case 0: return sbj.code
                case 1: return sbj.title
                case 2: return '*' if sbj.note else None
                case _: return None
        elif role == Qt.CheckStateRole:
            if idx.column() > 0:
                return None
            return Qt.Checked if sbj.is_selected else Qt.Unchecked
        else:
            return None
        
    @helpers.resetting_model
    def setData(self, idx, value, role):
        if role != Qt.CheckStateRole or idx.column() > 0:
            return super().setData(idx, value, role)
        sbj = self.__subjects[idx.row()]
        sbj.is_selected = (value == Qt.Checked.value)
        return True

    def flags(self, idx):
        result = super().flags(idx)
        if idx.column() == 0:
            result |= Qt.ItemIsUserCheckable
        return result

    @helpers.resetting_model
    def reload(self):
        with data.connect() as cursor:
            cursor.execute(_SELECT_SUBJ_SQL)
            self.__subjects = [ data.Subject(**x) for x in cursor]
        
        
        
        