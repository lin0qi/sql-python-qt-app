# -*- coding: utf-8 -*-
from typing import Dict, List
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

class WgtAddLine(QtWidgets.QWidget):
    def __init__(self, sql_func=None, parent=None):
        super().__init__(parent)
        self.parent_ = parent
        self.sql_func = sql_func
        
        self.data_headers : List[str]= sql_func.login_wgt.data_headers
        self.post_data : Dict[str, str] = {}
        self.confirm_event : function = lambda : 0

        self.vertical_layout = QVBoxLayout()
        self.edit_dict : Dict[str, QLineEdit] = {}
        self.label_dict : Dict[str, QLabel] = {}
        self.hlayout_dict : Dict[str, QHBoxLayout] = {}
        self.left_spacer_dict : Dict[str, QSpacerItem] = {}
        self.right_spacer_dict : Dict[str, QSpacerItem] = {}

        self.hlayout_btn = QHBoxLayout()
        self.left_spacer_btn = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.confirm_btn = QPushButton()
        self.cancel_btn = QPushButton()
        self.right_spacer_btn = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)


        for header in self.data_headers:
            self.hlayout_dict[header] = QHBoxLayout()
            self.edit_dict[header] = QLineEdit()
            self.label_dict[header] = QLabel()
            self.left_spacer_dict[header] = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.right_spacer_dict[header] = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.init_ui()
        self.retranslate_ui()
        self.set_reflect()

    def show(self):
        self.__init__(sql_func=self.sql_func)
        super().show()

        
    def init_ui(self):
        '''
        使用循环添加多个输入框
        Add input boxes with loop
        '''
        for header in self.data_headers:
            self.hlayout_dict[header].addSpacerItem(self.left_spacer_dict[header])
            self.hlayout_dict[header].addWidget(self.label_dict[header])
            self.hlayout_dict[header].addWidget(self.edit_dict[header])
            self.hlayout_dict[header].addSpacerItem(self.right_spacer_dict[header])

            self.vertical_layout.addLayout(self.hlayout_dict[header])

        '''
        添加按钮和弹簧
        Add button and spacer
        '''
        self.hlayout_btn.addSpacerItem(self.left_spacer_btn)
        self.hlayout_btn.addWidget(self.confirm_btn)
        self.hlayout_btn.addWidget(self.cancel_btn)
        self.hlayout_btn.addSpacerItem(self.right_spacer_btn)
        
        '''
        别动
        dont change it
        '''
        self.vertical_layout.addLayout(self.hlayout_btn)
        self.setLayout(self.vertical_layout)
        
    def retranslate_ui(self):
        for header in self.data_headers:
            self.label_dict[header].setText(header)
        self.confirm_btn.setText('提交')
        self.cancel_btn.setText('取消')

    def set_reflect(self):
        self.confirm_btn.clicked.connect(self.confirm_btn_clicked)
        self.cancel_btn.clicked.connect(self.cancel_btn_clicked)

    def confirm_btn_clicked(self):
        statement = 'insert into {} values('.format(self.sql_func.login_wgt.table_name)
        for header in self.data_headers:
            self.post_data[header] = self.edit_dict[header].text()
        for i in range(len(self.data_headers)):
            statement += "'{}'".format(self.post_data[self.data_headers[i]])
            if i < len(self.data_headers) - 1:
                statement += ','
            else :
                statement += ');'
        
        self.sql_func.login_wgt.db_exec(statement)
        self.sql_func.login_wgt.data_list.append(self.post_data)
        self.sql_func.login_wgt.show_query()
        self.sql_func.status = 'add line'
        self.close()

    def cancel_btn_clicked(self):
        self.close()
        