from PySide6.QtWidgets import QTableView, QHeaderView, QSizePolicy, QApplication
from PySide6.QtGui import QColor, QDrag
from PySide6.QtCore import QAbstractTableModel, Qt, Slot, QModelIndex, QMimeData
import re
import json
import io

import data
import helpers

bgColors = [
    [ QColor('#E8D5B8'), QColor('#F4EADC') ],
    [ QColor('#E7DCCB'), QColor('#F3EDE5') ],
    [ QColor('#EAE4D9'), QColor('#F4F1EB') ],
]

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

    def rowCount(self, idx_parent=QModelIndex()):
        if self.__iids_subgroup:
            R = sum( len(sg['students']) for sg in self.__subgroups )
            R += len(self.__subgroups)
            return R
        else:
            return len(self.__students)

    def columnCount(self, idx_parent):
        return 4

    def find_obj(self, number):
        row = number
        sgrp = iter(self.__subgroups)
        try:
            obj = next(sgrp)
        except StopIteration:
            return None, -1, -1
        stud = iter(obj['students'])
        student_no = -1
        group_no = 0
        while row > 0:
            try:
                obj = next(stud)
                student_no += 1
            except StopIteration:
                obj = next(sgrp)
                stud = iter(obj['students'])
                group_no += 1
                student_no = -1
            row -= 1
        return obj, group_no, student_no

    def data_nogroups_display(self, idx):
        st = self.__students[idx.row()]
        match idx.column():
            case 0: return st.full_name
            case 1: return st.phone
            case 2: return st.phone_parents
            case 3: return st.note
            case _: return None

    def data_nogroups_groupid(self, idx):
        return None

    def data_nogroups_studentid(self, idx):
        st = self.__students[idx.row()]
        return st.iid

    def data_nogroups(self, idx, role):
        if role == Qt.DisplayRole: return self.data_nogroups_display(idx)
        elif role == Qt.UserRole + 1: return self.data_nogroups_studentid(idx)
        elif role == Qt.UserRole + 2: return self.data_nogroups_groupid(idx)
        return None

    def data_groups_display(self, idx):
        obj, group_no, student_no = self.find_obj(idx.row())
        if student_no < 0:
            if idx.column() == 0:
                return obj['title']
        else:
            match idx.column():
                case 0: return obj.full_name
                case 1: return obj.phone
                case 2: return obj.phone_parents
                case 3: return obj.note
        return None

    def data_groups_background(self, idx):
        _, group_no, student_no = self.find_obj(idx.row())
        no = group_no % len(bgColors)
        if student_no < 0:
            return bgColors[no][1]
        return None

    def data_groups_groupid(self, idx):
        _, group_no, student_no = self.find_obj(idx.row())
        return self.__subgroups[group_no]['iid']

    def data_groups_studentid(self, idx):
        _, group_no, student_no = self.find_obj(idx.row())
        if student_no < 0:
            return None
        return self.__subgroups[group_no]['students'][student_no].iid

    def data_groups(self, idx, role):
        obj, group_no, student_no = self.find_obj(idx.row())
        if role == Qt.DisplayRole: return self.data_groups_display(idx)
        elif role == Qt.BackgroundRole: return self.data_groups_background(idx)
        elif role == Qt.UserRole + 1: return self.data_groups_groupid(idx)
        elif role == Qt.UserRole + 2: return self.data_groups_studentid(idx)
        return None

    def data(self, idx, role):
        if self.__iids_subgroup:
            return self.data_groups(idx, role)
        else:
            return self.data_nogroups(idx, role)

    def horizontal_headerData(self, section, role):
        if role != Qt.DisplayRole:
            return super().headerData(section, Qt.Horizontal, role)
        match section:
            case 0: return self.tr('FIO')
            case 1: return self.tr('Phone')
            case 2: return self.tr('Phone of parents')
            case 3: return self.tr('Note')
            case _: return None

    def vertical_headerData(self, section, role):
        if role != Qt.DisplayRole:
            return super().headerData(section, Qt.Horizontal, role)
        if not self.__iids_subgroup:
            return super().headerData(section, Qt.Horizontal, role)
        _, _, no = self.find_obj(section)
        return None if no < 0 else no + 1

    def headerData(self, section, orientation, role):
        match orientation:
            case Qt.Horizontal:
                return self.horizontal_headerData(section, role)
            case Qt.Vertical:
                return self.vertical_headerData(section, role)
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
        self.setup()

    def setup(self):
        self.__dragStartPos = None
        self.setWordWrap(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.clearSpans()
        for r in range(0, self.__model.rowCount()):
            _, group_no, student_no = self.__model.find_obj(r)
            if group_no >= 0 and student_no < 0:
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
        self.setup()

    @Slot(list, list)
    def on_subgroups_selected(self, sg_iids, sbj_iids):
        self.__model.select_subgroups(sg_iids, sbj_iids)
        self.setup()

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.__dragStartPos = None
            idx = self.indexAt(event.pos())
            if idx.isValid():
                obj, group_no, student_no = self.__model.find_obj(idx.row())
                if group_no >= 0 and student_no >= 0:
                    self.__dragStartPos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.__dragStartPos is None:
            return super().mouseMoveEvent(event)
        if not (event.buttons() & Qt.LeftButton):
            return super().mouseMoveEvent(event)
        dist = (event.pos() - self.__dragStartPos).manhattanLength()
        if dist < QApplication.startDragDistance(): return

        idx = self.indexAt(self.__dragStartPos)
        group_id = idx.data(Qt.UserRole + 1)
        student_id = idx.data(Qt.UserRole + 2)
        data = {
            'iid_group': idx.data(Qt.UserRole + 1),
            'iid_student': idx.data(Qt.UserRole + 2),
        }
        data = json.dumps(data).encode('utf-8')

        mimedata = QMimeData()
        mimedata.setData('application/json', data)

        drag = QDrag(self)
        drag.setMimeData(mimedata)
        drop_action = drag.exec(Qt.MoveAction)
        super().mouseMoveEvent(event)

    def dragEnterEvent(self, event):
        if not event.mimeData().hasFormat('application/json'):
            return
        idx = self.indexAt(event.pos())
        if not idx.isValid():
            return
        if idx.data(Qt.UserRole + 2) is not None:
            return
        data = event.mimeData().data('application/json')
        data = json.loads(bytes(data).decode('utf-8'))
        if idx.data(Qt.UserRole + 1) == data['iid_group']:
            return
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        print(self.dragDropMode())

    def dropEvent(self, event):
        print('Drop')
