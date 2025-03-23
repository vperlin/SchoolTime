from PySide6.QtWidgets import QFrame, QVBoxLayout, QFileDialog
from PySide6.QtCore import Slot
from datetime import date

import data
from . import menu
from . import SClasses
from .SClassFrame import SClassFrame


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__menu = menu.Menu(parent=self)
        self.__layout = lay = QVBoxLayout(self)

        self.__load_sclass_action = act = self.__menu.addAction(self.tr('Загрузить класс'))
        act.triggered.connect(self.on_load_sclass)

        self.__sclasses = wid = SClasses.View(parent=self)
        lay.addWidget(wid)

        self.__sclass_frame = frm = SClassFrame(parent=self)
        lay.addWidget(frm)
        
        self.__sclasses.iid_sclass_selected.connect(self.__sclass_frame.setSClassId)
        self.__sclass_frame.setSClassId(self.__sclasses.currentData())

    @property
    def menus(self):
        return [self.__menu]

    @Slot()
    def on_load_sclass(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            self.tr('Открыть файл для загрузки'),
            '.',
            'CSV Files (*.csv);;All Files (*)')
        if not filename:
            return
        with open(filename, 'rt', encoding='utf-8') as src:
            with data.connect() as cursor:
                title, fio = next(src).strip().split(',')
                teacher = data.Teacher.find_fio(cursor, *fio.split())
                sclass = data.SClass.find_title(cursor, title)
                sclass.iid_leader = teacher.iid
                sclass.name_leader = teacher.fio
                sclass.phone_leader = teacher.phone
                sclass.save(cursor)
                print(sclass)
                print(teacher)
                subgroup = None
                for x in (x.strip() for x in src):
                    if ',' in x:
                        student = data.Student()
                        fio, gender, bdate, student.phone, student.phone_parents, *dt = x.split(',')
                        student.last_name, student.first_name, student.middle_name = fio.split()
                        student.gender = gender.upper() == 'М'
                        y, m, d = (int(q) for q in bdate.split('.'))
                        student.birth_date = date(y, m, d)
                        student.iid_sclass = sclass.iid
                        student.save(cursor)
                        cursor.execute('''
                                insert into subgroups_students(iid_subgroup, iid_student)
                                    values( %s, %s ) ;''', (subgroup.iid, student.iid))
                    else:
                        subgroup = data.Subgroup(title=x, iid_sclass=sclass.iid)
                        subgroup.save(cursor)
            self.__sclasses.reload()
