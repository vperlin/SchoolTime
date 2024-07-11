from PySide6.QtWidgets import QFrame, QTableView, QVBoxLayout


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__layout = lay = QVBoxLayout(self)

        # Временно
        tbl = QTableView(parent=self)
        lay.addWidget(tbl)
