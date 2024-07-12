from PySide6.QtWidgets import QFrame, QVBoxLayout, QTableView, QDockWidget, QTreeView
from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex, Slot

import data
from . import menu
from . import Subjects

import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class Model(QAbstractItemModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__subjects = []
        self.__teachers = []

    def index(self, row, column, idx_parent=QModelIndex()):
        if not idx_parent.isValid():
            match row:
                case 0:
                    return self.createIndex(row, column,
                                            data.Kind.SUBJECT.value)
                case 1:
                    return self.createIndex(row, column,
                                            data.Kind.TEACHER.value)
                case _:
                    LOG.warning(f'Invalid row number = {row}')
                    return QModelIndex()
        else:
            LOG.debug('Unknown index()')
            return QModelIndex()

    def parent(self, idx):
        if idx.internalId() in {data.Kind.SUBJECT.value,
                                data.Kind.TEACHER.value}:
            return QModelIndex()
        else:
            LOG.debug('Unknown parent')
            return QModelIndex()

    def rowCount(self, idx_parent=QModelIndex()):
        if not idx_parent.isValid():
            return 2
        LOG.debug('Unknown rowCount()')
        return 0
        # return 0 if idx_parent.isValid() else len(self.__content)

    def columnCount(self, idx_parent=QModelIndex()):
        if not idx_parent.isValid():
            return 1
        LOG.debug('Unknown columnCount()')
        return 0
        # return 0 if idx_parent.isValid() else 8

    def data(self, idx, role=Qt.DisplayRole):
        match role:
            case Qt.DisplayRole:
                match idx.internalId():
                    case data.Kind.SUBJECT.value:
                        return self.tr('Subjects')
                    case data.Kind.TEACHER.value:
                        return self.tr('Teachers')
                    case _:
                        LOG.warning(f'Invalid kind ID: {idx.internalId(): x}')
                        return '???'
                # dt = self.__content[idx.row()]
                # match idx.column():
                #     case 0:
                #         return dt.iid
                #     case 1:
                #         return dt.last_name
                #     case 2:
                #         return dt.first_name
                #     case 3:
                #         return dt.middle_name
                #     case 4:
                #         return dt.phone
                #     case 5:
                #         return 'subjects'
                #     case 6:
                #         return 'класс'
                #     case 7:
                #         return dt.note
                #     case _:
                #         return None
            case _:
                return None

    @Slot()
    def reload(self):
        LOG.debug('Reloading model')
        # with data.connect(data.Teacher) as cursor:
        #     cursor.execute('''
        #         select iid, last_name, first_name, middle_name, phone, note
        #             from teachers ;
        #     ''')
        #     self.beginResetModel()
        #     try:
        #         self.__content = list(cursor)
        #     finally:
        #         self.endResetModel()


class View(QTreeView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__model = mdl = Model(parent=self)
        self.setModel(mdl)
        mdl.reload()


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__menu = menu.Menu(parent=self)
        self.__layout = lay = QVBoxLayout(self)

        tbl = View(parent=self)
        lay.addWidget(tbl)

        dock = QDockWidget(self.tr('Subjects'), parent=self)
        self.__subjects_dock = dock
        self.__subjects_frame = frm = Subjects.Frame(parent=dock)
        dock.setWidget(frm)

    def __del__(self):
        self.__subjects_dock.deleteLater()

    @property
    def menus(self):
        return [self.__menu]

    @property
    def docks(self):
        return [
            ( self.__subjects_dock, Qt.RightDockWidgetArea )
        ]
