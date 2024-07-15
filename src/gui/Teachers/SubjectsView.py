from PySide6.QtWidgets import QTableView

import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class SubjectsView(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

    def setModel(self, model):
        super().setModel(model)
        self.setRootIndex(model.idx_subjects)
