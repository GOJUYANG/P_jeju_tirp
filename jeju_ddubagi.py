import sys, os
import time
import datetime
from dateutil.relativedelta import *

from bs4 import BeautifulSoup as bs
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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
main = resource_path('./qt/jeju.ui')
main_class = uic.loadUiType(main)[0]

class DataBase:
    con = sq3.connect("./database/jeju.db")
    cur = con.cursor()

    user_sex = cur.execute("select sex from USERS").fetchone()
    user_age_band = cur.execute("select age_band from USERS").fetchone()
    user_area = cur.execute("select area from USERS").fetchone()

class Loading(QDialog):
    def __init__(self, txt):
        super().__init__()
        self.ui = uic.loadUiType('./qt/loading.ui', self)

        self.setWindowTitle("안녕 낯선 여행자, 뚜벅이님!")
        self.setGeometry(750,400, 400,302)

        self.loading_img = QLabel(self)
        self.loading_img.resize(401,271)
        self.loading_img.move(0,0)

        movie = QMovie('./img/hourglass.gif')
        self.loading_img.setPixmap(QPixmap('./img/hourglass.gif'))
        self.loading_img.setMovie(movie)
        movie.start()

        self.loading_msg = QLabel(self)
        self.loading_msg.resize(401,31)
        self.loading_msg.move(0,270)

        self.loading_timer = QTimer(self)
        self.loading_timer.timeout.connect(self.txt_anim)
        self.loading_timer.start(100)
        self.current_index = 0

        if txt == '관광지':
            self.loading_txt = f"뚜벅이님을 위한 {txt} 검색 중.. 잠시만 기다려주세요..!"
        elif txt == '음식점':
            self.loading_txt = f"뚜벅이님을 위한 {txt} 검색 중.. 잠시만 기다려주세요..!"

        timer = QTimer(self)
        timer.timeout.connect(self.close)
        timer.start(6000)

    def txt_anim(self):
        if self.current_index < len(self.loading_txt):
            self.loading_msg.setText(self.loading_txt[:self.current_index + 1])
            self.current_index += 1
        else:
            self.loading_timer.stop()

        self.loading_msg.setFont(QFont('Neo둥근모 Pro', 10))
        self.loading_msg.setAlignment(Qt.AlignCenter)

    def center(self, e):
        super().showEvent(e)
        Jeju_window_rect = self.Jeju_window.geometry()
        Jeju_window_width = Jeju_window_rect.width()
        Jeju_window_height = Jeju_window_rect.height()

        loading_dlg_width = self.width()
        loading_dlg_height = self.height()

        dlg_x = Jeju_window_rect.x() + (Jeju_window_width + Jeju_window_height) // 2
        dlg_y = Jeju_window_rect.y() + (Jeju_window_width + Jeju_window_height) // 2

        self.setGeometry(dlg_x, dlg_y, loading_dlg_width, loading_dlg_height)

class Jeju(QMainWindow, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.counter = 0
        self.timer = QTimer()
        self.timer.start(800)
        self.timer.timeout.connect(self.change_start_img)

        #변수
        self.cnt = 0

       #QT 디자인 설정
        self.resize(561,888)
        self.setWindowTitle("뚜벅이용 제주도 관광명소 안내")
        movie_ = QMovie('./img/뚜벅초.gif')
        self.poketmon.setPixmap(QPixmap('./img/뚜벅초.gif'))
        self.poketmon.setMovie(movie_)
        movie_.start()
        self.setCursor(QCursor(QPixmap('./img/뚜벅초.png').scaled(80,80)))
        self.stackedWidget.setStyleSheet(
            "#start_page {"
            "background-color:blue;"
            "}"
            "#check_page,#facility_page,#food_page,#olleh_page {"
            "background-color: qlineargradient(spread:pad,x1:0.971591, y1:0.636, x2:1, y2:1,"
            "stop:0 rgba(85, 255, 127, 255),"
            " stop:1 rgba(255, 255, 255, 255));"
            "}"
        )
        self.shadow_1 = QGraphicsDropShadowEffect(self, blurRadius=9.0, offset=QPointF(1.0, 1.0))
        self.frame_date.setGraphicsEffect(self.shadow_1)
        self.shadow_2 = QGraphicsDropShadowEffect(self, blurRadius=9.0, offset=QPointF(1.0, 1.0))
        self.frame_age.setGraphicsEffect(self.shadow_2)
        self.shadow_3 = QGraphicsDropShadowEffect(self, blurRadius=9.0, offset=QPointF(1.0, 1.0))
        self.frame_area.setGraphicsEffect(self.shadow_3)

        #QT 값 설정
        self.cmb_month.currentIndexChanged.connect(lambda month=self.cmb_month.currentIndex(): self.choice_date(month))

        # 정적페이지 크롤링(날씨)
        self.crawling_weather_naver()
        time_s, degree_s, status_s = self.time_degree_status('서귀포')
        time_j, degree_j, status_j = self.time_degree_status('제주도')
        dust_s, ultra_dust_s, uv_s, sunset_s = self.dust_uv_sunset('서귀포')
        dust_j, ultra_dust_j, uv_j, sunset_j = self.dust_uv_sunset('제주시')

        self.suguipo_1.setText(f"지금 서귀포시는 {degree_s.strip()} {status_s}")
        self.suguipo_2.setText(f"지금 서귀포시는 {degree_s.strip()} {status_s}")
        self.suguipo_3.setText(f"지금 서귀포시는 {degree_s.strip()} {status_s}")

        self.jeju_1.setText(f"지금 제주시는  {degree_j.strip()} {status_j}")
        self.jeju_2.setText(f"지금 제주시는  {degree_j.strip()} {status_j}")
        self.jeju_3.setText(f"지금 제주시는  {degree_j.strip()} {status_j}")

        # print(f"{self.find_area()[0]} 시간: {time_s}입니다.")
        # print(f"서귀포시 온도: {degree_s.strip()}입니다.")
        # print(f"서귀포시 상태: {status_s}가 내리는 중입니다.")
        # print(f"서귀포시의 미세먼지는 {dust_s}")
        # print(f"서귀포시의 초미세먼지는 {ultra_dust_s}")
        # print(f"서귀포시의 자외선 정도는 {uv_s}")
        # print(f"서귀포시의 일몰시간은 {sunset_s}")
        # print("--")
        # print(f"{self.find_area()[1]} 시간: {time_j}입니다.")
        # print(f"제주시 온도: {degree_j.strip()}입니다.")
        # print(f"제주시 상태: {status_j}가 내리는 중 입니다.")
        # print(f"제주시의 미세먼지는 {dust_j}")
        # print(f"제주시의 초미세먼지는 {ultra_dust_j}")
        # print(f"제주시의 자외선 정도는 {uv_j}")
        # print(f"제주시의 일몰시간은 {sunset_j}")

        self.fir_insert_done.clicked.connect(self.user_tdate_sex_age_save)
        self.area_btn.clicked.connect(self.search_facility)
        self.attraction.clicked.connect(lambda _,obj_name=self.attraction.objectName().upper(): self.show_facility(obj_name))
        self.leisure.clicked.connect(lambda _,obj_name=self.leisure.objectName().upper(): self.show_facility(obj_name))
        self.camping.clicked.connect(lambda _,obj_name=self.camping.objectName().upper(): self.show_facility(obj_name))
        self.pharmacy.clicked.connect(lambda _,obj_name=self.pharmacy.objectName().upper(): self.show_facility(obj_name))
        self.fishing.clicked.connect(lambda _,obj_name=self.fishing.objectName().upper(): self.show_facility(obj_name))
        self.facility.clicked.connect(lambda _,obj_name=self.facility.objectName().upper(): self.show_facility(obj_name))
        self.next_pg.clicked.connect(self.show_food)


    def change_start_img(self):
        self.counter += 1
        if self.counter % 2 != 0:
            idx = 0
        else:
            idx = 1
        self.start_animation.setCurrentIndex(idx)

    def choice_date(self, idx):
        self.cmb_date.clear()
        today = datetime.datetime.today()
        month_first = datetime.datetime(today.year, today.month, 1) + relativedelta(months=idx+1)
        month_last = month_first + relativedelta(seconds=-1)
        month_last_date = month_last.strftime("%d")
        for i in range(1, int(month_last_date)+1):
            self.cmb_date.addItem(str(i))

    def user_tdate_sex_age_save(self):
        self.cnt += 1
        t_month = self.cmb_month.currentText()
        t_date = self.cmb_date.currentText()
        u_age = int(self.line_age.text())
        u_age_band = str((u_age//10)*10)+'대'
        if self.female.isChecked():
            DataBase.cur.execute(f"insert into USERS values({self.cnt}, '여성', '{u_age_band}', NULL)")
        elif self.male.isChecked():
            DataBase.cur.execute(f"insert into USERS values({self.cnt}, '남성', '{u_age_band}', NULL)")

        DataBase.con.commit()
        cur_date = DataBase.cur.execute("select * from USERS").fetchone()
        print(cur_date)

        self.stackedWidget.setCurrentIndex(2)

    #제주, 서귀포시 오늘의 날씨 검색
    def crawling_weather_naver(self):
        url_s = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%A0%9C%EC%A3%BC%EB%8F%84+%EC%84%9C%EA%B7%80%ED%8F%AC%EC%8B%9C+%EB%82%A0%EC%94%A8"
        html_s = requests.get(url_s)
        self.soup_s = bs(html_s.text, 'html.parser')

        url_j = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%A0%9C%EC%A3%BC%EB%8F%84+%EC%A0%9C%EC%A3%BC%EC%8B%9C+%EC%98%A4%EB%8A%98%EB%82%A0%EC%94%A8"
        html_j = requests.get(url_j)
        self.soup_j = bs(html_j.text, 'html.parser')

    def time_degree_status(self, area):
        now = datetime.datetime.now().strftime("%H시")
        #시간/상태/온도
        if area == '서귀포':
            data_1_s = self.soup_s.find('div', {'class': 'graph_inner _hourly_weather'})
            data_time_statue_temper_s = data_1_s.findAll('dl')
            data_time_s = data_1_s.findAll('dt', {'class': 'time'})
            data_degree_s = data_1_s.findAll('dd', {'class':'degree_point'})
            data_status_s = data_1_s.findAll('span', {'class':'blind'})

        elif area == '제주도':
            data_1_j = self.soup_j.find('div', {'class': 'graph_inner _hourly_weather'})
            data_time_statue_temper_s = data_1_j.findAll('dl')
            data_time_s = data_1_j.findAll('dt', {'class': 'time'})
            data_degree_s = data_1_j.findAll('dd', {'class':'degree_point'})
            data_status_s = data_1_j.findAll('span', {'class':'blind'})

        for i in range(len(data_time_s)):
            if now == data_time_s[i].text:
                return data_time_s[i].text, data_degree_s[i].text, data_status_s[i].text

    def dust_uv_sunset(self, area):
        #미세먼지/초미세먼지/자외선상태/일몰시간

        if area == '서귀포':
            data_2_s = self.soup_s.find('ul', {'class': 'today_chart_list'})
            data_4_s = data_2_s.findAll('li')
            dust_level = data_4_s[0].find('span', {'class':'txt'}).text
            ultra_dust_level = data_4_s[1].find('span', {'class':'txt'}).text
            uv_rays = data_4_s[2].find('span', {'class':'txt'}).text
            sunset_time = data_4_s[3].find('span', {'class':'txt'}).text
            return dust_level, ultra_dust_level, uv_rays, sunset_time

        elif area == '제주시':
            data_2_j = self.soup_j.find('ul', {'class': 'today_chart_list'})
            data_4_j = data_2_j.findAll('li')
            dust_level = data_4_j[0].find('span', {'class': 'txt'}).text
            ultra_dust_level = data_4_j[1].find('span', {'class': 'txt'}).text
            uv_rays = data_4_j[2].find('span', {'class': 'txt'}).text
            sunset_time = data_4_j[3].find('span', {'class': 'txt'}).text
            return dust_level, ultra_dust_level, uv_rays, sunset_time

    def find_area(self):
        #지역
        data_3_s = self.soup_s.find('div', {'class': 'title_area _area_panel'})
        area_name_suguipo = data_3_s.find('h2', {'class': 'blind'}).text
        data_3_j = self.soup_j.find('div', {'class': 'title_area _area_panel'})
        area_name_jejusi = data_3_j.find('h2', {'class': 'blind'}).text

        return area_name_suguipo, area_name_jejusi

    def search_facility(self):
        txt = '관광지'
        loading_dlg = Loading(txt)
        loading_dlg.exec_()
        area = self.user_area.text()
        DataBase.cur.execute(f"update USERS set area = '{area}' where idx = 1")
        DataBase.con.commit()

    def show_facility(self, obj_name):
        area = self.user_area.text()

        if obj_name == 'PHARMACY':
            valuse = DataBase.cur.execute(
                f"select 안전시설명, 안전시설유형, 지번주소 from '{obj_name}' where 읍면동명 = '{area[-3:]}'").fetchall()
            self.hashtag_list.setHorizontalHeaderLabels(['안전시설명','안전시설유형','지번주소'])

        elif obj_name == 'FACILITY':
            valuse = DataBase.cur.execute(
                f"select 편의시설명, 편의시설유형, 지번주소 from '{obj_name}' where 읍면동명 = '{area[-3:]}'").fetchall()
            self.hashtag_list.setHorizontalHeaderLabels(['편의시설명', '편의시설유형', '지번주소'])

        else:
            valuse = DataBase.cur.execute(
                f"select 관광지명, 관광지유형, 지번주소 from '{obj_name}' where 읍면동명 = '{area[-3:]}'").fetchall()
            self.hashtag_list.setHorizontalHeaderLabels(['관광지명', '관광지유형', '지번주소'])

        if not valuse:
            self.hashtag_list.insertRow(0)
            self.hashtag_list.setItem(0, 0, QTableWidgetItem('-'))
            self.hashtag_list.setItem(0, 1, QTableWidgetItem('-'))
            self.hashtag_list.setItem(0, 2, QTableWidgetItem('해당 지역에 낚시터가 없습니다'))
            self.hashtag_list.setHorizontalHeaderLabels(['관광지명', '관광지유형', '지번주소'])
        else:
            self.hashtag_list.clearContents()
            self.hashtag_list.setRowCount(0)
            for value in valuse:
                rowposition = self.hashtag_list.rowCount()
                self.hashtag_list.insertRow(rowposition)
                t_name, t_type, t_address = value[0], value[1], value[2]
                self.hashtag_list.setItem(rowposition, 0, QTableWidgetItem(t_name))
                self.hashtag_list.setItem(rowposition, 1, QTableWidgetItem(t_type))
                self.hashtag_list.setItem(rowposition, 2, QTableWidgetItem(t_address))

    def show_food(self):
        txt = '음식점'
        loading_dlg = Loading(txt)
        loading_dlg.exec_()

        self.lb_area.setText(f"{DataBase.user_area[0]}")
        self.lb_age_band.setText(f"#{DataBase.user_age_band[0]}")
        self.lb_sex.setText(f"#{DataBase.user_sex[0]}")

        self.choice_url_type()

        self.stackedWidget.setCurrentIndex(3)


    def choice_url_type(self):
        """user table에 저장된 내용과 비교하여 일치하는 url 반환"""
        type_sex = self.lb_sex.text()
        type_age = self.lb_age_band.text()
        type_area = self.lb_area.text()

        if type_sex == '여성':
            if type_age == '20대':
                url = "https://www.diningcode.com/list.dc?query=%EC%A0%9C%EC%A3%BC%EB%8F%84&keyword=%ED%98%BC%EB%B0%A5%2C%EC%97%AC%EC%84%B1%2C20%EB%8C%80"
            elif type_age == '30대':
                url = "https://www.diningcode.com/list.dc?query=%EC%A0%9C%EC%A3%BC%EB%8F%84&keyword=%ED%98%BC%EB%B0%A5%2C30%EB%8C%80%2C%EC%97%AC%EC%84%B1"
            elif type_age == '40대':
                url = "https://www.diningcode.com/list.dc?query=%EC%A0%9C%EC%A3%BC%EB%8F%84&keyword=%ED%98%BC%EB%B0%A5%2C40%EB%8C%80%2C%EC%97%AC%EC%84%B1"
        else:
            if type_age == '20대':
                url = "https://www.diningcode.com/list.dc?query=%EC%A0%9C%EC%A3%BC%EB%8F%84&keyword=%ED%98%BC%EB%B0%A5%2C20%EB%8C%80%2C%EB%82%A8%EC%84%B1"
            elif type_age == '30대':
                url = "https://www.diningcode.com/list.dc?query=%EC%A0%9C%EC%A3%BC%EB%8F%84&keyword=%ED%98%BC%EB%B0%A5%2C30%EB%8C%80%2C%EB%82%A8%EC%84%B1"
            elif type_age == '40대':
                url = "https://www.diningcode.com/list.dc?query=%EC%A0%9C%EC%A3%BC%EB%8F%84&keyword=%ED%98%BC%EB%B0%A5%2C%EB%82%A8%EC%84%B1%2C40%EB%8C%80"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Jeju()
    ex.show()
    app.exec_()