from dataclasses import dataclass

_FIND_TITLE_SQL = '''
    select iid, lyear, letter, iid_leader, note
        from sclasses
        where lyear = %s and letter = %s ;
'''

_INSERT_SQL = '''
    insert into sclasses ( lyear, letter, iid_leader, note )
        values ( %s, %s, %s, %s )
        returning iid ;
'''

_UPDATE_SQL = '''
    update sclasses set
            lyear = %s,
            letter = %s,
            iid_leader = %s,
            note = %s
        where iid = %s ;
'''


@dataclass
class SClass(object):
    
    iid: int = None
    lyear: int = None
    letter: str = None
    iid_leader: int = None
    note: str = None
    name_leader: str = None
    phone_leader: str = None
    
    def __str__(self):
        if self.iid_leader is None:
            return f'({self.iid}) {self.lyear}{self.letter}'
        return f'({self.iid}) {self.lyear}{self.letter} --- {self.name_leader} тел. {self.phone_leader}'

    @property
    def is_new(self):
        return self.iid is None

    @property
    def insert_data(self):
        return (self.lyear, self.letter, self.iid_leader, self.note)

    @property
    def update_data(self):
        return (self.lyear, self.letter, self.iid_leader, self.note, self.iid)

    def save(self, cursor):
        if self.is_new:
            cursor.execute(_INSERT_SQL, self.insert_data)
            self.iid = cursor.fetchone()['iid']
        else:
            cursor.execute(_UPDATE_SQL, self.update_data)
        return self

    @classmethod
    def find_title(cls, cursor, title):
        lyear = int(title[:-1])
        letter = title[-1]
        cursor.execute(_FIND_TITLE_SQL, (lyear, letter,))
        if cursor.rowcount <= 0:
            return cls(lyear=lyear, letter=letter).save(cursor)
        return cls(**cursor.fetchone())
