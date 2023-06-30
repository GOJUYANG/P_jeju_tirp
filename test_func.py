import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# Chrome WebDriver 경로 설정
webdriver_path = "./chromedriver.exe"

# Chrome WebDriver 서비스 설정
s = Service(webdriver_path)

# Chrome WebDriver 실행
driver = webdriver.Chrome(service=s)

# 웹 페이지로 이동
twenty_woman_url = "https://www.diningcode.com/list.dc?query=%EC%A0%9C%EC%A3%BC%EB%8F%84&keyword=%ED%98%BC%EB%B0%A5%2C%EC%97%AC%EC%84%B1%2C20%EB%8C%80"
twenty_man_url = "https://www.diningcode.com/list.dc?query=%EC%A0%9C%EC%A3%BC%EB%8F%84&keyword=%ED%98%BC%EB%B0%A5%2C20%EB%8C%80%2C%EB%82%A8%EC%84%B1"

thirty_woman_url = "https://www.diningcode.com/list.dc?query=%EC%A0%9C%EC%A3%BC%EB%8F%84&keyword=%ED%98%BC%EB%B0%A5%2C30%EB%8C%80%2C%EC%97%AC%EC%84%B1"
thirty_man_url = "https://www.diningcode.com/list.dc?query=%EC%A0%9C%EC%A3%BC%EB%8F%84&keyword=%ED%98%BC%EB%B0%A5%2C30%EB%8C%80%2C%EB%82%A8%EC%84%B1"

forty_woman_url = "https://www.diningcode.com/list.dc?query=%EC%A0%9C%EC%A3%BC%EB%8F%84&keyword=%ED%98%BC%EB%B0%A5%2C40%EB%8C%80%2C%EC%97%AC%EC%84%B1"
forty_man_url = "https://www.diningcode.com/list.dc?query=%EC%A0%9C%EC%A3%BC%EB%8F%84&keyword=%ED%98%BC%EB%B0%A5%2C%EB%82%A8%EC%84%B1%2C40%EB%8C%80"

driver.get(twenty_woman_url)

# '지역' 버튼 찾기
button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[text()='지역']")))
button.click()

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1)

province = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[text()='제주']")))
province.click()

city = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, f"//button[text()='서귀포시']")))
city.click()

town = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, f"//button/span[contains(text(), '중문')]")))
town.click()

choice_done =WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "Location__Popup__Submit")))
choice_done.click()

time.sleep(3)

info = driver.find_elements(By.CLASS_NAME, "Info")
img_list = driver.find_element(By.CLASS_NAME, "sc-gYrpUN eJNRnf Poi__List__Wrap")
img = img_list.find_elements(By.TAG_NAME, 'img')
img_source = []
for k in range(len(img)):
    img_source.append(img[k].get_attribute("src"))
print(img_source)

info_header = []
category = []
tag = []
rate = []

for i in range(len(info)):
    info_header.append(info[i].find_element(By.CLASS_NAME, "InfoHeader").text)
    category.append(info[i].find_element(By.CLASS_NAME, "Category").text)
    tag.append(info[i].find_element(By.CLASS_NAME, "Hash").text)
    rate.append(info[i].find_element(By.CLASS_NAME, "Rate").text)

print(info_header)
print(category)
print(tag)
print(rate)

while True:
    pass