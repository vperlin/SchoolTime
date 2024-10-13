from PySide6.QtWidgets import QTableView, QFileDialog
from PySide6.QtCore import Slot
from pathlib import Path


import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class TeachersView(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

    def setModel(self, model):
        super().setModel(model)
        self.setRootIndex(model.idx_teachers)
        model.modelReset.connect(self.on_model_reset)

    def on_model_reset(self):
        self.setRootIndex(self.model().idx_teachers)

    @Slot()
    def load_teachers(self):
        title = self.tr('Open teacher list')
        filters = 'CSV files (*.csv);;XLSX Files (*.xlsx);;All Files (*)'
        fl, _ = QFileDialog.getOpenFileName(self, title, '.', filters)
        if not fl:
            return
        fl = Path(fl)
        match fl.suffix.lower():
            case '.csv':
                self.model().load_teachers_csv(fl)
            case '.xlsx':
                self.model().load_teachers_xlsx(fl)
            case _:
                return
