# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from sql_func import SqlFunc




app = QtWidgets.QApplication(sys.argv)
sql_login = SqlFunc()
sql_login.show()
sys.exit(app.exec_())

