from PySide6.QtWidgets import QFrame, QRadioButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Slot

from . import SClassStudents
from .Subgroups import SubgroupsFrame


class SClassFrame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        lay = QVBoxLayout(self)

        self.__subgroups = sub = SubgroupsFrame(parent=self)
        # sub.setStyleSheet('background: green')
        lay.addWidget(sub)

        self.__students = vie = SClassStudents.View(parent=self)
        # vie.setStyleSheet('background: blue')
        lay.addWidget(vie)

        sub.subgroups_selected.connect(vie.on_subgroups_selected)

    @Slot(int)
    def setSClassId(self, iid_sclass):
        self.__subgroups.setSClassId(iid_sclass)
        self.__students.setSClassId(iid_sclass)
