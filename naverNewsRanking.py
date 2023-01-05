import requests  # 서버 접속
from bs4 import BeautifulSoup  # HTML 해석
from datetime import datetime  # 오늘의 날짜
import pandas as pd  # 데이터 프레임(표) 만들기

url = "https://news.naver.com/main/ranking/popularDay.naver"  # 네이버 뉴스 랭킹 사이트
headers = {"User-Agent": "Mozilla/5.0"}  # user-agent 를 입력하지 않으면 오류
# user-agent의 값은 https://www.whatismybrowser.com/detect/what-is-my-user-agent에 들어가면 됨
res = requests.get(url, headers=headers)  # 서버 접속
soup = BeautifulSoup(res.text, "html.parser")  # html 해석

all_box = soup.find_all("div", attrs={"class": "rankingnews_box"})  # 신문사별 1~5위 데이터 담긴 div 모두 가져오기

lst_all_data = []  # 모든 데이터 담을 리스트
count = 1  # 몇번째 반복인지 알기 위한 count 변수
for box in all_box:  # 각 신문사별 1~5위 데이터 접근
    company_name = box.strong.text  # 신문사 이름
    lst_all_rank = box.find_all("li")  # 1~5위 li 모두 가져오기
    num_rank = 1  # 뉴스 랭킹 1위부터 입력
    for rank in lst_all_rank:  # 1~5위 각각 접근
        lst_data = []  # 각 데이터 담을 리스트
        lst_data.append(datetime.now().strftime("%Y-%m-%d"))  # 오늘의 날짜 "2022-03-04" 형식으로 lst_data에 추가
        lst_data.append(company_name)  # 회사 이름 lst_data에 추가
        if rank.a == None:  # 만약 데이터가 없는 경우 다음 신문사로 넘어가기 / all_box[66]이 이에 해당
            continue
        lst_data.append(num_rank)  # 뉴스 랭킹 lst_data에 추가
        lst_data.append(rank.a.text)  # 뉴스 타이틀 lst_data에 추가
        lst_data.append(rank.a["href"])  # 뉴스 링크 lst_data에 추가
        num_rank += 1  # 뉴스 랭킹 +1 추가
        lst_all_data.append(lst_data)  # 개별 신문사의 1~5위 데이터 lst_all_data에 추가
    print(f"전체 {str(len(all_box))} 중 {count}회 종료")  # 몇회째 실시 되고 있는지 확인
    count += 1

# DataFrame(표)로 만들기
df = pd.DataFrame(lst_all_data, columns=["date", "company", "rank", "title", "link"])
today = datetime.now().strftime("%Y%m%d")
df.to_csv(f"{today}NaverNew.csv", encoding="utf-8-sig")