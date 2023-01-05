import requests
from bs4 import BeautifulSoup
import pyautogui

keyword = pyautogui.prompt('검색어를 입력하세요.')
lastPage = pyautogui.prompt('마지막 페이지 번호를 입력하세요.')
pageNum = 1
for i in range(1, int(lastPage) * 10, 10): #int형으로 lagePage 형변환
    print(f'{pageNum} 페이지 -----------------------------------')
    response = requests.get(f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={keyword}&start={i}')
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.select('.news_tit')
    for link in links:
        title = link.text
        url = link.attrs['href']
        print(title, url)
    pageNum = pageNum + 1