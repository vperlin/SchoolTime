from dataclasses import dataclass, field


@dataclass
class Teacher(object):

    iid: int = None
    last_name: str = None
    first_name: str = None
    middle_name: str = None
    phone: str = None
    note: str = None
    subjects: list[int] = field(default_factory=list)
    lead_group: int = None
