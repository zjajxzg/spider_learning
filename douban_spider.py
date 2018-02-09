#-*-coding:utf-8-*-
import urllib2
import re
import requests
import sys
import MySQLdb
from bs4 import BeautifulSoup

reload(sys)           #重新加载sys，因为setdefaultencoding函数已被调用，需重新加载才能重新调用
sys.setdefaultencoding('utf-8')           #设置默认编码格式为utf-8
db = MySQLdb.connect(host = '127.0.0.1',user = 'root',passwd = 'root',db = 'spider',charset = 'utf8')         #建立和数据库连接
cur = db.cursor()          #创建游标
url = 'https://movie.douban.com/chart'      #豆瓣2017新片榜

response = requests.get(url)             #获取页面源码
#print response.text
soup = BeautifulSoup(response.text,'lxml')           #bs4解析页面源码，使用lxml解析器，返回BeautifulSoup对象
#print soup.prettify()       #格式化输出
#print soup.title
#print soup.title.name
title = soup .find('h2')       #查找第一个h2标签,title1 = soup.body.h2:查找body下的第一个h2标签
rating_nums = soup.find_all('span','rating_nums')
movies = soup.find_all('a','nbg')         #等同于soup.find_all('a',class_='nbg')
print title.string[0:5]
#print rating_nums
#print movies
movies_list = []
rating_nums_list = []
soups_list = []
soups_list.append(movies)
soups_list.append(rating_nums)
#print soups_list
for i in range(10):
    print '电影:{0},评分:{1}'.format(soups_list[0][i]['title'],soups_list[1][i].string)
    print type(soups_list[0][i]['title'])
    cur.execute('insert into douban_2017_new_movies(movies_name,rating_nums) values (%s,%s)'% ('中文'.encode('utf-8'),soups_list[1][i].string))
    db.commit()
for tag in movies:
    print 'movies:<<{0}>>'.format(tag['title'])
for rating_num in rating_nums:
    print rating_num.string            #标签内容
db.close()