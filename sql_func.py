# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from sql_login_wgt import SqlLoginWidget
from wgt_add_line import WgtAddLine
from wgt_cmd import WgtCmd
from para import Para

class SqlFunc(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.version = Para.version
        self.status = 'Unlogin'
        self.choose_status = 'No Choose'
        self.python_status = 'No Python'
        self.default_output = 'No Information'
        self.mean_of_column = 'No Mean'

        '''
        menubar
        '''
        #first menu File
        self.menu_file = QMenu()
        self.action_quit = QAction()

        #second menu Edit
        self.menu_edit = QMenu()
        self.action_new_line = QAction()
        self.action_delete_line = QAction()

        #third menu Project
        self.menu_proj = QMenu()
        self.action_new_wgt = QAction()
        self.action_quit_wgt = QAction()

        #forth menu Tool
        self.menu_tool = QMenu()
        self.action_stats = QAction()
        self.action_avg = QAction()
        self.action_new_cmd = QAction()
        self.action_people_stats = QAction()
        self.action_avg_grade = QAction()

        '''
        tool bar
        '''


        '''
        central widget
        '''
        self.login_wgt = SqlLoginWidget(self)
        '''
        other widget
        '''
        self.add_wgt = WgtAddLine(sql_func=self)

        '''
        cmd widget
        '''
        self.cmd_wgt = WgtCmd(sql_func=self)


        '''
        status bar
        '''
        self.status_bar = QStatusBar()

        self.init_ui()
        self.retranslate_ui()
        self.set_reflect()

    def event(self, e : QtCore.QEvent):
        try:
            self.status_show()
        except Exception:
            pass
        return super().event(e)

    def init_ui(self):
        '''
        central widget init
        初始化中间那个表格
        '''
        self.setCentralWidget(self.login_wgt)

        '''
        menubar init
        add four menu to menubar
        添加4个菜单栏
        '''
        self.menuBar().addMenu(self.menu_file)
        self.menuBar().addMenu(self.menu_edit)
        self.menuBar().addMenu(self.menu_proj)
        self.menuBar().addMenu(self.menu_tool)

        '''
        submenu (action) init
        add action to 4 menu
        给4个菜单栏添加二级菜单
        '''
        self.menu_file.addAction(self.action_quit)
        self.menu_edit.addAction(self.action_new_line)
        self.menu_edit.addAction(self.action_delete_line)
        self.menu_proj.addAction(self.action_new_wgt)
        self.menu_proj.addAction(self.action_quit_wgt)
        self.menu_tool.addAction(self.action_new_cmd)
        self.menu_tool.addAction(self.action_stats)
        self.menu_tool.addAction(self.action_avg)
        self.menu_tool.addAction(self.action_people_stats)
        self.menu_tool.addAction(self.action_avg_grade)

        '''
        toolbar init
        工具栏
        '''


        '''
        status bar init
        状态栏
        '''
        self.setStatusBar(self.status_bar)      
        '''
        设置窗口大小
        resize window
        '''
        self.resize(900, 600)
    
    def retranslate_ui(self):
        '''
        menubar title translate
        menubar text
        菜单栏显示的文字
        '''
        self.menu_file.setTitle('&File')
        self.menu_edit.setTitle('&Edit')
        self.menu_tool.setTitle('&Tool')
        self.menu_proj.setTitle('&Project')

        '''
        action translate
        submenu text
        二级菜单文字
        '''
        self.action_quit.setText(           'Quit               Esc')
        self.action_new_wgt.setText(        'New Widget            ')
        self.action_quit_wgt.setText(       'Quit Widget           ')
        self.action_new_line.setText(       'New Line              ')
        self.action_delete_line.setText(    'Delete Line          D')
        self.action_new_cmd.setText(        'Open Cmd        Ctrl+P')
        self.action_stats.setText(          'Stats           Ctrl+X')
        self.action_avg.setText(            'Average         Ctrl+V')
        self.action_people_stats.setText(   'People Stats          ')
        self.action_avg_grade.setText(      'Avg Grade             ')

        '''
        toolbar translate
        '''

        '''
        widget show
        widget of database add line
        数据库添加的弹窗
        '''
        self.add_wgt.close()


        '''
        cmd 
        '''
        self.cmd_wgt.close()


        '''
        status bar tanslate
        状态栏显示
        '''
        self.status_show()


    def set_reflect(self):
        self.action_new_cmd.triggered.connect(self.input_cmd)
        self.action_quit.triggered.connect(self.close)
        self.action_new_wgt.triggered.connect(self.show_wgt)
        self.action_quit_wgt.triggered.connect(self.close_wgt)
        self.action_delete_line.triggered.connect(self.wgt_delete_line)
        self.action_new_line.triggered.connect(self.wgt_add_line)
        self.action_stats.triggered.connect(self.statics)
        self.action_avg.triggered.connect(self.get_average)
        self.action_people_stats.triggered.connect(self.people_stats)
        self.action_avg_grade.triggered.connect(self.get_avg_grade)

    def keyPressEvent(self, e : QtGui.QKeyEvent) -> None:
        if e.key() == QtCore.Qt.Key.Key_D:
            self.wgt_delete_line()
        elif e.key() == QtCore.Qt.Key.Key_Enter:
            self.login_wgt.confirm_btn_clicked()
        elif e.key() == QtCore.Qt.Key.Key_F5:
            self.login_wgt.confirm_btn_clicked()
        elif e.key() == QtCore.Qt.Key.Key_X:
            if QApplication.keyboardModifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
                self.statics()
        elif e.key() == QtCore.Qt.Key.Key_V:
            if QApplication.keyboardModifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
                self.get_average()
        elif e.key() == QtCore.Qt.Key.Key_P:
            if QApplication.keyboardModifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
                self.input_cmd()
        elif e.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        return super().keyPressEvent(e)

    
        

    def show_wgt(self):
        self.login_wgt.show()
        self.status = 'Unlogin'
    def close_wgt(self):
        self.login_wgt.quit_btn_clicked()
    def wgt_delete_line(self):
        
        s = "delete from {} where {}='{}'".format(
            self.login_wgt.table_name,
            self.login_wgt.data_headers[0],
            self.login_wgt.table_widget.item(self.login_wgt.cur_cell_row, 0).text()
            )
        self.login_wgt.table_widget.removeRow(self.login_wgt.cur_cell_row)

        self.login_wgt.db_exec(s)
        
    def wgt_add_line(self):
        self.add_wgt.show()

    def input_cmd(self):
        self.cmd_wgt.show()
        self.status = 'Cmd Input'

    def statics(self):
        self.login_wgt.data_list.sort(
            key=lambda x : x[self.login_wgt.data_headers[self.login_wgt.cur_cell_col]])
        self.login_wgt.show_query()

    def get_average(self):
        try:
            key = self.login_wgt.data_headers[self.login_wgt.cur_cell_col]
            sum, data_len = 0., len(self.login_wgt.data_list)
            for data_row in self.login_wgt.data_list:
                try:
                    sum += float(data_row[key])
                except Exception as e:
                    QMessageBox.information(self, 'Error', e.__str__())
                    self.python_status = 'Python Convert Error'

                    self.mean_of_column = 'Cacul Error'
                    return
                    
            self.mean_of_column = 'Column Mean:' + str(sum / data_len)
            self.python_status = 'Python Normal'
            self.login_wgt.refresh_info(self.mean_of_column)
        except Exception as e:
            print(e.__str__())
            QMessageBox.information(self, 'Error', 'your table should be format')
            

        
    def people_stats(self):
        try:
            self.login_wgt.connect_db()
            cursor = self.login_wgt.conn.cursor(as_dict=True)

            #select
            cursor.execute('select * from t_classinfo')
            
            class_dict, class_people_dict = {}, {}
            for row in cursor:
                class_dict[row['class_id']] = row['class_name']
                class_people_dict[row['class_id']] = 0

            cursor.execute('select * from t_grade')
            
            for row in cursor:
                class_people_dict[row['class_id']] += 1

            people_stats_info = ''
            for k, v in class_people_dict.items():
                people_stats_info += '{}--{} | '.format(
                    class_dict[k],
                    v
                )
            self.python_status = 'Python Normal'
            self.login_wgt.refresh_info(people_stats_info)
        except Exception as e:
            print(e.__str__())
            QMessageBox.information(self, 'Error', 'your table should be format')


    def get_avg_grade(self):
        self.login_wgt.connect_db()
        cursor = self.login_wgt.conn.cursor(as_dict=True)

        cls_grade_dict = {}
        cls_choose_dict = {}

        cursor.execute('select * from t_grade')
        for row in cursor:
            if row['class_name'] not in cls_grade_dict.keys():
                cls_grade_dict[row['class_name']] = 0.
                cls_choose_dict[row['class_name']] = 0
            else :
                try:
                    cls_grade_dict[row['class_name']] += float(row['class_grade'])
                    cls_choose_dict[row['class_name']] += 1
                except Exception as e:
                    QMessageBox.information(self, 'Error', e.__str__())
                    self.python_status = 'Python Error'
                    return
        avg_info = ''
        for k, v in cls_grade_dict.items():
            avg_info += '''{}--{:.3f} | '''.format(
                k, v / cls_choose_dict[k]
            )
        self.login_wgt.refresh_info(avg_info)
        self.mean_of_column = 'Multiple'
        self.python_status = 'Python Normal'


    def pyexec(self, s : str):
        if(s == 'init'):
            self.login_wgt.sql_init()
            self.python_status = 'Python Init'
        elif(s == 'new'):
            self.wgt_add_line()
        elif s == 'quit':
            self.cmd_wgt.close()
        else :
            try:
                exec(s)
            except Exception as e:
                print(e.__str__())
                QMessageBox.information(self, 'Error', e.__str__())

    def statusbar_show(self, s : str):
        self.status_bar.showMessage(self.version + ' | ' + s, 0)

    def status_show(self):
        self.statusbar_show(self.status + ' | ' + 
        self.choose_status + ' | ' + 
        self.python_status + ' | ' + 
        self.mean_of_column)


