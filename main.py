from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib import request

WEB_DRIVER_PATH = "./chromedriver.exe"

s = Service(WEB_DRIVER_PATH)
# 드라이버 객체 생성 및 해당 드라이버에게 주소 get 명령
driver = webdriver.Chrome(service=s)
driver.get("https://static.wikia.nocookie.net/pokemon/images/f/fc/%EB%8F%84%ED%8A%B8_6XY_043.gif/revision/latest?cb=20140728063010&path-prefix=ko")
menu_img = driver.find_element(By.XPATH, "/html/body")
img_url = menu_img.find_element(By.TAG_NAME, "img").get_attribute("src")
request.urlretrieve(img_url, f'./img/뚜벅초.gif')
driver.close()