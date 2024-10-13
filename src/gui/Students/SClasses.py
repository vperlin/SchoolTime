from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

import data


def _resetting_model(function):
    def function_resetting_model(self, *args, **kwargs):
        self.beginResetModel()
        try:
            return function(self, *args, **kwargs)
        finally:
            self.endResetModel()
    return function_resetting_model


SELECT_ALL_SQL = '''
    select iid, lyear, letter, iid_leader, note
        from sclasses
        order by lyear, letter ;
'''


class Model(QAbstractTableModel):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.__sclasses = []
        
    @_resetting_model
    def reload(self):
        with data.connect() as cursor:
            cursor.execute(SELECT_ALL_SQL)
            self.__sclasses = [data.SClass(**x) for x in cursor]
            
    def rowCount(self, idx_parent=QModelIndex()):
        if idx_parent.isValid():
            return 0
        return len(self.__sclasses)
                  
    def columnCount(self, idx_parent=QModelIndex()):
        if idx_parent.isValid():
            return 0
        return 2
        
    def data(self, idx, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if idx.column() == 0:
                return self.__sclasses[idx.row()].iid
            elif idx.column() == 1:
                return str(self.__sclasses[idx.row()])
            else:
                return None
        else:
            return None


class View(QComboBox):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__model = Model(parent=self)
        self.__model.reload()
        
        self.setModel(self.__model)
        
