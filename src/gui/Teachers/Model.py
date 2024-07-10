from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
import psycopg
import data


class Model(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__data = []

    def rowCount(self, idx_parent=QModelIndex()):
        if idx_parent.isValid():
            return 0
        return len(self.__data)

    def columnCount(self, idx_parent=QModelIndex()):
        if idx_parent.isValid():
            return 0
        return 7

    def data(self, idx, role):
        match role:
            case Qt.DisplayRole:
                dt = self.__data[idx.row()]
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
                        return dt.subjects
                    case 6:
                        return dt.note
                    case _:
                        return '???'
            case _:
                return None

    def load(self):
        with data.connect(psycopg.rows.class_row(data.Teacher)) as curs:
            curs.execute('''
select 
    iid, 
    last_name,
    first_name,
    middle_name,
    phone,
    note,
    sids as iids_subject,
    codes as codes_subject,
    false as is_new
   from teachers_info ;
            ''')
            
            self.beginResetModel()
            self.__data = list(curs)
            self.endResetModel()

    def load_new(self, filepath):
        