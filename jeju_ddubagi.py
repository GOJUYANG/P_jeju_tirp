import sys, os
import numpy as np
import pandas as pd
import sqlite3 as sq3

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# 메인화면
main = resource_path('../qt/waffle_universe_start.ui')
main_class = uic.loadUiType(main)[0]

class DataBase:
    con = sq3.connect("./database/jeju.db")

class Jeju(QMainWindow, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi()

#변수ZONE
        #초기화 설정 변수

#함수ZONE

    #화면 어느 곳을 클릭하면 시작화면에서 사용자 입력화면으로 전환


    #여행일자/여행인원/성별 및 연령대 입력내용 오입력, 누락내용 없는지 확인
    def insert_none_check(self):
        for i in range(3):
            self.user_insert_text = self.user_info_widget.findChildren(QLineEdit)
            self.user_insert_text[i]


    #여행일자/여행인원/성별 및 연령대 입력내용 DB저장

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Jeju()
    ex.show()
    app.exec_()