from dataclasses import dataclass, field


@dataclass
class Teacher(object):

    iid: int = None
    last_name: str = None
    first_name: str = None
    middle_name: str = None
    phone: str = None
    note: str = None
    iids_subject: list[int] = field(default_factory=list)
    codes_subject: list[str] = field(default_factory=list)

    is_new: bool = True
    is_changed: bool = False

    @property
    def subjects(self):
        return ', '.join(self.codes_subject)

