# -*- coding: utf-8 -*-
import random
import pymssql as pysql
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from para import Para


class SqlLoginWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.usr = Para.usr
        self.pwd = Para.pwd
        self.server = Para.server
        self.database = Para.database
        self.table_name = Para.table_name

        self.conn = None

        self.parent_ = parent

        self.info = "<div style='color:blue;'>No Infomation</div>"


        self.select_statement = lambda : 'select * from {}'.format(self.table_name)
        self.search_tables_statement = lambda : 'select name from sys.tables'

        self.data_list = []
        self.data_headers = []
        self.table_row = 0
        self.table_col = 0

        self.cur_cell_row = -1
        self.cur_cell_col = -1

        self.server_label = QLabel()
        self.server_edit = QLineEdit()

        self.usr_label = QLabel()
        self.usr_edit = QLineEdit()

        self.db_label = QLabel()
        self.db_edit = QLineEdit()

        self.pwd_label = QLabel()
        self.pwd_edit = QLineEdit()

        self.table_label = QLabel()
        self.table_editable_combo = QComboBox()
        self.combo_item_num = 0

        self.refresh_btn = QPushButton()
        self.confirm_btn = QPushButton()
        self.cancel_btn = QPushButton()
        self.quit_btn = QPushButton()
        

        self.horizontal_layout1 = QHBoxLayout()
        self.spacer1_left = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacer1_right = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout2 = QHBoxLayout()
        self.spacer2_left = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacer2_right = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout3 = QHBoxLayout()
        self.spacer3_left = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacer3_right = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.vbox_layout1 = QVBoxLayout()
        self.table_widget = QtWidgets.QTableWidget()
       # self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.info_label = QLabel()

        self.init_ui()
        self.retranslate_ui()
        self.set_reflect()

    def init_ui(self):
        '''
        给第一行添加服务器数据框和一个用户名输入框，并且在两侧安装弹簧使其挤向中间
        Add two input line which one for server input and another for user'name input.
        '''
        self.horizontal_layout1.addItem(self.spacer1_left) #左弹簧
        self.horizontal_layout1.addWidget(self.server_label) #服务器文字
        self.horizontal_layout1.addWidget(self.server_edit) #服务器编辑框
        self.horizontal_layout1.addWidget(self.usr_label)   #用户名文字
        self.horizontal_layout1.addWidget(self.usr_edit)  #用户名编辑框
        self.horizontal_layout1.addItem(self.spacer1_right)#右弹簧

        '''
        同上
        The same as last.
        '''
        self.horizontal_layout2.addItem(self.spacer2_left)
        self.horizontal_layout2.addWidget(self.db_label)
        self.horizontal_layout2.addWidget(self.db_edit)
        self.horizontal_layout2.addWidget(self.table_label)
        self.horizontal_layout2.addWidget(self.table_editable_combo)
        self.horizontal_layout2.addWidget(self.pwd_label)
        self.horizontal_layout2.addWidget(self.pwd_edit)
        self.horizontal_layout2.addItem(self.spacer2_right)

        """
        同上，只不过输入框变成了按钮
        The same as last except input box which instead of button
        """
        self.horizontal_layout3.addItem(self.spacer3_left)
        self.horizontal_layout3.addWidget(self.refresh_btn)
        self.horizontal_layout3.addWidget(self.confirm_btn)
        self.horizontal_layout3.addWidget(self.cancel_btn)
        self.horizontal_layout3.addWidget(self.quit_btn)
        self.horizontal_layout3.addItem(self.spacer3_right)
    
        '''
        conbination
        '''
        self.vbox_layout1.addLayout(self.horizontal_layout1)
        self.vbox_layout1.addLayout(self.horizontal_layout2)
        self.vbox_layout1.addLayout(self.horizontal_layout3)
        self.vbox_layout1.addWidget(self.table_widget)
        self.vbox_layout1.addWidget(self.info_label)

        self.setLayout(self.vbox_layout1)
        
        

    def retranslate_ui(self):
        self.server_label.setText('服务器')
        self.server_edit.setPlaceholderText(self.server)
        self.server_edit.setText(self.server)

        self.usr_label.setText('用户名')
        self.usr_edit.setPlaceholderText(self.usr)
        self.usr_edit.setText(self.usr)

        self.db_label.setText('数据库')
        self.db_edit.setPlaceholderText(self.database)
        self.db_edit.setText(self.database)

        self.table_label.setText('表名')
        self.table_editable_combo.setEditable(True)
        self.table_editable_combo.setPlaceholderText(self.table_name)
        self.table_editable_combo.setCurrentText(self.table_name)

        self.info_label.setText(self.info)
        self.info_label.resize(self.width(), 150)

        self.pwd_label.setText('密码')
        self.pwd_edit.setPlaceholderText(self.pwd)
        self.pwd_edit.setText(self.pwd)

        self.refresh_btn.setText('刷新')
        self.confirm_btn.setText('连接')
        self.cancel_btn.setText('取消')
        self.quit_btn.setText('关闭')

        self.setWindowTitle("登录窗口")
        self.resize(900, 600)
        

    def set_reflect(self):
        self.refresh_btn.clicked.connect(self.refresh_btn_clicked)
        self.confirm_btn.clicked.connect(self.confirm_btn_clicked)
        self.cancel_btn.clicked.connect(self.cancel_btn_clicked)
        self.quit_btn.clicked.connect(self.quit_btn_clicked)
        self.table_widget.cellPressed.connect(self.get_cell_pos)

    
        

    def connect_db(self):
        try:
            self.conn = pysql.connect(self.server, self.usr, self.pwd, self.database, charset='GBK')
            if self.conn:
                print('connect sucess')
            else :
                print('connect fault')
            return True
        except Exception as e:
            print('''connect fault, please check server name and database name
            your server name :{}
            your database :{}
            your user:{}
            your password:{}'''.format(self.server, self.database, self.usr, self.pwd))
            print(e)
            QMessageBox.information(self, 'Connect Error', e.__str__())
            return False
            
    def db_query(self):
        cursor = self.conn.cursor(as_dict=True)

        #get table
        cursor.execute(self.search_tables_statement())
        result = cursor.fetchall()
        i = self.combo_item_num
        while i > 0:
            self.table_editable_combo.removeItem(0)
            i -= 1
        self.combo_item_num = len(result)
        self.table_editable_combo.addItems([d['name'] for d in result])

        self.table_editable_combo.setCurrentText(self.table_name)

        #select
        print(self.select_statement())
        cursor.execute(self.select_statement())
        
        self.data_list = []
        for row in cursor:
            self.data_list.append(row)

        self.conn.close()
    
    def db_exec(self, statement : str):
        print(statement)
        try:
            self.connect_db()
            cursor = self.conn.cursor(as_dict=True)
            cursor.execute(statement)
            self.conn.commit()
        except Exception as e:
            print('there is some error')
            print(e)
            QMessageBox.information(self, 'Delete Error', e.__str__())

    def show_query(self):
        self.table_row = len(self.data_list)
        if self.table_row == 0:
            self.table_col = 0
        else:
            self.data_headers = list(self.data_list[0].keys())
            self.table_col = len(self.data_headers)

        self.table_widget.setColumnCount(self.table_col)
        self.table_widget.setRowCount(self.table_row)

        for i in range(self.table_row):
            item = QtWidgets.QTableWidgetItem()
            item.setText('{}'.format(i))
            self.table_widget.setVerticalHeaderItem(i, item)
        
        for i in range(self.table_col):
            item = QtWidgets.QTableWidgetItem()
            item.setText(self.data_headers[i])
            self.table_widget.setHorizontalHeaderItem(i, item)

        for i in range(self.table_row):
            for j in range(self.table_col):
                self.table_widget.setItem(i, j, 
                QtWidgets.QTableWidgetItem(
                    str(list( self.data_list[i].values()
                        )[j])
                        ))
        
 
    def cancel_btn_clicked(self):
        print('cancel')
        self.parent_.status = 'Input Cancel'

    def confirm_btn_clicked(self):
        self.server = self.server_edit.text()
        self.usr = self.usr_edit.text()
        self.pwd = self.pwd_edit.text()
        self.database = self.db_edit.text()
        self.table_name = self.table_editable_combo.currentText()

        if self.connect_db():
            self.parent_.status = 'Login Success'
            self.db_query()
            self.show_query()
        else :
            self.parent_.status = 'Login Fail'

    def refresh_btn_clicked(self):
        try:
            set_s = ''
            for i in range(self.table_col):
                set_s += self.data_headers[i]
                set_s += "='{}'".format(self.table_widget.item(self.cur_cell_row, i).text())
                if i != self.table_col - 1:
                    set_s += ','

            where_s = ''
            for i in range(self.table_col):
                where_s += self.data_headers[i]
                where_s += "='{}' ".format(self.data_list[self.cur_cell_row][self.data_headers[i]])
                if i != self.table_col - 1:
                    where_s += ' and '
                
            s = '''update {} set {} where {}'''.format(self.table_name, set_s, where_s)
            self.connect_db()
            self.db_exec(s)
            print(s)
        except Exception as e:
            print(e.__str__())
            QMessageBox.information(self.parent_, 'Error', e.__str__())

    def quit_btn_clicked(self):
        self.close()
        self.data_list = []
        self.show_query()
        self.parent_.status = 'Widget Quit'

    def get_cell_pos(self, row, col):
        self.cur_cell_row = row
        self.cur_cell_col = col
        self.parent_.choose_status = 'Current Choose--Row:{}, Col:{}'.format(row, col)

    def refresh_info(self, info : str):
        self.info_label.setText("<div style='color:blue;'>{}</div>".format(info))

    def sql_init(self):
        self.connect_db()
        cursor = self.conn.cursor(as_dict=True)
        cursor.execute('select * from t_classinfo')

        def delete_blank(s : str):
            ret = ''
            for ch in s:
                if ch != ' ':
                    ret += ch
            return ret
        
        class_dict = {}
        for row in cursor:
            class_dict[delete_blank(row['class_id'])] = delete_blank(row['class_name'])
        for stu_id in range(16):
            stu_id_str = '{:0>3d}'.format(stu_id)
            for cls_id in range(5):
                cls_id_str = '{:0>3d}'.format(cls_id)
                try:
                    cursor = self.conn.cursor()
                    s = '''insert into t_grade values('{}', '{}', '{}', '{}')'''.format(
                            random.randint(60, 98),
                            class_dict[cls_id_str],
                            cls_id_str,
                            stu_id_str)
                    
                    print(s)
                    cursor.execute(s)
                    self.conn.commit()
                except Exception as e:
                    print(e)
            s = '''insert into t_studentrelation values('{}', '{}')'''.format(
                '{:0>3d}'.format(random.randint(0, 4)),
                stu_id_str
            )
            try:
                cursor = self.conn.cursor()
                cursor.execute(s)
                self.conn.commit()
            except Exception as e:
                print(e)
                    