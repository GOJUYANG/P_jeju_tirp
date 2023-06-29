from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome WebDriver 경로 설정 (다운로드 필요)
WEB_DRIVER_PATH = "./chromedriver.exe"

# Chrome WebDriver 시작
s = Service(WEB_DRIVER_PATH)
driver = webdriver.Chrome(service=s)
driver.get("https://www.diningcode.com/list.dc?query=%EC%A0%9C%EC%A3%BC%EB%8F%84")
html = driver.find_element(By.TAG_NAME, 'html')

# 웹 페이지로 이동
driver.get("https://www.diningcode.com/list.dc?query=%EC%A0%9C%EC%A3%BC%EB%8F%84")

# '이용자층' 버튼 찾기
# button = WebDriverWait(driver, 9999).until(EC.presence_of_element_located((By.XPATH, "//button[text()='이용자층']")))
# button.click()

# '지역' 카테고리 열기
category_location = WebDriverWait(driver, 9999).until(EC.presence_of_element_located((By.XPATH, "//button[text()='지역']")))
category_location.click()

# '광역시도' 선택 (예시: 제주)
province = WebDriverWait(driver, 9999).until(EC.presence_of_element_located((By.XPATH, "//label[text()='광역시/도']/following-sibling::ul//label[text()='제주']")))
province.click()

#
# # '시군구' 선택 (예시: 제주시)
# city = WebDriverWait(driver, 9999).until(EC.presence_of_element_located((By.XPATH, "//label[text()='제주시']")))
# city.click()
#
# # '읍면동' 선택 (예시: 구좌읍)
# town = WebDriverWait(driver, 9999).until(EC.presence_of_element_located((By.XPATH, "//label[text()='구좌읍']")))
# town.click()



# 크롤링 코드 작성
# ...

# WebDriver 종료
driver.quit()
