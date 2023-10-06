import selenium
from selenium import webdriver as wd
import time
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime


title_text = []
category_text = []
population_text = []
result = {}

result_path = 'C:/Users/tlswo/Desktop/'
now = datetime.now()

driver = wd.Chrome('C:/Users/tlswo/Desktop/chromedriver.exe')
page = 1

while page <= 34:
    driver.get("https://www1.president.go.kr/petitions/best?page=%s" % (page))

    # 뷰티풀소프의 인자값 지정
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 청원 제목 추출
    sources = soup.select(
        "#cont_view > div.cs_area > div > div > div.board.text > div.b_list.category > div.bl_body > ul > li")
    for atag in sources:
        title_text.append(atag.find("div", class_="bl_subject").text[3:])

    # 청원 분류 추출
    for source in sources:
        category_text.append(source.find(
            "div", class_="bl_category cs").text[3:])

    # 청원 인원 추출
    for num in sources:
        temp = num.find("div", class_="bl_agree cb wv_agree").text[5:]
        clean = re.sub('명', "", temp)
        population_text.append(clean)

    df = pd.DataFrame({"category": category_text,
                       "title": title_text, "population": population_text})
    print(page)

    page += 1


# 파일 이름 지정
outputFileName = '%s-%s-%s  %s시 %s분 %s초 merging.xlsx' % (
    now.year, now.month, now.day, now.hour, now.minute, now.second)
df.to_excel(result_path + outputFileName, sheet_name='sheet1')
