from PySide6.QtGui import QAction


class StudentsModeAction(QAction):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setText( self.tr('Students') )
