from dataclasses import dataclass

_INSERT_SQL = '''
    insert into subjects( code, title, note )
        values ( %s, %s, %s )
        returning iid ;
'''

_UPDATE_SQL = '''
    update subjects set
          code = %s,
          title = %s,
          note = %s
       where iid = %s ;
'''


@dataclass
class Subject(object):

    iid: int = None
    code: str = None
    title: str = None
    note: str = None
    
    is_changed: bool = False
    is_selected: bool = False
    
    @property
    def is_new(self):
        return self.iid is None

    @property
    def insert_data(self):
        return ( self.code, self.title, self.note )
    
    @property
    def update_data(self):
        return ( self.code, self.title, self.note, self.iid )

    def __getitem__(self, index):
        match index:
            case 0:
                return self.iid
            case 1:
                return self.code
            case 2:
                return self.title
            case 3:
                return self.note
            case _:
                return None

    def save(self, cursor):
        if self.is_new:
            cursor.execute(_INSERT_SQL, self.insert_data )
            self.iid = cursor.fetchone()['iid']
        elif self.is_changed:
            cursor.execute(_UPDATE_SQL, self.update_data)
            
            
            
            