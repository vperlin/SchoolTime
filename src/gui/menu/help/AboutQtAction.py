from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QAction
from PySide6.QtCore import Slot


class AboutQtAction(QAction):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setText( self.tr('About Qt ...') )
        
        self.triggered.connect(self.on_triggered)
        
    @Slot()
    def on_triggered(self):
        QMessageBox.aboutQt(self.parent())