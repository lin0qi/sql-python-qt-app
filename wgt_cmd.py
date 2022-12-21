# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

class WgtCmd(QtWidgets.QWidget):
    def __init__(self, sql_func=None, parent=None):
        super().__init__(parent)
        self.parent_ = parent
        self.sql_func = sql_func

        self.vertical_layout = QVBoxLayout()
        self.hlayout_cmd = QHBoxLayout()
        self.edit_cmd = QLineEdit()
        self.label_cmd = QLabel()

        self.hlayout_btn = QHBoxLayout()
        self.left_spacer_btn = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.confirm_btn = QPushButton()
        self.cancel_btn = QPushButton()
        self.right_spacer_btn = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.init_ui()
        self.retranslate_ui()
        self.set_reflect()

        
    def init_ui(self):
        '''
        add cmd line
        '''
        self.hlayout_cmd.addWidget(self.label_cmd)
        self.hlayout_cmd.addWidget(self.edit_cmd)

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
        self.vertical_layout.addLayout(self.hlayout_cmd)
        self.vertical_layout.addLayout(self.hlayout_btn)
        self.setLayout(self.vertical_layout)
        
    def retranslate_ui(self):
        self.label_cmd.setText('>:')
        self.edit_cmd.setText("print('hello world')")
        self.edit_cmd.setText("init")
        self.confirm_btn.setText('提交')
        self.cancel_btn.setText('关闭')

    def set_reflect(self):
        self.confirm_btn.clicked.connect(self.confirm_btn_clicked)
        self.cancel_btn.clicked.connect(self.cancel_btn_clicked)

    def confirm_btn_clicked(self):
        txt = self.edit_cmd.text()
        self.sql_func.pyexec(txt)

    def cancel_btn_clicked(self):
        self.close()
        
