from PySide6.QtWidgets import QFrame, QRadioButton, QVBoxLayout, QHBoxLayout


from . import SClassStudents


class SClassFrame(QFrame):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        lay = QVBoxLayout(self)
        
        radiolay = QHBoxLayout()
        lay.addLayout(radiolay)
        
        self.__no_subgroup = btn = QRadioButton(parent=self)
        btn.setText(self.tr('no subgroups'))
        btn.setChecked(True)
        radiolay.addWidget(btn)
        
        self.__subgroups = []
        # Заглушки
        btn = QRadioButton(parent=self)
        btn.setText(self.tr('subgroup 1'))
        self.__subgroups.append(btn)
        radiolay.addWidget(btn)
        btn = QRadioButton(parent=self)
        btn.setText(self.tr('subgroup 2'))
        self.__subgroups.append(btn)
        radiolay.addWidget(btn)
        # конец заглушек
        
        # Заглушка
        self.__students = vie = SClassStudents.View(parent=self)
        lay.addWidget(vie)
        