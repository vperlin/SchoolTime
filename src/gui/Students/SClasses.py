from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex

import data
from helpers import resetting_model


SELECT_ALL_SQL = '''
    select iid, lyear, letter, iid_leader, note, name_leader, leader_phones as phone_leader
        from sclass_info
        order by lyear, letter ;
'''


class Model(QAbstractListModel):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.__sclasses = []
        
    @resetting_model
    def reload(self):
        with data.connect() as cursor:
            cursor.execute(SELECT_ALL_SQL)
            self.__sclasses = [data.SClass(**x) for x in cursor]
            
    def rowCount(self, idx_parent=QModelIndex()):
        return len(self.__sclasses)
                  
    def data(self, idx, role=Qt.DisplayRole):
        match role:
            case Qt.DisplayRole:
                return str(self.__sclasses[idx.row()])
            case Qt.UserRole:
                return self.__sclasses[idx.row()].iid
            case _:
                return None


class View(QComboBox):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__model = Model(parent=self)
        self.__model.reload()
        
        self.setModel(self.__model)
        
