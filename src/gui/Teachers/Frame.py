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
            match idx_parent.internalId():
                case data.Kind.SUBJECT.value:
                    return self.createIndex(row, column,
                                            data.Kind.SUBJECT.value | 1)
                case data.Kind.TEACHER.value:
                    return self.createIndex(row, column,
                                            data.Kind.TEACHER.value | 1)
                case _:
                    LOG.warning('Unknown index()')
                    return QModelIndex()

    def parent(self, idx):
        if idx.internalId() in {data.Kind.SUBJECT.value,
                                data.Kind.TEACHER.value}:
            return QModelIndex()
        else:
            match idx.internalId() & data.Kind.KIND.value:
                case data.Kind.SUBJECT.value:
                    return self.createIndex(0, 0, data.Kind.SUBJECT.value)
                case data.Kind.TEACHER.value:
                    return self.createIndex(1, 0, data.Kind.TEACHER.value)
                case _:
                    LOG.warning('Unknown parent')
                    return QModelIndex()

    def rowCount(self, idx_parent=QModelIndex()):
        if not idx_parent.isValid():
            return 2
        match idx_parent.internalId():
            case data.Kind.SUBJECT.value:
                return len(self.__subjects)
            case data.Kind.TEACHER.value:
                return len(self.__teachers)
            case _:
                return 0

    def columnCount(self, idx_parent=QModelIndex()):
        if not idx_parent.isValid():
            return 1
        match idx_parent.internalId():
            case data.Kind.SUBJECT.value:
                return 4
            case data.Kind.TEACHER.value:
                return 8
            case _:
                return 0

    def data(self, idx, role=Qt.DisplayRole):
        match role:
            case Qt.DisplayRole:
                match idx.internalId():
                    case data.Kind.SUBJECT.value:
                        return self.tr('Subjects')
                    case data.Kind.TEACHER.value:
                        return self.tr('Teachers')
                    case _:
                        match idx.internalId() & data.Kind.KIND.value:
                            case data.Kind.TEACHER.value:
                                dt = self.__teachers[idx.row()]
                                match idx.column():
                                    case 0:
                                        return dt.iid
                                    case 1:
                                        return dt.last_name
                                    case 2:
                                        return dt.first_name
                                    case 3:
                                        return dt.middle_name
                                    case 4:
                                        return dt.phone
                                    case 5:
                                        return 'subjects'
                                    case 6:
                                        return 'класс'
                                    case 7:
                                        return dt.note
                                    case _:
                                        return None
                            case data.Kind.SUBJECT.value:
                                dt = self.__subjects[idx.row()]
                                match idx.column():
                                    case 0:
                                        return dt.iid
                                    case 1:
                                        return dt.code
                                    case 2:
                                        return dt.title
                                    case 3:
                                        return dt.note
                                    case _:
                                        return None
                            case _:
                                return None
            case _:
                return None

    @Slot()
    def reload(self):
        self.beginResetModel()
        try:

            with data.connect() as cursor:

                cursor.execute('''
                    select iid, code, title, note
                        from subjects ;
                ''')
                self.__subjects = [ data.Subject(**x) for x in cursor ]

                cursor.execute('''
                    select iid, last_name, first_name, middle_name, phone, note
                        from teachers ;
                ''')
                self.__teachers = [ data.Teacher(**x) for x in cursor ]

            # @TODO Возможны дополнительные операции

        finally:
            self.endResetModel()


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
