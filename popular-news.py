import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random
import os

# 봇 탐지 방지 설정
options = Options()
# UA = ("") # UA 값 변경 필요
# options.add_argument(f"user-agent={UA}") # User-Agent 값 입력
options.add_argument("--disable-blink-features=AutomationControlled") #navigator.webdriver 값 속이기(봇 아니예요)

# 사용자의 다운로드 폴더 경로를 찾기 위한 함수
def get_download_folder():
    home_dir = os.path.expanduser("~")  # 사용자의 홈 디렉토리 경로
    download_dir = os.path.join(home_dir, "Downloads")  # 다운로드 폴더 경로
    return download_dir

# 다운로드 경로 설정
download_folder = get_download_folder()
prefs = {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)

# Chrome WebDriver 생성
browser = webdriver.Chrome(options=options)
browser.maximize_window()

# 1. 페이지 이동(네이버 해외축구 스포츠 탭, 인기순)
title_texts = []

url = "https://sports.news.naver.com/wfootball/news/index?isphoto=N&type=popular&page="
for page in range(1, 20):
    browser.get(url + str(page))
    time.sleep(random.uniform(3, 5))
    news_list_element = browser.find_element(By.ID, "_newsList")
    title_elements = news_list_element.find_elements(By.CLASS_NAME, "title")
    
    for i in title_elements:
        title = i.text
        title_texts.append(title)
        print(f"현재 {page}페이지 완료")

# 수집한 데이터를 DataFrame으로 변환
data = {'Title': title_texts}
df = pd.DataFrame(data)

# CSV 파일로 저장
csv_file_path = os.path.join(download_folder, 'news_titles.csv')
df.to_csv(csv_file_path, index=False)

# 저장된 파일 경로 출력
print("CSV 파일이 저장되었습니다:", csv_file_path)