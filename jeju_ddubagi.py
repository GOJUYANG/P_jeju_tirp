import sys, os
import datetime

from bs4 import BeautifulSoup as bs
import requests

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

class Jeju(QMainWindow, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.counter = 0
        self.timer = QTimer()
        self.timer.start(800)
        self.timer.timeout.connect(self.change_start_img)

        # 정적페이지 크롤링(날씨)
        self.crawling_weather_naver()
        time_s, degree_s, status_s = self.time_degree_status('서귀포')
        time_j, degree_j, status_j = self.time_degree_status('제주도')
        dust_s, ultra_dust_s, uv_s, sunset_s = self.dust_uv_sunset('서귀포')
        dust_j, ultra_dust_j, uv_j, sunset_j = self.dust_uv_sunset('제주시')

        print(f"{self.find_area()[0]} 시간: {time_s}입니다.")
        print(f"서귀포시 온도: {degree_s.strip()}입니다.")
        print(f"서귀포시 상태: {status_s}가 내리는 중입니다.")
        print(f"서귀포시의 미세먼지는 {dust_s}")
        print(f"서귀포시의 초미세먼지는 {ultra_dust_s}")
        print(f"서귀포시의 자외선 정도는 {uv_s}")
        print(f"서귀포시의 일몰시간은 {sunset_s}")
        print("--")
        print(f"{self.find_area()[1]} 시간: {time_j}입니다.")
        print(f"제주시 온도: {degree_j.strip()}입니다.")
        print(f"제주시 상태: {status_j}가 내리는 중 입니다.")
        print(f"제주시의 미세먼지는 {dust_j}")
        print(f"제주시의 초미세먼지는 {ultra_dust_j}")
        print(f"제주시의 자외선 정도는 {uv_j}")
        print(f"제주시의 일몰시간은 {sunset_j}")


    def change_start_img(self):
        self.counter += 1
        if self.counter % 2 != 0:
            idx = 0
        else:
            idx = 1
        self.start_animation.setCurrentIndex(idx)


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Jeju()
    ex.show()
    app.exec_()