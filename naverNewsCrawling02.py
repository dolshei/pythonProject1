from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sys
import getpass

# username
username = getpass.getuser()

# save
sys.stdout = open('C:\\Users\\'+username+'\\Desktop\\news_data.txt','a', encoding='UTF-8')

# webdriver
path = 'C:\\Users\\'+username+'\\Desktop\\chromedriver.exe'
driver = webdriver.Chrome(path)
driver.implicitly_wait(3)


def title_search(url, date, page):
    url = url + date + '&page=' + str(page)
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 1. 기사제목
    title_list = []  # 기사제목
    for i in soup.find('div', {'class': 'list_body newsflash_body'}).find_all('a'):
        title_text = i.get_text(strip=True)
        # title_text = title_text.strip('\n''\t'' ') # \n, \t, 공백 문자열 제거
        # title_text = title_text.replace(' ','')
        # title_text = title_text.replace(',','')	# , 문자 제거
        # title_text = title_text.replace('"','')	# " 문자 제거
        title_list.append(title_text)
    title_list = list(filter(None, title_list))  # 빈 리스트 삭제

    # 2. href
    href_list = []  # href
    # href 주소
    for i in soup.find('div', {'class': 'list_body newsflash_body'}).find_all('li'):
        href_list.append([i.find('a')['href']])

    # 딕셔너리
    data_dic = dict(zip(title_list, href_list))

    return data_dic


# ------------------------------------------------------------------------------------------
# URL
url_date = '20220309'
url_page = 6  # max page(페이지 입력)
url = 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=259&mid=shm&sid1=101&date='
# ------------------------------------------------------------------------------------------


data_dic_all = dict()
# main
# title, href 서치
for page in range(url_page):
    result = title_search(url, url_date, page + 1)
    for i in list(result):
        if i in list(data_dic_all):
            del result[i]
    data_dic_all.update(result)


def content_search(url):
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    content_list = []
    for i in soup.find('div', {'id': 'articleBodyContents'}):
        content_text = i.get_text()
        content_text = content_text.strip('\n''\t'' ')  # \n, \t 문자열 제거
        content_text = content_text.replace('\'', '"')
        # content_text = content_text.replace(' ','')
        content_list.append(content_text)
    # content_list = [i.strip('\n') for i in content_list[:]]
    content_list = list(filter(None, content_list))
    content_list.remove(content_list[0])

    content = ''
    for i in content_list:
        content = content + ' ' + i

    return content


# 기사내용 서치
for i in data_dic_all:
    content = content_search(data_dic_all[i][0])
    data_dic_all[i].append(content)

# 결과
for i in data_dic_all:      # {'타이틀',['주소','기사내용']}
    print('뉴스 제목: ' + str(i))
    print('주소: ' + str(data_dic_all[i][0]))
    print('내용: ' + str(data_dic_all[i][1]))
    print('')

# webdriver 종료
driver.quit()