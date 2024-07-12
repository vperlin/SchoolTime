from enum import Enum


class Kind(Enum):

    STUDENT = 0x80000000
    GROUP   = 0x40000000  # @IgnorePep8
    SUBJECT = 0x20000000
    TEACHER = 0x10000000

    KIND = 0xFF000000
    ITEM = 0x00FFFFFF
