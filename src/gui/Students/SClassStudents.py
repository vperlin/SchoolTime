from PySide6.QtWidgets import QTableView, QHeaderView
from PySide6.QtCore import QAbstractTableModel, Qt, Slot, QModelIndex, QMimeData
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
import re
import json

import data
import helpers
from .. import Subjects

import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


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
select  sg.iid_subgroup,
        st.iid as iid,
        st.last_name as last_name,
        st.first_name as first_name,
        st.middle_name as middle_name, 
        st.phone as phone,
        st.phone_parents as phone_parents,
        st.note as note
    from  subgroups_students as sg
    inner join students as st
        on sg.iid_student = st.iid
    where sg.iid_subgroup in ( {} )
    order by last_name, first_name, middle_name ;
'''

STUDENT_OTHER_SELECT_SQL = '''
with grpst as (
       select  sg.iid_student as iid
        from  subgroups_students as sg
        where sg.iid_subgroup in ( {} )
)
select
        st.iid as iid,
        st.last_name as last_name,
        st.first_name as first_name,
        st.middle_name as middle_name, 
        st.phone as phone,
        st.phone_parents as phone_parents,
        st.note as note
    from students as st
    where iid_sclass = %s and st.iid not in ( select iid from grpst )
    order by last_name, first_name, middle_name ;
'''

ASSIGN_SUBJECT_SQL = '''
    insert into subgroups_subjects( iid_subgroup, iid_subject)
        values( %s, %s ) ;
'''


class Model(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__iid_sclass = None
        self.__iids_subgroup = []
        self.__iids_subject = []
        self.__students = []
        self.__subgroups = []

    @property
    def sg_shown(self) -> bool:
        return bool(self.__iids_subgroup)

    @property
    def sbj_shown(self) -> bool:
        return bool(self.__iids_subject)

    @Slot(list, list)
    def select_subgroups(self, sg_iids, sbj_iids):
        self.__iids_subgroup = list(sg_iids)
        self.__iids_subject = list(sbj_iids)
        self.reload()

    def remove_subgroup(self, iid_subgroup):
        self.__iids_subgroup.remove(iid_subgroup)

    @Slot()
    def setSClassId(self, iid_sclass):
        self.__iid_sclass = iid_sclass
        self.__iids_subgroup = []
        self.__iids_subject = []
        self.reload()

    def rowCount(self, idx_parent=QModelIndex()):
        if self.__iids_subgroup:
            R = sum( len(sg['students']) for sg in self.__subgroups )
            R += len(self.__subgroups)
            return R
        else:
            return len(self.__students)

    def columnCount(self, idx_parent=QModelIndex()):
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

    def find_obj_subgroup(self, number):
        row = number
        sgrp = iter(self.__subgroups)
        obj = next(sgrp)
        subgroup_no = 0
        stud = iter(obj['students'])
        student_no = -1
        while row > 0:
            try:
                obj = next(stud)
                student_no += 1
            except StopIteration:
                try:
                    obj = next(sgrp)
                    stud = iter(obj['students'])
                    subgroup_no += 1
                    student_no = -1
                except StopIteration:
                    return None, -1, -1
            row -= 1
        return obj, subgroup_no, student_no

    def find_obj_nosubgroup(self, number):
        if number > len(self.__students):
            return None, -1, -1
        return self.__students[number], -1, number

    def find_obj(self, number):
        if self.__subgroups:
            return self.find_obj_subgroup(number)
        else:
            return self.find_obj_nosubgroup(number)

    def data_groups(self, idx, role):
        obj, subgroup_no, student_no = self.find_obj(idx.row())
        if role == Qt.DisplayRole:
            if isinstance(obj, data.Student):
                match idx.column():
                    case 0: return obj.full_name
                    case 1: return obj.phone
                    case 2: return obj.phone_parents
                    case 3: return obj.note
                    case _: return None
            else:
                match idx.column():
                    case 0: return obj['title']
                    case _: return None
        elif role == Qt.BackgroundRole:
            if isinstance(obj, data.Student):
                return None
            else:
                if obj['iid'] < 0:
                    return QColor('#FF8888')
                return QColor('#FFDEAD')
        else:
            return None

    def data(self, idx, role):
        if self.__iids_subgroup:
            return self.data_groups(idx, role)
        else:
            return self.data_nogroups(idx, role)

    def headerData(self, section, orientation, role):
        if role == Qt.BackgroundRole and orientation == Qt.Vertical:
            obj, _, _ = self.find_obj(section)
            if not isinstance(obj, data.Student):
                if obj['iid'] < 0:
                    return QColor('#FF8888')
                return QColor('#FFDEAD')
            return None
        if role != Qt.DisplayRole:
            return super().headerData(section, orientation, role)
        if orientation == Qt.Horizontal:
            match section:
                case 0: return self.tr('FIO')
                case 1: return self.tr('Phone')
                case 2: return self.tr('Phone of Parents')
                case 3: return self.tr('Note')
                case _: None
        else:
            if self.sg_shown:
                obj, _, no = self.find_obj(section)
                if isinstance(obj, data.Student):
                    return no + 1
                return None
            else:
                return super().headerData(section, orientation, role)

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
                'iid': -1,
                'title': self.tr('<not included in any subgroup>'),
                'note': None,
            })
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
            sgrp[-1]['students'] = [ data.Student(**x) for x in cursor ]


    def reload(self):
        if self.__iids_subgroup:
            self.reload_groups()
        else:
            self.reload_nogroups()

    def flags(self, idx):
        result = super().flags(idx)
        if self.sg_shown:
            obj, _, _ = self.find_obj(idx.row())
            if isinstance(obj, data.Student):
                result |= Qt.ItemIsDragEnabled
            else:
                result |= Qt.ItemIsDropEnabled
        return result

    def supportedDropActions(self):
        return Qt.MoveAction

    def mimeTypes(self):
        return [ 'application/json' ]

    def mimeData(self, indexes):
        for idx in indexes:
            _, sg_no, st_no = self.find_obj(idx.row())
            dt = {
                'iid_subgroup': self.__subgroups[sg_no]['iid'],
                'iid_student': self.__subgroups[sg_no]['students'][st_no].iid
            }
            dt = json.dumps(dt).encode('utf-8')

            result = QMimeData()
            result.setData('application/json', dt)
            return result

    def canDropMimeData(self, dt, action, row, column, parent_idx):
        if not parent_idx.isValid():
            return False
        if not dt.hasFormat('application/json'):
            return False
        obj, _, _ = self.find_obj(parent_idx.row())
        if isinstance(obj, data.Student):
            return False
        dt = bytes(dt.data('application/json')).decode('utf-8')
        dt = json.loads(dt)
        return dt['iid_subgroup'] != obj['iid']

    def dropMimeData(self, dt, action, row, column, parent_idx):

        if not self.canDropMimeData(dt, action, row, column, parent_idx):
            return False

        if action == Qt.IgnoreAction:
            return True

        dt = bytes(dt.data('application/json')).decode('utf-8')
        dt = json.loads(dt)
        iid_student = dt['iid_student']
        iid_subgroup_old = dt['iid_subgroup']

        obj, _, _ = self.find_obj(parent_idx.row())
        iid_subgroup_new = obj['iid']

        with data.connect() as cursor:
            if iid_subgroup_old >= 0:
                cursor.execute('''
                    delete from subgroups_students
                       where iid_subgroup = %s and iid_student = %s ;
                ''', (iid_subgroup_old, iid_student,))
            if iid_subgroup_new >= 0:
                cursor.execute('''
                    insert into subgroups_students (iid_subgroup, iid_student)
                       values ( %s, %s ) ;
                ''', (iid_subgroup_new, iid_student,))
        self.reload()

        return True


class View(QTableView):

    subgroup_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.__action_set_subject = act = self.addAction(self.tr('Set subject'))
        act.triggered.connect(self.on_set_subject)
        act.setEnabled(False)

        self.__model = mdl = Model(parent=self)
        self.setModel(mdl)
        self.__model.modelReset.connect(self.setup)

    @Slot()
    def setup(self):
        self.setWordWrap(False)
        if hdr := self.horizontalHeader():
            hdr.setSectionResizeMode(QHeaderView.ResizeToContents)
            hdr.setSectionResizeMode(0, QHeaderView.Stretch)
        if hdr := self.verticalHeader():
            hdr.setSectionResizeMode(QHeaderView.Fixed)

        self.clearSpans()
        for r in range(0, self.__model.rowCount()):
            obj, subgroup_no, student_no = self.__model.find_obj(r)
            if subgroup_no >= 0 and student_no < 0:
                self.setSpan(r, 0, 1, 4)

        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(QTableView.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QTableView.InternalMove)

    @Slot(int)
    def setSClassId(self, iid):
        self.__model.setSClassId(iid)

    @Slot(list, list)
    def on_subgroups_selected(self, sg_iids, sbj_iids):
        self.__model.select_subgroups(sg_iids, sbj_iids)

    def selectionChanged(self, selected, deselected):
        super().selectionChanged(selected, deselected)
        if self.__model.sbj_shown or not self.__model.sg_shown:
            self.__action_set_subject.setEnabled(False)
            return
        if not selected.indexes():
            self.__action_set_subject.setEnabled(False)
            return

        row = selected.indexes()[0].row()
        obj, _, _ = self.__model.find_obj(row)
        if isinstance(obj, data.Student):
            self.__action_set_subject.setEnabled(False)
        else:
            self.__action_set_subject.setEnabled(True)

    @Slot()
    def on_set_subject(self):
        dia = Subjects.Dialog(parent=self)
        if dia.exec():
            row = self.selectedIndexes()[0].row()
            obj, _, _ = self.__model.find_obj(row)
            sg_iid = obj['iid']
            with data.connect() as cursor:
                for sbj_iid in dia.selected_iids:
                    cursor.execute(ASSIGN_SUBJECT_SQL, (sg_iid, sbj_iid,))
            self.subgroup_changed.emit()
            self.__model.remove_subgroup(sg_iid)
            self.__model.reload()

