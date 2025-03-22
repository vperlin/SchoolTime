from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout
from .View import View
from .Model import Model


class Dialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__model = mdl = Model(parent=self)

        lay = QVBoxLayout(self)

        self.__view = vie = View(parent=self)
        vie.setModel(mdl)
        lay.addWidget(vie)

        self.__buttons = btn = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        lay.addWidget(btn)

        btn.rejected.connect(self.reject)
        btn.accepted.connect(self.accept)
        mdl.reload()

    @property
    def selected_iids(self):
        return self.__model.selected_iids

