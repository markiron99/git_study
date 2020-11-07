import requests
import re
from bs4 import BeautifulSoup

for i in range(1,6): # 페이지 검색
    print("페이지 : ", i) # 현재 페이지 나타냄
    url = "https://www.coupang.com/np/search?q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={0}&rocketAll=false&searchIndexingToken=1=4&backgroundColor=".format(i)
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    items = soup.find_all("li", attrs={"class":re.compile("^search-product")})
    # print(items[0].find("div", attrs={"class":"name"}).get_text())
    for item in items:
        # 광고상품 제외
        ad_badge = item.find("span", attrs={"class":"ad-badge-text"})
        if ad_badge:
            print(" <광고상품은 제외합니다.>")
            continue

        name = item.find("div", attrs={"class":"name"}).get_text() #물품 이름
        if "Apple" in name:
            print(" <Apple 제품은 제외합니다.>")
            continue

        price = item.find("strong", attrs={"class":"price-value"}).get_text() #가격
        
        rate = item.find("em", attrs={"class":"rating"}) #평점
        if rate:
            rate = rate.get_text()
        else:
            print(" <평점이 없는 상품은 제외합니다.>")
            continue
        
        rating_total = item.find("span", attrs={"class":"rating-total-count"}) #평점수
        if rating_total:
            rating_total = rating_total.get_text()[1:-1] #괄호 지우기
        else:
            print(" <평점 수 없는 상품은 제외합니다.>")
            continue

        link = item.find("a", attrs={"class":"search-product-link"})["href"]

        if float(rate) >= 4.5 and int(rating_total) > 20:
            print(f"제품명 : {name}")
            print(f"가격 : {price} 원")
            print(f"평점 : {rate} 점 ({rating_total})개")
            print(f"제품링크 : https://www.coupang.com{link}")
            print("-"*100) # 줄긋기
