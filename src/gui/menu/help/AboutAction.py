from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QAction
from PySide6.QtCore import Slot


class AboutAction(QAction):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setText( self.tr('About ...') )
        
        self.triggered.connect(self.on_triggered)
        
    @Slot()
    def on_triggered(self):
        QMessageBox.about(
            self.parent(),
            self.tr('AWP SchoolTime'),
            self.tr('Authomated workplace for School Manager')
        )