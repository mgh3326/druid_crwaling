import urllib.request
from bs4 import BeautifulSoup
import requests
from itertools import count
import os
import datetime
import sys


def get_html(url):  # 날씨 코드를 받아오기
    _html = ""
    resp = requests.get(url)
    if resp.status_code == 200:
        _html = resp.text
    return _html


def getLastNum():  # 결과값을 년도, 달별로 받기
    my_url = "http://druid.kw.ac.kr/Board/Contents/Algorithm"
    html = get_html(my_url)  # html로 문자열 반환 자료값을 받기
    soup_data = BeautifulSoup(html, 'html.parser')  # beautiful함수로 실행
    store_table = soup_data.find('table', attrs={'class': 'table'})
    tbody = store_table.find('tbody')  # tbody에 있는 정보만 가져오기
    _index = 0
    for i in tbody.findAll('th'):
        if _index == 1:
            return i.get_text()
        _index += 1


def get_board(result, num):  # 결과값을 년도, 달별로 받기
    my_url = "http://druid.kw.ac.kr/Board/Algorithm/%d" % (
        num)  # 년도와 달을 매개변수를 이용하여 주소값을 입력
    html = get_html(my_url)  # html로 문자열 반환 자료값을 받기
    soup_data = BeautifulSoup(html, 'html.parser')  # beautiful함수로 실행
    # print(soup_data)
    store_title = soup_data.find('h1', attrs={'class': 'title'})
    # print(store_title.find('div'))
    if(store_title.find('div') != None):
        return result
    # print(store_title)  # 제목 출력
    # print(store_title.get_text())  # 제목 출력
    result += str(num)+','
    result += store_title.get_text()+','
    store_description = soup_data.find('div', attrs={'class': 'description'})
    # if '<br/>' in store_description:
    #     store_description=store_description.replace('<br/>','')
    # print(str(store_description).replace('<br/>','').split('<div class="description">')[1].split('</div>')[0].strip())
    # print(store_description)
    # store_description=store_description.replace('<br/>','')

    # print(store_description.get_text().strip())  # 내용 출력
    # oh_description = store_description.get_text().strip()
    # oh_description.reaplce('\n','   ')
    result += str(store_description).replace('<br/>', '').replace('<br/>', '').replace('\n', ' ').split('<div class="description">')[1].split(
        '</div>')[0].strip().replace('\n', ' ').replace('\n', ' ').replace(',', '\,')+','  # 이렇게 해야 공백 다 지워지는거 같다.
    # result += store_description.get_text().strip()+','

    store_createTime = soup_data.find('span', attrs={'class': 'createTime'})
    # print(store_createTime.get_text())  # 시간 출력
    result += store_createTime.get_text().strip()+'\n'
    # print(result)
    return result


out = ""
oh = ""
# print(getLastNum())
print("start")
for i in range(0, int(getLastNum())):
    print(i)
    out = get_board(out, i+1)
print(out)
f = open("out.csv", 'w', encoding='utf-8')
f.write(str(out))
f.close()
print("완료 되었습니다.")
