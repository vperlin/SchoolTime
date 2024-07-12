from PySide6.QtWidgets import QFrame, QVBoxLayout, QTableView, QDockWidget, QTreeView
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Slot, QAbstractItemModel

from enum import Enum

import data
from . import menu
from . import Subjects

import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


def trace(function):
    def traced_func(self, *args, **kwargs):
        call = f'{function.__name__}({args}, {kwargs})'
        result = function(self, *args, **kwargs)
        LOG.debug(f'{call} -> {result}')
        return result
    return traced_func


class Kind(Enum):
    GROUP = 0x20000000
    SUBJECT = 0x40000000
    TEACHER = 0x80000000
    KIND = 0xFF000000
    ITEM = 0x00FFFFFF


class Model(QAbstractItemModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__teachers = []
        self.__subjects = []

    def index(self, row, column, idx_parent=QModelIndex()):
        if not idx_parent.isValid():
            match row:
                case 0:
                    return self.createIndex(row, column, Kind.SUBJECT.value)
                case 1:
                    return self.createIndex(row, column, Kind.TEACHER.value)
                case _:
                    return QModelIndex()
        else:
            match idx_parent.internalId():
                case Kind.SUBJECT.value:
                    internal_id = Kind.SUBJECT.value | ( row + 1 )
                    return self.createIndex(row, column, internal_id)
                case Kind.TEACHER.value:
                    internal_id = Kind.TEACHER.value | ( row + 1 )
                    return self.createIndex(row, column, internal_id)
                case _:
                    return QModelIndex()

    def parent(self, idx):
        if idx.internalId() in { Kind.SUBJECT.value, Kind.TEACHER.value }:
            return QModelIndex()
        else:
            match idx.internalId() & Kind.KIND.value:
                case Kind.TEACHER.value:
                    return self.createIndex(1, 0, Kind.TEACHER.value)
                case Kind.SUBJECT.value:
                    return self.createIndex(0, 0, Kind.SUBJECT.value)
                case _:
                    return QModelIndex()

    def rowCount(self, idx_parent=QModelIndex()):
        if not idx_parent.isValid():
            return 2
        match idx_parent.internalId():
            case Kind.SUBJECT.value:
                return len(self.__subjects)
            case Kind.TEACHER.value:
                return len(self.__teachers)
            case _:
                return 0

    def columnCount(self, idx_parent=QModelIndex()):
        if not idx_parent.isValid():
            return 1
        match idx_parent.internalId():
            case Kind.SUBJECT.value:
                return 4
            case Kind.TEACHER.value:
                return 8
            case _:
                return 0

    def data(self, idx, role=Qt.DisplayRole):
        match role:
            case Qt.DisplayRole:
                match idx.internalId():
                    case Kind.SUBJECT.value:
                        return 'subjects'
                    case Kind.TEACHER.value:
                        return 'teachers'
                    case _:
                        match idx.internalId() & Kind.KIND.value:
                            case Kind.SUBJECT.value:
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
                            case Kind.TEACHER.value:
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
                            case _:
                                return '???'
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
        finally:
            self.endResetModel()


class View(QTreeView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__model = mdl = Model(parent=self)
        self.setModel(mdl)
        mdl.reload()

    def setModel(self, model):
        super().setModel(model)
        self.setRootIndex(model.index(1, 0))


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__menu = menu.Menu(parent=self)
        self.__layout = lay = QVBoxLayout(self)

        tbl = View(parent=self)
        lay.addWidget(tbl)

        dock = QDockWidget(self.tr('Subjects'), parent=self)
        self.__subjects_dock = dock
        #self.__subjects_frame = frm = Subjects.Frame(parent=dock)
        #dock.setWidget(frm)

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
