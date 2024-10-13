from dataclasses import dataclass


@dataclass
class SClass(object):
    
    iid: int = None
    lyear: int = None
    letter: str = None
    iid_leader: int = None
    note: str = None
    
    def __str__(self):
        return f'({self.iid}) {self.lyear}{self.letter} -- {self.iid_leader}'
