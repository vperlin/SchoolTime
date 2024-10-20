from dataclasses import dataclass


@dataclass
class Student(object):
    
    iid: int = None
    iid_sclass: int = None
    last_name: str = None
    first_name: str = None
    middle_name: str = None
    phone: str = None
    phone_parents: str = None
    note: str = None
    
    @property
    def full_name(self):
        if self.middle_name is None:
            return f'{self.last_name} {self.first_name}'
        return  f'{self.last_name} {self.first_name} {self.middle_name}'
    
    