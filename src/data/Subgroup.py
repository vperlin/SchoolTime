from dataclasses import dataclass

_INSERT_SQL = '''
    insert into subgroups(title, iid_sclass, note)
        values( %s, %s, %s )
        returning iid ;
'''

_UPDATE_SQL = '''
    update subgroups set
            title = %s,
            iid_sclass = %s,
            note = %s
        where iid = %s ;
'''


@dataclass
class Subgroup(object):

    iid: int = None
    title: str = None
    iid_sclass: int = None
    note: str = None

    @property
    def is_new(self):
        return self.iid is None
    
    @property
    def insert_data(self):
        return ( self.title, self.iid_sclass, self.note )
    
    @property
    def update_data(self):
        return ( self.title, self.iid_sclass, self.note, self.iid )
    
    def save(self, cursor):
        if self.is_new:
            cursor.execute(_INSERT_SQL, self.insert_data)
            self.iid = cursor.fetchone()['iid']
        else:
            cursor.execute(_UPDATE_SQL, self.update_data)
        return self
