from dataclasses import dataclass, field

from .Subject import Subject


@dataclass
class Teacher(object):

    iid: int = None
    last_name: str = None
    first_name: str = None
    middle_name: str = None
    phone: str = None
    email: str = None
    note: str = None
    subjects: list[Subject] = field(default_factory=list)
    lead_group: int = None

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
