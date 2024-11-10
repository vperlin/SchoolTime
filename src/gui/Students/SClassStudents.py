from PySide6.QtWidgets import QTableView
from PySide6.QtCore import QAbstractTableModel, Qt, Slot
import re

import data
import helpers


STUDENTS_SELECT_SQL = '''
    select iid, last_name, first_name, middle_name, 
           phone, phone_parents, note, iid_sclass
        from students
        where iid_sclass = %s
        order by last_name, first_name, middle_name ;
'''


SUBGROUPS_SELECT_SQL = '''
    select iid, title, note
        from subgroups
        where iid in ( {} ) ;
'''


class Model(QAbstractTableModel):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.__iid_sclass = None
        self.__iids_subgroup = []
        self.__iids_subject = []
        self.__students = []
        self.__subgroups = []
        
    @Slot(list, list)
    def select_subgroups(self, sg_iids, sbj_iids):
        self.__iids_subgroup = list(sg_iids)
        self.__iids_subject = list(sbj_iids)
        self.reload()

    @Slot()
    def setSClassId(self, iid_sclass):
        self.__iid_sclass = iid_sclass
        self.__iids_subgroup = []
        self.__iids_subject = []
        self.reload()
                
    def rowCount(self, idx_parent):
        return len(self.__students)
    
    def columnCount(self, idx_parent):
        return 4
    
    def data(self, idx, role):
        if role == Qt.DisplayRole:
            st = self.__students[idx.row()]
            match idx.column():
                case 0:
                    return st.full_name
                case 1:
                    return st.phone
                case 2:
                    return st.phone_parents
                case 3:
                    return st.note
                case _:
                    return None
        else:
            return None

    @helpers.resetting_model
    def reload_nogroups(self):
        self.__subgroups = []
        with data.connect() as cursor:
            cursor.execute(STUDENTS_SELECT_SQL, (self.__iid_sclass,))
            self.__students = [data.Student(**x) for x in cursor]

    @helpers.resetting_model
    def reload_groups(self):
        with data.connect() as cursor:
            iid_txt = ','.join(map(str,self.__iids_subgroup))
            if not re.match(r'[,\d]+', iid_txt):
                return
            SQL = SUBGROUPS_SELECT_SQL.format(iid_txt)
            cursor.execute(SQL)
            self.__subgroups = list(cursor)
            print(self.__subgroups)

    def reload(self):
        if self.__iids_subgroup:
            self.reload_groups()
        else:
            self.reload_nogroups()

        
class View(QTableView):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.__model = mdl = Model(parent=self)
        self.setModel(mdl)
        
    @Slot(int)
    def setSClassId(self, iid):
        self.__model.setSClassId(iid)
        
    @Slot(list, list)
    def on_subgroups_selected(self, sg_iids, sbj_iids):
        self.__model.select_subgroups(sg_iids, sbj_iids)        
        