from dataclasses import dataclass


@dataclass
class Subject(object):

    iid: int = None
    code: str = None
    title: str = None
    note: str = None
