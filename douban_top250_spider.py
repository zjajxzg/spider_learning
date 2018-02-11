#-*-coding:utf-8-*-
'''
author:xzg
'''
import requests
import sys
import MySQLdb
import re
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
db = MySQLdb.connect(host = '127.0.0.1',user = 'root',passwd = 'root',db = 'spider',charset = 'utf8')          #建立数据库连接
cur = db.cursor()      #创建游标
url = 'https://movie.douban.com/top250/'

def get_page(url):
    response = requests.get(url).text         #获取页面源码，text表示返回Unicode数据
    return response

def parse_html(html):
    movie_name_list = []        #电影名称
    star_count_list = []        #评价人数
    rating_num_list = []        #评分
    inq_list = []               #短评
    soup = BeautifulSoup(html,'lxml')
    ol = soup.find('ol','grid_view')
    for li in ol.find_all('li'):
        movie_name = li.find('span','title').string
        rating_num = li.find('span','rating_num').string
        star_count = li.find(text=re.compile('人评价'))
        inq = li.find('span','inq').string
        movie_name_list.append(movie_name)
        star_count_list.append(star_count)
        rating_num_list.append(rating_num)
        inq_list.append(inq)
    return movie_name_list,star_count_list,rating_num_list,inq_list

def put_db():
    pass

def main():
    movie_name_list = []  # 电影名称
    star_count_list = []  # 评价人数
    rating_num_list = []  # 评分
    inq_list = []
    response = get_page(url)
    movie_name_list, star_count_list, rating_num_list, inq_list = parse_html(response)
    print ','.join(movie_name_list)
    #print ','.join(star_count_list)
    print star_count_list
    print rating_num_list
    print ''.join(inq_list)

if __name__ == '__main__':
    main()