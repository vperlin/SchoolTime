from dataclasses import dataclass, field

from .Subject import Subject
from typing import List


_INSERT_SQL = '''
    insert into teachers (
        last_name,
        first_name,
        middle_name,
        phone,
        email,
        note
    ) values ( %s, %s, %s, %s, %s, %s )
    returning iid ;
'''


_UPDATE_SQL = '''
    update teachers set
            last_name = %s,
            first_name = %s,
            middle_name = %s,
            phone = %s,
            email = %s,
            note = %s
        where iid = %s ;
'''

_FIND_FIO_SQL = '''
    select iid, last_name, first_name, middle_name,
           phone, email, note
        from teachers
        where last_name = %s
              and first_name = %s
              and coalesce(middle_name,'') = coalesce(%s,'') ;
'''

_SELECT_SUBJ_SQL = '''
    select sbj.iid, sbj.code, sbj.title, sbj.note
        from subjects sbj
        inner join teachers_subjects tsb on tsb.iid_subject = sbj.iid
        where tsb.iid_teacher = %s ;
'''

_INSERT_SUBJ = '''
    insert into teachers_subjects ( iid_teacher, iid_subject )
        values ( %s, %s ) ; 
'''


_DELETE_SUBJ = '''
    delete from teachers_subjects where iid_teacher = %s ;
'''


@dataclass
class Teacher(object):

    iid: int = None
    last_name: str = None
    first_name: str = None
    middle_name: str = None
    phone: str = None
    email: str = None
    note: str = None
    subjects: List[Subject] = field(default_factory=list)
    lead_group: int = None
    
    @property
    def is_new(self):
        return self.iid is None
    
    @property
    def insert_data(self):
        return (self.last_name,
                self.first_name,
                self.middle_name,
                self.phone,
                self.email,
                self.note, )

    @property
    def update_data(self):
        return (self.last_name,
                self.first_name,
                self.middle_name,
                self.phone,
                self.email,
                self.note,
                self.iid, )

    def __getitem__(self, index):
        match index:
            case 0:
                return self.iid
            case 1:
                return self.last_name
            case 2:
                return self.first_name
            case 3:
                return self.middle_name
            case 4:
                return self.phone
            case 5:
                return self.email
            case 6:
                r = [ s.code for s in self.subjects ]
                return ', '.join(r)
            case 7:
                return 'класс'
            case 8:
                return self.note
            case _:
                return None
            
    def save(self, cursor):
        if self.is_new:
            cursor.execute(_INSERT_SQL, self.insert_data)
            self.iid = cursor.fetchone()['iid']
        else:
            cursor.execute(_UPDATE_SQL, self.update_data)
            cursor.execute(_DELETE_SUBJ, (self.iid,))
        for subj in self.subjects:
            cursor.execute(_INSERT_SUBJ, (self.iid, subj.iid,))

    @classmethod
    def find_fio(cls, cursor, last_name, first_name, middle_name):
        dt = (last_name, first_name, middle_name)
        cursor.execute(_FIND_FIO_SQL, dt)
        if cursor.rowcount <= 0:
            result = cls(last_name=last_name,
                     first_name=first_name, middle_name=middle_name)
            result.save(cursor)
            return result
        result = cls(**cursor.fetchone())
        cursor.execute(_SELECT_SUBJ_SQL, (result.iid,))
        result.subjects = [ Subject(**x) for x in cursor ]
        return result

    @property
    def fio(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name} {self.middle_name}'
        else:
            return f'{self.last_name} {self.first_name}'
