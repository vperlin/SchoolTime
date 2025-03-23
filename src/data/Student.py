from dataclasses import dataclass
from datetime import date

_INSERT_SQL = '''
    insert into students (
        iid_sclass,
        last_name, first_name, middle_name,
        phone, phone_parents,
        note,
        gender, birth_date
    ) values ( %s, %s, %s, %s, %s, %s, %s, %s, %s )
    returning iid ;
'''

_UPDATE_SQL = '''
    update students set
            iid_sclass = %s,
            last_name = %s,
            first_name = %s,
            middle_name = %s,
            phone = %s,
            phone_parents %s,
            note = %s,
            gender = %s
        where iid = %s ;
'''


@dataclass
class Student(object):
    
    iid: int = None
    iid_sclass: int = None
    last_name: str = None
    first_name: str = None
    middle_name: str = None
    phone: str = None
    phone_parents: str = None
    note: str = None
    gender: bool = None
    birth_date: date = None

    @property
    def is_new(self):
        return self.iid is None

    @property
    def insert_data(self):
        return (
            self.iid_sclass,
            self.last_name,
            self.first_name,
            self.middle_name,
            self.phone,
            self.phone_parents,
            self.note,
            self.gender,
            self.birth_date,
        )

    @property
    def update_data(self):
        return (
            self.iid_sclass,
            self.last_name,
            self.first_name,
            self.middle_name,
            self.phone,
            self.phone_parents,
            self.note,
            self.gender,
            self.birth_date,
            self.iid,
        )

    @property
    def full_name(self):
        if self.middle_name is None:
            return f'{self.last_name} {self.first_name}'
        return  f'{self.last_name} {self.first_name} {self.middle_name}'

    def save(self, cursor):
        if self.is_new:
            cursor.execute(_INSERT_SQL, self.insert_data)
            self.iid = cursor.fetchone()['iid']
        else:
            cursor.execute(_UPDATE_SQL, self.update_data)
        return self
