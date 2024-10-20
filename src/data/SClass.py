from dataclasses import dataclass


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
