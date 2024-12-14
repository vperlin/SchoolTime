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

STUDENT_SUBGROUPS_SELECT_SQL = '''
select
    st.iid as iid,
    sg.iid_subgroup as iid_subgroup,
    last_name, first_name, middle_name,
           phone, phone_parents, st.note,
           st.iid_sclass
    from subgroups_students as sg
    inner join students as st
        on sg.iid_student = st.iid
    where iid_subgroup in ( {} )
    order by last_name, first_name, middle_name ;
'''

STUDENT_OTHER_SELECT_SQL = '''
with sg_std as (
select
    st.iid as iid
    from subgroups_students as sg
    right outer join students as st
        on sg.iid_student = st.iid
    where iid_subgroup in ( {} )
) select
    st.iid as iid,
    last_name, first_name, middle_name,
           phone, phone_parents, st.note,
           st.iid_sclass
    from students as st
    where st.iid_sclass = %s
        and st.iid not in ( select iid from sg_std )
    order by last_name, first_name, middle_name ;
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
        if self.__iids_subgroup:
            R = sum( len(sg['students']) for sg in self.__subgroups )
            R += len(self.__subgroups)
            return R
        else:
            return len(self.__students)

    def columnCount(self, idx_parent):
        return 4

    def data_nogroups(self, idx, role):
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

    def data_groups(self, idx, role):
        row = idx.row()
        sgrp = iter(self.__subgroups)
        obj = next(sgrp)
        stud = iter(obj['students'])
        while row > 0:
            try:
                obj = next(stud)
            except StopIteration:
                obj = next(sgrp)
                stud = iter(obj['students'])
            row -= 1
        if role == Qt.DisplayRole:
            if isinstance(obj, data.Student):
                match idx.column():
                    case 0:
                        return obj.full_name
                    case 1:
                        return obj.phone
                    case 2:
                        return obj.phone_parents
                    case 3:
                        return obj.note
                    case _:
                        return None
            else:
                match idx.column():
                    case 0:
                        return obj['title']
                    case _:
                        return None
        else:
            return None

    def data(self, idx, role):
        if self.__iids_subgroup:
            return self.data_groups(idx, role)
        else:
            return self.data_nogroups(idx, role)

    @helpers.resetting_model
    def reload_nogroups(self):
        self.__subgroups = []
        with data.connect() as cursor:
            cursor.execute(STUDENTS_SELECT_SQL, (self.__iid_sclass,))
            self.__students = [data.Student(**x) for x in cursor]

    @helpers.resetting_model
    def reload_groups(self):
        self.__students = []
        with data.connect() as cursor:
            iid_txt = ','.join(map(str,self.__iids_subgroup))
            if not re.match(r'[,\d]+', iid_txt):
                return
            SQL = SUBGROUPS_SELECT_SQL.format(iid_txt)
            cursor.execute(SQL)
            self.__subgroups = list(cursor)
            self.__subgroups.append({
                'iid':-1,
                'title': self.tr('<not specified>'),
                'note': None})
            sgrp = {}
            for sg in self.__subgroups:
                sgrp[sg['iid']] = sg
                sg['students'] = []
            SQL = STUDENT_SUBGROUPS_SELECT_SQL.format(iid_txt)
            cursor.execute(SQL)
            for student in cursor:
                iid_subgroup = student.pop('iid_subgroup')
                student = data.Student(**student)
                sgrp[iid_subgroup]['students'].append(student)
            SQL = STUDENT_OTHER_SELECT_SQL.format(iid_txt)
            cursor.execute(SQL, (self.__iid_sclass,))
            sgrp[-1]['students'] = [data.Student(**x) for x in cursor]

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
        
