#!/usr/bin/env python
# coding: utf-8

# In[25]:


from selenium import webdriver as wd
import time
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


# In[26]:

p_name = input("신문사 입력: ")
c_name = input("분야 입력: ")
s_date = input("시작 날짜 입력(2021.11.11): ")
period = int(input("검색 일수 기간(30): "))

s_date = s_date.replace('.', '')
driver = wd.Chrome('C:/Users/tlswo/Desktop/chromedriver.exe')

result_path = 'C:/Users/tlswo/Desktop/'
now = datetime.now()


# In[27]:


# In[28]:


# 날짜 변환 코드
def decr_date(x):
    year = x[0:4]
    month = int(x[4:6])
    day = int(x[6:])

    if day > 1:
        day -= 1
    else:
        month -= 1
        if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
            day = 31
        elif month == 4 or 6 or 9 or 11:
            day = 30
        else:
            day = 28

    month = str(month).zfill(2)
    day = str(day).zfill(2)
    date = year+month+day

    return date


# In[29]:


# 신문사 코드
def press_code(x):
    press_num = {"경향신문": 11, "국민일보": 45, '뉴스1': 396, '뉴시스': 21, '동아일보': 190, '연합뉴스': 2, '조선일보': 200,
                 '중앙일보': 8, '한겨례': 17, '한국일보': 49, "EBS": 244, "JTBC": 310, "KBS": 327, "KTV": 75, "MBC": 98,
                 "MBN": 60, "SBS": 73, "SBS Biz": 189, "YTN": 23, "연합뉴스tv": 318, "채널A": 317, "한국경제TV": 134}.get(x, "default")
    return press_num


press_num = press_code(p_name)


# In[30]:


# 분야별 코드
def category_code(x):
    category_num = {"사회": 1001, "정치": 1002, "경제": 1006, "국제": 1007, "문화": 1003,
                    "연예": 1005, "스포츠": 1004, "IT": 1008, "칼럼": 1009}.get(x, "default")
    return category_num


category_num = category_code(c_name)


# In[31]:


title_text = []
press_text = []
time_text = []
temp_title = ""


page = 1
#idx = 1


# In[32]:


for i in range(period):

    while True:

        driver.get(('https://news.daum.net/cp/%s?page=%s&cateId=%s&regDate=%s') %
                   (press_num, page, category_num, s_date))

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        sources = soup.select('#mArticle > div.box_etc > ul > li')

        if sources[-1].find('a', class_='link_txt').text == temp_title:
            break

        for atag in sources:
            title_text.append(atag.find('a', class_='link_txt').text)

        for info in sources:
            press_text.append(
                info.find("span", class_="info_news").text.split('·')[0])
            time_text.append(
                info.find("span", class_="info_news").text.split('·')[1])

        df = pd.DataFrame({"category": c_name, "title": title_text,
                          'press': press_text, 'period': time_text})

        print(page)

        temp_title = title_text[-1]

        page += 1
        #idx += 1

    #idx = 1
    page = 1
    s_date = str(s_date)
    s_date = decr_date(s_date)
    print(s_date)


driver.close()

outputFileName = '%s-%s-%s  %s시 %s분 %s초 merging.xlsx' % (
    now.year, now.month, now.day, now.hour, now.minute, now.second)
df.to_excel(result_path + outputFileName, sheet_name='sheet1')
