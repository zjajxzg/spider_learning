#-*-coding:utf-8-*-
import urllib2
import re
import requests
from bs4 import BeautifulSoup

url = 'https://movie.douban.com/chart'      #豆瓣2017新片榜
#request = urllib2.Request(url)
#response = urllib2.urlopen(request)
#content = response.read()
#pattern = re.compile()
response = requests.get(url)             #获取页面源码
#print response.text
soup = BeautifulSoup(response.text,'lxml')           #bs4解析页面源码，使用lxml解析器，返回BeautifulSoup对象
#print soup.prettify()       #格式化输出
print soup.title
print soup.title.name
soups = soup.find_all('a',class_="nbg")
for tag in soups:
    print tag['title']
