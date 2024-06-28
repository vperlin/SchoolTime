from dataclasses import dataclass


@dataclass
class Teacher(object):

    __tablename__ = 'teachers'

    iid: int = None
    last_name: str = None
    first_name: str = None
    middle_name: str = None
    phone: str = None
    note: str = None

    __field_names = []
