import requests
from bs4 import BeautifulSoup

response = requests.get('https://search.naver.com/search.naver?display=15&f=&filetype=0&page=11&query=%ED%8C%8C%EC%9D%B4%EC%8D%AC&research_url=&sm=tab_pge&start=1&where=web')
search_page = response.text

soup = BeautifulSoup(search_page, 'html.parser')
titles = soup.select('div > div.total_tit_group > div.total_tit > a')
desc = soup.select('div > div.total_group > div.total_dsc_wrap > a > div.api_txt_lines dsc_txt')

for title in titles:
    print(title.get_text())
