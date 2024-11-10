from PySide6.QtWidgets import QFrame, QRadioButton, QHBoxLayout
from PySide6.QtCore import Slot, Signal
import data


SELECT_SGROUPS = '''
   select
         iids_subgroup,
         titles_subgroup,
         iids_subject,
         codes_subject
      from subgroups_by_subjects
      where iid_sclass = %s ;
'''


class SubgroupsFrame(QFrame):
    
    subgroups_selected = Signal(list, list)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.__layout = lay = QHBoxLayout(self)
        
        lay.addStretch()
        
        self.__no_subgroups = btn = QRadioButton(self.tr('no subgroups'), self)
        btn.toggled.connect(self.on_nogroup_toggled)
        lay.addWidget(btn)
        
        self.__noname = btn = QRadioButton(self.tr('noname'), self)
        self.__noname_subgroup_ids = []
        self.__noname_subgroup_titles = None
        btn.toggled.connect(self.on_noname_toggled)
        lay.addWidget(btn)
        
        self.__other = []
       
        lay.addStretch()
        
    @Slot(int)
    def setSClassId(self, iid_sclass):
        self.__iid_sclass = iid_sclass
        self.__no_subgroups.setChecked(True)
        self.reload()
        
    def reload(self):
        self.__noname_subgroup_ids = []
        self.__noname_subgroup_titles = None
        for x in self.__other:
            x['button'].deleteLater()
        self.__other = []
        with data.connect() as cursor:
            cursor.execute(SELECT_SGROUPS, (self.__iid_sclass,))
            for x in cursor:
                if x['iids_subject'] is None:
                    self.__noname_subgroup_ids = x['iids_subgroup']
                    self.__noname_subgroup_titles = x['titles_subgroup']
                else:
                    btn = QRadioButton(x['codes_subject'], self)
                    self.__layout.insertWidget(3+len(self.__other), btn)
                    x['button'] = btn
                    btn.toggled.connect(self.on_sbj_toggled)
                    btn.setProperty('number', len(self.__other))
                    self.__other.append(x)

    @Slot(bool)
    def on_nogroup_toggled(self, checked):
        if checked:
            self.subgroups_selected.emit(None, None)
            
    @Slot(bool)
    def on_noname_toggled(self, checked):
        if checked:
            self.subgroups_selected.emit(self.__noname_subgroup_ids, None)
            
    @Slot(bool)
    def on_sbj_toggled(self, checked):
        if not checked: return
        btn = self.sender()
        number = btn.property('number')
        x = self.__other[number]
        sg_iids = x['iids_subgroup']
        sbj_iids = x['iids_subject']
        self.subgroups_selected.emit(sg_iids, sbj_iids)
