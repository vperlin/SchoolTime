from PySide6.QtWidgets import QFrame, QRadioButton, QHBoxLayout


class SubgroupsFrame(QFrame):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        lay = QHBoxLayout(self)
        
        lay.addStretch()
        
        self.__no_subgroups = btn = QRadioButton(self.tr('no subgroups'), self)
        lay.addWidget(btn)
        
        self.__noname = btn = QRadioButton(self.tr('noname'), self)
        lay.addWidget(btn)
        
        self.__other = []
        # Заглушки
        btn = QRadioButton(self.tr('eng, inf'), self)
        self.__other.append(btn)
        lay.addWidget(btn)
        btn = QRadioButton(self.tr('mat, lab'), self)
        self.__other.append(btn)
        lay.addWidget(btn)
        # конец заглушек
        
        lay.addStretch()