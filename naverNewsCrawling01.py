from bs4 import BeautifulSoup
import requests
import openpyxl
from openpyxl import Workbook
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows

wb = Workbook()
sheet = wb.active
sheet.append(['발행일', '언론사', '기사제목', 'URL', '내용'])

p = {'중앙일보', '동아일보', '한겨레', '오마이뉴스언론사 선정', '조선일보', '경향일보', 'MBC', 'KBS', 'SBS'}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

# 1, 11, 21....91
for page in range(1, 70, 10):

    # Get 요청, naver 서버에 대화 시도
    response = requests.get(f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%9E%A5%EC%95%A0%EC%9D%B8%20%EC%9D%B4%EB%8F%99%EA%B6%8C%20%EC%8B%9C%EC%9C%84&sort=0&photo=0&field=0&pd=3&ds=2022.01.01&de=2022.01.31&cluster_rank=51&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20220101to20220131,a:all&start={page}')

    # 네이버에서 html 제공, text 메소드로 태그 내 텍스트만 추출
    html = response.text

    # html 번역선생님으로 수프 만듦
    soup = BeautifulSoup(html, 'html.parser')
    news = soup.select('div.news_wrap.api_ani_send')
    for n in news:
        title = n.select_one('a.news_tit').text
        press = n.select_one('a.info.press').text
        # date = n.select_one('span.info').text
        if press in p:
            try:
                url = n.select_one('div.info_group > a:nth-of-type(2)')['href']
            except:
                continue
            article = requests.get(url, headers=headers)
            article_html = BeautifulSoup(article.text, "html.parser")

            try:
                date = article_html.select_one('div.sponsor > span.t11').text
            except:
                continue
            try:
                content = article_html.select_one('div.content > div#articleBody > div#articleBodyContents').text
            except:
                continue
            sheet.append([date, press, title, url, content])
            # sheet.append([date, press, title,url])
        else:
            continue

# 간격조절
sheet.column_dimensions['A'].width = 10
sheet.column_dimensions['B'].width = 10
sheet.column_dimensions['C'].width = 30
sheet.column_dimensions['D'].width = 40
sheet.column_dimensions['E'].width = 50
wb.save(filename='2월.xlsx')